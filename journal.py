import logging
from os import remove
from myPost2 import send_email

_log_format = f"%(asctime)s - %(message)s"
_name_file = "journal.txt"

def _get_file_handler():
    file_handler = logging.FileHandler(_name_file, mode='a')
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter(_log_format,"%Y-%m-%d %H:%M:%S"))
    return file_handler  

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(_get_file_handler())    


class Journal:
    def __init__(self):
        """Объект сохраняет логи журналирования, отправляет их на электронную почту при достижении
        их количества до _count. 
        _name_shop используется для заголовка письма"""
        self._name_shop = "Магазин не установлен"  
        self._count = 50

    def set_name_shop(self, name):
        self._name_shop = name

    def set_count(self, count):
        self._count = count

    def log(self, msg):
        logger.info(msg)
        self._check_count()

    def _send_mail(self):
        subj = "Журнал: " + self._name_shop
        text = self._name_shop
        files = [_name_file]
        send_email("alex.vorozhcov@yandex.ru", subj, text, files)

    def _check_count(self):
        with open(_name_file, "r") as f:
            data = f.readlines()
        if len(data)>self._count:        
            self._send_mail()
            logging.shutdown()
            remove(_name_file)
            self.log(f"Данные({len(data)} записей) отправлены на почту разработчику.")



if __name__ == "__main__":
    journal = Journal()
    journal.set_name_shop("Gamepark (Европейский)")
    journal.log("Запись журнала!!")
    for i in range(50):
        journal.log("Запись журнала!!")
  


