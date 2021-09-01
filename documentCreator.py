from abc import ABC, abstractmethod
from docxtpl import DocxTemplate
from os import startfile
from datetime import datetime
from assistant import get_name_month
from num2words import num2words
from settings import name_FOLDER_TEMPLATES, join, name_FOLDER_SAVING_CLAIM, logging

logger = logging.getLogger(__name__) 

class DocumentCreator(ABC):
    """
    Класс создания документов word из шаблонов
    """
    def __init__(self, dictData : dict):
        """[Абстрактный класс создания документа docx из шаблона с jinja]
        Args:
            dictData (dict): [словарь с данными для рендеринга шаблона]
        """
        logger.info(f"Запуск {self.__class__.__name__}")
        self.dictData = dictData 
        logger.info(f"Принятый словарь: {self.dictData}")
        self.docType = self._getDocType()
        logger.info(f"Тип документа: {self.docType}")
        self.fileDocx = self._getFileDocx()
        logger.info(f"Создаваемый файл: {self.fileDocx}")
        self.template = self._getTemlpateFile()
        logger.info(f"Используемый шаблон: {self.template}")
        self.context = self._getContext()
        logger.info(f"Сгенерированный контент: {self.context}")
        self._startDocument()

    @abstractmethod
    def _getDocType(self):
        """Возвращает тип документа - добавляет его в имя создаваемого файла
        """
        pass
    
    @abstractmethod    
    def _getFileDocx(self):
        """Возвращает имя создаваемого файла
        """
        pass

    @abstractmethod
    def _selectTemplate(self):
        """Возвращает выбранный на основе данных словаря шаблон
        """
        pass

    def _getTemlpateFile(self):
        """Returns:
            [str]: [полное имя шаблона, который будет использоваться ]
        """
        template = self._selectTemplate()
        if template: return join(name_FOLDER_TEMPLATES, template)   

    @abstractmethod
    def _getContext(self):
        """Формирует и возвращает словарь, который используется для замены jinja в шаблоне
        """
        pass

    def _startDocument(self):
        """ Стартует формирование документа из шаблона
        """
        logger.info("Старт формирования документа")
        try:
            self.doc = DocxTemplate(self.template)
            self.doc.render(self.context)
            self.doc.save(self.fileDocx)
            startfile(self.fileDocx)
        except Exception as e:
            logger.error(f"Не удалось создать документ {self.fileDocx}. Ошибка: {str(e)}")
        logger.info("Успешно.")

