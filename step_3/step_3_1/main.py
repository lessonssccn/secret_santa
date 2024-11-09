#пример консольного приложения для распределения тайных сант, в процедурном стиле 
#здесь лего видеть насколько разросся код по сравнению с первым шагом
#хотя функционал не изменился (если только незначительно)
#в шаге 3_1 будте только ввод с клавиатуры загрузка из файла будет в шаге 3_2, в шаге 3_3 планируется совмещать оба шага
#возможность редактировать данных загруженных из файла, ввод имени файла для сохранния результат и тд
#здесь разбиение на процедуры и функции произведенно не сильно оптимально большая часть функций работает с вводом выводом
#очень мало функций содержат логику, тоесть занимаются распределением пар и генерацией сообщений
from random import shuffle #функция для перемешивания списка

#функция дл получения коректного номера элемента
#с проверкой корекности ввода пользователя
#valid_values - список возможных значений целые числа
def select_item(valid_values:list[int]=None) -> int:
    while True:#пока пользователья не ввел подходящее значение продолжаем требовать номальный ввод
        number = input()#получаем строку от пользователя
        if number.isnumeric(): #проверяем что строка содержит число
           number = int(number) # преобразуем строку в число
           #проверка если не предали списко или список пуст или введенное значение из этого списка,
           #значит полученное число коректно
           if valid_values==None or len(valid_values)==0 or (number in valid_values):
               return number# возвращаем его
        show_msg("error_select") #выводим сообщение о том что введено не верное значение

#получение не пустой строки из консоли, удаляет лишнии пробелы вначале и конце
#так же есть проверка значений на совпадение со списком строк
def input_non_empty_str(valid_values:list[str]=None) -> str:
    while True:
        value=input().strip()#считываем строку и удаляем лишние пробелы
        if len(value):#проверяе пустая строка или нет
            #если передан не пустой списко валидных значений, то проверяем на вхождение в список
            if valid_values == None or len(valid_values)==0 or (value in valid_values):
                return value #возвращаем полученную строку
            else:
                show_msg("error_value")#сообщаем о не валидности введеннго значения
        else:
            show_msg("empty_str")#сообщаем о пустой строку

#получение положительного целого числа без ограничений ограничений по вличине
def input_positive_int_number() -> int:
    while True:
        value = input()
        if value.isnumeric():
            value = int(value)
            if value > 0:#елси число больше нуля
                return value #возвращаем его
            else:
                show_msg("error_positive")#сообщаем что число не положительное
        else:
            show_msg("error_int")#сообщаем что введенно не чсило

#функция возвращабщее список элементов меню, по названию меню
#принимает строку с названием меню и возврщает словарь где ключ номер действия задан как целое число, 
#а значение строка содержащая текст который нужно показать при вывод этого меню
# если по переданной на вход строке не найденно значение, то будет возвращет словарь  {0:"Закончить"}
#облегчает от части наполнение меню
#заполняем меню так чтобы 0 был отменой действия или выходом
def get_menu_items(type_menu: str) -> dict[int, str]:
    #все работает за счет словаря, где ключи имена меню, а значения словари,
    #в идиале такая структура должна читаться из файла, а не храниться в программе, но пока так
    menu_dict = {
        "main":{
            1: "Вввод с клавиатуры",
            2: "Загрузить анкеты из файлов",
            0: "Остановить работу",
        },
        "console":{
            1: "Начать распределение сант",
            2: "Отредактировать анкету участника",
            3: "Добавить нового участника",
            4: "Удалить участника",
            5: "Показать состав команды",
            6: "Повторить, я сильно ошибся, надо начать все поновой",
            0: "Выйти в главное меню",
        },
        "console_editor":{
            1: "Изменить имя",
            2: "Изменить желение",
            3: "Изменить все",
            0: "У нас отмена!",
        }
    }
    #get берет значение по ключу если значения нет, берет второй параметр как значение по умолчанию
    return menu_dict.get(type_menu, {0:"Закончить"})

