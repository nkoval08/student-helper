import json
from pathlib import Path
import subjects

DATA_FILE = Path(__file__).resolve().parent / "data" / "grades.json"

grades = {}

def load_grades():
    """Загружает оценки из JSON-файла."""
    global grades

    if DATA_FILE.exists():
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            grades = json.load(file)

def save_grades():
    """Сохраняет оценки в JSON-файл."""
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(grades, file, ensure_ascii=False, indent=4)

def choose_subject():
    """Позволяет выбрать предмет."""
    if not subjects.subjects:
        print("Сначала добавьте хотя бы один предмет.")
        return None

    print("\nВаши предметы:")

    for number, subject in enumerate(subjects.subjects, start=1):
        print(f"{number}. {subject}")

    try:
        number = int(input("Выберите номер предмета: "))

        if 1 <= number <= len(subjects.subjects):
            return subjects.subjects[number - 1]

        print("Такого номера нет.")
        return None

    except ValueError:
        print("Введите число.")
        return None

    except ValueError:
        print("Введите число.")
        return None

def add_grade():
    """Добавляет оценку."""
    subject = choose_subject()

    if subject is None:
        return

    try:
        grade = int(input(f"Введите оценку по предмету '{subject}' (2-5): "))

        if grade < 2 or grade > 5:
            print("Оценка должна быть от 2 до 5.")
            return

        if subject not in grades:
            grades[subject] = []

        grades[subject].append(grade)

        save_grades()

        print(f"Оценка {grade} добавлена по предмету '{subject}'.")

    except ValueError:
        print("Введите целое число.")

def show_grades():
    """Показывает все оценки."""
    if not grades:
        print("Оценок пока нет.")
        return

    print("\n=== МОИ ОЦЕНКИ ===")

    for subject, subject_grades in grades.items():
        print(f"{subject}: {', '.join(map(str, subject_grades))}")

def delete_grade():
    """Удаляет одну оценку."""
    subject = choose_subject()

    if subject is None:
        return

    if subject not in grades or not grades[subject]:
        print(f"У предмета '{subject}' пока нет оценок.")
        return

    print(f"\nОценки по предмету '{subject}':")

    for number, grade in enumerate(grades[subject], start=1):
        print(f"{number}. {grade}")

    try:
        number = int(input("Введите номер оценки для удаления: "))

        if 1 <= number <= len(grades[subject]):
            deleted_grade = grades[subject].pop(number - 1)

            if not grades[subject]:
                del grades[subject]

            save_grades()

            print(f"Оценка {deleted_grade} удалена.")

        else:
            print("Такого номера нет.")

    except ValueError:
        print("Введите число.")

def show_average():
    """Показывает средний балл."""
    if not grades:
        print("Оценок пока нет.")
        return

    print("\n=== СРЕДНИЙ БАЛЛ ===")

    all_grades = []

    for subject, subject_grades in grades.items():
        if subject_grades:
            average = sum(subject_grades) / len(subject_grades)

            print(f"{subject}: {average:.2f}")

            all_grades.extend(subject_grades)

    if all_grades:
        total_average = sum(all_grades) / len(all_grades)
        print(f"\nОбщий средний балл: {total_average:.2f}")

def grades_menu():
    """Меню оценок."""
    while True:
        print("\n=== МОИ ОЦЕНКИ ===")
        print("1. Добавить оценку")
        print("2. Показать оценки")
        print("3. Удалить оценку")
        print("4. Средний балл")
        print("0. Назад")

        choice = input("Выберите пункт: ")

        if choice == "1":
            add_grade()

        elif choice == "2":
            show_grades()

        elif choice == "3":
            delete_grade()

        elif choice == "4":
            show_average()

        elif choice == "0":
            break

        else:
            print("Такого пункта нет.")