class DocumentCreator_Claim(DocumentCreator):
    
    def __init__(self, dictData : dict):
        super().__init__(dictData)
          
    def _getDocType(self):
        return ("заявление")

    def _getFileDocx(self):
        """
        Возвращает название сохраняемого файла docx
        """
        namefile = self.dictData.get("fio_original", "None") + self.docType
        return join(name_FOLDER_SAVING_CLAIM, namefile + '.docx')

    def _selectTemplate(self):
        template = None
        if self.dictData.get("set1") or self.dictData.get("set2"): template = "template - claim.docx"
        if self.dictData.get("set3"): template = "template - claim and RKO.docx"
        return template

    def _getContext(self):
        """
        Возвращает словарь для использования в шаблоне word-документа
        """
        # claim = self.dictData.get
        nonvalue = "Нет"
        context = { 
            'магазин' : self.dictData.get("name_org", nonvalue),
            'заявитель' : self.dictData.get("fio_short_declen", nonvalue),
            'паспорт' : self.dictData.get("passport", nonvalue),
            'адрес' : self.dictData.get("address", nonvalue),
            'телефон' : self.dictData.get("phone", nonvalue),
            'заявитель_полностью' : self.dictData.get("fio_total", nonvalue),
            'товар' : self.dictData.get("name_product", nonvalue),
            'дата_покупки' : self.dictData.get("purchase_date", nonvalue),
            'номер_чека' : self.dictData.get("check_number", nonvalue),
            'стоимость' : self.dictData.get("price", nonvalue),
            'недостатки' : self.dictData.get("defective", nonvalue),
            'заявитель_кратко' : self.dictData.get("fio_short", nonvalue),
            'сотрудник' : self.dictData.get("co_worker", nonvalue),
            'дата' : self.dictData.get("date_of_claim", nonvalue),
            'дата_акт' : "_"*15
            }
        if self.dictData.get("is_woman"): context['окончание'] = "а"
        if self.dictData.get("is_gamereplay"): context['товар'] += " (БУ)"
        if self.dictData.get("is_discount"): context['товар'] += " (Discount)"
        if self.dictData.get("is_check_lost"): context['номер_чека'] += " (чек утерян)"
        if self.dictData.get("is_pay_cash"): context['способ_оплаты']= "наличные"
        if self.dictData.get("is_pay_card"): context['способ_оплаты']= "банковская карта"
        if self.dictData.get("is_pay_internet"): context['способ_оплаты']= "оплата в интернет-магазине"
        if self.dictData.get("is_reason1"): context['причина']= "Ошибка выбора."
        if self.dictData.get("is_reason2"): context['причина']= "Недостаток товара."
        if self.dictData.get("is_reason3"): context['причина']= ""
        if self.dictData.get("is_demand1"): context['требование']= "провести проверку качества товара, расторгнуть договор купли-продажи и вернуть деньги"
        if self.dictData.get("is_demand2"): context['требование']= "провести проверку качества товара, устранить указанные недостатки"
        if self.dictData.get("is_demand3"): context['требование']= "провести проверку качества товара, обменять товар на аналогичный"
        if self.dictData.get("is_demand4"): context['требование']= self.dictData.get("demand_other", nonvalue )
        if self.dictData.get("YES"):
            context['описание'] = self.dictData.get("description", nonvalue)
            context['номер_чека_акт'] = self.dictData.get("check_number", nonvalue)
            if self.dictData.get("is_check_lost"): context['номер_чека_акт'] = " чек утерян "
            context['дата_покупки_акт'] = self.dictData.get("purchase_date", nonvalue)
            context['дата_акт'] = datetime.date(datetime.today()).strftime("%d.%m.%Y")
        if self.dictData.get("set3"):
            context['организация'] = self.dictData.get("OOO", nonvalue)
            context['подразделение'] = self.dictData.get("OP", nonvalue)
            context['дата_рко'] = datetime.date(datetime.today()).strftime("%d.%m.%Y")
            context['сумма00'] = self.dictData.get("price", nonvalue) + ",00"
            context['заявитель_дательный_падеж'] = self.dictData.get("fio_short_dative", nonvalue)
            context['основание'] = "расторжение договора купли-продажи, возврат денег"
            try:
                context['сумма_прописью'] = num2words (int(self.dictData.get("price", nonvalue)), lang = 'ru')
            except Exception as e:
                context['сумма_прописью'] = ""
            context['приложение1'] = "заявление от " + self.dictData.get("date_of_claim", nonvalue) + ""
            context['приложение2'] = "акт передачи товара от " + context['дата_акт']
            context['ч'] = datetime.today().day
            context['месяц'] = get_name_month(datetime.today().month)
            context['год'] = datetime.today().year
            context['документ'] = 'паспорту ' + self.dictData.get("passport", nonvalue)
        return context

class DocumentCreator_Letter(DocumentCreator):
    def __init__(self, dictData : dict):
        super().__init__(dictData)

    def _getDocType(self):
        return "(отказное письмо)"

    def _getFileDocx(self):
        """
        Возвращает название сохраняемого файла docx
        """
        namefile = self.dictData.get("fio_original", "None") + self.docType
        return join(name_FOLDER_SAVING_CLAIM, namefile + '.docx')

    def _selectTemplate(self):
        template = None
        if self.dictData.get("situation1"): template ="letter_001 (TSG).docx" 
        if self.dictData.get("situation2"): template ="letter_002 (BOOKS).docx"
        if self.dictData.get("situation3"): template ="letter_003 (others - not kept in presentation).docx"
        if self.dictData.get("situation4"): template ="letter_004 (others - more than 14 days have passed).docx"
        return template
        
    def _getContext(self):
        context = { 'реквизиты' : self.dictData.get("OOO") + ", \n " +
                        self.dictData.get("OP") + ", \n" + 
                        self.dictData.get("adress_org"),
                    'заявитель' : self.dictData.get("fio_short_declen"),
                    'дата' : self.dictData.get("date_of_claim"),
                    'товар' : self.dictData.get("name_product"),
                    'магазин' : self.dictData.get("name_org"),
                    'ОППП' : self.dictData.get("phone_oppp"),
                    'директор' : self.dictData.get("director"),
                    'дата_письма' : datetime.date(datetime.today()).strftime("%d.%m.%Y"),
                    'заявитель_полностью' : self.dictData.get("fio_total"),
                    'телефон' : self.dictData.get("phone"),
                    'адрес' : self.dictData.get("address")
                    }
        return context

