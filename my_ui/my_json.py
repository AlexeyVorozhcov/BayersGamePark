import json
import logging

logger = logging.getLogger(__name__)

def write_in_jsonFile (data, nameFile):
    """Записывает данные в json-файл
    Возвращает True Или False
    """
    logger.info(f"START - запись json-файла {nameFile}.")
    try:
        with open(nameFile, "w", encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
            logger.info("Записано успешно")  
    except Exception as e:
        logger.error(str(e))
        print(e)
        return False
    else: return True      

def read_from_jsonFile (nameFile):
    """
    Возвращает данные из json-файла.
    Возвращает None при ошибке.
    """
    result = None
    logger.info(f"START - чтение json-файла {nameFile}")
    try:
        with open(nameFile, 'r', encoding='utf-8') as f:
            result =  json.load(f)
            logger.info("Прочитано успешно")  
    except Exception as e:
        logger.error(str(e)) 
        print(e)             
    return result    

def read_dict_from_jsonFile(namefile):
    """
    Возвращает словарь из файла filename
    При ошибке возвращает пустой словарь
    """
    data = read_from_jsonFile(namefile)
    if not is_dict(data):
        data = {}
    return data    

def is_dict(data):
    """Возвращает True, если data - это словарь
        False - если не словарь
    """
    if type(data) == dict:
            logger.debug("Полученные данные - словарь.")
            return True
    else:
        logger.debug(f"Полученные данные не словарь. {str(type(data))}")
        return False     