#функция что по имени сообщения возвращает его текст
#может быть возвращет список строк если сообщение должно состоять из нескольких строк
#или одна строка, если сообщение должно содержать места для подстановки {} - это они вни указанно значение какой переменной в них подставить
#имя перенной(параметра) должно соовпадать с тем что казаанно в {}
#облегчает изменение текста сообщений ненадо искать по всему коду что редактировать 
def get_msg(type_msg: str) -> list[str]|str:
    #работает на базе словаря ключ имя сообщения значение само сообщение ввиде списка строк или строки с подставновками
    msg_dict = {
        "empry_row":["\n"],
        "hi":["Привет, я помогу тебе с распределением участников товоей команды для тайного санты"],
        "ok":["Хорошо с этим разобрались", "Идем дальше"],
        "restart":["Хорошо","Начнем по новой"],
        "menu":["Введи номер дейсвтия", "Нужно ввести один из предложенных номеров и ничего больше. Иначе ничего не получиться"],
        "error_select":["Выбери один из предложенных вариантов","Введи только номер", "Только цифры и ничего больше"],
        "action_not_found":["Что-то пошло не так", "Дейсвтие не найдено, придеться попробовать снова"],
        "finish":["Пока", "Ты, заходи, если что"],
        "error_int":["Введи число", "Я знаю ты это сможешь сделать"],
        "error_positive":["Число должно быть больше нуля"],
        "group_name":["Введи имя команды"],
        "group_size":"Введи количестов участников команды {group_name}",
        "error_value":["Введенно не коректное значение", "Попробуй снова", "Я предложил варианты выше"],
        "empty_str":["Введи не пустую строку", "Пробелы не считаются", "Не надо хитрить"],
        "input_forms":"Заполни анкеты участников команды {group_name}",
        "person_name":"Введи имя {index} участника",
        "person_wish":"Введи желание {person_name}",
        "next_step": ["Что будем делать дальше", "Может ты хочешь, что-то поменть?"],
        "group": "Вот состав участников команды {group_name}",
        "edit_group": "Анекут кого из участников команды '{group_name}' ты хочешь отредактировать",
        "input_person_number": ["Введи номер участника", "Целое положительное число", "Номера участников тебе выведены ничего придумывть ненадо", "Если передумал введи 0"],
        "edit_person": "Что именно ты хочешь отредактировать для {person_name}",
        "new_name": "Ввведи ново имя для {person_name}",
        "new_wish": "Ввведи ново желание для {person_name}",
        "add_new_person": "Кого добавим в {group_name}",
        "delete_person": "Кого выкинем из {group_name}",
        "group_empty": "Ого, кажется в группе {group_name} никого нет",
        "distribution": "Вот так можно распределить участников команды {group_name}",
        "clones":["Команде будет не просто", "У вас завелись клоны", "При желании можно все исправить или осавить как есть", "Вот их имена:"],
        "less_then_3_persons":["Команда слишком мала", "Нужно минимум 3 участника, а то интриги небудет"],
        "pair_wish": "Кто: {who}\nКому: {whom}\nЖелание: {wish}\n",
        "in_next_verion":["Пока не доступно будет", "Будет в следующей версии", "Пока придеться использовать то что есть"],
        "menu_item":"{number}) {text}",
        "person_info":"{number}) {person_name} {wish}",
        "edit_clone": ["Уберем клонов, отредктирова группы перед стартом", "1 - да", "0 - нет"]
    }
    #если в словаре нет указанно ключа возвращаем дефолтное сообщение ввиде списка с одной строкой ["Упс, что-то пошло не так"]
    return msg_dict.get(type_msg, ["Упс, что-то пошло не так"])
