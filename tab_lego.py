from documentCreator import DocumentCreator_Lego_auto
from typing import List
from PyQt5.QtCore import QThread
from PyQt5.QtGui import QColor, QGuiApplication
from PyQt5.QtWidgets import QLabel, QPushButton,  QSizePolicy,  QTextEdit, QFrame, QHBoxLayout, QLineEdit
from my_chatBot.chatBot_2 import ChatBot, StepOfScript, logger_chat
import my_ui.ui_creator_elements
from my_ui.ui_datas import UiData
from assistant import MessagesForUser
from settings import DATE_TODAY_STR
from settings import journal


def _report(message):
    logger_chat.debug(message)
    # print(message)


class TabLego:
    def __init__(self, ui):
        self.ui = ui
        self.init_ui()
        self.elements = my_ui.ui_creator_elements.from_tab_lego(ui)
        self.ui_data:  UiData = UiData(self.ui, self.elements)
        self.msg = MessagesForUser(self.ui.centralwidget)

    def init_ui(self):
        """Инициализация элементов UI"""
        self.lineEdit_shop_lego_2: QLineEdit = self.ui.lineEdit_shop_lego_2
        self.lineEdit_shop_lego_2.setText(self.ui.lineEdit_organisation.text())
        self.lineEdit_data_lego_2: QLineEdit = self.ui.lineEdit_data_lego_2
        self.lineEdit_data_lego_2.setText(DATE_TODAY_STR)
        self.lineEdit_personal_lego_2: QLineEdit = self.ui.lineEdit_personal_lego_2
        self.lineEdit_klient_lego_2: QLineEdit = self.ui.lineEdit_klient_lego_2
        self.lineEdit_detal_total: QLineEdit = self.ui.lineEdit_detal_total
        self.lineEdit_detal_lego: QLineEdit = self.ui.lineEdit_detal_lego
        self.lineEdit_ves: QLineEdit = self.ui.lineEdit_ves
        self.lineEdit_tara: QLineEdit = self.ui.lineEdit_tara

        self.pushButton_printAktLego: QPushButton = self.ui.pushButton_printAktLego
        self.pushButton_printAktLego.clicked.connect(
            self.onClickBtn_printAktLego)

        self.chat = Chat(self.ui)

    def onClickBtn_printAktLego(self):
        """Нажатие на кнопку"""
        self.ui_data.update_elements_from_widgets()
        DocumentCreator_Lego_auto(self.ui_data.createDictFromElements())
        journal.log("Сформирован Акт приемки Лего")


class PushButtonMakerMessage(QPushButton):
    def __init__(self, text, cmd):
        QPushButton.__init__(self)
        self.my_text = text
        self.cmd = cmd
        self.setText(self.my_text)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        self.setStyleSheet("padding: 5px 15px 5px 15px;")


