import my_ui.ui_creator_elements
from my_ui.ui_datas import UiData
from settings import join, journal 
from settings import name_FILE_REQUISITES, DATE_TODAY_STR, name_FOLDER_SAVING_CLAIM, FILE_EXTENSION_SAVING_CLAIM
from documentCreator import DocumentCreator_Claim, DocumentCreator_Letter
import assistant

class TabClaim_TabOtkasy:
    def __init__(self, ui):
        self.ui = ui 
        # список элементов интерфейса для использования во вкладке
        self.elements = my_ui.ui_creator_elements.from_tab_claim(ui) 
        self.elements.extend(my_ui.ui_creator_elements.from_tab_otkazy(ui) )
        # все элементы в одном объекте
        self.ui_data :  UiData = UiData(ui, self.elements)
        self.init_ui()
        self.msg = assistant.MessagesForUser(self.ui.centralwidget)
       
    def init_ui(self):
        """Инициализация элементов UI"""
        self.load_requisites()
        self.ui.textEdit_other.setVisible(False)  # скрываю поле Другое
        self.ui.textEdit_description.setVisible(False)  # скрываю поле Описание        
        self.ui.pushButton_load.clicked.connect(self.load) # привязываю метод к кнопке Загрузить заявление
        self.ui.pushButton_complete_claim.clicked.connect(self.onClickBtn_toCreateClaim) # привязываю метод к кнопке Сформировать заявление
        self.ui.pushButton_refuse.clicked.connect(self.onClickBtn_toCreateLetter) # привязываю метод к кнопке Сформировать отказное письмо
        self.ui.pushButton_save_reqvisits.clicked.connect(self.onClickBtn_toSaveRequisites) # привязываю метод к кнопке Сохранить реквизиты
        self.ui.pushButton_load_requisites.clicked.connect(self.load_requisites) # команда на кнопку Загрузить реквизиты
        self.ui.pushButton_clear.clicked.connect(self.onClickBtn_clear) # команда на кнопку Очистить все поля

    def load(self, name_file=None):
        """Загружает данные из файла. Если name_file пустое - открывает диалоговое окно для выбора файла"""
        if not name_file:
            name_file = self.msg.user_select_file("Выберите файл", name_FOLDER_SAVING_CLAIM, FILE_EXTENSION_SAVING_CLAIM)    
        self.ui_data.load_data(name_file)
        self.load_requisites()
         
    def load_requisites(self):
        """Загрузка и вставка в ui реквизитов"""
        self.ui_data.load_data(name_FILE_REQUISITES, my_ui.ui_creator_elements.list_of_requisites())
        # копирую название магазина из строки реквизитов
        self.ui.lineEdit_organisation.setText(self.ui.lineEdit_nameShop.text()) 
        # Устанавливаю название текущего магазина в Журнале
        journal.set_name_shop(self.ui.lineEdit_nameShop.text())
        self.ui.lineEdit_date.setText(DATE_TODAY_STR) # ставлю строку в поле с датой

    def onClickBtn_clear(self):
        self.ui_data.clear_all()
        self.load_requisites()

    def onClickBtn_toCreateClaim(self):
        """
        Клик по кнопке "Сформировать заявление"
        Обновляет данные с виджетов
        Сохраняет данные в файл
        Сохраняет реквизиты в файл
        Если проходит провеку: создает документ из шаблона
        """       
        # Обновить данные с виджетов
        self.ui_data.update_elements_from_widgets()         
        # Провести проверку заполненности полей из списка list_of_checking_value_on_claim()
        check_result = self.ui_data.is_all_values_are_filled(my_ui.ui_creator_elements.list_of_checking_value_on_claim())
        if check_result == "YES":
            # Если проверка завешилась успешно
            name_file = self.create_name_file_for_claim()
            self.ui_data.save_data(name_file) # сохранение в файл всех полей 
            dict_for_document = self.ui_data.createDictFromElements()  # создание словаря для использования в документе
            dict_for_document = self.append_in_dict_surnames(dict_for_document)  # добавление склонений фамилии заявителя        
            DocumentCreator_Claim(dict_for_document)
            journal.log(f"Сформировано заявление: {dict_for_document['fio_short']}")
        else:
            # Если обнаружены незаполненные обязательные поля
            self.report_blank_fields(check_result) 
  
    def onClickBtn_toCreateLetter(self):
        """Клик по кнопке Создать отказное письмо"""
        self.ui_data.update_elements_from_widgets()        
        check_result = self.ui_data.is_all_values_are_filled(my_ui.ui_creator_elements.list_of_checking_value_on_claim())
        if check_result == "YES":
            # Если проверка завешилась успешно
            name_file = self.create_name_file_for_claim()
            self.ui_data.save_data(name_file)
            # self.ui_data.save_data(name_FILE_REQUISITES, my_ui.ui_creator_elements.list_of_requisites())
            dict_for_document = self.ui_data.createDictFromElements()
            dict_for_document = self.append_in_dict_surnames(dict_for_document)  # добавление склонений фамилии заявителя 
            DocumentCreator_Letter(dict_for_document)
            journal.log(f"Сформировано отказное письмо: {dict_for_document['fio_short']}")
        else:
            # Если обнаружены незаполенные обязательные поля
            self.report_blank_fields(check_result)    
        

    def onClickBtn_toSaveRequisites(self):
        """Клик по кнопке Сохранить реквизиты"""
        self.ui_data.update_elements_from_widgets()
        self.ui_data.save_data(name_FILE_REQUISITES, my_ui.ui_creator_elements.list_of_requisites())
        self.msg.showMessageBox(0, "Информация","Реквизиты сохранены.")

    def get_bowed_surnames(self):
        fio = self.ui_data.get_value("fio_original")
        is_men = self.ui_data.get_value("is_man")
        not_inclined = self.ui_data.get_value("not_inclined")
        return assistant.get_bowed_surname(fio,not_inclined,is_men) 

    def append_in_dict_surnames(self, old_dict):
        new_dict = old_dict
        fio_short_declen, fio_short_dative, fio_short, fio_total = self.get_bowed_surnames()
        new_dict['fio_short_declen'] = fio_short_declen
        new_dict['fio_short'] = fio_short
        new_dict['fio_total'] = fio_total
        new_dict['fio_short_dative'] = fio_short_dative    
        return new_dict

    def create_name_file_for_claim(self):
        """Создает и возвращет имя файла для сохранения. За основу берется fio_original"""
        fio = self.ui_data.get_value("fio_original")
        return   join(name_FOLDER_SAVING_CLAIM, fio + FILE_EXTENSION_SAVING_CLAIM)    

    def report_blank_fields(self, check_result):
        """Сообщить о незаполненных полях"""
        text="Не заполнены поля:  "
        for element in check_result:
            text += element.name
            text += ";  "
        self.msg.showMessageBox(2, "Внимание", text)     