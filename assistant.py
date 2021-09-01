from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QFileDialog
from os.path import abspath, curdir, join
from os import path, mkdir
from shutil import rmtree
import logging
# import main_ui


logger = logging.getLogger(__name__)


def get_path(name_file, subdir=""):
    if type(name_file) != str:
        name_file = ""
    if type(subdir) != str:
        subdir = ""
    directory_of_script = abspath(curdir)
    result = None
    if subdir == "":
        result = join(directory_of_script, name_file)
    else:
        result = join(directory_of_script, subdir, name_file)
    if name_file == "":
        result = join(directory_of_script, subdir)
    return result


def get_bowed_surname(fio_original, not_inclined, is_man):
    """
    Возвращает необходимые варианты склонения и сокращения фамилии, имени, инициалов
    """
    if fio_original:
        family = ""
        name = ""
        name2 = ""
        try:
            fio = fio_original.split()  # разделяю строку на слова
            family = fio[0]
            name = fio[1]
            name2 = fio[2]
        except Exception:
            name2 = ""
        initials = get_initials(name, name2)
        fio_short_declen = get_family_genitive(
            family, not_inclined, is_man) + " " + initials
        fio_short_dative = get_family_dative(
            family, not_inclined, is_man) + " " + initials
        fio_short = family + " " + initials
        fio_total = family + " " + name + " " + name2
        return fio_short_declen, fio_short_dative, fio_short, fio_total
    else:
        return "ФИО не введены", "ФИО не введены", "ФИО не введены", "ФИО не введены"



def get_family_genitive(family:str, not_inclined: bool, is_man: bool):
    """
    Возвращает фамилию в родительном падеже
    """
    if len(family)<2: return family
    result = family
    if not not_inclined:
        if is_man:
            if family[-2:] == "ий":
                result = family[:-2] + 'ого'
            else:
                result = family + 'а'
        else:
            if family[-2:] == "ая":
                result = family[:-2] + 'ой'
            else:
                result = family[:-1] + 'ой'
    return result


# получить фамилию  в дательном падеже
def get_family_dative(family:str, not_inclined: bool, is_man: bool):
    """
    Возвращает фамилию в дательном падеже
    """
    result = family
    if not not_inclined:
        if is_man:
            if family[-2:] == "ий":
                result = family[:-2] + 'ому'
            else:
                result = family + 'у'
        else:
            if family[-2:] == "ая":
                result = family[:-2] + 'ой'
            else:
                result = family[:-1] + 'ой'
    return result


def get_initials(name, name2):
    """
    Возвращает инициалы
    """    
    if type(name) != str: name=""
    if type(name2) != str: name2=""
    s1, s2 = "", ""
    if len(name) > 0:
        s1 = name[0] + '.'
    if len(name2) > 0:
        s2 = name2[0] + '.'
    return s1 + s2

class MessagesForUser:
    def __init__(self, widget):
        """Через этот объект вызываются методы общения с пользователем:
        showMessageBox и user_select_file"""
        self.widget = widget

    def showMessageBox(self, type=0, caption="Информация", text=""):
        """type=1: критическая ошибка, другое значение: информация"""
        if type == 1:
            QMessageBox.critical(self.widget, caption, text, QMessageBox.Ok)
        else:
            QMessageBox.information(self.widget, caption, text, QMessageBox.Ok)

    def user_select_file(self, caption, directory, file_extension ):
        """
        Возвращает имя файла, выбранное пользователем в диалоговом окне
        """
        result = None
        win_dialog = QFileDialog()
        try:
            result = win_dialog.getOpenFileName(self.widget, caption, directory, "*" + file_extension)[0]
        except Exception as e:
            logger.error(str(e))
            self.showMessageBox(1, "Ошибка", str(e))
        return result        




def get_name_month(n):
    data = {1: 'января',
            2: 'февраля',
            3: 'марта',
            4: 'апреля',
            5: 'мая',
            6: 'июня',
            7: 'июля',
            8: 'августа',
            9: 'сентября',
            10: 'октября',
            11: 'ноября',
            12: 'декабря'
            }
    return data[n]


def remove_dir(directory):
    paths = path.join(path.abspath(path.dirname(__file__)), directory)
    rmtree(paths)


def remove_all_from_dir(directory):
    remove_dir(directory)
    mkdir(directory)


if __name__ == "__main__":
    pass
