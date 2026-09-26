from subjects import subjects_menu, load_subjects
from grades import grades_menu, load_grades
from tasks import tasks_menu, load_tasks
print("================================")
print("        STUDENT HELPER")
print("================================")
load_subjects()
load_grades()
load_tasks()
while True:
    print()
    print("1. Мои предметы")
    print("2. Мои баллы")
    print("3. Мои задачи")
    print("4. Расписание")
    print("0. Выход")

    choice = input("\nВыберите пункт: ")

    if choice == "1":
        subjects_menu()

    elif choice == "2":
        grades_menu()

    elif choice == "3":
        tasks_menu()

    elif choice == "4":
        print("Раздел расписания")

    elif choice == "0":
        print("До свидания!")
        break

    else:
        print("Такого пункта нет.")
