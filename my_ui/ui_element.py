from PyQt5 import QtWidgets
import logging
# from typing import List

logger = logging.getLogger(__name__)


class UiElement:
    def __init__(self, name, widget=None, value=None):
        """
        Один элемент на UI
        name - название элемента
        value - значение элемента
        widget - виджет элемента
        """
        self.name = name
        self.value = value
        self.widget = widget

    def post_in_widget(self):
        """
        Объект помещает свое value в свой widget (при наличии)
        """
        if self.widget:
            _post_data_in_widget(self.value, self.widget)

    def update_from_widget(self):
        """
        Объект обновляет свое value из своего widget (при наличии)
        """
        if self.widget:
            new_value = _get_data_from_widget(self.widget)
            self.set_new_value(new_value)

    def set_new_value(self, new_value):
        """
        Объект устанавливает свое новое value
        """
        self.value = new_value

    def your_name_is(self, name):
        """Твое имя?"""
        if name == self.name:
            return True
        else:
            return False

    def value_is_none(self):
        """Возвращает True, если значение пустое"""
        if self.value in ["", None]:
            return True
        else:
            return False    

def _post_data_in_widget(data, widget):
    """
    Устанавливает данные data в виджет widget
    """
    try:
        if isinstance(widget, QtWidgets.QLineEdit):
            widget.setText(data)
        if isinstance(widget, QtWidgets.QRadioButton):
            if data == None:
                data = False
            widget.setChecked(data)
        if isinstance(widget, QtWidgets.QTextEdit):
            widget.setPlainText(data)
        if isinstance(widget, QtWidgets.QCheckBox):
            if data == None:
                data = False
            widget.setChecked(data)
    except Exception as e:
        logger.error(f"Ошибка заполнения виджета данными: {str(e)}")
        logger.error(f"Виджет: {widget}")
        logger.error(f"Данные: {data}")


def _get_data_from_widget(widget):
    """
    Возвращает данные с виджета widget
    """
    data = None
    if isinstance(widget, QtWidgets.QLineEdit):
        data = widget.text()
    if isinstance(widget, QtWidgets.QRadioButton):
        data = widget.isChecked()
    if isinstance(widget, QtWidgets.QTextEdit):
        data = widget.toPlainText()
    if isinstance(widget, QtWidgets.QCheckBox):
        data = widget.isChecked()
    return data
