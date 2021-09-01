from PyQt5.QtCore import QObject, pyqtSignal
from .chatScripts import ChatScript, Commands, StepOfScript
from typing import List, Union
import logging

logging.basicConfig(level=logging.DEBUG, filename="logging_chat.txt", filemode="w",
                    format='%(levelname)s : %(name)s  :  %(funcName)s : %(message)s')

logger_chat = logging.getLogger(__name__)


def _report(message):
    logger_chat.debug(message)
    # print(message)


class ChatBot(QObject):
    # сигнал ответа на запрос
    signal_answer = pyqtSignal('PyQt_PyObject')
    # сигнал о процессе (собеседник печатает)
    signal_process = pyqtSignal(str)

    def __init__(self, nameBot, text_color="black"):
        QObject.__init__(self)
        self.nameBot = nameBot
        self.text_color = text_color
        self.scripts: List[ChatScript] = []
        self.scripts.append(ChatScript(name="111"))
        self.current_number_of_script = 0
        self.current_script = self.scripts[self.current_number_of_script]
        self.current_step = 0
        self.add_info = None
        self.commands = Commands

    def tuktuk(self, inbox_message: Union[str, Commands, dict]):
        if type(inbox_message) is str:
            _report(f"Принята строка: {inbox_message}")

        if type(inbox_message) is Commands:
            _report(f"Принята команда: {inbox_message}")
            self._command_processing(inbox_message)
            self._send_awser(self._create_answer())

        if type(inbox_message) is dict:
            _report(f"Принят словарь: {inbox_message}")
            self.kipper_dict.extend(inbox_message)
            self._command_processing(Commands.to_next)
            self._send_awser(self._create_answer())

        return "ok"

    def _command_processing(self, message):
        """Обработка входящей команды
        """
        if message == Commands.to_start:
            self._cmd_to_start()
        if message == Commands.to_next:
            self._cmd_to_next()
        if message == Commands.to_previous:
            self._cmd_to_previous()
        if message == Commands.to_break:
            self._cmd_to_break()

    def _create_answer(self):
        answer = self.current_script.steps[self.current_step]
        return answer

    def _send_awser(self, answer):
        self.signal_answer.emit(answer)

    def _cmd_to_start(self):
        _report("Выполняется команда to_start")
        self.current_step = 0

    def _cmd_to_next(self):
        _report("Выполняется команда to_next")
        self.current_step += 1
        if self.current_step > self.current_script.max_step:
            self.current_step = self.current_script.max_step
        if self.current_step == self.current_script.max_step:
            self.add_info = Commands.is_last

    def _cmd_to_previous(self):
        _report("Выполняется команда to_previous")
        self.current_step -= 1
        if self.current_step < 0:
            self.current_step = 0
        if self.current_step == 0:
            self.add_info = Commands.is_first

    def _cmd_to_break(self):
        pass
