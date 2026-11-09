
import json
from pathlib import Path
from datetime import datetime

from interface import (
    show_title,
    show_success,
    show_error,
    show_warning
)

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
    show_title("ДОБАВЛЕНИЕ ЗАНЯТИЯ")

    day = input(
        "Введите день недели (например, Понедельник): "
    ).strip().capitalize()

    valid_days = [
        "Понедельник",
        "Вторник",
        "Среда",
        "Четверг",
        "Пятница",
        "Суббота",
        "Воскресенье"
    ]

    if day not in valid_days:
        show_error("Такого дня недели нет.")
        return

    time = input(
        "Введите время занятия (например, 08:30): "
    ).strip()

    try:
        datetime.strptime(time, "%H:%M")
    except ValueError:
        show_error(
            "Неверное время. Используйте формат ЧЧ:ММ, "
            "например 08:30."
        )
        return

    subject = input("Введите название предмета: ").strip()

    if not subject:
        show_error("Название предмета не может быть пустым.")
        return
    
    for lesson in schedule:
        if (
            lesson["day"] == day
            and lesson["time"] == time
        ):
            show_error(
                "На этот день и время занятие уже добавлено."
            )
            return


    lesson = {
        "day": day,
        "time": time,
        "subject": subject
    }

    schedule.append(lesson)
    save_schedule()

    show_success("Занятие успешно добавлено!")


def show_schedule():
    if not schedule:
        show_warning("Расписание пока пустое.")
        return

    weekdays = [
        "Понедельник",
        "Вторник",
        "Среда",
        "Четверг",
        "Пятница",
        "Суббота",
        "Воскресенье"
    ]

    show_title("МОЁ РАСПИСАНИЕ")

    for day in weekdays:
        lessons = [
            lesson for lesson in schedule
            if lesson.get("day", "").lower() == day.lower()
        ]

        if lessons:
            print(f"\n📅 {day.upper()}")

            lessons.sort(key=lambda lesson: lesson["time"])

            for lesson in lessons:
                print(
                    f"  {lesson['time']} — "
                    f"{lesson['subject']}"
                )


def show_schedule_by_day():
    if not schedule:
        show_warning("Расписание пока пустое.")
        return

    day = input(
        "Введите день недели (например, Понедельник): "
    ).strip().lower()

    if not day:
        show_error("День недели не может быть пустым.")
        return

    found_lessons = [
        lesson for lesson in schedule
        if lesson.get("day", "").lower() == day
    ]

    if not found_lessons:
        show_warning("На этот день занятий нет.")
        return

    found_lessons.sort(key=lambda lesson: lesson["time"])

    show_title(f"РАСПИСАНИЕ: {day.upper()}")

    for number, lesson in enumerate(found_lessons, start=1):
        print(f"{number}. {lesson['time']} — {lesson['subject']}")


def delete_lesson():
    if not schedule:
        show_warning("Расписание пока пустое.")
        return

    show_schedule()

    try:
        day = input(
            "\nВведите день недели удаляемого занятия: "
        ).strip().lower()

        day_lessons = [
            lesson for lesson in schedule
            if lesson.get("day", "").lower() == day
        ]

        if not day_lessons:
            show_warning("На этот день занятий нет.")
            return

        day_lessons.sort(key=lambda lesson: lesson["time"])

        for number, lesson in enumerate(day_lessons, start=1):
            print(f"{number}. {lesson['time']} — {lesson['subject']}")

        number = int(input("Введите номер занятия для удаления: "))

        if number < 1 or number > len(day_lessons):
            show_error("Такого номера нет.")
            return

        lesson_to_delete = day_lessons[number - 1]
        schedule.remove(lesson_to_delete)
        save_schedule()

        show_success("Занятие удалено!")

    except ValueError:
        show_error("Введите номер цифрами.")

def delete_day_schedule():
    if not schedule:
        show_warning("Расписание пока пустое.")
        return

    show_title("ОЧИСТКА РАСПИСАНИЯ ЗА ДЕНЬ")

    day = input(
        "Введите день недели: "
    ).strip().capitalize()

    valid_days = [
        "Понедельник",
        "Вторник",
        "Среда",
        "Четверг",
        "Пятница",
        "Суббота",
        "Воскресенье"
    ]

    if day not in valid_days:
        show_error("Такого дня недели нет.")
        return

    day_lessons = [
        lesson for lesson in schedule
        if lesson["day"] == day
    ]

    if not day_lessons:
        show_warning("На этот день занятий нет.")
        return

    print(f"\nНайдено занятий: {len(day_lessons)}")

    confirm = input(
        "Вы действительно хотите удалить все занятия? (да/нет): "
    ).strip().lower()

    if confirm != "да":
        show_warning("Удаление отменено.")
        return

    for lesson in day_lessons:
        schedule.remove(lesson)

    save_schedule()
    show_success("Все занятия за выбранный день удалены!")
    
