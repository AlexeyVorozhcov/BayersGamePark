import urllib.request
from PyQt5.QtCore import QObject, pyqtSignal
import logging

logger = logging.getLogger(__name__)

class _MyDownload(QObject):
    signal = pyqtSignal(int, str)
    def __init__(self):
        super().__init__()
        opener = urllib.request.build_opener()
        opener.addheaders = [('User-Agent',
                            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                            'Chrome/36.0.1941.0 Safari/537.36')]
        urllib.request.install_opener(opener)
     
    def run_downloading(self, urlfile, localfile):
        """
        Скачивает файл. Возвращает True при успехе, False при ошибке
        """
        self.name = urlfile
        result = False
        logger.debug(f"Старт скачивания файла {urlfile}")
        try:
            urllib.request.urlretrieve(urlfile, localfile, self.reporthook)
            result = True
            logger.debug(f"Успешно скачано в {localfile}")
        except Exception as e:
            logger.error(f"Ошибка: {str(e)}")    
        return result

    def reporthook(self, blocknum, blocksize, totalsize):
        if blocknum*blocksize < totalsize:
            self.signal.emit(int(round(blocknum*blocksize/totalsize*100)), self.name)
        else:
            self.signal.emit(100, self.name)   


def downloading_file(url_file, downloaded_file, status_func=None):
    """
    Cкачивает файл url_file с сервера и сохраняет его копию в файл downloaded_file.
    Возвращает True или False.
    status_func - функция, которая принимает сигнал о прогрессе выполнения.
    """
    process = _MyDownload()
    # коннектит сигнал из dwn с функцией detect_signal_from_downloading
    if status_func: process.signal.connect(status_func)
    return  process.run_downloading(url_file, downloaded_file)  


# def _test_printing(n):
#     print (f"{n} %")
    

# if __name__=="__main__":
#     localfile = "TEMPLATES.zip"
#     urlfile = gv.URL_SERVER + localfile
#     dwn = MyDownload()
#     dwn.signal.connect(_test_printing)
#     dwn.run_downloading(urlfile, localfile)




