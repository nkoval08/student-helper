import json
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parent / "data" / "schedule.json"

schedule = []

def load_schedule():
    """Загружает расписание."""
    global schedule

    if DATA_FILE.exists():
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            schedule = json.load(file)

def save_schedule():
    """Сохраняет расписание."""
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(schedule, file, ensure_ascii=False, indent=4)

def add_lesson():
    """Добавляет занятие."""
    day = input("Введите день недели: ")

    if not day:
        print("День недели не может быть пустым.")
        return

    time = input("Введите время занятия (например, 09:00): ")

    if not time:
        print("Время не может быть пустым.")
        return

    subject = input("Введите название предмета: ")

    if not subject:
        print("Название предмета не может быть пустым.")
        return

    lesson = {
        "day": day,
        "time": time,
        "subject": subject
    }

    schedule.append(lesson)
    save_schedule()

    print("Занятие добавлено!")

def show_schedule():
    """Показывает расписание."""
    if not schedule:
        print("Расписание пока пустое.")
        return

    days = [
        "Понедельник",
        "Вторник",
        "Среда",
        "Четверг",
        "Пятница",
        "Суббота",
        "Воскресенье"
    ]

    print("\n=== РАСПИСАНИЕ ===")

    for day in days:
        lessons = [
            lesson for lesson in schedule
            if lesson["day"].lower() == day.lower()
        ]

        if lessons:
            print(f"\n{day}:")

            lessons.sort(key=lambda lesson: lesson["time"])

            for number, lesson in enumerate(lessons, start=1):
                print(f"{number}. {lesson['time']} — {lesson['subject']}")

def delete_lesson():
    """Удаляет занятие."""
    if not schedule:
        print("Расписание пока пустое.")
        return

    print("\nВсе занятия:")

    for number, lesson in enumerate(schedule, start=1):
        print(
            f"{number}. {lesson['day']} — "
            f"{lesson['time']} — {lesson['subject']}"
        )

    try:
        number = int(input("Введите номер занятия для удаления: "))

        if 1 <= number <= len(schedule):
            deleted_lesson = schedule.pop(number - 1)

            save_schedule()

            print(
                f"Занятие '{deleted_lesson['subject']}' "
                f"удалено!"
            )

        else:
            print("Такого номера нет.")

    except ValueError:
        print("Введите число.")

def schedule_menu():
    """Меню расписания."""
    while True:
        print("\n=== РАСПИСАНИЕ ===")
        print("1. Добавить занятие")
        print("2. Показать расписание")
        print("3. Удалить занятие")
        print("0. Назад")

        choice = input("Выберите пункт: ")

        if choice == "1":
            add_lesson()

        elif choice == "2":
            show_schedule()

        elif choice == "3":
            delete_lesson()

        elif choice == "0":
            break

        else:
            print("Такого пункта нет.")