def search_lessons():
    if not schedule:
        show_warning("Расписание пока пустое.")
        return

    show_title("ПОИСК ЗАНЯТИЙ")

    search = input(
        "Введите название предмета для поиска: "
    ).strip().lower()

    if not search:
        show_error("Введите название предмета.")
        return

    found_lessons = [
        lesson for lesson in schedule
        if search in lesson["subject"].lower()
    ]

    if not found_lessons:
        show_warning("Занятия по этому предмету не найдены.")
        return

    found_lessons.sort(
        key=lambda lesson: (
            [
                "Понедельник", "Вторник", "Среда",
                "Четверг", "Пятница", "Суббота", "Воскресенье"
            ].index(lesson["day"]),
            lesson["time"]
        )
    )

    show_title("РЕЗУЛЬТАТЫ ПОИСКА")

    for number, lesson in enumerate(found_lessons, start=1):
        print(
            f"{number}. {lesson['day']} — "
            f"{lesson['time']} — {lesson['subject']}"
        )

    print(f"\nВсего найдено занятий: {len(found_lessons)}")

def search_lessons():
    if not schedule:
        show_warning("Расписание пока пустое.")
        return

    show_title("ПОИСК ЗАНЯТИЙ")

    search = input(
        "Введите название предмета для поиска: "
    ).strip().lower()

    if not search:
        show_error("Введите название предмета.")
        return

    found_lessons = [
        lesson for lesson in schedule
        if search in lesson["subject"].lower()
    ]

    if not found_lessons:
        show_warning("Занятия по этому предмету не найдены.")
        return

    found_lessons.sort(
        key=lambda lesson: (
            [
                "Понедельник", "Вторник", "Среда",
                "Четверг", "Пятница", "Суббота", "Воскресенье"
            ].index(lesson["day"]),
            lesson["time"]
        )
    )

    show_title("РЕЗУЛЬТАТЫ ПОИСКА")

    for number, lesson in enumerate(found_lessons, start=1):
        print(
            f"{number}. {lesson['day']} — "
            f"{lesson['time']} — {lesson['subject']}"
        )

    print(f"\nВсего найдено занятий: {len(found_lessons)}")


def count_lessons_by_day():
    if not schedule:
        show_warning("Расписание пока пустое.")
        return

    show_title("КОЛИЧЕСТВО ЗАНЯТИЙ")

    weekdays = [
        "Понедельник",
        "Вторник",
        "Среда",
        "Четверг",
        "Пятница",
        "Суббота",
        "Воскресенье"
    ]

    total = 0

    for day in weekdays:
        count = 0

        for lesson in schedule:
            lesson_day = lesson.get("day", "").strip().lower()

            if lesson_day == day.lower():
                count += 1

        print(f"{day}: {count} занятий")

        total += count

    print("-" * 30)
    print(f"Всего занятий за неделю: {total}")

def show_today_schedule():
    from datetime import date

    if not schedule:
        show_warning("Расписание пока пустое.")
        return

    weekdays = [
        "Понедельник",
        "Вторник",
        "Среда",
        "Четверг",
        "Пятница",
        "Суббота",
        "Воскресенье"
    ]

    today = weekdays[date.today().weekday()]

    today_lessons = [
        lesson for lesson in schedule
        if lesson.get("day", "").strip().lower() == today.lower()
    ]

    show_title(f"РАСПИСАНИЕ НА СЕГОДНЯ: {today.upper()}")

    if not today_lessons:
        show_warning("На сегодня занятий нет.")
        return

    today_lessons.sort(key=lambda lesson: lesson["time"])

    for number, lesson in enumerate(today_lessons, start=1):
        print(
            f"{number}. {lesson['time']} — "
            f"{lesson['subject']}"
        )

    print("-" * 30)
    print(f"Всего занятий сегодня: {len(today_lessons)}")

