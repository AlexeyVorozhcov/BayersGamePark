import logging
from my_json import write_in_jsonFile, read_dict_from_jsonFile
from .ui_element import UiElement
from typing import List
from .myError import StopProcess

logger = logging.getLogger(__name__)

class UiData:
    """Класс для работы со множеством UiElement"""
    def __init__(self, ui, elements):
        """Объект хранит список ui-элементов и предоставляет методы для работы с множеством ui-элементов"""
        self.ui = ui
        self.elements : List[UiElement] = elements

    def _post_elements_in_wigets(self):
        """
        Размещает значения из всех Элементов в виджеты (только из тех, у которых есть виджет)
        """
        for element in self.elements:
            element.post_in_widget()

    def update_elements_from_widgets(self):
        """
        Собирает все данные из виджетов в словарь (только те элементы, у которых есть виджет)
        """
        for element in self.elements:
            element.update_from_widget()

    def is_all_values_are_filled (self, checking_list : list):
        """Проверяет? что все значения элементов из checking_list заполнены.
        Возвращает True, если все значения заполнены.
        В противном случае возвращает список элементов, у которых значения не заполнены"""
        result = []
        for element in self.elements:
            if element.name in checking_list:
                if element.value_is_none():
                    result.append(element)
        if len(result)>0: return result
        return "YES"            

    def _find_element(self, name):
        """
        Возвращает элемент с именем name
        Если такого элемента нет, возвращает None
        """
        for element in self.elements:
            if element.name == name:
                return element

    def get_value(self, name):
        """
        Возвращает значение элемента с именем name
        Если элемента с таким именем нет, возвращает None
        """
        findedElement = self._find_element(name)
        if findedElement:
            return findedElement.value

    def get_widget(self, name):
        """
        Возвращает виджет элемента с именем name
        Если элемента с таким именем нет или у элемента нет виджета, возвращает None
        """
        findedElement = self._find_element(name)
        if findedElement and findedElement.widget:
            return findedElement.widget

    def load_data(self, name_file: str, selection_on_name : list = []):
        """
        Загрузка элементов из файла name_file. Если имя файла пустое - ничего не выполнит.
        Из файла загружаются данные элементов, копируются в elements и размещаются в виджетах.
        Принимает имя файла и список имен элементов объекта, которые нужно загрузить. Если список пустой,
        загружаются все элементы объекта
        """
        logger.info("Запуск загрузки данных элементов из файла")
        try:
            if not name_file:
                raise StopProcess(
                    "Имя файла для открытия - пустое, загрузки не будет")
            loaded_data = read_dict_from_jsonFile(name_file)
            for element in self.elements:
                if selection_on_name==[] or element.name in selection_on_name:
                    element.set_new_value(loaded_data.get(element.name))
        except Exception as e:
            print(str(e))
            logging.error(str(e))

        logger.info(f"Загрузка данных из файла {name_file} завершена.")
        self._post_elements_in_wigets()

    def save_data(self, name_file, selection_on_name : list = []):
        """
        Сохранение данных объекта в файл. Возвращает True при успехе, False при ошибке
        Принимает имя файла и список имен элементов объекта, которые нужно записать. Если список пустой,
        запишутся все эелементы объекта.
        """
        dataForSave = self.createDictFromElements(selection_on_name)
        if write_in_jsonFile(dataForSave, name_file):
            logger.info(f"Запись заявления в файл {name_file} успешно.")
            return True
        else:
            logger.error(f"Не удалось записать заявление в файл {name_file}")
            return False

   
    def createDictFromElements(self, selection_on_name : list = []):
        """Возвращает словарь ИмяЭлемента : ЗначениеЭлемента
        selection_on_name - отбирает только те элементы, чьи имена есть в списке.
        Если список пустой - создает словарь из всех элементов."""
        dataDict = {}
        for element in self.elements:
            if selection_on_name == []:
                dataDict[element.name] = element.value
            elif element.name in selection_on_name:    
                dataDict[element.name] = element.value

        return dataDict

    def clear_all(self):
        for element in self.elements:
            element.update_from_widget()
            value = element.value
            if type(value) == str:
                element.set_new_value("")
                element.post_in_widget()

if __name__ == "__main__":
    pass
