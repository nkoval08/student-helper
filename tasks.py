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

def tasks_menu():
    while True:
        show_title("МОИ ЗАДАЧИ")

        print("1. Добавить задачу")
        print("2. Показать задачи")
        print("3. Выполнить задачу")
        print("4. Удалить задачу")
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

        elif choice == "0":
            break

        else:
            show_error("Такого пункта нет.")