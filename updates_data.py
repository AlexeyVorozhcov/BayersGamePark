
import logging
from my_json import read_dict_from_jsonFile, write_in_jsonFile

logger = logging.getLogger(__name__)

class DataOfUpdate:
    """
    Класс для хранения информации об обновлении
    .namefile = имя файла, в котором хранитcя информация об обновлении
    .version = название версии
    .archive = название файла скачиваемого архива
    .is_downloaded = загружено или нет
    .is_unzipped = распаковано или нет
    """

    def __init__(self, namefile, datatest=None):
        logger.info(f"Получение данных из информационного файла {namefile}")
        self.namefile = namefile
        data = datatest
        data = self.load()
        self.version = data.get("version")
        self.archive = data.get("archive")
        self.is_downloaded = data.get("is_downloaded")
        self.is_unzipped = data.get("is_unzipped")

    def load(self):
        return read_dict_from_jsonFile(self.namefile)

    def save(self):
        """Записывает в json-файл данные самого себя"""
        _dict = _create_dict_from_data(self)
        logger.info(f"Запись словаря в информационный файл {self.namefile}")
        logger.info(_dict)
        return write_in_jsonFile(_dict, self.namefile)

def _create_dict_from_data(object : DataOfUpdate):
    """Возвращает словарь, созданный из объекта DataOfUpdate"""
    _dict = {"version": object.version,
            "archive": object.archive,
            "is_downloaded": object.is_downloaded,
            "is_unzipped": object.is_unzipped
            }
    return _dict        


if __name__=="__main__":
    start = {"version": "07.05.2021",
             "archive": "TEMPLATES.zip",
             "is_downloaded": False,
             "is_unzipped": False
             }
    t = DataOfUpdate("version_templates_test.txt", datatest=start)         
    t.save()