#функция вывода на консоль сообщений
#msg - список строк или строка с подстановками, предполагаем что если передали строку то вней должна быть подставновка
#**kwargs позволяет передать не ограниченное число именнованных аргументов в нутри функции сним можно рабоать как со словарем с именм kwargs
def print_msg_console(msg: list[str]|str, **kwargs) -> None:
    if type(msg) == str:#проверяем тип
        print(msg.format(**kwargs)) #если строка то вызываем форматирование, чтобы заменить подстановку внутри строки
        #format предлагает передать ему неограниченное количесвто агументов или именованных аргументов
        # мы передаем именованные аргументы разбивая словарь kwargs спомощь ** на отедльные именнованные аргументы при вызове метода 
        # format - это метод который сформирует новую строку после замены всех подстановок и мы эту строку принтанем
    else:
        for row in msg:#если передан список проходимся по элементам списка
            print(row)#выводим каждую строку из списка на консоль
    
#вывод на экран пунктов меню в формате
#номер и текст по одному пунку на каждой строке
#навход идет словарь из ключ - целое число номер дейсвия, значение - текст пунта меню
def print_menu_console(menu_items: dict[int, str]) -> None:
    # menu_items.items() возвращаяет аля списко из кортежей где нулево элемент это ключ а первый значение
    #for number, text in menu_items.items(): пайтон самостоятельно разобьет кортеж на две отдельных переменных
    for number, text in menu_items.items():#проходимя по всему словарю
        print_msg_console(get_msg("menu_item"), number = number, text = text)
    
#функция которая принимает на вход словарь представляющий из себя пункты меню 
#и возвращающая список из ключей словаря
def get_valid_action(menu_items: dict[int, str]) -> list[int]:
    return list(menu_items.keys())# keys() возвращает не до список из ключей поэтому его преобразуем в список через list()

#выводит сообщение по его имени
#принимает имя он же тип сообщения и неограниченный набор именнованных аргументов 
def show_msg(type_msg:str, **kwargs) -> None:
    print_msg_console(get_msg(type_msg.lower()), **kwargs) #type_msg.lower() преобразуем имя сообщения в нижний регистр чтоюы уменьшить ошибку тк в словаре будем хранить все ключи в нижнем регистре

#печатаем меню и выводим сообщение с правилами работы с ним
def show_menu(type_menu:str) -> None:
    print_menu_console(get_menu_items(type_menu))
    show_msg("menu")

#основной цила программы
def main_loop() -> None:
    show_msg("hi")#выврдим приветсвие
    while True:#запускаем показ главного меню и опрос како дейсвтие вывбрать, а также анализируем выбор пользователя
        show_menu("main")#покзываем меню
        #get_menu_items - возвращает меню по имени
        #get_valid_action - возвращает значения номеров пунктов для валидации при вводе
        action = select_item(get_valid_action(get_menu_items("main")))#ждем ввод пользователя для валидации передаем номера пунктов меню 
        if action == 0:#ввели 0
            finish() #заваершаем программу
        elif action == 1:
            console_loop() #запускаем цикл для работчы с консольным вводом
        elif action == 2:
            file_loop()#не реализованно но будет запускать чтение файлов
        else:
            show_msg("action_not_found")#на всякий лсучай сделанно такого быть не должно, но если что выводим что дейсвие не найеденно

#функция красивого замерешния програмы
def finish() -> None:
    show_msg("finish")#выводим финальное сообщение
    exit(0)#останавливаем програму с кодом 0

#функция для облегчения ввода первого состава группы
def input_person_list(group_size:int) -> list[dict[str,str]]:
    persons = []
    for index in range(1, group_size+1):#через цикл гененируем номер для члекнов группы
            persons.append(input_person(index))#вызывае функцию для ввода информации о члене группы передавая внее номер участника
    return persons

#функция редактирования одного участника группы
def edit_person_console(person:dict[str,str]) -> None: #
    person_name = person["person_name"]#извлекаем имя из словаря для удобсва
    show_msg("edit_person", person_name = person_name)#предложение о редактиовании
    show_menu("console_editor")#вывод меню для редактирования
    action = select_item(get_valid_action(get_menu_items("console_editor")))#получаем ввода
    if action == 1:
        show_msg("new_name", person_name=person_name)#проссим ввести новое имя
        person["person_name"] = input_non_empty_str() #вводим имя и сразу заменяем значение в словаре словарь измениться тк ссылочный тип данных
    elif action == 2:
        show_msg("new_wish", person_name=person_name) #просим ввести новое желание
        person["wish"] = input_non_empty_str() #вводим новое желение 
    elif action == 3: #объеденяем предыдущие шаги
        show_msg("new_name", person_name=person_name)
        person["person_name"] = input_non_empty_str()
        show_msg("new_wish", person_name = person["person_name"])
        person["wish"] = input_non_empty_str()
    elif action == 0:
        return
    else:
        show_msg("action_not_found")

