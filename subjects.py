import json
from pathlib import Path
DATA_FILE = Path(__file__).resolve().parent / "data" / "subjects.json"
subjects = []

def load_subjects():
    """Загружает предметы из JSON-файла."""
    global subjects

    if DATA_FILE.exists():
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            subjects = json.load(file)

def save_subjects():
    """Сохраняет предметы в JSON-файл."""
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(subjects, file, ensure_ascii=False, indent=4)

def add_subject():
    """Добавляет новый предмет."""
    name = input("Введите название предмета: ")

    if name:
        subjects.append(name)
        save_subjects()
        print("Предмет добавлен!")
    else:
        print("Название предмета не может быть пустым.")

def show_subjects():
    """Показывает список предметов."""
    if not subjects:
        print("Список предметов пока пуст.")
        return
    print("\nВаши предметы:")

    for number, subject in enumerate(subjects, start=1):
        print(f"{number}. {subject}")

def delete_subject():
    """Удаляет предмет."""
    if not subjects:
        print("Список предметов пуст.")
        return

    show_subjects()

    try:
        number = int(input("Введите номер предмета для удаления: "))

        if 1 <= number <= len(subjects):
            deleted_subject = subjects.pop(number - 1)
            save_subjects()
            print(f'Предмет "{deleted_subject}" удалён!')
        else:
            print("Такого номера нет.")

    except ValueError:
        print("Введите число.")

def subjects_menu():
    """Меню управления предметами."""
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