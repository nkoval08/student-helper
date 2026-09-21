print("================================")
print("        STUDENT HELPER")
print("================================")

while True:
    print()
    print("1. Мои предметы")
    print("2. Мои оценки")
    print("3. Мои задачи")
    print("4. Расписание")
    print("0. Выход")

    choice = input("\nВыберите пункт: ")

    if choice == "1":
        print("Раздел предметов")

    elif choice == "2":
        print("Раздел оценок")

    elif choice == "3":
        print("Раздел задач")

    elif choice == "4":
        print("Раздел расписания")

    elif choice == "0":
        print("До свидания!")
        break

    else:
        print("Такого пункта нет.")