class Chat:
    def __init__(self, ui):
        self.init_chat(ui)
        self.color_usertext = "black"

    def init_chat(self, ui):
        """Начальные настройки чата - все поля скрываются, кнопка Позвать помощника - активируется"""
        # кнопка "Позвать помощника"
        self.pushButton_start: QPushButton = ui.pushButton_start
        self.pushButton_start.setVisible(True)
        self.pushButton_start.setText("Позвать помощника")
        self.pushButton_start.clicked.connect(self.click_start)
        # окно чата
        self.chatWindow: QTextEdit = ui.textEdit_chat
        self.chatWindow.setVisible(False)
        # строка "Собеседник печатает"
        self.label_status_print: QLabel = ui.label_status_print
        self.label_status_print.setText("")
        self.label_status_print.setVisible(False)
        # блок с кнопками-ответами
        self.frame_for_btns: QFrame = ui.frame_for_btns
        self.frame_for_btns.setSizePolicy(
            QSizePolicy.Fixed, QSizePolicy.Preferred)
        # self.frame_for_btns.setLayout(QHBoxLayout())
        self.frame_for_btns.setVisible(True)
        # информационный блок
        self.lineEdit_detal_total: QLineEdit = ui.lineEdit_detal_total
        self.lineEdit_detal_total.textEdited.connect(
            self.edit_text_in_lineEdit)
        self.lineEdit_detal_not_lego: QLineEdit = ui.lineEdit_detal_lego
        self.lineEdit_detal_not_lego.textEdited.connect(
            self.edit_text_in_lineEdit)
        self.label_procent_nonoriginal: QLabel = ui.label_procent_original

    def click_start(self):
        """Кнопка старт - позвать помощника, начать сеанс чата"""
        self.pushButton_start.hide()  # скрывается кнопка Позвать помощника
        # устанвливается видимость виджетов чата
        self.chatWindow.setVisible(True)
        self.chatWindow.setPlainText("")
        self.label_status_print.setVisible(True)
        self.frame_for_btns.setVisible(True)
        # создается новый чат-бот
        self.chatBot = ChatBot("Помощник", text_color="blue")
        self.chatBot.signal_answer.connect(self.get_answer_from_chatBot)
        self.commands = self.chatBot.commands
        # стучимся к чат-боту, отправляем ему команду
        self.chatBot.tuktuk(self.commands.to_start)
        journal.log("Запущен помощник приемки Лего")

    def get_answer_from_chatBot(self, answer):
        """Получение сигнала от чат-бота, принимается ответ answer"""
        self.pause()
        if type(answer) is StepOfScript:
            # Если ответ в виде объекта StepOfScript, получаем из него message, buttons и add_command
            step: StepOfScript = answer
            message: str = step.message
            buttons: List[dict] = step.buttons
            add_command = step.add_command
            self._delete_buttons()
            self._create_buttons(buttons)
            # размещается сообщение  в поле  чата
            message = self.chatBot.nameBot + ": " + message + "\n"
            self._post_message_in_chatWindow(
                message, color=self.chatBot.text_color)
            # обрабатывается команда add_command
            if add_command == self.commands.to_next_message:
                self.chatBot.tuktuk(self.commands.to_next)
            if add_command == self.commands.to_break:
                self.command_to_break()

    def _delete_buttons(self):
        """Скрытие устаревших кнопок-ответов"""
        buttons: List[PushButtonMakerMessage] = self.frame_for_btns.findChildren(
            PushButtonMakerMessage)
        for btn in buttons:
            btn.hide()

    def _create_buttons(self, buttons):
        """Создание кнопок-ответов (если buttons не пустой)"""
        if buttons:
            self.frame_for_btns.setVisible(True)
            for button in buttons:
                for _text, _cmd in button.items():
                    push_button = PushButtonMakerMessage(_text, _cmd)
                    self.frame_for_btns.layout().addWidget(push_button)
                    push_button.clicked.connect(self.clickBtn_answers)

    def clickBtn_answers(self):
        """Клик по кнопке-ответу"""
        sender: PushButtonMakerMessage = self.frame_for_btns.sender()
        msg = sender.my_text
        cmd = sender.cmd
        self._delete_buttons()  # удаление старых кнопок
        message = "Вы: " + msg + "\n"
        self._post_message_in_chatWindow(message, color=self.color_usertext)
        if cmd != self.commands.to_break:
            # отправка чат-боту новой команды, которая содержится в нажатой кнопке
            self.chatBot.tuktuk(cmd)
        else:
            self.command_to_break()

    def edit_text_in_lineEdit(self):
        total = self.lineEdit_detal_total.text()
        not_lego = self.lineEdit_detal_not_lego.text()
        try:
            int_total = int(total)
            int_notLego = int(not_lego)
            self.label_procent_nonoriginal.setText(
                str(int(int_notLego/int_total*100)))
        except Exception:
            self.label_procent_nonoriginal.setText("---")

    def command_to_break(self):
        """Действия при получении команды to_break"""
        message = self.chatBot.nameBot + ": BYE !"
        self._post_message_in_chatWindow(
            message, color=self.chatBot.text_color)
        self._delete_buttons()
        self.pushButton_start.setVisible(True)

    def _post_message_in_chatWindow(self, message, color=None):
        """Размещение текста в поле чата"""
        if color:
            self.chatWindow.setTextColor(QColor(color))
        self.chatWindow.append(message)
        QGuiApplication.processEvents()

    def pause(self):
        _report("Сейчас будет пауза")
        self.label_status_print.setVisible(True)
        frame = [self.chatBot.nameBot + " печатает"]
        frame.append(self.chatBot.nameBot + " печатает.")
        frame.append(self.chatBot.nameBot + " печатает..")
        frame.append(self.chatBot.nameBot + " печатает...")
        for k in range(2):
            for f in frame:
                self.label_status_print.setText(f)
                QGuiApplication.processEvents()
                QThread.msleep(200)
        self.label_status_print.setText("")
