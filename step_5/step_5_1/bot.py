#@BotFather - один бот чтобы править всеми - регистрация бота, находим в телеге и заводим бот там
#https://t.me/secret_santa_sccn_bot - завел для тестов бот, не запущен большую чать времени
#пример простого тг бота для распределения тайных сант, работает через пулинг, тоесть отправляет запросы к тг и ждет ответов от него
#продимонстрировано хранение данных в памяти
#кнопки к сообщениям
#получение текстовой информации от пользователя
#используется библиотека для работы с api bot tg https://github.com/python-telegram-bot/python-telegram-bot

#импорт классов, функций, и прочего из библиотеки для работы с api bot telegram
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, ConversationHandler, CallbackQueryHandler, CommandHandler, MessageHandler, filters
#для работы с регулярными выраениями используется тут для провекри имени команды, чтобы были буквы цифры пробелы и нижние подчеркивания и больше ничего
import re
#используется для распределния тайных сант перемещивания индексов списка
from random import shuffle

#у команд должны быть уникальные имена, у участникво в одной команде должны быть уникальные имена
#чтобы команда была создана окончательно надо указать ей пароль
#чтобы анкета участника была создана окончательно надо указать его желание
#при распределении таыйных сант будут учитываться участники только с полностью заполенной анектой имя и желание

#токен полученный при регистрации бота через @BotFather
TOKEN = "сюда надо вствить токен полученный от BotFather"

#дальше идет список констант, которые будут использоваться в коде
#пайтон не поддерживает константы как таковые, поэтому приходиться использовать соглашение которое позволяет узнать их в коде константы пишем только заглавными буквами
#
# константы для bot_date keys
GROUPS = "groups"
OWNER = "owner"
PERSONS = "persons"
PSW = "psw"
PERSON_WISH = "preson_wish"
PERSON_TG_ID = "person_tg_id"

#константы user_data keys
GROUP_NAME = "group_name"
PERSON_NAME = "person_name"
#bot_date, user_data - встроенные в библиотеку локальные хранилища, для временного хранения информации, есть еще chat_data
#ниже пара ссылок раскрывающие суть этих хранилищь
#если просто по дефолту это три словаря, каждый из которых имеет свою область применения, но доступны в рамках всех функций
# user_data - записи уникальные для одного пользователя
# chat_data - уникальные записи в рамках чата
# bot_date - общее хранилище записей для всего бота
#https://docs-python.ru/packages/biblioteka-python-telegram-bot-python/hranenie-dannyh/
#https://makesomecode.me/2022/11/telegram-bot-persistence/

#callback_data та информация которая возвращается боту после того как пользователь нажал на одну из кнопок под сообщением
CREATE_GROUP = 1
JOIN_GROUP = 2
SELECT_GROUP = 3
GENERATE = 4

#состояния по которым проходит бот, в рамках одного сосотояния мы ограничиваем действия пользователя допустим ждем текстовое сообщение остальные игнорируем или ждем когда он нажмет на одну из кнопок
STATE_SELECT_ACTION = 1
STATE_INPUT_NEW_GROUP_NAME = 2
STATE_INPUT_EXIST_GROUP_NAME = 3
STATE_INPUT_PSW_NEW_GROUP = 4
STATE_INPUT_PSW_EXIST_GROUP = 5
STATE_ADD_NEW_PERSON = 6
STATE_ADD_NEW_WISH = 7
STATE_FINISH = 8
STATE_SELECT_GROUP = 9
STATE_SHOW_GROUP = 10

#функция скопированна из шага 3.1 как есть со всеми коментариями
#чтобы показать пример переиспользования кода, сама функция кране неудачная, но тем интереснее пример
#функция неудачная тем, что принимает навход словарь описывающий группу участников вместе с именем группы и списком участников
#данная функция была относительно удобна в шаге 3.1 тк весь код был так или иначе завязан на подобный формат хранения данных в ОП(оперативной памяти)
#здесь такой формат не используется и для работы функции имеющиеся данны придеться приводить к формату который использует функция
#как минимум на вход нужно подать словарь с ключом persons по которому храниться список участников, но нассамом деле
#если мы посмотрим код функции внимательно 
#функции важна только длинна списка persons, но не его содержимое. тоесть посути можно подать в функцию словарь с одним ключом persons, 
#а в качетсве значения предать словарь из n любых элементов хоть целых чисел главное чтобы n было равно количеству участников команды

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