def show_free_time():
    if not schedule:
        show_warning("Расписание пока пустое.")
        return

    weekdays = [
        "Понедельник",
        "Вторник",
        "Среда",
        "Четверг",
        "Пятница",
        "Суббота",
        "Воскресенье"
    ]

    day = input(
        "Введите день недели: "
    ).strip().capitalize()

    if day not in weekdays:
        show_error("Такого дня недели нет.")
        return

    lessons = [
        lesson for lesson in schedule
        if lesson.get("day", "").strip().lower() == day.lower()
    ]

    if len(lessons) < 2:
        show_warning(
            "Для расчёта свободного времени нужно минимум 2 занятия."
        )
        return

    lessons.sort(key=lambda lesson: lesson["time"])

    show_title(f"СВОБОДНОЕ ВРЕМЯ: {day.upper()}")

    for i in range(len(lessons) - 1):
        first_time = datetime.strptime(
            lessons[i]["time"], "%H:%M"
        )

        second_time = datetime.strptime(
            lessons[i + 1]["time"], "%H:%M"
        )

        difference = second_time - first_time

        minutes = difference.total_seconds() // 60

        print(
            f"После {lessons[i]['subject']} "
            f"до {lessons[i + 1]['subject']}: "
            f"{int(minutes)} минут"
        )

def show_next_lesson():
    if not schedule:
        show_warning("Расписание пока пустое.")
        return

    weekdays = [
        "Понедельник",
        "Вторник",
        "Среда",
        "Четверг",
        "Пятница",
        "Суббота",
        "Воскресенье"
    ]

    day = input(
        "Введите день недели: "
    ).strip().capitalize()

    if day not in weekdays:
        show_error("Такого дня недели нет.")
        return

    lessons = [
        lesson for lesson in schedule
        if lesson.get("day", "").strip().lower() == day.lower()
    ]

    if not lessons:
        show_warning("На этот день занятий нет.")
        return

    lessons.sort(key=lambda lesson: lesson["time"])

    next_lesson = lessons[0]

    show_title("БЛИЖАЙШЕЕ ЗАНЯТИЕ")

    print(f"День: {next_lesson['day']}")
    print(f"Время: {next_lesson['time']}")
    print(f"Предмет: {next_lesson['subject']}")

def search_lessons_by_time():
    if not schedule:
        show_warning("Расписание пока пустое.")
        return

    show_title("ПОИСК ЗАНЯТИЙ ПО ВРЕМЕНИ")

    search_time = input(
        "Введите время занятия (например, 10:00): "
    ).strip()

    try:
        datetime.strptime(search_time, "%H:%M")
    except ValueError:
        show_error("Неверное время. Используйте формат ЧЧ:ММ.")
        return

    found_lessons = [
        lesson for lesson in schedule
        if lesson.get("time", "").strip() == search_time
    ]

    if not found_lessons:
        show_warning("Занятий на это время нет.")
        return

    show_title("НАЙДЕННЫЕ ЗАНЯТИЯ")

    for number, lesson in enumerate(found_lessons, start=1):
        print(
            f"{number}. {lesson['day']} — "
            f"{lesson['time']} — {lesson['subject']}"
        )

    print("-" * 30)
    print(f"Всего найдено занятий: {len(found_lessons)}")

def change_lesson_day():
    if not schedule:
        show_warning("Расписание пока пустое.")
        return

    show_title("ИЗМЕНЕНИЕ ДНЯ ЗАНЯТИЯ")

    for number, lesson in enumerate(schedule, start=1):
        print(
            f"{number}. {lesson['day']} — "
            f"{lesson['time']} — {lesson['subject']}"
        )

    try:
        number = int(input("\nВведите номер занятия: "))

        if number < 1 or number > len(schedule):
            show_error("Такого номера нет.")
            return

    except ValueError:
        show_error("Введите номер цифрами.")
        return

    lesson = schedule[number - 1]

    valid_days = [
        "Понедельник",
        "Вторник",
        "Среда",
        "Четверг",
        "Пятница",
        "Суббота",
        "Воскресенье"
    ]

    new_day = input(
        "Введите новый день недели: "
    ).strip().capitalize()

    if new_day not in valid_days:
        show_error("Такого дня недели нет.")
        return

    for other_lesson in schedule:
        if (
            other_lesson is not lesson
            and other_lesson["day"] == new_day
            and other_lesson["time"] == lesson["time"]
        ):
            show_error(
                "На этот день и время занятие уже добавлено."
            )
            return

    lesson["day"] = new_day

    save_schedule()

    show_success("День занятия успешно изменён!")

