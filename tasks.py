import json
from pathlib import Path

from datetime import datetime, date


from interface import show_title, show_success, show_error, show_warning

DATA_FILE = Path(__file__).resolve().parent / "data" / "tasks.json"
tasks = []

def load_tasks():
    global tasks

    if DATA_FILE.exists():
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            tasks = json.load(file)

def save_tasks():
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(tasks, file, ensure_ascii=False, indent=4)



def add_task():
    title = input("Введите название задачи: ").strip()

    if not title:
        show_error("Название задачи не может быть пустым.")
        return

    deadline = input(
        "Введите дедлайн (например, 28.10.2026): "
    ).strip()

    try:
        datetime.strptime(deadline, "%d.%m.%Y")
    except ValueError:
        show_error(
            "Неверная дата. Используйте формат ДД.ММ.ГГГГ "
            "и укажите существующую дату."
        )
        return

    print("\nВыберите приоритет:")
    print("1. Низкий")
    print("2. Средний")
    print("3. Высокий")

    priority_choice = input("Ваш выбор: ")

    priorities = {
        "1": "Низкий",
        "2": "Средний",
        "3": "Высокий"
    }

    if priority_choice not in priorities:
        show_error("Неверный выбор приоритета.")
        return

    task = {
        "title": title,
        "deadline": deadline,
        "completed": False,
        "priority": priorities[priority_choice]
    }

    tasks.append(task)
    save_tasks()

    show_success(f'Задача "{title}" добавлена!')


def show_tasks():
    if not tasks:
        show_warning("Задач пока нет.")
        return

    def get_deadline(task):
        deadline = task.get("deadline", "")

        try:
            date = datetime.strptime(deadline, "%d.%m.%Y")
            return (0, date)
        except ValueError:
            # Если дата введена неправильно,
            # такую задачу покажем в конце списка.
            return (1, datetime.max)

    sorted_tasks = sorted(tasks, key=get_deadline)

    show_title("МОИ ЗАДАЧИ — ПО ДЕДЛАЙНУ")

    for number, task in enumerate(sorted_tasks, start=1):
        if task["completed"]:
            status = "✅ Выполнена"
        else:
            status = "❌ Не выполнена"

        priority = task.get("priority", "Средний")

        print(f"\n{number}. {task['title']}")
        print(f"   Дедлайн: {task['deadline']}")
        print(f"   Приоритет: {priority}")
        print(f"   Статус: {status}")


def search_tasks():
    if not tasks:
        show_warning("Задач пока нет.")
        return

    search_text = input(
        "Введите название задачи или его часть: "
    ).strip().lower()

    if not search_text:
        show_error("Поисковый запрос не может быть пустым.")
        return

    found_tasks = []

    for task in tasks:
        if search_text in task["title"].lower():
            found_tasks.append(task)

    if not found_tasks:
        show_warning("Задачи по вашему запросу не найдены.")
        return

    show_title("РЕЗУЛЬТАТЫ ПОИСКА")

    for number, task in enumerate(found_tasks, start=1):
        status = (
            "Выполнена"
            if task["completed"]
            else "Не выполнена"
        )

        print(f"\n{number}. {task['title']}")
        print(f"   Дедлайн: {task['deadline']}")
        print(f"   Приоритет: {task.get('priority', 'Средний')}")
        print(f"   Статус: {status}")

def show_overdue_tasks():
    today = date.today()
    overdue_tasks = []

    for task in tasks:
        if task["completed"]:
            continue

        try:
            deadline = datetime.strptime(
                task["deadline"], "%d.%m.%Y"
            ).date()

            if deadline < today:
                overdue_tasks.append(task)

        except ValueError:
            continue

    if not overdue_tasks:
        show_success("Просроченных задач нет!")
        return

    show_title("ПРОСРОЧЕННЫЕ ЗАДАЧИ")

    for number, task in enumerate(overdue_tasks, start=1):
        print(f"\n{number}. {task['title']}")
        print(f"   Дедлайн: {task['deadline']}")
        print(
            f"   Приоритет: "
            f"{task.get('priority', 'Средний')}"
        )
        print("   Статус: ❌ Не выполнена")

def filter_tasks():
    if not tasks:
        show_warning("Задач пока нет.")
        return

    print("\nКакие задачи показать?")
    print("1. Все задачи")
    print("2. Только невыполненные")
    print("3. Только выполненные")

    choice = input("Выберите пункт: ")

    if choice == "1":
        filtered_tasks = tasks
    elif choice == "2":
        filtered_tasks = [
            task for task in tasks
            if not task["completed"]
        ]
    elif choice == "3":
        filtered_tasks = [
            task for task in tasks
            if task["completed"]
        ]
    else:
        show_error("Такого пункта нет.")
        return

    if not filtered_tasks:
        show_warning("Задач с таким статусом нет.")
        return

    show_title("РЕЗУЛЬТАТЫ ФИЛЬТРА")

    for number, task in enumerate(filtered_tasks, start=1):
        status = (
            "Выполнена"
            if task["completed"]
            else "Не выполнена"
        )

        print(f"\n{number}. {task['title']}")
        print(f"   Дедлайн: {task['deadline']}")
        print(
            f"   Приоритет: "
            f"{task.get('priority', 'Средний')}"
        )
        print(f"   Статус: {status}")

