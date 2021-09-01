from .ui_element import UiElement

def from_tab_claim (ui):
    """Возвращает список ui-элементов.
    Каждый ui-элемент состоит из имени и виджета."""
    elements = []
    # person
    elements.append(UiElement("fio_original", ui.lineEdit_FIO))
    elements.append(UiElement("is_man", ui.radioButton_man))
    elements.append(UiElement("is_woman", ui.radioButton_woman))
    elements.append(UiElement("not_inclined", ui.checkBox_family_declen))
    elements.append(UiElement("passport", ui.textEdit_passport))
    elements.append(UiElement("address", ui.textEdit_address))
    elements.append(UiElement("phone", ui.lineEdit_phone))
    # product
    elements.append(UiElement("name_product", ui.lineEdit_product))
    elements.append(UiElement("is_new", ui.radioButton_new))
    elements.append(UiElement("is_gamereplay", ui.radioButton_gamereplay))
    elements.append(UiElement("is_discount", ui.radioButton_discount))
    elements.append(UiElement("price", ui.lineEdit_price))
    elements.append(UiElement("purchase_date", ui.lineEdit_purchase_date))
    elements.append(UiElement("check_number", ui.lineEdit_check_number))
    elements.append(UiElement("is_check_lost", ui.checkBox_check_lost))
    elements.append(UiElement("is_pay_cash", ui.radioButton_cash))
    elements.append(UiElement("is_pay_card", ui.radioButton_card))
    elements.append(UiElement("is_pay_internet", ui.radioButton_internet))
    elements.append(UiElement("is_reason1", ui.radioButton_reason01))
    elements.append(UiElement("is_reason2", ui.radioButton_reason02))
    elements.append(UiElement("is_reason3", ui.radioButton_reason03))
    elements.append(UiElement("defective", ui.textEdit_defective))
    elements.append(UiElement("description", ui.textEdit_description))
    elements.append(UiElement("is_demand1", ui.radioButton_demand1))
    elements.append(UiElement("is_demand2", ui.radioButton_demand2))
    elements.append(UiElement("is_demand3", ui.radioButton_demand3))
    elements.append(UiElement("is_demand4", ui.radioButton_demand4))
    elements.append(UiElement("demand_other", ui.textEdit_other))
    elements.append(UiElement("YES", ui.radioButton_YES))
    elements.append(UiElement("set1", ui.radioButton_set1))
    elements.append(UiElement("set2", ui.radioButton_set2))
    elements.append(UiElement("set3", ui.radioButton_set3))
    # organisation
    elements.append(UiElement("name_org", ui.lineEdit_organisation))
    elements.append(UiElement("co_worker", ui.lineEdit_personal))
    elements.append(UiElement("date_of_claim", ui.lineEdit_date))
    return elements

def from_tab_otkazy (ui):
    """Возвращает список ui-элементов.
    Каждый ui-элемент состоит из имени и виджета."""
    elements = []
    elements.append(UiElement("name_shop", ui.lineEdit_nameShop))
    elements.append(UiElement("OOO", ui.lineEdit_OOO))
    elements.append(UiElement("OP", ui.lineEdit_OP))
    elements.append(UiElement("adress_org", ui.textEdit_adress))
    elements.append(UiElement("director", ui.lineEdit_director))
    elements.append(UiElement("phone_oppp", ui.lineEdit_CRP))
    elements.append(UiElement("situation1", ui.radioButton_situation1))
    elements.append(UiElement("situation2", ui.radioButton_situation2))
    elements.append(UiElement("situation3", ui.radioButton_situation3))
    elements.append(UiElement("situation4", ui.radioButton_situation4))
    return elements

def from_tab_sertificate (ui):
    """Возвращает список ui-элементов.
    Каждый ui-элемент состоит из имени и виджета."""
    elements = []
    elements.append(UiElement("sert_nominal", ui.lineEdit_sert_nominal))
    elements.append(UiElement("deadline_sert", ui.lineEdit_sert_deadline))
    elements.append(UiElement("code_sert", ui.lineEdit_sert_code))
    elements.append(UiElement("sert_01", ui.radioButton_sert01))
    elements.append(UiElement("sert_02", ui.radioButton_sert02))
    elements.append(UiElement("sert_03", ui.radioButton_sert03))
    elements.append(UiElement("sert_04", ui.radioButton_sert04))
    elements.append(UiElement("sert_05", ui.radioButton_sert05))
    elements.append(UiElement("sert_06", ui.radioButton_sert06))
    elements.append(UiElement("formatA4", ui.checkBox_a4))
    
    return elements

def from_tab_lego(ui):
    """Возвращает список ui-элементов.
    Каждый ui-элемент состоит из имени и виджета."""
    elements = []
    elements.append(UiElement("shop", ui.lineEdit_shop_lego_2))
    elements.append(UiElement("date", ui.lineEdit_data_lego_2))
    elements.append(UiElement("personal", ui.lineEdit_personal_lego_2))
    elements.append(UiElement("client", ui.lineEdit_klient_lego_2))
    elements.append(UiElement("kol_all", ui.lineEdit_detal_total))
    elements.append(UiElement("kol_not_lego", ui.lineEdit_detal_lego))
    elements.append(UiElement("ves", ui.lineEdit_ves))
    elements.append(UiElement("tara", ui.lineEdit_tara))
    return elements



def list_of_checking_value_on_claim():
    result = ["fio_original", "passport", "phone", "name_product", "price",
              "purchase_date", "check_number", "name_org", "co_worker", "date_of_claim"]
    return result

def list_of_requisites():
    result = ["name_shop","OOO", "OP",
              "adress_org", "director", "phone_oppp"]
    return result    
