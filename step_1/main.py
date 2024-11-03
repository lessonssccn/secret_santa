#Пример простого консолькно приложения для реализации расспределения для тайного санты
#организатор должент внести название команды, имена и пожелания участников и дождаться заврешения распределения
#приложение последовательно проводит орагнизатора по этапам заполнения проверяет коректность ввода если в этом есть необходиомсь
#в коде идет осознанное дублиррование и неиспользуються многие методы, чтобы показать, что для на писания кода достаточно знать базовый функционала
from random import randint # имноритируетм функцию генерации случайного целого числа

print("Привет, я помогу тебе c распределением обязаностей тайного санты") #приветсивие к оганизатору

group_name = input("Укажи название группы: ") # приглашение к вводу имени команды и получение ввода пользовталя (имя команды может быть пустым)
number_person = input("Скольо будет участников: ")#ввод количества участником проверяется на коректность ввода целого числа со значением 3 и более

while True: #бесконечный цикл для получения корректного значнения количества участников группы
    correct_int = True #флаг коректности того что ввод пользоватля содержит только симолы относящиеся к цифрам от 0 до 9

    for ch in number_person: #проверяем каждый символ строки на коректность
        if ch not in "0123456789": #если симол не входит в строку  0123456789
            correct_int = False #то считаем что строка введенна не коректно

    if correct_int and len(number_person)>0: #проверяем коректность ввода строка содержит только символы цифр и строка имеет длину больше нуля
        number_person = int(number_person) #преобразуем строку в целое число
        if number_person >= 3: # если полученное число больше или равно 3
            break #завершаем ввод количества участников
        else:
            print("Группа должна быть от 3 человек") #если полученное число меньше 3 выводим сообщение об этом
    else:
        print("Введи число которое состоит тольо из цифр 0,1,2,3,4,5,6,7,8,9") #если полученна строка не коректна сообщаем об этом

    number_person = input("Скольо будет участников: ") #повторный ввод строки с количеством участников


print(f"Отлично группа {group_name} на {number_person} участников создана")# сообщаем об окончании регистрации групы

persons = {} #словарь где будем хранить имена и пожелания участников имя будет ключом и мы будем требовать его уникальности, значением текст пожелания
#для упрощения имя и текст пожелания будут считыаться в разных строках и подразумевается, что пожелание буедет записанно в одну строку без переносов на новую
for i in range(number_person):#запускаем цикл по количеству участников
    name = input(f"Укажи имя {i+1}-ого участника: ")# предлагаем начать ввод имени участника под номером i+1, +1 нужно чтобы номерация шла от 1, i начинается с нуля
    #допускается что имя одного из участников будет путым, при желании можно добаить провекру на не пустоту имени
    while name in persons: # проверяем, что имя ранее не использовалось, если оно уже есть как ключ в словаре
        name = input(f"Имя {name} уже занято другим участником группы, попробуй укзать другое: ")# просим переввести имя участника
    wish = input("Пожелание: ") #получаем пожелание участника имя которого вводили выше пожелание может быть пустым (допустимо)
    persons[name] = wish# сохраняем пару имя - пожелание в словарь 

