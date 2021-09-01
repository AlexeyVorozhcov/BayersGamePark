from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon
import v3
from sys import exit
from settings import logging, journal
from settings import FILENAME_ICON, TITLE_PROGRAMM, MODE_IS_DEBUG
from tab_lego import TabLego
from tab_sertificate import TabSertificate
from tab_claim_and_otkasy import TabClaim_TabOtkasy
from tab_update import tabUpdate

logger = logging.getLogger(__name__)

def close_programm():
    exit(0)

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        """Окно программы"""
        super(MainWindow, self).__init__()  # инициализация главного окна
        self.ui = v3.Ui_MainWindow()  # объект с интерфейсом
        self.ui.setupUi(self)  # инициализация интерфейса
        self.setWindowIcon(QIcon(FILENAME_ICON))  # установка иконки
        self.setWindowTitle(TITLE_PROGRAMM)  # установка имени окна
        self.ui.tabWidget.setCurrentIndex(0)  # установка стартовой вкладки tab
                
        self.tab_claim = TabClaim_TabOtkasy(self.ui)
        self.tab_sertificate = TabSertificate(self.ui)
        self.tab_lego = TabLego(self.ui)
        if not MODE_IS_DEBUG:      
            self.tab_update = tabUpdate(self.ui.statusBar) 
            self.tab_update.signal_to_close_programm.connect(close_programm)

logger.debug("Старт основной программы")
journal.log("--------------------")
journal.log("Программа запущена")
journal.log("--------------------")
app = QtWidgets.QApplication([])
window_of_programm = MainWindow()
window_of_programm.show()
print ("MODE IS DEBUG = " + str(MODE_IS_DEBUG))

exit(app.exec())