#функция которая запускается при получении команды /start
#это бот написан неудачно интерфес взаимодействия намерено упрощен и надо будеть использовать команду /start часто, чтобы вренуться в основное меню
#другие способы возврата не предусмотрены, сделанно это намеренно для упрощения кода, так же как и тест сообщений прямо в коде функций, как и логикак прямо в обработчкиках
#так делать ненадо, но для простоты сделанн такой пример

#все функции которые обрабатывают ответы сервера телеграм(напоминаю мы постоянно запрашиваем сервер есть для нашего бота новые сообщения или нет, и получаем в ответ информацию о новых сообщениях, поэтому все наши функции обрабатываю ответы тг, в данном случае)
#имеют минимум 2 параметра update: Update, context: ContextTypes.DEFAULT_TYPE
#update: Update - базовая информация о полученом от пользоватлея сообщении и информация о самом пользователе, также о чате и прочее
#context: ContextTypes.DEFAULT_TYPE - контекст бота, концепция контекста, довольно замудренная, но если просто, то это все данные,
#которые необходимы для функционирования приложения и некий набор дополнительных данных связанных с текущим сеансом работы приложения
#для данного примера из контекста мы будем получать ссылку на объект бот, и доступ к временным хранилищам таким как bot_data, user_data
#по завершении работы функция должна вернуть номер сосотояния в которое переводиться бот для пользователя которого мы обсуживаем
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    name = "Незнакомец"#дефолтное имя которое будем выводим в рамках сообшения 
    user_id = update.effective_user.id #определяем тг ид пользователя отправившего сообщения, тг ид для пользовтеля общий на разных устройствах
    if update.effective_user.first_name:#проверям есть ли имя у этого пользовтеля в тг
        name = update.effective_user.first_name #если есть берем его 
    #формируем строку с сообщением для пользовтеля - это сообщение уйдет ему в ответ на команду /start 
    msg = f"Привет {name}\n\nЯ бот который поможет тебе в распределении тайных сант для твоей команды\n\nТы можешь создать свою команду или присоеденениться к сущестсующей"
    #формируем кнопочную клавиатуру для начала это масив массиово, вложенные массивы это строки клавиатуры, а элементы вложенных массивов это кнопки
    #[ [1], [2], [3] ] - три строки на каждой строке по одной кнопке первая строка кнопка 1, вторая строка кнопка 2, третья строка кнопка 3
    #[ [1, 2], [3, 4] ] - две строки на каждой по 2 кнопки, первая строка кнопки 1 2 вторая строка кнопки 3 4
    
    #InlineKeyboardButton("Создать команду", callback_data=str(CREATE_GROUP)), - создает объект кнопки с надписью Создать команду
    #если пользователь нажал на кнопку в ответ прилитит та строка что указана в параметре callback_data тоесть текстовое представление константы 
    #CREATE_GROUP в данном примере 1
    keyboard = [
        [
            InlineKeyboardButton("Создать команду", callback_data=str(CREATE_GROUP)),
        ],
        [
            InlineKeyboardButton("Присоедениться", callback_data=str(JOIN_GROUP)),
        ]
    ]
    # по дефолту создаем клавиатуру с 2 кнопками создать команду и присоедениться к команде логикак их работы разная пусть внешне и похожа
    # но если пользовтаель уже создавал команды то добавляем 3 кнопку мои команды позволяющую просмотреть состав команд и распределить сант если это необходимо

    #заводим флаг того что пользоватлеь является владельцем хоть одной команды, изначально предпологаем, что не является
    is_owner = False
    #будем идти по списку всех команд которые держит в памяти бот и проверять их владельца/создателя если совпало с тг ид пользовтеля значит
    #сменим значение флага на истину
    groups = context.bot_data.get(GROUPS, {})#получаем из bot_data словарь коанд ключи в словаре команд - имена команд, значения - словари с информацией о владельце, пароле, и список участникв
    for group_data in groups.values(): #имена команд нам не нужны нам интересны только словари с информацией о команде, в частности о владельце, поэтому перебираем только значения values()
        if group_data[OWNER] == user_id: #group_data - словарь берпем значение хранимое по ключу OWNER и свреяем его с тг ид пользовтеля
            is_owner = True #если совпало то запоминаем что текущий поьзовтель уже является владельцем команды
            break #сколько еще команд у него есть нам не интересно завершаемся на этом
    #не самый фективный сопосб хранения, но используется тут для демонстрации работы со словарем
    
    if is_owner: #если текущий пользователь уже ранее создавал команды 
        keyboard.append([#добавляем к клавиатуре новую строку с кнопкой
            InlineKeyboardButton("Мои команды", callback_data=str(SELECT_GROUP)),
        ])
    
    reply_markup = InlineKeyboardMarkup(keyboard)#клавиатру надо сврерстать в правильную понятную для тг разметку
    #для этого используем InlineKeyboardMarkup, без нее тг не поймет что мы хотим отправить, да и сама библиотека не сможет сформировать пакет
    await update.message.reply_text(msg, reply_markup=reply_markup)#отправляем в ответ пользовтелю сообщение, 
    #кому и в какой чат отправить определит сама библиотеаа по информации из объекта update и message
    #в сообщении идет текст и клавиатура
    return STATE_SELECT_ACTION#указываем в какое состояние переходит бот, чтобы ограничить дейсвтия пользователя

