from typing import List

class StepOfScript:
    """Шаг скрипта, одна единица ответа чат-бота
    message -  текст для отображения в окне чата
    buttons - кнопки с вариантами ответов [{Текст кнопки : Отправляемая ею команда}]
    add_command - дополнительная команда
    """
    def __init__(self, message : str, buttons: List[dict] = [], add_command=None ):
        self. message = message
        self.buttons = buttons
        self.add_command = add_command