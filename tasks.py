import json
from pathlib import Path


DATA_FILE = Path(__file__).resolve().parent / "data" / "tasks.json"

tasks = []


def load_tasks():
    """Загружает задачи из JSON-файла."""
    global tasks

    if DATA_FILE.exists():
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            tasks = json.load(file)


def save_tasks():
    """Сохраняет задачи в JSON-файл."""
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(tasks, file, ensure_ascii=False, indent=4)


def add_task():
    """Добавляет новую задачу."""
    title = input("Введите название задачи: ")

    if not title:
        print("Название задачи не может быть пустым.")
        return

    deadline = input("Введите дедлайн (например, 28.09.2026): ")

    if not deadline:
        print("Дедлайн не может быть пустым.")
        return

    task = {
        "title": title,
        "deadline": deadline,
        "completed": False
    }

    tasks.append(task)
    save_tasks()

    print("Задача добавлена!")


def show_tasks():
    """Показывает все задачи."""
    if not tasks:
        print("Задач пока нет.")
        return

    print("\n=== МОИ ЗАДАЧИ ===")

    for number, task in enumerate(tasks, start=1):
        if task["completed"]:
            status = "✅ Выполнена"
        else:
            status = "❌ Не выполнена"

        print(f"\n{number}. {task['title']}")
        print(f"   Дедлайн: {task['deadline']}")
        print(f"   Статус: {status}")


def complete_task():
    """Отмечает задачу выполненной."""
    if not tasks:
        print("Задач пока нет.")
        return

    show_tasks()

    try:
        number = int(input("\nВведите номер выполненной задачи: "))

        if 1 <= number <= len(tasks):
            tasks[number - 1]["completed"] = True
            save_tasks()

            print("Задача отмечена как выполненная!")

        else:
            print("Такого номера нет.")

    except ValueError:
        print("Введите число.")


def delete_task():
    """Удаляет задачу."""
    if not tasks:
        print("Задач пока нет.")
        return

    show_tasks()

    try:
        number = int(input("\nВведите номер задачи для удаления: "))

        if 1 <= number <= len(tasks):
            deleted_task = tasks.pop(number - 1)
            save_tasks()

            print(f'Задача "{deleted_task["title"]}" удалена!')

        else:
            print("Такого номера нет.")

    except ValueError:
        print("Введите число.")


def tasks_menu():
    """Меню задач."""
    while True:
        print("\n=== МОИ ЗАДАЧИ ===")
        print("1. Добавить задачу")
        print("2. Показать задачи")
        print("3. Выполнить задачу")
        print("4. Удалить задачу")
        print("0. Назад")

        choice = input("Выберите пункт: ")

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
            print("Такого пункта нет.")