def complete_task():
    if not tasks:
        show_warning("Задач пока нет.")
        return

    show_tasks()

    try:
        number = int(input("\nВведите номер выполненной задачи: "))

        if 1 <= number <= len(tasks):
            tasks[number - 1]["completed"] = True
            save_tasks()

            show_success("Задача отмечена как выполненная!")

        else:
            show_error("Такого номера нет.")

    except ValueError:
        show_error("Введите число.")

def delete_task():
    if not tasks:
        show_warning("Задач пока нет.")
        return

    show_tasks()

    try:
        number = int(input("\nВведите номер задачи для удаления: "))

        if 1 <= number <= len(tasks):
            deleted_task = tasks.pop(number - 1)
            save_tasks()

            show_success(
                f'Задача "{deleted_task["title"]}" удалена!'
            )

        else:
            show_error("Такого номера нет.")

    except ValueError:
        show_error("Введите число.")

def change_deadline():
    if not tasks:
        show_warning("Задач пока нет.")
        return

    show_title("ИЗМЕНЕНИЕ ДЕДЛАЙНА")

    # Показываем задачи в порядке хранения,
    # чтобы выбранный номер соответствовал нужной задаче.
    for number, task in enumerate(tasks, start=1):
        print(f"{number}. {task['title']} — {task['deadline']}")

    try:
        number = int(input("\nВведите номер задачи: "))

        if number < 1 or number > len(tasks):
            show_error("Такого номера нет.")
            return

    except ValueError:
        show_error("Введите номер цифрами.")
        return

    new_deadline = input(
        "Введите новый дедлайн (например, 28.10.2026): "
    ).strip()

    if not new_deadline:
        show_error("Дедлайн не может быть пустым.")
        return

    task = tasks[number - 1]
    task["deadline"] = new_deadline

    save_tasks()
    show_success("Дедлайн успешно изменён!")

def change_task_title():
    if not tasks:
        show_warning("Задач пока нет.")
        return

    show_title("ИЗМЕНЕНИЕ НАЗВАНИЯ ЗАДАЧИ")

    # Показываем задачи в порядке хранения,
    # чтобы номер точно соответствовал нужной задаче.
    for number, task in enumerate(tasks, start=1):
        print(f"{number}. {task['title']}")

    try:
        number = int(input("\nВведите номер задачи: "))

        if number < 1 or number > len(tasks):
            show_error("Такого номера нет.")
            return

    except ValueError:
        show_error("Введите номер цифрами.")
        return

    new_title = input("Введите новое название задачи: ").strip()

    if not new_title:
        show_error("Название не может быть пустым.")
        return

    tasks[number - 1]["title"] = new_title

    save_tasks()
    show_success("Название задачи изменено!")

def change_task_priority():
    if not tasks:
        show_warning("Задач пока нет.")
        return

    show_title("ИЗМЕНЕНИЕ ПРИОРИТЕТА")

    for number, task in enumerate(tasks, start=1):
        priority = task.get("priority", "Средний")
        print(f"{number}. {task['title']} — {priority}")

    try:
        number = int(input("\nВведите номер задачи: "))

        if number < 1 or number > len(tasks):
            show_error("Такого номера нет.")
            return

    except ValueError:
        show_error("Введите номер цифрами.")
        return

    print("\nВыберите новый приоритет:")
    print("1. Низкий")
    print("2. Средний")
    print("3. Высокий")

    choice = input("Ваш выбор: ")

    priorities = {
        "1": "Низкий",
        "2": "Средний",
        "3": "Высокий"
    }

    if choice not in priorities:
        show_error("Неверный выбор приоритета.")
        return

    tasks[number - 1]["priority"] = priorities[choice]

    save_tasks()
    show_success("Приоритет задачи изменён!")

def tasks_menu():
    while True:
        show_title("МОИ ЗАДАЧИ")

        print("1. Добавить задачу")
        print("2. Показать задачи")
        print("3. Выполнить задачу")
        print("4. Удалить задачу")
        print("5. Фильтр задач")
        print("6. Изменить дедлайн")
        print("7. Изменить название задачи")
        print("8. Изменить приоритет задачи")
        print("9. Найти задачу")
        print("10. Показать просроченные задачи")
        print("0. Назад")

        choice = input("\nВыберите пункт: ")

        if choice == "1":
            add_task()

        elif choice == "2":
            show_tasks()

        elif choice == "3":
            complete_task()

        elif choice == "4":
            delete_task()

        elif choice == "5":
            filter_tasks()

        elif choice == "6":
            change_deadline()

        elif choice == "7":
            change_task_title()

        elif choice == "8":
            change_task_priority()

        elif choice == "9":
            search_tasks()

        elif choice == "10":
            show_overdue_tasks()
        
        elif choice == "0":
            break

        else:
            show_error("Такого пункта нет.")