class DocumentCreator_Sert(DocumentCreator):
    def __init__(self, dictData : dict):
        super().__init__(dictData)
            
    def _getDocType(self):
        return ""

    def _getFileDocx(self):
        return join(name_FOLDER_SAVING_CLAIM, 'sertificate.docx')    
    
    def _selectTemplate(self):
        if self.dictData.get("sert_01"):
            if not self.dictData.get("formatA4"):
                return "template - stamp on a gift certificate.docx"
            else:
                return "template - stamp on a gift certificate_a4.docx"
        if self.dictData.get("sert_02") :
            if not self.dictData.get("formatA4"):
                return "template - stamp on a gift certificate.docx"
            else:
                return "template - stamp on a gift certificate_a4.docx"
        if self.dictData.get("sert_03"):
            if not self.dictData.get("formatA4"):
                return "template - stamp on a gift certificate.docx"
            else:
                return "template - stamp on a gift certificate_a4.docx"

        if self.dictData.get("sert_04"):
            if not self.dictData.get("formatA4"):
                return "template - stamp on a gift certificate_2.docx"
            else:
                return "template - stamp on a gift certificate_2_a4.docx"
        if self.dictData.get("sert_05"):
            if not self.dictData.get("formatA4"):
                return "template - stamp on a gift certificate_2.docx"
            else:
                return "template - stamp on a gift certificate_2_a4.docx"
        if self.dictData.get("sert_06"):
            if not self.dictData.get("formatA4"):
                return "template - stamp on a gift certificate_2.docx"
            else:
                return "template - stamp on a gift certificate_2_a4.docx"
        
        
    def _getContext(self):
        context = { 
            'сум' : self.dictData.get("sert_nominal"),
            'срок' : self.dictData.get("deadline_sert"),
            'код' : self.dictData.get("code_sert")
            }
        return context    

class DocumentCreator_Lego_auto(DocumentCreator):
    def __init__(self, dictData : dict):
        super().__init__(dictData)
            
    def _getDocType(self):
        return "(приемка лего)"

    def _getFileDocx(self):
        namefile = self.dictData.get("client", "None") + self.docType
        return join(name_FOLDER_SAVING_CLAIM, namefile + '.docx')     

    def _selectTemplate(self):
        return "template - Lego auto.docx"
        
    def _getContext(self):
        context = { 
            'магазин' : self.dictData.get("shop"),
            'дата' : self.dictData.get("date"),
            'сотрудник' : self.dictData.get("personal"),
            'клиент' : self.dictData.get("client"),
            'кол_всего' : self.dictData.get("kol_all"),
            'кол_без_марк' : self.dictData.get("kol_not_lego"),
            'вес' : self.dictData.get("ves"),
            'тара' : self.dictData.get("tara")
            }
        try:
            context['кол_с_марк'] = int(self.dictData.get("kol_all"))-int(self.dictData.get("kol_not_lego")) 
        except Exception:
            pass        
        return context 

if __name__=="__main__":
    dictData = {"sert_nominal" : "500",
                "deadline_sert" : "31.08.2021",
                "code_sert" : "545454544",
                "sert_01" : True
                }
    DocumentCreator_Sert(dictData)      

    dictData = {'OOO' : "ООО КомТрейдХолдинг",
                'fio_short_declen' : "Петрова И.А.",
                'date_of_claim' : "15.04.2021",
                'name_product' : "Приставка Sony PlayStation 4",
                'name_org' : "Gamepark",
                'phone_oppp' : "202-17-08",
                'director' : "Котов Артем Михайлович",
                'fio_total' : "Петров Иван Андреевич",
                'phone' : "89152586321",
                'address' : "г. Н.Новгород, ул. Бетанкура 17-55",
                "fio_original" : "Петров Иван Андреевич",
                "situation1" : True
                }
    # DocumentCreator_Letter(dictData)

