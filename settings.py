import logging
from os.path import abspath, curdir, join, exists
from os import mkdir
from datetime import datetime
from dateutil.relativedelta import relativedelta
from my_json import read_dict_from_jsonFile 
from journal import Journal


logging.basicConfig(level=logging.DEBUG, filename="logging.txt", filemode="w",
                    format='%(levelname)s : %(name)s  :  %(funcName)s : %(message)s')
logger = logging.getLogger(__name__)

journal = Journal()
journal.set_count = 50


def overrideConst(key_dict, const):
    """Возвращает значение словаря SETTING_DICT по ключу key_dict. Если такого ключа нет, возвращает значение const"""
    return SETTINGS_DICT.get(key_dict,const)

# Файл с настройками
FILE_SETTINGS = "settings.txt"

# Словарь настроек, загруженный из файла. Если файла нет - пустой словарь.
SETTINGS_DICT = read_dict_from_jsonFile(FILE_SETTINGS) 
if not SETTINGS_DICT:
    logger.debug("SETTINGS DICT не прочитан!")
    print ("SETTINGS DICT не прочитан!")

# Папка запущенной программы
BASE_PATH = abspath(curdir)

# Папка с контентом
FOLDER_CONTENT = join(BASE_PATH,"content")
FOLDER_CONTENT = overrideConst("FOLDER_CONTENT", FOLDER_CONTENT)

# Адрес сервера
URL_SERVER = "http://q920294x.beget.tech/files/"
URL_SERVER = overrideConst("URL_SERVER", URL_SERVER)

# Режим работы программы
MODE_IS_DEBUG = False
MODE_IS_DEBUG = overrideConst("MODE_IS_DEBUG", MODE_IS_DEBUG)

# Название версии программы
VERSION = "4.00"
VERSION = overrideConst("VERSION", VERSION)

# Заголовок программы
TITLE_PROGRAMM = f"Buyers (ver.{VERSION}) "

# Файл иконки программы
FILENAME_ICON = join(FOLDER_CONTENT,'icon.ico')
FILENAME_ICON = join(FOLDER_CONTENT, overrideConst("FILENAME_ICON", FILENAME_ICON))

# Файл, в котором хранятся реквизиты магазина
name_FILE_REQUISITES = "data.pickle"
name_FILE_REQUISITES = overrideConst("name_FILE_REQUISITES", name_FILE_REQUISITES)

# сегодняшняя дата в str
DATE_TODAY_STR = datetime.date(datetime.today()).strftime("%d.%m.%Y")

# количество месяцев действия подарочных сертификатов
CERTIFICATE_PERIOD = 6
CERTIFICATE_PERIOD = overrideConst("CERTIFICATE_PERIOD", CERTIFICATE_PERIOD)

# деадлайн действия сертификатов
CERTIFICATE_DEADLINE = datetime.date(datetime.today() + relativedelta(months=CERTIFICATE_PERIOD)).strftime("%d.%m.%Y")

# папка, где хранятся сохраненные заявления
name_FOLDER_SAVING_CLAIM = join(BASE_PATH, "SAVED FILES" )
name_FOLDER_SAVING_CLAIM = join(BASE_PATH, overrideConst("name_FOLDER_SAVING_CLAIM", name_FOLDER_SAVING_CLAIM))
# если папка не существует, создать ее
if not exists(name_FOLDER_SAVING_CLAIM):
    logger.debug(f"Папка {name_FOLDER_SAVING_CLAIM} не найдена. Будет создана новая.")
    mkdir(name_FOLDER_SAVING_CLAIM)

# расширения файлов, в которые сохраняются заявления
FILE_EXTENSION_SAVING_CLAIM = ".claim"
FILE_EXTENSION_SAVING_CLAIM = overrideConst("FILE_EXTENSION_SAVING_CLAIM", FILE_EXTENSION_SAVING_CLAIM)

# папка, где хранятся шаблоны документов
name_FOLDER_TEMPLATES = join(BASE_PATH, "TEMPLATES" )
name_FOLDER_TEMPLATES = join(BASE_PATH, overrideConst("name_FOLDER_TEMPLATES", name_FOLDER_TEMPLATES))

# название файла, в котором лежит название скачанного, но не распакованного архива
name_FILENAME_FOR_PROGRAMM_UPDATE = "downloadingfile.txt"
name_FILENAME_FOR_PROGRAMM_UPDATE = overrideConst("name_FILENAME_FOR_PROGRAMM_UPDATE", name_FILENAME_FOR_PROGRAMM_UPDATE)


# название файла контроля версии шаблонов
FILENAME_VERSION_TEMPLATES = "version_templates_3.txt"
FILENAME_VERSION_TEMPLATES = overrideConst("FILENAME_VERSION_TEMPLATES", FILENAME_VERSION_TEMPLATES)

# название файла контроля версии update
FILENAME_VERSION_UPDATE = "version_update_3.txt"
FILENAME_VERSION_UPDATE = overrideConst("FILENAME_VERSION_UPDATE", FILENAME_VERSION_UPDATE)

# название файла контроля версии основной программы
# FILENAME_VERSION_PROGRAM = "version_program.txt"
FILENAME_VERSION_PROGRAM = "version_program_3.txt"
FILENAME_VERSION_PROGRAM = overrideConst("FILENAME_VERSION_PROGRAM", FILENAME_VERSION_PROGRAM)

# название файла контроля версии настроек
FILENAME_VERSION_SETTING = "version_setting_3.txt"
FILENAME_VERSION_SETTING = overrideConst("FILENAME_VERSION_SETTING", FILENAME_VERSION_SETTING)

if __name__== "__main__":
    print(VERSION)