def change_lesson_time():
    if not schedule:
        show_warning("Расписание пока пустое.")
        return

    show_title("ИЗМЕНЕНИЕ ВРЕМЕНИ ЗАНЯТИЯ")

    for number, lesson in enumerate(schedule, start=1):
        print(
            f"{number}. {lesson['day']} — "
            f"{lesson['time']} — {lesson['subject']}"
        )

    try:
        number = int(input("\nВведите номер занятия: "))

        if number < 1 or number > len(schedule):
            show_error("Такого номера нет.")
            return

    except ValueError:
        show_error("Введите номер цифрами.")
        return

    lesson = schedule[number - 1]

    new_time = input(
        "Введите новое время (например, 09:30): "
    ).strip()

    try:
        datetime.strptime(new_time, "%H:%M")
    except ValueError:
        show_error("Неверное время. Используйте формат ЧЧ:ММ.")
        return

    for other_lesson in schedule:
        if (
            other_lesson is not lesson
            and other_lesson["day"] == lesson["day"]
            and other_lesson["time"] == new_time
        ):
            show_error(
                "На этот день и время занятие уже добавлено."
            )
            return

    lesson["time"] = new_time

    save_schedule()
    show_success("Время занятия изменено!")

def change_lesson_time():
    if not schedule:
        show_warning("Расписание пока пустое.")
        return

    show_title("ИЗМЕНЕНИЕ ВРЕМЕНИ ЗАНЯТИЯ")

    for number, lesson in enumerate(schedule, start=1):
        print(
            f"{number}. {lesson['day']} — "
            f"{lesson['time']} — {lesson['subject']}"
        )

    try:
        number = int(input("\nВведите номер занятия: "))

        if number < 1 or number > len(schedule):
            show_error("Такого номера нет.")
            return

    except ValueError:
        show_error("Введите номер цифрами.")
        return

    lesson = schedule[number - 1]

    new_time = input(
        "Введите новое время (например, 09:30): "
    ).strip()

    try:
        datetime.strptime(new_time, "%H:%M")
    except ValueError:
        show_error("Неверное время. Используйте формат ЧЧ:ММ.")
        return

    for other_lesson in schedule:
        if (
            other_lesson is not lesson
            and other_lesson["day"] == lesson["day"]
            and other_lesson["time"] == new_time
        ):
            show_error(
                "На этот день и время занятие уже добавлено."
            )
            return

    lesson["time"] = new_time

    save_schedule()
    show_success("Время занятия изменено!")

def change_lesson_subject():
    if not schedule:
        show_warning("Расписание пока пустое.")
        return

    show_title("ИЗМЕНЕНИЕ ПРЕДМЕТА")

    for number, lesson in enumerate(schedule, start=1):
        print(
            f"{number}. {lesson['day']} — "
            f"{lesson['time']} — {lesson['subject']}"
        )

    try:
        number = int(input("\nВведите номер занятия: "))

        if number < 1 or number > len(schedule):
            show_error("Такого номера нет.")
            return

    except ValueError:
        show_error("Введите номер цифрами.")
        return

    new_subject = input(
        "Введите новое название предмета: "
    ).strip()

    if not new_subject:
        show_error("Название предмета не может быть пустым.")
        return

    schedule[number - 1]["subject"] = new_subject

    save_schedule()
    show_success("Название предмета успешно изменено!")


def schedule_menu():
    while True:
        show_title("МОЁ РАСПИСАНИЕ")

        print("1. Добавить занятие")
        print("2. Показать расписание")
        print("3. Удалить занятие")
        print("4. Расписание по дням недели")
        print("5. Изменить время занятия")
        print("6. Изменить название предмета")
        print("7. Очистить расписание за день")
        print("8. Найти занятие по предмету")
        print("9. Количество занятий по дням недели")
        print("10. Расписание на сегодня")
        print("11. Свободное время между занятиями")
        print("12. Ближайшее занятие")
        print("13. Найти занятия по времени")
        print("14. Изменить день занятия")
        print("0. Назад")

        choice = input("\nВыберите пункт: ")

        if choice == "1":
            add_lesson()
        elif choice == "2":
            show_schedule()
        elif choice == "3":
            delete_lesson()
        elif choice == "4":
            show_schedule_by_day()
        elif choice == "5":
            change_lesson_time()
        elif choice == "6":
            change_lesson_subject()
        elif choice == "7":
            delete_day_schedule()
        elif choice == "8":
            search_lessons()
        elif choice == "9":
            count_lessons_by_day()
        elif choice == "10":
            show_today_schedule()
        elif choice == "11":
            show_free_time()
        elif choice == "12":
            show_next_lesson()
        elif choice == "13":
            search_lessons_by_time()
        elif choice == "14":
            change_lesson_day()
        elif choice == "0":
            break
        else:
            show_error("Такого пункта нет.")
