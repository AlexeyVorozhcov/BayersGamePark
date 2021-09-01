class MyCustomError(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return (self.__class__.__name__) + ": " +self.message
        else:
            return (self.__class__.__name__) + ": какая-то ошибка"


class StopUpdate(MyCustomError):
    def __init__(self, *args):
        """Исключение для остановки обновления"""
        super().__init__(*args)

class StopProcess(MyCustomError):
    def __init__(self, *args):
        """Исключение для остановки обновления"""
        super().__init__(*args)        

            


if __name__=="__main__":
    try:
        raise StopUpdate("Не найден файл")
    except Exception as e:
        print(str(e))    