from os import remove
import threading
from PyQt5.QtCore import QObject, pyqtSignal
import zipfile
from settings import URL_SERVER, BASE_PATH, join, name_FILENAME_FOR_PROGRAMM_UPDATE
from downloading import downloading_file
import logging
from time import sleep
from updates_data import DataOfUpdate
from myError import StopUpdate
from settings import journal
# from my_json import read_from_jsonFile, write_in_jsonFile
# # from updateModuls import downloading_file

logger = logging.getLogger(__name__)
ERROR = False
STOP_THREAD = False


def control_update(list_threads: list):
    """
    Запускает по очереди потоки из списка list_threads
    """
    for thread in list_threads:
        thread.start()
        thread.join()

class Update (threading.Thread, QObject):
    """
    Класс, выполняющий проверку необходимости обновления и само обновление
    """
    # стандартный сигнал о ходе выполенения обновления
    signal = pyqtSignal(str, int)
    # сигнал о готовности к запуску обновления, которое not is_need_unzip
    signal_update_ready = pyqtSignal()

    def __init__(self, name: str, is_need_unzip: bool):
        QObject.__init__(self)
        threading.Thread.__init__(self)
        self.name = name
        self.is_need_unzip = is_need_unzip
        self.local_infofile = join(BASE_PATH, self.name)
        self.url_infofile = URL_SERVER+self.name
        self.downloaded_infofile = join(BASE_PATH, "downloaded_"+self.name)
        self.local_data = None
        self.url_data = None

    def _downloading_url_infofile(self):
        """Скачивает информационный файл"""
        result = downloading_file(
            self.url_infofile, self.downloaded_infofile, self.detect_signal_from_downloading)
        if result == ERROR:
            raise StopUpdate ("Не удалось скачать информационный файл с сервера.")

    def _create_info(self):
        """Создает информационные объекты local_data и url_data из информационных файлов"""
        logger.debug(f"Создание объектов local_data и url_data")
        self.local_data = DataOfUpdate(self.local_infofile)
        self.url_data = DataOfUpdate(self.downloaded_infofile)
        remove(self.downloaded_infofile)
        logger.debug(f"Временный файл удален - {self.downloaded_infofile}")

    def _version_checking(self):
        """Сравнивает версии из self.local_data и self.url_data"""
        logger.debug(f"Сравнение названий версий в local_data и url_data")
        logger.debug(f"Урл-версия - {self.url_data.version}")
        logger.debug(f"Локальная версия - {self.local_data.version}")
        if self.url_data.version == None:
            raise StopUpdate("Урл-версия неизвестна.")
        if self.url_data.version == self.local_data.version:
            raise StopUpdate("Версии равны.")
        logger.debug(f"Версии не равны, сейчас будет скачиваться архив.")

    def _downloading_archive(self):
        """Скачивает архив"""
        url_archive = URL_SERVER+self.url_data.archive
        local_archive = join(BASE_PATH, self.url_data.archive)
        result = downloading_file(
            url_archive, local_archive, self.detect_signal_from_downloading)
        if result == ERROR:
            raise StopUpdate("Не удалось скачать архив.")

    def _update_info_after_downloading_archive(self):
        """
        Обновляет информационный объект после загрузки архива
        Сохраняет даннные в файл
        """
        logger.info(f"Обновляю данные в local_data")
        self.local_data.version = self.url_data.version
        self.local_data.archive = self.url_data.archive
        self.local_data.is_downloaded = True
        self.local_data.is_unzipped = False
        self.local_data.save()

    def _checking_unpacking_is_necessary(self):
        logger.debug(
            f"Проверка необходимости распаковки сразу после скачивания")
        if self.is_need_unzip == False:
            self._save_namefile_for_update_later()
            raise StopUpdate("is_need_unzip = False, распаковка не требуется")

    def _unzipped_archive(self):
        """
        Распаковывает архив        
        Удаляет архив после успешной распаковки
        Возвращает True при успешном результате
        """
        self.signal.emit("Обновление устанавливается...", 0)
        logger.debug(
            f"Сейчас буду распаковывать архив: {self.local_data.archive}")
        path_archive = join(BASE_PATH, self.local_data.archive)
        result_of_extracting_zip = extracting_zip(path_archive)
        if result_of_extracting_zip == True:
            logger.debug(f"Архив распакован успешно")
            self.signal.emit(f"Обновление установлено успешно", 0)
            sleep(3)
            remove(path_archive)
            logger.debug(f"Распакованный архив удален")            
        else:
            raise StopUpdate("Не удалось распаковать архив.")

    def _update_info_after_unzipped_archive(self):
        """
        Обновляет информационный объект после распаковки архива
        Сохраняет даннные в файл
        """
        logger.debug("Обновление local_info после распаковки архива")
        self.local_data.is_unzipped = True
        self.local_data.save()

    def _save_namefile_for_update_later(self):
        """
        Записывает в файл FILENAME_FOR_PROGRAMM_UPDATE имя архива,
        который должна распаковать программа update.exe
        """
        logger.info(
            f"Для последующей распаковки записываю название обновления в файл {name_FILENAME_FOR_PROGRAMM_UPDATE}")
        if write_data_in_file([self.name], name_FILENAME_FOR_PROGRAMM_UPDATE):
            logger.debug("Файл записан")
        else:
            logger.error("Файл не записан")

    def _checking_previous_download(self):
        """Проверка данных на наличие скачанного, но не распакованного архива"""
        logger.debug(
            f"Проверка {self.name} на наличие ранее скачанного, но не распакованного архива")
        if self.local_data.is_downloaded and not self.local_data.is_unzipped:
            logger.debug (f"Есть нераспакованный архив {self.local_data.archive}")
            logger.debug (f"Отправляю специальный сигнал во внешний мир")
            self.signal_update_ready.emit()
        else:
            self.signal.emit(f"Доступных обновлений нет", 0)
            logger.debug("Нет нераспакованного архива")

    def run(self):
        """
        Старт потока обновления
        """
        logger.info(f"Старт потока обновления {self.name}")
        journal.log(f"Старт потока обновления {self.name}")
        try:
            self._downloading_url_infofile()    # загрузка информационного файла с сервера
            self._create_info()  # создание информационных объектов local_data и url_data
            self._version_checking() # сравнение версий из двух информационных объектов local_data и url_data
            self._downloading_archive()  # загрузка архива            
            self._update_info_after_downloading_archive() # обновление информационного объекта после успешной загрузки архива
            self._checking_unpacking_is_necessary()  # проверка необходимости распаковки
            self._unzipped_archive()  # распаковка архива
            self._update_info_after_unzipped_archive() # обновление информационного объекта после успешной распаковки архива
        except Exception as e:
            logger.debug(str(e))
            journal.log(str(e))
        
        self._checking_previous_download()

    def detect_signal_from_downloading(self, percents, s):
        """
        При обнаружении сигнала из downloading генерируется сигнал из текущего объекта во внешний мир
        """
        self.signal.emit(f"Загрузка обновления {s} - {percents}%", 0)


def extracting_zip(arh, directory=""):
    """
    Распаковывает зип-архив arh в папку directory
    Если успешно, возвращает True, если нет - False
    """
    result = False
    try:
        z = zipfile.ZipFile(arh, 'r')
        z.extractall(path=directory)
        result = True
    except Exception as e:
        logger.error(f"Ошибка распаковки архива: {arh} : {str(e)}")
    return result


def get_data_from_file(namefile):
    """
    Возвращает данные из файла filename в виде списка строк либо None
    """
    result = None
    try:
        with open(namefile, 'r') as f:
            result = f.read().split('\n')
    except Exception as e:
        logger.error(f"Ошибка при чтении из файла {namefile} : {str(e)}")
    return result


def write_data_in_file(data: list, namefile):
    """
    Записывает данные в файл filename 
    """
    result = False
    logger.debug(f"Запись данных в файл {namefile}")
    logger.debug(data)
    try:
        with open(namefile, 'w') as f:
            for line in data:
                if line:
                    f.write(str(line)+'\n')
        result = True
        logger.debug("Записано успешно")
    except Exception as e:
        logger.error(f"Ошибка записи в файл {namefile} : {str(e)}")
    return result
