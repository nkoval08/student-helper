import json
from pathlib import Path

from interface import show_title, show_success, show_error, show_warning
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
    name = input("Введите название предмета: ")

    if not name:
        show_error("Название предмета не может быть пустым.")
        return

    subjects.append(name)
    save_subjects()

    show_success(f'Предмет "{name}" добавлен!')

def show_subjects():
    if not subjects:
        show_warning("Предметов пока нет.")
        return

    print()

    for number, subject in enumerate(subjects, start=1):
        print(f"{number}. {subject}")

def delete_subject():
    if not subjects:
        show_warning("Предметов пока нет.")
        return

    show_subjects()

    try:
        number = int(input("\nВведите номер предмета для удаления: "))

        if 1 <= number <= len(subjects):
            deleted_subject = subjects.pop(number - 1)
            save_subjects()

            show_success(
                f'Предмет "{deleted_subject}" удалён!'
            )

        else:
            show_error("Такого номера нет.")

    except ValueError:
        show_error("Введите число.")

def subjects_menu():
    while True:
        show_title("МОИ ПРЕДМЕТЫ")

        print("1. Добавить предмет")
        print("2. Показать предметы")
        print("3. Удалить предмет")
        print("0. Назад")

        choice = input("\nВыберите пункт: ")

        if choice == "1":
            add_subject()

        elif choice == "2":
            show_subjects()

        elif choice == "3":
            delete_subject()

        elif choice == "0":
            break

        else:
            show_error("Такого пункта нет.")