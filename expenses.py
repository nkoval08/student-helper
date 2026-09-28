import json
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parent / "data" / "expenses.json"

expenses = []

def load_expenses():
    """Загружает расходы из JSON-файла."""
    global expenses

    if DATA_FILE.exists():
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            expenses = json.load(file)

def save_expenses():
    """Сохраняет расходы в JSON-файл."""
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(expenses, file, ensure_ascii=False, indent=4)

def add_expense():
    """Добавляет новый расход."""
    name = input("Введите название расхода: ")

    if not name:
        print("Название расхода не может быть пустым.")
        return

    category = input(
        "Введите категорию "
        "(еда, транспорт, учёба, другое): "
    )

    if not category:
        print("Категория не может быть пустой.")
        return

    try:
        amount = float(input("Введите сумму: "))

        if amount <= 0:
            print("Сумма должна быть больше нуля.")
            return

    except ValueError:
        print("Введите число.")

        return

    expense = {
        "name": name,
        "category": category,
        "amount": amount
    }

    expenses.append(expense)
    save_expenses()

    print("Расход добавлен!")

def show_expenses():
    """Показывает все расходы."""
    if not expenses:
        print("Расходов пока нет.")
        return

    print("\n=== МОИ РАСХОДЫ ===")

    for number, expense in enumerate(expenses, start=1):
        print(
            f"{number}. {expense['name']} — "
            f"{expense['amount']:.2f} ₽ "
            f"({expense['category']})"
        )

def show_total():
    """Показывает общую сумму расходов."""
    if not expenses:
        print("Расходов пока нет.")
        return

    total = sum(expense["amount"] for expense in expenses)

    print(f"\nОбщая сумма расходов: {total:.2f} ₽")

def show_categories():
    """Показывает расходы по категориям."""
    if not expenses:
        print("Расходов пока нет.")
        return

    categories = {}

    for expense in expenses:
        category = expense["category"]

        if category not in categories:
            categories[category] = 0

        categories[category] += expense["amount"]

    print("\n=== РАСХОДЫ ПО КАТЕГОРИЯМ ===")

    for category, amount in categories.items():
        print(f"{category}: {amount:.2f} ₽")

def delete_expense():
    """Удаляет расход."""
    if not expenses:
        print("Расходов пока нет.")
        return

    show_expenses()

    try:
        number = int(
            input("\nВведите номер расхода для удаления: ")
        )

        if 1 <= number <= len(expenses):
            deleted_expense = expenses.pop(number - 1)

            save_expenses()

            print(
                f"Расход '{deleted_expense['name']}' "
                f"удалён!"
            )

        else:
            print("Такого номера нет.")

    except ValueError:
        print("Введите число.")

def expenses_menu():
    """Меню расходов."""
    while True:
        print("\n=== МОИ РАСХОДЫ ===")
        print("1. Добавить расход")
        print("2. Показать расходы")
        print("3. Общая сумма")
        print("4. Расходы по категориям")
        print("5. Удалить расход")
        print("0. Назад")

        choice = input("Выберите пункт: ")

        if choice == "1":
            add_expense()

        elif choice == "2":
            show_expenses()

        elif choice == "3":
            show_total()

        elif choice == "4":
            show_categories()

        elif choice == "5":
            delete_expense()

        elif choice == "0":
            break

        else:
            print("Такого пункта нет.")