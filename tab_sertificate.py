from my_ui.ui_datas import UiData
from PyQt5 import QtWidgets
from settings import CERTIFICATE_DEADLINE
from documentCreator import DocumentCreator_Sert
import my_ui.ui_creator_elements
from assistant import MessagesForUser
from settings import journal

class TabSertificate:
    def __init__(self, ui ):
        self.ui = ui 
        self.init_ui() 
        self.elements = my_ui.ui_creator_elements.from_tab_sertificate(ui)
        self.ui_data :  UiData = UiData(self.ui, self.elements)
        self.msg = MessagesForUser(self.ui.centralwidget)

    def init_ui(self):
        """Инициализация элементов UI"""
        self.lineEdit_sert_nominal : QtWidgets.QLineEdit = self.ui.lineEdit_sert_nominal
        self.lineEdit_date : QtWidgets.QLineEdit = self.ui.lineEdit_sert_deadline    
        self.lineEdit_sert_code : QtWidgets.QLineEdit = self.ui.lineEdit_sert_code
        self.pushButton_sert : QtWidgets.QPushButton = self.ui.pushButton_sert
        self.lineEdit_date.setText(CERTIFICATE_DEADLINE)
        self.pushButton_sert.clicked.connect(self.onClickBtn_toPrintSertificate)
        

    def onClickBtn_toPrintSertificate(self):
        """Нажатие на кнопку"""
        self.ui_data.update_elements_from_widgets()
        DocumentCreator_Sert(self.ui_data.createDictFromElements())    
        journal.log("Сформирован документ для печати на подарочном сертификате")