from PyQt5.QtWidgets import QStatusBar, QPushButton
from PyQt5.QtCore import QObject, pyqtSignal
from os import startfile
import logging
from settings import join, BASE_PATH, FILENAME_VERSION_SETTING, FILENAME_VERSION_TEMPLATES, FILENAME_VERSION_UPDATE, FILENAME_VERSION_PROGRAM
from updates import Update, control_update
import threading
from settings import journal

logger = logging.getLogger(__name__)

class tabUpdate (QObject):
    # сигнал о необходимости закрыть программу
    signal_to_close_programm = pyqtSignal()
    def __init__(self, statusbar : QStatusBar):
        QObject.__init__(self)
        self.statusbar = statusbar
        self.making_updates()

    def message_in_statusBar(self, message, msecs=0):
        self.statusbar.showMessage(message, msecs)    

    def show_button_update(self):
        self.message_in_statusBar("", 0)
        self.btn = QPushButton("Обновление готово к установке, нажмите тут, чтобы установить")
        self.btn.clicked.connect(self.start_update_programm)
        self.statusbar.addWidget(self.btn)
        self.btn.show()    

    def start_update_programm(self):
        try:
            journal.log("Старт обновления программы...")
            startfile(join(BASE_PATH, "update2.exe"))
            self.signal_to_close_programm.emit()
        except Exception as e:
            logger.error(f"Ошибка старта обновления программы: {str(e)}")
            self.btn.setText("Ошибка старта обновления, " + str(e))
            journal.log("Ошибка старта обновления программы...")
            journal.log(str(e))

    def making_updates(self):
        thread_update_setting = Update(FILENAME_VERSION_SETTING, is_need_unzip=True)
        thread_update_setting.signal.connect(self.message_in_statusBar)
        list_threads = [thread_update_setting]

        thread_update_templataes = Update(FILENAME_VERSION_TEMPLATES, is_need_unzip=True)
        thread_update_templataes.signal.connect(self.message_in_statusBar)
        thread_update_templataes.signal_update_ready.connect(self.show_button_update)
        list_threads.append (thread_update_templataes)

        thread_update_update_exe = Update(FILENAME_VERSION_UPDATE, is_need_unzip=True)
        thread_update_update_exe.signal.connect(self.message_in_statusBar)
        thread_update_update_exe.signal_update_ready.connect(self.show_button_update)
        list_threads.append(thread_update_update_exe)

        thread_update_program = Update(FILENAME_VERSION_PROGRAM, is_need_unzip=False)
        thread_update_program.signal.connect(self.message_in_statusBar)
        thread_update_program.signal_update_ready.connect(self.show_button_update)
        list_threads.append(thread_update_program)

        # TODO is_need_unzip = False должно быть только в последнем потоке. Предыдущие будут перекрываться.
        # Подумать как это исправить

        thread_of_update = threading.Thread(target=control_update, args=(list_threads, ))
        thread_of_update.start()