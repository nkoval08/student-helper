import json
from pathlib import Path

from interface import show_title, show_success, show_error, show_warning


DATA_FILE = Path(__file__).resolve().parent / "data" / "schedule.json"

schedule = []


def load_schedule():
    global schedule

    if DATA_FILE.exists():
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            schedule = json.load(file)


def save_schedule():
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(schedule, file, ensure_ascii=False, indent=4)


def add_lesson():
    day = input("Введите день недели: ")

    if not day:
        show_error("День недели не может быть пустым.")
        return

    time = input("Введите время занятия (например, 09:00): ")

    if not time:
        show_error("Время не может быть пустым.")
        return

    subject = input("Введите название предмета: ")

    if not subject:
        show_error("Название предмета не может быть пустым.")
        return

    lesson = {
        "day": day,
        "time": time,
        "subject": subject
    }

    schedule.append(lesson)
    save_schedule()

    show_success(f'Занятие "{subject}" добавлено!')


def show_schedule():
    if not schedule:
        show_warning("Расписание пока пустое.")
        return

    show_title("РАСПИСАНИЕ")

    days = [
        "Понедельник",
        "Вторник",
        "Среда",
        "Четверг",
        "Пятница",
        "Суббота",
        "Воскресенье"
    ]

    for day in days:
        lessons = [
            lesson
            for lesson in schedule
            if lesson["day"].lower() == day.lower()
        ]

        if lessons:
            print(f"\n{day}:")

            lessons.sort(key=lambda lesson: lesson["time"])

            for lesson in lessons:
                print(f"  {lesson['time']} — {lesson['subject']}")


def delete_lesson():
    if not schedule:
        show_warning("Расписание пока пустое.")
        return

    print("\nВсе занятия:")

    for number, lesson in enumerate(schedule, start=1):
        print(
            f"{number}. "
            f"{lesson['day']} — "
            f"{lesson['time']} — "
            f"{lesson['subject']}"
        )

    try:
        number = int(input("\nВведите номер занятия для удаления: "))

        if 1 <= number <= len(schedule):
            deleted_lesson = schedule.pop(number - 1)
            save_schedule()

            show_success(
                f'Занятие "{deleted_lesson["subject"]}" удалено!'
            )

        else:
            show_error("Такого номера нет.")

    except ValueError:
        show_error("Введите число.")


def schedule_menu():
    while True:
        show_title("РАСПИСАНИЕ")

        print("1. Добавить занятие")
        print("2. Показать расписание")
        print("3. Удалить занятие")
        print("0. Назад")

        choice = input("\nВыберите пункт: ")

        if choice == "1":
            add_lesson()

        elif choice == "2":
            show_schedule()

        elif choice == "3":
            delete_lesson()

        elif choice == "0":
            break

        else:
            show_error("Такого пункта нет.")