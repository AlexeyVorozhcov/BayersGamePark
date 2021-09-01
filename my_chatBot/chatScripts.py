import enum
from typing import List
from .stepOfScript import StepOfScript

class Commands(enum.Enum):
    to_start = "start" # запустить стартовый шаг
    to_next = "next" # перейти к следующему шагу
    is_last = "is_last" # это последний шаг в скрипте
    to_previous = "previous" # перейти к предыдущему шагу
    is_first = "is_first" # это первый шаг в скрипте
    to_next_message = "to_next_message" # показать следующее сообщение
    to_break = "to_break" # завершить диалог
   

def _createChatScript() -> List[StepOfScript]:
    chatScript = []
    message = "Привет! Основная задача проверки товара - не допустить выкупа аналога (конструктора других фирм), конструктора в плохом состоянии и посторонних предметов."
    add_command = Commands.to_next_message
    chatScript.append(StepOfScript(message,add_command=add_command))

    message = "Начнем?" 
    buttons = [{"Да" : Commands.to_next}]
    chatScript.append(StepOfScript(message, buttons=buttons))

    message = "ШАГ 1. Убедитесь, что детали конструктора сухие, выраженные запахи отсутствуют."
    add_command = Commands.to_next_message
    chatScript.append(StepOfScript(message,add_command=add_command))

    message = "Если конструктор мокрый или влажный, если он имеет ярко выраженный запах – ОТКАЖИТЕ В ПРИЁМКЕ."
    buttons = [{"Конструктор сухой, без запахов" : Commands.to_next,
                "Отказываю в приемке" : Commands.to_break}]
    chatScript.append(StepOfScript(message, buttons=buttons))

    message = "ШАГ 2. Осмотрите конструктор на наличие крупных посторонних предметов, видных с первого взгляда, таких как: канцелярские предметы, игрушки, не имеющие отношения к конструктору (куклы / машинки) и прочие."
    add_command = Commands.to_next_message
    chatScript.append(StepOfScript(message,add_command=add_command))

    message = "ПРИ ОБНАРУЖЕНИИ ТАКИХ ПРЕДМЕТОВ НЕОБХОДИМО ИХ ИЗВЛЕЧЬ И ПЕРЕДАТЬ ОБРАТНО КЛИЕНТУ."
    buttons = [{"Посторонних предметов нет" : Commands.to_next},
               {"Я извлек посторонние предметы" : Commands.to_next}]
    chatScript.append(StepOfScript(message, buttons=buttons))

    message = "ШАГ 3. Проверьте крупные детали, которые имеют размер с ладонь и больше, на наличие маркировки Lego и на состояние"
    add_command = Commands.to_next_message
    chatScript.append(StepOfScript(message,add_command=add_command))

    message = "Они не должны быть сломаны, разрисованы несмываемым маркером, быть испачканными пластилином, клеем и т.д."
    add_command = Commands.to_next_message
    chatScript.append(StepOfScript(message,add_command=add_command))

    message = "В случае, если крупные детали повреждены или испачканы, если на них нет маркировки Lego, ИЗВЛЕКИТЕ ИХ И ПЕРЕДАЙТЕ КЛИЕНТУ."
    buttons = [{"Крупные детали - в порядке" : Commands.to_next},
                {"Я извлёк поврежденные или испачканные крупные детали " : Commands.to_next}]
    chatScript.append(StepOfScript(message, buttons=buttons))

    message = "ШАГ 4. Проверьте конструктор на наличие деталей военно-зеленого цвета, в том числе и в составе собранных моделей. Если такие детали обнаружены, необходимо убедиться, что на них есть маркировка Lego."
    add_command = Commands.to_next_message
    chatScript.append(StepOfScript(message,add_command=add_command))

    message = "Если маркировка отсутствует – ПЕРЕДАЙТЕ ТАКИЕ ДЕТАЛИ ОБРАТНО КЛИЕНТУ."
    buttons = [{"Таких деталей нет" : Commands.to_next},
               {"Все такие детали - с маркировкой" : Commands.to_next},
               {"Я передал детали без маркировки обратно клиенту" : Commands.to_next}]
    chatScript.append(StepOfScript(message, buttons=buttons))

    message = "ШАГ 5. Осмотрите детали конструктора поверхностно."
    add_command = Commands.to_next_message
    chatScript.append(StepOfScript(message,add_command=add_command))

    message = "Если на первый взгляд видно, что 10% деталей или более являются аналогом - ОТКАЖИТЕ В ПРИЁМКЕ"
    add_command = Commands.to_next_message
    chatScript.append(StepOfScript(message,add_command=add_command))

    message = "Предложите клиенту перебрать конструктор и принести его снова."
    buttons = [{"Всё в порядке" : Commands.to_next},
               {"Отказываю в приёмке" : Commands.to_break}]
    chatScript.append(StepOfScript(message, buttons=buttons))

    message = "ШАГ 6. Теперь нужно провести выборочную детальную проверку деталей на оригинальность."
    add_command = Commands.to_next_message
    chatScript.append(StepOfScript(message,add_command=add_command))

    message = "Вытащите по 50-60 случайных деталей из каждого пакета(мешка, коробки), в которых клиент принес конструктор."
    add_command = Commands.to_next_message
    chatScript.append(StepOfScript(message,add_command=add_command))

    message = "Проверьте эти детали на наличие маркировки LEGO"
    add_command = Commands.to_next_message
    chatScript.append(StepOfScript(message,add_command=add_command))

    message = "Нужно посчитать, сколько деталей из извлеченных НЕ ИМЕЮТ маркировку"
    add_command = Commands.to_next_message
    chatScript.append(StepOfScript(message,add_command=add_command))

    message = "Введите количества в блок инфорации под чатом."
    add_command = Commands.to_next_message
    chatScript.append(StepOfScript(message,add_command=add_command))

    message = "Если доля аналога выше 10% - откажите в приёмке."
    buttons = [{"Доля аналога меньше 10%" : Commands.to_next},
               {"Отказываю в приёмке" : Commands.to_break}]
    chatScript.append(StepOfScript(message, buttons=buttons))

    message = "Теперь необходимо пересыпать конструктор из тары, в которой его принес клиент, в тару для хранения и транспортировки - синие сумки."
    add_command = Commands.to_next_message
    chatScript.append(StepOfScript(message,add_command=add_command))

    message = "Если в глубине тары, принесенной клиентом, состояние и содержимое конструктора кардинально отличается от того, что вы увидели при первичной проверке, в худшую сторону, и не соответствует правилам выкупа - откажите в приёмке."
    buttons = [{"Всё в порядке" : Commands.to_next},
               {"Отказываю в приёмке" : Commands.to_break}]
    chatScript.append(StepOfScript(message, buttons=buttons))

    message = "Теперь нужно взвесить принимаемую партию конструктора"
    add_command = Commands.to_next_message
    chatScript.append(StepOfScript(message,add_command=add_command))

    message = "Проверьте, что ваши весы настроены НА КИЛОГРАММЫ, а не на фунты !!"
    add_command = Commands.to_next_message
    chatScript.append(StepOfScript(message,add_command=add_command))

    message = "Введите общий вес принимаемой партии конструктора в соответствующее поле под окном чата"
    buttons = [{"Взвешивание произвел" : Commands.to_next}]
    chatScript.append(StepOfScript(message, buttons=buttons))

    message = "Теперь  заполните остальные поля информации, необходимые для печати Акта приёмки"
    buttons = [{"Заполнил" : Commands.to_next}]
    chatScript.append(StepOfScript(message, buttons=buttons))

    message = "Теперь распечатайте Акт приемки в нескольких экземплярах - по количеству сумок"
    buttons = [{"Распечатал" : Commands.to_next}]
    chatScript.append(StepOfScript(message, buttons=buttons))

    message = "Уточните у клиента, он хочет получить за сданный конструктор поинты или наличные"
    add_command = Commands.to_next_message
    chatScript.append(StepOfScript(message,add_command=add_command))

    message = "Произведите приёмку конструктора в 1С - в форме приёмки БУ"
    add_command = Commands.to_next_message
    chatScript.append(StepOfScript(message,add_command=add_command))

    message = "Код конструктора 570978"
    buttons = [{"Приемку в 1С произвел" : Commands.to_next}]
    chatScript.append(StepOfScript(message, buttons=buttons))

    message = "Отлично! Теперь нужно как можно быстрее (в отсутствие посетителей) запаковать тару таким образом, чтобы исключить свободный доступ к ее содержимому во время хранения и транспортировки"
    add_command = Commands.to_next_message
    chatScript.append(StepOfScript(message,add_command=add_command))

    message = "К каждой таре (сумке) нужно прикрепить по 1 экземпляру Акта приемки. На Акте должно быть указано общее количество тар и номер текущей тары. Например - 1 из 3, 2 из 3, 3 из 3"
    buttons = [{"Готово!" : Commands.to_next}]
    chatScript.append(StepOfScript(message, buttons=buttons))
    
    message = "Не забудьте уведомить руководителя магазина о данной приёмке."
    add_command = Commands.to_next_message
    chatScript.append(StepOfScript(message,add_command=add_command))

    message = "Был рад помочь, всего хорошего!"
    add_command = Commands.to_break
    chatScript.append(StepOfScript(message,add_command=add_command))

    return chatScript

class ChatScript:
    def __init__(self, name = None):
        self.name = name
        self.steps  = _createChatScript()
        self.max_step = len(self.steps)



    

