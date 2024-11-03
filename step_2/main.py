import os
from random import shuffle

generate = True
select_group = True
while select_group:
    list_dir = []
    for item in os.listdir('.'):
        if os.path.isdir(item):
            list_dir.append(item)

    list_dir.sort()

    for item in list_dir:
        print(item, end="\t")
    print()

    group_name = input("Введи имя команды из предложенных выше: ")

    while group_name not in list_dir:
        group_name = input(f"Введенное имя {group_name} отсутвует в списке выше. Попробуй указать дургое: ")

    while True:
        print(f"Проверка анкет команды {group_name}")

        error_format_files = list()
        form_name = dict()
        persons = list()

        for item in os.listdir(group_name):
            path = os.path.join(group_name, item)
            if os.path.isfile(path):
                file = open(path, "r", encoding="utf-8")
                rows = file.readlines()
                file.close()
                if len(rows) >= 2:
                    name_person = rows[0].strip()
                    person = {
                        "name": name_person,
                        "form": path,
                        "wish": [s.strip() for s in rows[1:]]
                    }
                    persons.append(person)
                    list_path = form_name.get(name_person, [])
                    list_path.append(path)
                    form_name[name_person] = list_path
                else:
                    error_format_files.append(path)

        count_person = len(persons)
        print(f"Я нашел {count_person} участников")
        if count_person > 0:
            print("Вот их имена, их желания я показывать не стану, а то магии не будет")
            for index, item in enumerate(persons):
                print(f"{index+1}) {item['name']}")


        erroe_name_person = {}
        for name_person, list_path in form_name.items():
            if len(list_path) > 1:
                erroe_name_person[name_person] = list_path

        error = 0
        if count_person < 3:
            error += 1
            print("Упс, похоже в выбранной команде не хватает участников")
            print("Должно быть минимум 3 заполненных анкеты, на 3 разных участников")
        if len(error_format_files)>0:
            error += 1
            print("Кажеться у тебя есть неверно заполненые анкеты")
            print("Вот они")
            for index, item in enumerate(error_format_files):
                print(f"{index+1}) {item}")
        if len(erroe_name_person)>0:
            error += 1
            print(f"Ох, команда {group_name} придется не просто")
            print("Кое-кто не проявил оригинальности при заполнении анект")
            print("Есть одинаковые имена")
            print("Понять кому и что дарить будет не просто")
            print("Вот эти анкеты")
            for index, name_person in enumerate(erroe_name_person):
                print(f"{index+1}) имя: {name_person}\nанкеты:")
                for path in erroe_name_person[name_person]:
                    print(f"\t{path}")
                    

        if error>0:
            print()
            print("Все можно исправить!")
            print("Попросите участником заполнить анкеты повторно, а потом замените старые на новые")

        action = "-"
        while action not in ("1", "2", "3", "4"):
            print("Что будем делать дальше? Ввведи новмер одного из возможных действий")
            print(f"1 - к распределению сант {'[НЕДОСТУПНО]' if count_person<3 else ''}")
            print(f"2 - повторно проверить анкеты команды {group_name}")
            print("3 - выбрать другую команду")
            print("0 - закончить без распределения сант")
            action = input()

        if action == "1":
            if count_person >= 3:
                select_group = False
                break
            else:
                print("\nК сожалению сейчас команда не полная\n")
        elif action == "2":
            continue
        elif action == "3":
            break
        elif action == "0":
            generate = False
            select_group = False
            break
        else:
            print("Какжеться что-то пошло не так")

if generate:
    count_person = len(persons)
    list_shuffled_index = list(range(0, count_person))
    shuffle(list_shuffled_index)
    
    error_index = []
    for index in range(0, count_person):
        if index == list_shuffled_index[index]:
            list_shuffled_index[index], list_shuffled_index[index-1] = list_shuffled_index[index-1], list_shuffled_index[index]


    path_dir = os.path.join(group_name, "result")
    result_number = 1
    while os.path.exists(path_dir):
        path_dir = os.path.join(group_name,f"result_{result_number}")
        result_number+=1
    os.mkdir(path_dir)
    print(f"распределение завершенно результат смотри в {path_dir}")
    for who, whom in enumerate(list_shuffled_index):
        file_name = f"{persons[who]["name"]}_{who+1}.txt"
        path = os.path.join(path_dir, file_name)
        file = open(path, "w")
        file.write(f"Кому:\n{persons[whom]["name"]}\n")
        file.write(f"Анкета:\n{persons[whom]["form"]}\n")
        file.write(f"Что:\n{"\n".join(persons[whom]["wish"])}")
        file.close()       



