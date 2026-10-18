import json
from pathlib import Path

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

    if not deadline:
        show_error("Дедлайн не может быть пустым.")
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

    show_title("МОИ ЗАДАЧИ")

    priority_order = {
        "Высокий": 1,
        "Средний": 2,
        "Низкий": 3
    }

    sorted_tasks = sorted(
        tasks,
        key=lambda task: priority_order.get(
            task.get("priority", "Средний"), 2
        )
    )

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

def tasks_menu():
    while True:
        show_title("МОИ ЗАДАЧИ")

        print("1. Добавить задачу")
        print("2. Показать задачи")
        print("3. Выполнить задачу")
        print("4. Удалить задачу")
        print("5. Фильтр задач")
        print("6. Изменить дедлайн")
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

        elif choice == "0":
            break

        else:
            show_error("Такого пункта нет.")