#фнкция для опроса кого именно из группы хотим от редачить
#требует ввести номер участника группы
def edit_group_console(group:dict) -> None:
    group_name = group['group_name']
    persons = group['persons']
    show_msg("edit_group", group_name = group_name)
    show_group(group, show_wish=True)
    show_msg("input_person_number")
    number = select_item(list(range(0, len(persons)+1)))# для валидации передаем список с номерами участников и 0 если надо отменить действие
    if number != 0: #если выбран не 0 то редактируем 
        edit_person_console(persons[number-1])#вычитаем еденицу из номера тк индексация от 0 а не с 1

#для вывода на консоль состава группы принимает группу и флаг необходимости вывода желения участника
#group - словарь из 2 ключей ключ group_name - имя групы как значение 
# и ключ persons - списко информации об участника группы
# один участник это словарь из 2 ключаей person_name - имя и wish желение все строки
def show_group(group:dict, show_wish:bool=False) -> None:
    persons = group["persons"] #для удобства получаем список участникив
    if len(persons) > 0:#проверяем список на пустоту 
        show_msg("group", group_name=group["group_name"])#если не пусто выводим сообщение 
        for index, person in enumerate(persons):#и список участников enumerate - генерирует индексы которые мы увеличим на 1 
            wish = person['wish'] if show_wish else '' #используем тернарную операцию для формирования желания если надо берем из словаря иначе пустая строка 
            show_msg("person_info", number = index+1, person_name = person['person_name'], wish = wish)
    else:
        show_msg("group_empty", group_name=group["group_name"])#если группы пустая сообшаем об этом
    
#функция первичного заполения информации о группе
def first_console_input_for_group() -> dict:
    show_msg("group_name")#предложение ввести имя грппы
    group_name = input_non_empty_str() # принимаем имя группы
    show_msg("group_size", group_name=group_name)#предлагаем ввести количество участников для первичного заполения =
    group_size = input_positive_int_number()#считываем колво участников
    show_msg("input_forms", group_name=group_name) #прдлагаем заполнить анекты участникво
    persons = input_person_list(group_size)#запскаем функцию ввода нужного числа участников
    return {
        "group_name":group_name,
        "persons":persons
    }#формируем словарь и возвращеем его как результат

#функйия для ввода информации об одном участнике группы
#принимает на вход номер участника для крассивого вывода информации
def input_person(number:int) -> dict[str, str]:
    show_msg("person_name", index=number)#предлагаем ввести имя уучастника с указанием его номера
    person_name = input_non_empty_str()#получаем имя участника
    show_msg("person_wish", person_name=person_name)#предлагаем ввести желание участника при этом выводим имя участника
    wish = input_non_empty_str()# получаем желание
    return {"person_name": person_name, "wish": wish}#формируем словарь и возвращаем его

#функция дбавления нового участника
def add_new_person(group:dict) -> None:
    persons = group["persons"] #для удобства получаем список текущих участникво
    show_msg("add_new_person", group_name = group["group_name"])#предлагаем ввести инофрмацию оновом участнике
    persons.append(input_person(len(persons)+1))#добовляем участника в список после ввода информации о нем номер участника длина списк + 1
    #список ссылочный тип данных потому он изменяется в самой группе

#удаление участника из группы 
def delete_person(group:dict):
    persons = group["persons"] #берем список участников
    show_msg("delete_person", group_name = group["group_name"])
    show_group(group, show_wish=True)#выводим списко участников вместе с их желаниями
    show_msg("input_person_number")#предлагаем ввести номер удаляемого участника
    number = select_item(list(range(0, len(persons)+1)))# ждем ввод номера или 0 для отмены
    if number != 0:
        persons.pop(number-1) #удаляем из списка нормер - 1 тк индексы идут от 0 а нумирацию мы показываем от 1