#цикл для провекри и исправления первоначального ввода, чтука не сильно нужная но демонстрационно полезная
while True:# запускаем бесконечный цикл, который можно остановит только одним образом
    print("Проверь имена участников и их пожелания")# приветственное сообщение
    print(f"Участники команды {group_name}:")#еще одно, но с именем команды
    for index, name in enumerate(persons): #проходимя по словарю, используем enumerate для генерации нормер от 0, поэтому дальше добавляем +1
        print(f"{index + 1}) {name}: {persons[name]}")#выводим имена учасников с их пожеланиями и добовляем им номера
    #нескоолько сообщений объясняющих как пользоватся редактированием
    print("Если все хорошо нажми `enter`") 
    print("Если надо что-то поправить введите номер действия")
    print("1 - Добавить участника")
    print("2 - Изменить данные участника")
    print(f"Иной ввод возврат к редактированию сосатва команды {group_name}")
    
    action = input()#ждем ввод пользователя
    if action == "":#если пользователь просто нажл enter это ввод пустой строки
        break #завершаем работу редактора
    elif action == "1":#пользователь ввел едениц инажал enter
        #повторяем действия для добавления новго пользователя
        name = input(f"Укажи имя {len(persons) + 1}-ого участника: ") #номер новго полтзователя длинна словаря + 1
        while name in persons:
            name = input(f"Имя {name} уже занято другим участником группы, попробуй укзать другое: ")
        wish = input("Пожелание: ")
        persons[name] = wish
    elif action == "2":# введно 2 и нажат enter
        print("Укажи имя участника, данные которого надо изменить или enter для отмены действия") # сообщение с указанием дальнейщих действий

        name = input()#получаем имя участника
        if name=="":#если пустой ввода
            continue #возварат в начало цикла 

        while name not in persons: #проверяем что введенное имя есть среди ранее введенных
            name = input(f"Имя {name} отсутсует проверте написание или укажите другое")# просим ввести повторно если имени нет
        
        print(f"{name}:{persons[name]}") #выводим имя и пожаение
        print("Что именно вы хотите изменить? Введите номер") #вывод инструкции по тому как отредактировать записаь и что сней можно сделать
        print("1 - имя")
        print("2 - пожелание")
        print("3 - имя и пожелание")
        print("4 - удалить участника")
        print("Иной ввод отмена")
        
        action = input() #ждем ввода действия
        
        if action == "1":# введенна 1 и нажат enter редктиование имени
            new_name = input(f"Введите новое имя для участника {name}: ") # сохраняем ввод ннового имени в новую переменну чтобы не затереть старое
            while new_name in persons: # проверяем что новое имя не используется 
                new_name = input(f"Имя {new_name} уже занято другим участником группы, попробуй укзать другое: ") #если используется проссим переввести
            wish = persons[name] # сохраняем пожелаение во временную переменную
            del persons[name] #удаляем запись из словаря
            persons[new_name] = wish #вносим новую запись в словарь
        elif action == "2": # редактировани пожеления
            new_wish = input("Пожелание: ") #сохраняем новое пожеление во временную переменую не обязательный шаг
            persons[name] = new_wish # заменяем пожаление в словаре, замена значения по ключю имя мы получили раьше еще при выборе кого редактировать
        elif action == "3": # заменяем и имя и пожелание объеденения двух предыдущих действий
            new_name = input(f"Введите новое имя для участника {name}: ")
            while new_name in persons:
                new_name = input(f"Имя {new_name} уже занято другим участником группы, попробуй укзать другое: ")
            wish = persons[name]
            del persons[name]
            new_wish = input("Пожелание: ")
            persons[new_name] = new_wish
        elif action == "4": # удаление участника
            del persons[name] # имя участника мы получили еще на этапевыше осталось просто его удалить из словаря
# этап генерации и вывода резултатов 
while True:# делаем в бесконечном цикле тк могут потребоваться перегенерации результатов
    #алгоритм не соврешенный и может получиться там что с первого раза не сможет распределить нормально пары как пример
    #для 3 человек может выйти
    # 1 -> 2
    # 2 -> 1
    # остается что 3 уачсник должен дарить сам себе что не допустимо и алгоритм афтоматом перезапустит генерацию повторно пока не будет получен приемлемый резальтат
    set_name = set(persons)#получаем множесвто имен участников, те кому осталось подарит подарок, без пожеланий только ключи словаря
    result = [] # список кортежей из тех значений кто кому пожелание результат генерации выводиться только после удачной генерации
    re_choice = False # флаг который определяет что нужна перегенерация
    # для кажого участника из списка ищим того кому он будет дарить подарок
    for who in list(persons): #проходимя по списку имен who - кто дарит, дарит whom - кому дарить, на каждом шаге исключаем одного участника кому можно подарить подарок
        lst = list(set_name-set([who])) #определяем кому можно еще подарит подарок работаем через множества, разность множест
        #из общего списка вычитаем тек то уже получил своего санту и самого дарителя
        if len(lst)==0:# если список пустой значит вышла ситуация описанная выше
            re_choice = True# выставляем флаг что требуеться перегенерация
            break  # прерываем работу цикла чтобы начать перегенерацию
        rnd_index = randint(0, len(lst)-1) #генерируем случайное число из диапазона возможных индексо свписк имен потенциальных получателей подарка 
        whom = lst[rnd_index] #берем имя по индекус из списка имен
        result.append((who, whom, persons[whom]))# добовляем кортеж в список
        set_name -= set([whom]) # исключаем получтаеля подарка из множества тех кому осталось подарить подарок
        #[who] [whom] - списки из одного элемента их преобразуем в множество чтобы можно было сделать разность множест
    
    if re_choice: #если не удаолсь распределеить спервого раза запускаем перераспределение
        continue# чтобы запустить перераспределение достаточно вернуться в начала цыкла поэтом весь вывод сделан после расрпедленения
    
    print("Вот как вам можно распределиться") #выводим расрпеделение
    print("Кто -> Кому : Пожелание")
    for who, whom, wish in result: #проходимя по списку картежей для каждого элемента списка картеж разбиваем на 3 переменных
        print(f"{who} -> {whom} : {wish}")

    print()
    print("Если что-то не устраивает мточно провести повторное распределение")#выводим дополнительные инструкции
    print("1 - перераспределить (может совпасть с текщим результатом)")
    print("Иной ввод, завершить")

    action = input() # ждем ввода действия

    if action == "1":
        continue #запускаем перераспределения без гарантии что оно не повторит предыдущий результат
    else:
        break


        

