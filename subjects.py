subjects = []

def add_subject():
    name = input("Введите название предмета: ")

    if name:
        subjects.append(name)
        print("Предмет добавлен!")
    else:
        print("Название предмета не может быть пустым.")

def show_subjects():
    if not subjects:
        print("Список предметов пока пуст.")
        return

    print("\nВаши предметы:")

    for number, subject in enumerate(subjects, start=1):
        print(f"{number}. {subject}")

def delete_subject():
    if not subjects:
        print("Список предметов пуст.")
        return

    show_subjects()

    try:
        number = int(input("Введите номер предмета для удаления: "))

        if 1 <= number <= len(subjects):
            deleted_subject = subjects.pop(number - 1)
            print(f'Предмет "{deleted_subject}" удалён!')
        else:
            print("Такого номера нет.")

    except ValueError:
        print("Введите число.")

def subjects_menu():
    while True:
        print("\n=== МОИ ПРЕДМЕТЫ ===")
        print("1. Добавить предмет")
        print("2. Показать предметы")
        print("3. Удалить предмет")
        print("0. Назад")

        choice = input("Выберите пункт: ")

        if choice == "1":
            add_subject()

        elif choice == "2":
            show_subjects()

        elif choice == "3":
            delete_subject()

        elif choice == "0":
            break

        else:
            print("Такого пункта нет.")