#функция которая запускается если пользователь тыкнул на кнопку создать группу в сообщении отправленном из функции старт
#важный момент сообщения с текстом от пользователя и сообщения с информацией на каку кнопку тыкнул пользователь надо обрабатывать поразному
#для сообщнений с текстом от пользовталея update содержит поле message в котором есть поле с текстом
#для сообщений о том какую кнопку тыкнул пользователь поля message в update нет зато есть callback_query -объект содержащий функционал 
#для обработки сообщений ответов нажатия на кнопку
async def create_group(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query #для удобства сохраняем ссылку на объект callback_query в более короткую переменую query
    await query.answer()#нужно обязательно вызвать таковы требования тг и либы особенность обработки кнопок
    await query.edit_message_text("Для создания новой команды введи имя команды")#как правило после нажатия на кнопку мы видим следующее
    #сообщение с кнопкой редактируется текст меняется, как собственно и сами кнопки, либо кнопки вообще уходят
    #query.edit_message_text - как раз выполняет это меняет текст в сообщениии, но так как новых кнопок мы не прицепили, кнопки уходят
    return STATE_INPUT_NEW_GROUP_NAME

#все тоже самое что идля создания группы только текст сообщения другой и переводим в другое соостояние, 
#чтобы разделить ветки создания группы и приссоедениения к группе, чтобы их обрабатывали разные функции, 
#логикак у функций будет разная как и набор проверок 
async def join_group(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("Для присоеденения к команде введи ее имя")
    return STATE_INPUT_EXIST_GROUP_NAME

#пожалуй самая интересная функция котрая запускается после нажатия на кнопку мои команды
#формируется клавиатура с кнопками на которых написанны названия команд
async def select_group(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.effective_user.id
    query = update.callback_query
    await query.answer()
    
    keyboard = []
    groups = context.bot_data.get(GROUPS, {})
    for group_name, group_data in groups.items():#проходимся по словарю команд, имена команд пойдут в надписи на кнопки и callback_data, а из связанных значений нам интересны владельцы коанд
        if group_data[OWNER] == user_id and group_data[PSW]!=None:# провреям чтобы команда была полностью сформированной, тоесть задан пароль, команд оформление которых не законченно ишнорируем
            keyboard.append([# если парль задан и владелец команды совподает с текущим пользователем добовляем кнопу с именем команды в список
                InlineKeyboardButton(group_name, callback_data=group_name),#для каждой кнопки выделяем новую строку
            ])
    #не самое лучшее решение, как минимум тем что команд может быть очень много и работать с такой клавиатурой будет не удобно, да еще есть ограничения тг
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text("Какую команду посмотрим", reply_markup = reply_markup)
    return STATE_SELECT_GROUP

#не менее интересная функция обрабаботчик которая запускается полсе нажатия на кнопку с именем комнады
#для просмотра инфорации о команде название/пароль и спиок участников заполнивших анкету полностью
#если участников не меньше двух и ид пользовтаеля совпадает с владельцем команды, то добавляем кнопу Распределить сант
async def show_group(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.effective_user.id
    query = update.callback_query
    await query.answer()
    group_name = query.data#получаем информацию о том какую кнопку тыкнул пользоватлеь в поле data будет лежать тоже что и в callback_data кнопки, у нас там название группы
    groups = context.bot_data.get(GROUPS, {})

    persons = []#список имен участников команды, которые заполнили анкету польностью указали имя и жедание
    for person_name, person_data in groups[group_name][PERSONS].items(): #участники команды храняться ввидеде словаря где ключ имя а значение это словарь с желанием и тг ид
        if person_data[PERSON_WISH]!=None:#если желание для данного участника указанно
            persons.append(person_name) #добавляем его в списко


    reply_markup = None #дефлтное значение для клавиатуру None означает что ее нет
    if groups[group_name][OWNER] == user_id and len(persons)>=2:#но если участиков 2 и более (сделано для облегчения тестов раньше было 3) и сюда провалился владелец команды
        reply_markup = InlineKeyboardMarkup([ #формируем клавиатуру с одной кнопкой Распределить сант
            [
                InlineKeyboardButton("Распределить сант", callback_data=str(GENERATE)),
            ]
        ])

    context.user_data[GROUP_NAME] = group_name # запоминаем в user_data[GROUP_NAME] какую команду выбрал пользователь
    await query.edit_message_text(f"Команда: {group_name}\nПароль: {groups[group_name][PSW]}\nУчасники заполнившие анкеты полностью:\n{'\n'.join(persons)}", reply_markup = reply_markup)
    return STATE_SHOW_GROUP

#функция которая запускается если владелец команды нажал Распределить сант в сообщении из функции отправленной выще
#распределяет сант и отправяет каждому учатнику команды информацию о том кому и что он должен подарить
async def generate(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()

    group_name = context.user_data.get(GROUP_NAME)#вытаскиваем информацию о команде которую выбрал пользоватлеь для распределения сант
    groups = context.bot_data.get(GROUPS, {})

    persons = []#составляем список участников каждый элемент списка словарь с трея ключачами имя участника, жедание, тг ид
    #берем толкьо тех кто указал жедение остальные мимо

    for person_name, person_data in groups[group_name][PERSONS].items():
        if person_data[PERSON_WISH]!=None:# если есть желание
            persons.append({ #добавляем словарь в спсиок
                "person_name": person_name,
                "wish": person_data[PERSON_WISH],
                "tg_id":person_data[PERSON_TG_ID],
                })
    #формируем словарь для передачи в функцию generate_pair как уже писал функция неудачная, поэтому нужен такой костыль для соблюдения интерфеса
    group = {
                "persons": persons
            }
    #вызываем функцию распредения пар, список кортежей получем как результат
    pair_list = generate_pair(group)
    
    await query.edit_message_text(f'Участникам команды "{group_name}" были направленны имена и желания их получателей подарков')

    #а вот теперь самое интересное, отправка сообщений пользователям по их тг ид
    for who, whom in pair_list:
        await context.bot.send_message(persons[who]['tg_id'], text=f'Ура, {persons[who]['person_name']}\nТы одариваешь {persons[whom]['person_name']} из команды "{group_name}"\nВот что хочет этот человек\n{persons[whom]['wish']}')
    #context.bot.send_message - позволяет отправить сообщение пользовтаелю по его тг ид важно чтобы этот пользователь ранее писал боту сам иначе тг заблочит отправку
    return STATE_FINISH
    
#создание группы состоить из 2 этапов ввод коректного имени и ввода параолья
#эта функция на целенна на получение коректного имени группы от пользователя имя содержит имя содержит токлько буквы цифры и _ 
#еще имя должно быть никем другим не занято
async def create_group_validate_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    name = update.message.text.strip() #берем сообщение отправленное пользователем убираем пробелы в начале и в конце
    #^[A-Za-zА-ЯА-яЁё0-9_ ]+$ - патерн который задетет правило что отначла до конца строки в строке должно быть быть одно или несколько вхождений
    #указаных в квадратных скобках
    #^-свреять от начала сроки
    #$-сверять до конца строки
    #+ - одно и более повторений, того что записанно слева здесь в квадратных скобакх
    # A-Z - диапазон больших букв в английском a-z тоже но для малых
    #А-Я а-я тоже самое но для русских
    #Ёё - надо указать отдельно тк не входят в диапазоны А-Я а-я
    if not re.match("^[A-Za-zА-ЯА-яЁё0-9_ ]+$", name):#проверяем на соответсвие регулярному выражению
        await update.message.reply_text(f'Не допустимое имя команды "{name}"\nИмя должно содержать только буквы, цыфры, пробелы и нижние подчеркивания')
        return STATE_INPUT_NEW_GROUP_NAME# отпраяляем сообщение о не соответсвии имени и остаемся в томже состоянии
    groups = context.bot_data.get(GROUPS, {})
    user_id = update.effective_user.id
    if name in groups and groups[name][OWNER] != user_id:#если имя уже есть в списке команд и эта команда создана не этим пользователем то все плохо
        await update.message.reply_text(f'Команда с именем "{name}" уже существует\nПридумай что-то еще')#сообщаем об этом
        return STATE_INPUT_NEW_GROUP_NAME#остоемся в том же состоянии
    
    context.user_data[GROUP_NAME] = name #запоминаем введенное имя в контексте пользователя
    groups[name] = { OWNER:user_id, PERSONS:{}, PSW: None } # запоминаем группу в словаре для запоминаем владейльцы и заполняетм дефолтно пароль и словарь пользователей
    context.bot_data[GROUPS] = groups #заносим словарь групп в общий контекс бота

    await update.message.reply_text(f'Команда "{name}" почти создана\nОсталось ее обезопасить придумай пароль, чтобы всякие проходимцы не могли в нее затесаться')
    return STATE_INPUT_PSW_NEW_GROUP #переходим в сосотояние ввода пароля

#функция присоедения к группе запускается поссле ввода имени группы
async def join_group_validate_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    name = update.message.text.strip()
    groups = context.bot_data.get(GROUPS, {})
    user_id = update.effective_user.id

    if name not in groups:#проверяем наличие группы в словаре групп
        await update.message.reply_text(f'Команды с именем "{name}" нет\nПопробуй указать другое имя')
        return STATE_INPUT_NEW_GROUP_NAME

    #проверяем начличие пользовартеля в группе, чтобы не включить его дважды в группу
    in_group = False

    for person_data in groups[name][PERSONS].values():#проходимся по всем участникам группы и проверяем их тг ид
        if person_data[PERSON_TG_ID] == user_id:
            in_group = True#запоминаем что пользователь в группе и так есть
            break #останавливаем проверку

    if in_group: #если и так в группе дальше не пускаем пользователя
        await update.message.reply_text(f'Не морочь мне голову. Ты и так участник "{name}"')
        return STATE_FINISH
    
    context.user_data[GROUP_NAME] = name #запоминаем имя группы куда хочет присоедениться пользователь

    await update.message.reply_text(f'Введи пароль для присоеденения к команде "{name}"')
    return STATE_INPUT_PSW_EXIST_GROUP#переводеем в состояния провекри пароля

#устанавливаем пароль для созданной группы, мимнум 4 символа чисто формальность, 
#немного осложнить жизнить тем кто хочет присоедениться к не то группе
async def create_group_validate_psw(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    psw = update.message.text.strip() #получаем пароль из сообщения пользовтеля
    name = context.user_data.get(GROUP_NAME, None)# извлекаем имя из контекста пользоваеля имя группы куда хотим задать пароль
    groups = context.bot_data.get(GROUPS, {}) 

    if not name or name not in groups:# чисто на перестраховку проверяем что группа никуда не делась
        await update.message.reply_text(f'Что-то пошло не так и имя команды потерялось, тебе предеться указать его снова')
        return STATE_INPUT_NEW_GROUP_NAME
    
    if len(psw) < 4: #проверяем длинну пароля
        await update.message.reply_text(f'Придеться постараться лучше и придмать пароль для команды "{name}" минимум из 4 символов')
        return STATE_INPUT_PSW_NEW_GROUP

    groups[name][PSW] = psw  #устанавливаем пароль для группы
    context.bot_data[GROUPS] = groups #сохраняем измеения в крнтекст

    await update.message.reply_text(f'Отлично мы сделали это команда "{name}" создана\nОсталось, заполнить анекту и разослать другим участникам приглашения\nНо пока введи имя, под которым тебя буду знать другие участники команды "{name}"')
    return STATE_ADD_NEW_PERSON #переходим в состояние регистрации пользователя в команде

#проверка пароля при присоедеинении к кгруппе запускается после ввода пароля
async def join_group_validate_psw(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    psw = update.message.text.strip()
    name = context.user_data.get(GROUP_NAME, None)#имя группы запомнили на прошлом шаге
    groups = context.bot_data.get(GROUPS, {}) 

    if groups[name][PSW] != psw: # провреям пароль введенный пользователем на совпадение с парлем группы
        await update.message.reply_text(f'Ты забыл пароль или пытаешься меня обмануть попробуй еще раз')
        return STATE_INPUT_PSW_EXIST_GROUP
    
    await update.message.reply_text(f'Окей, ты можешь стать одним из участникво команды "{name}"\nОсталось, заполнить анекту\nВведи имя, под которым тебя буду знать другие участники команды "{name}"')
    return STATE_ADD_NEW_PERSON#переходим в состояние регистрации пользователя в команде объеденяем ветки регистрации группы и присоедиения к группе в одну 

#регистрация пользоватял в группе начинается с ввода имени
#запускается после ввода имени пользовталея
async def add_new_person_input_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    person_name = update.message.text.strip()#получаем имя пользоватля из сообщения пользователя
    group_name = context.user_data.get(GROUP_NAME, None) #имя группы извлекаем из контекса
    groups = context.bot_data.get(GROUPS, {}) 
    user_id = update.effective_user.id # определяем тг ид
    #если имя пользоватял уже есть в группе и занято не этим пользователем то сообщаем о том что надо придмать новое и остаемся в том же состоянии
    if person_name in groups[group_name][PERSONS] and groups[group_name][PERSONS][person_name][PERSON_TG_ID] != user_id:
        await update.message.reply_text(f'Участник с именем {person_name} уже есть в команде {group_name}\nПридумай другое имя')
        return STATE_ADD_NEW_PERSON
    #добавляем пользователя в словарь пользователей группы, желание устанавливаем в None чтобы понимать что пользователь еще не польностью заполнил анекту
    groups[group_name][PERSONS][person_name]={PERSON_WISH: None, PERSON_TG_ID: user_id}
    context.user_data[PERSON_NAME] = person_name#сохраняем имя участника в контекст пользоватлея

    await update.message.reply_text(f'Отлично {person_name} введи свое желение и анкета будет заполнена')
    return STATE_ADD_NEW_WISH#переходим в остояние ввода желения

#ввод желания для пользователя
#запускается при получении текстового сообщения
#здесь особых проверок не делаем что ввел то и запоминаем
async def add_new_person_input_wish(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    person_wish = update.message.text.strip()#вытаскиваем желание из сообщения посути оно может оказаться пустой строкой
    group_name = context.user_data.get(GROUP_NAME, None)#извлекаем имя группы из контекста
    person_name = context.user_data.get(PERSON_NAME, None)#извлекаем имя имя участника из контекста
    groups = context.bot_data.get(GROUPS, {}) 
    user_id = update.effective_user.id

    await update.message.reply_text(f'Отлично вот твоя акета\nИмя: {person_name}\nЖелание: {person_wish}\nЯ сейчас же расскажу всем участникам команды "{group_name}", что ты присоеденился')
    
    groups[group_name][PERSONS][person_name]={PERSON_WISH: person_wish, PERSON_TG_ID: user_id}#запоминаем желаение только в словаре групп, но не в контексе пользоватля там оно ненужно

    #рассылаем всем участникам группы информацию, о том, что новый участник присоеденился к группе, в том чесле и самому новечку
    for person_data in groups[group_name][PERSONS].values():
        await context.bot.send_message(person_data[PERSON_TG_ID], text=f'{person_name} присоеденился к команде "{group_name}"')

    return STATE_FINISH #переходим в финишное состояние для которго нет обработчиков, единственный выход из него /start


#создаем бот с нашим токеном 
app = ApplicationBuilder().token(TOKEN).build()
#создаем специальный объект, который будет управлять состоянием бота
conv_handler = ConversationHandler(
    entry_points=[CommandHandler("start", start)],#состояние из которого начинаеться все
    states={ #словарь состоянией ключ значение возвращаемое функцией обработчиком значнеие список обработчиков которые надо запустить при том или ином сообщение от тг
        STATE_SELECT_ACTION: [
            CallbackQueryHandler(create_group, pattern="^" + str(CREATE_GROUP) + "$"),
            CallbackQueryHandler(join_group, pattern="^" + str(JOIN_GROUP) + "$"),
            CallbackQueryHandler(select_group, pattern="^" + str(SELECT_GROUP) + "$")
            #CallbackQueryHandler - связывает обработчик с сообщением о том что была нажата та или иная кнопка на клавиатуре
            #   pattern - по правилам re  опредлеляет какое сообщение было возвращенно при нажатии кнопки и если совпало то запускается обработчик 
        ],
        STATE_INPUT_NEW_GROUP_NAME:[
            MessageHandler(filters.TEXT & ~filters.COMMAND, create_group_validate_name)#MessageHandler запускает обработчик на любое сообщение соотвтествующее услвоия filters.TEXT & ~filters.COMMAND текст и не команда управления  
        ],
        STATE_INPUT_EXIST_GROUP_NAME:[
            MessageHandler(filters.TEXT & ~filters.COMMAND, join_group_validate_name)
        ],
        STATE_INPUT_PSW_NEW_GROUP:[
            MessageHandler(filters.TEXT & ~filters.COMMAND, create_group_validate_psw)
        ],
        STATE_INPUT_PSW_EXIST_GROUP:[
            MessageHandler(filters.TEXT & ~filters.COMMAND, join_group_validate_psw)
        ],
        STATE_ADD_NEW_PERSON:[
            MessageHandler(filters.TEXT & ~filters.COMMAND, add_new_person_input_name)
        ],
        STATE_ADD_NEW_WISH:[
            MessageHandler(filters.TEXT & ~filters.COMMAND, add_new_person_input_wish)
        ],
        STATE_SELECT_GROUP:[
            CallbackQueryHandler(show_group)  #здесь патерн не передаем тк нам нужно анализировать информацию в самом обработчике
        ],
        STATE_SHOW_GROUP:[
            CallbackQueryHandler(generate)#а здесь потому что ничего другого не ожидаем там только одна кнопаа
        ]
    },
    fallbacks=[CommandHandler("start", start)],#то действие которое можно выполнить в любой омент из любого состояние
)

app.add_handler(conv_handler)#указываем боту какие обработчики есть 
print("bot run")
app.run_polling(allowed_updates=Update.ALL_TYPES)#запускаем получение сообщений от тг