#выводим список ошибок сейчас не особо важна но позже будете интереснее 
def show_error(list_error):
    if len(list_error)>0:#если список не пуст печатем его на консоль
        print_msg_console(list_error)

#фнкция с циклом консольного заполения
def console_loop()->None:
    while True:#начала цикла повторного заполенения группы
        group = first_console_input_for_group()#предлагаем первичное заполнение информации о группе
        show_group(group, show_wish=True)#выводим сотав группы
        while True:#начало цикла редактирования группы
            show_msg("next_step")#предлагаем выбрать что делать дальше после заполнения информации о группе
            show_menu("console")#выводим меню для консольного редактирования
            action = select_item(get_valid_action(get_menu_items("console")))#ожидаем ввода дейстия
            '''
            1: "Начать распределение сант",
            2: "Отредактировать анкету участника",
            3: "Добавить нового участника",
            4: "Удалить участника",
            5: "Показать состав команды",
            6: "Повторить, я сильно ошибся, надо начать все поновой",
            0: "Выйти в главное меню",
            '''
            if action == 1:
                generation_possible, has_clone, list_error = validate_group(group)#проверяем группу на возможность генерации 
                # и участников с одинаковыми иминами из функции возвращается кортеж из 3 элементов 
                # 0 элемен доступна ли генерация 1 есть ли клоны(участники с одинаковыми иминами) 2 это сисок ошибок
                show_error(list_error)#выводим список ошибок если сипсок пуст ничего не выйдет
                if generation_possible:
                    if has_clone:#если есть клоны 
                        show_msg("edit_clone")# редлагаем отредачить группу
                        action = select_item([0,1])#предлагаем дейсвтие 0 - отмена 1 - редактирование
                        if action == 1: 
                            continue#если выбранно 1 то пропускам что ниже и возвращаемся в начало цикла редактироваания
                    #если выбранно 0 то проверяем доступность генерации если достпуно начинаем генерировать и выводить
                    #для не посредственного разбиения на пары используется generate_pair
                    #для формирования красивого вывода используем make_pretty_distribution 
                    #возвращает словарь с названием группы и список словарей со значениями кто кому и что дарит
                    #show_pretty_distribution выводит информацию о расрпеделении
                    show_pretty_distribution(make_pretty_distribution(group, generate_pair(group)))
            elif action == 2:
                edit_group_console(group)# предлагаем отредачить пользователя
                show_msg("ok")#
            elif action == 3:
                add_new_person(group)# добавляем новго пользователя без возможности отменить действие
                show_msg("ok")
            elif action == 4:
                delete_person(group)# удаление пользоватлея 
                show_msg("ok")
            elif action == 5:
                show_group(group, show_wish=True)# вывод сосстава группы в месте с их желаниями
            elif action == 6:
                show_msg("restart")# сообщение о начале заполенения группы поновой
                break# прерываем цикл редактирования и начианаем с нуля все заполнять возвращаясь в начало внешнего цикла
            elif action == 0:
                return# заврешаем работу функции прерываються оба цикал
            else:
                show_msg("action_not_found")

#красивый вывод расрпеделения сант
def show_pretty_distribution(distribution:dict) -> None:
    show_msg("distribution", group_name = distribution["group_name"])#выводим сообщение с вставленным именем команды
    for pair in distribution["pairs"]:#проходимя по прам 
        show_msg("pair_wish", who=pair['who'], whom=pair['whom'], wish=pair['wish'])#выводим информацию о паре и что дарить 
        #who - кто whom - кому wish - что

#из словоря клонов извлекаем список имен клонов
def get_list_clone_name(clones:dict[str,list[dict]]) -> list[str]:
    return list(clones.keys())

#функция формирующая список ошибко о клонах и cам список кловнов
def create_error_msg_clone(clones:dict[str,list[dict[str,str]]]) -> list[str]:
    list_clone_error_msg = []
    list_clone_error_msg.extend(get_msg("clones")) #extend берет спсиок и все его элементы добавляет в список указаный перед точкой
    list_clone_error_msg.extend(get_list_clone_name(clones))
    return list_clone_error_msg

#составляем словарь клонов ключ имя клона значение список клонов в списке хроняться словари описывающие участника команды
def find_clones(persons: list[dict[str,str]]) -> dict[str,list[dict[str,str]]]:
    clones = dict()
    #формируем словать из имен участников и спписка персон если дублей нет то в каждом списке будет ровно одна персона
    for person in persons:
        name = person["person_name"]
        list_person = clones.get(name, list())#прием описан в шаге 2 
        list_person.append(name)
        clones[name] = list_person
    #как уже писал items возврашет недосписок из кортежей этот недосписок чувстивтелене к изменению состава ключей 
    #словаря поэтому надо обязательно преобразовать в нормальный список и наче пойдут ошибки
    #при удлаении элементов из словаря
    #удаляем из словаря те пары для которых в списке одна персона значит это не клоны
    for name, list_person in list(clones.items()):
        if len(list_person) == 1:
            del clones[name]
    return clones

#проверяем группу на норамльность заполенения и чсиленность
def validate_group(group: dict) -> tuple[bool, bool, list[str]]:
    list_error = []
    generation_possible = True#фалга возможности начать генерацию
    persons = group["persons"]

    if len(persons) <3:#если менее 3 участников
        generation_possible = False#высталвяем флаг в занчение что генерация не возможна
        list_error.extend(get_msg("less_then_3_persons"))#добавлем в конец сипска ошибко все элементы сипска сообщенйи

    clones = find_clones(persons)#ищим клонов
    has_clone = len(clones) > 0 #если соварь не пуст клоны есть
    if has_clone:#если клоны есть
        list_error.extend(create_error_msg_clone(clones))#формируем списко ошибок о наличии клонов и добавляем его в список

    return generation_possible, has_clone, list_error #возвращем 3 значения

#генериуем список содержащий индексы кто дарит и кому дарит
#содержит сипсок кортежей из 2 элементов 0 - элемет индекс дарителя 1 - индекс кому дарить
def generate_pair(group:dict) -> list[tuple[int]]:
    count_person = len(group["persons"])#определеяем сколько участников в группе 
    list_shuffled_index = list(range(0, count_person)) #генеируем список индексов
    shuffle(list_shuffled_index) #перемешиваем его
    
    #проверяем если индекс остался на своем месте меняем его со значением слева оно точно не на своем месте, 
    #тк либо отсутвует и мы возмем элемент с конца, или уже проверенно и оно не совподает со своим индексом
    for index in range(0, count_person):
        if index == list_shuffled_index[index]:
            list_shuffled_index[index], list_shuffled_index[index-1] = list_shuffled_index[index-1], list_shuffled_index[index]
    return list(zip(range(0, count_person), list_shuffled_index)) # возвращаем список из кортежей, 
                                                                  #где каждый  каждый кортеж содержит пару элементов
                                                                  #нулеовй элемент - номер санты
                                                                  #первый элемен - номер получателя подарка
                                                                  #нумерация участникво от нуля

#формируем удобныое для вывода распределение с именем группы и списокм кто-кому-что
def make_pretty_distribution(group:dict, pair_list:list[type[int]]) ->dict:
    result = {}#результирующий ловать
    persons = group["persons"]
    result["group_name"] = group["group_name"]
    result["pairs"] = []

    for who, whom in pair_list: #проходимся по списку пайтон сам разбивает кортеж на отдельные пременные
        result["pairs"].append({
            "who":persons[who]["person_name"],
            "whom":persons[whom]["person_name"],
            "wish":persons[whom]["wish"]
        })#формируем словарь
    return result
    
#заготовка под цикл четения анкет из файлов
def file_loop():
    show_msg("in_next_verion")#

#функция вывзова основного цикла
def main():
    main_loop()#закскаем основной цикл


if __name__ == "__main__":#ровека что модуль запущен как основной
    main()#запуска
