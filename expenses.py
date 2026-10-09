import json
from pathlib import Path
from interface import show_title, show_success, show_error, show_warning

DATA_FILE = Path(__file__).resolve().parent / "data" / "expenses.json"

expenses = []


def load_expenses():
    global expenses

    if DATA_FILE.exists():
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            expenses = json.load(file)


def save_expenses():
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(expenses, file, ensure_ascii=False, indent=4)


def add_expense():
    name = input("Введите название расхода: ").strip()

    if not name:
        show_error("Название расхода не может быть пустым.")
        return

    category = input(
        "Введите категорию (еда, транспорт, учёба, другое): "
    ).strip()

    if not category:
        show_error("Категория не может быть пустой.")
        return

    try:
        amount = float(
            input("Введите сумму: ").replace(",", ".")
        )

        if amount <= 0:
            show_error("Сумма должна быть больше нуля.")
            return

    except ValueError:
        show_error("Введите корректную сумму.")
        return

    expense = {
        "name": name,
        "category": category,
        "amount": amount
    }

    expenses.append(expense)
    save_expenses()

    show_success(f'Расход "{name}" добавлен!')


def show_expenses():
    if not expenses:
        show_warning("Расходов пока нет.")
        return

    show_title("МОИ РАСХОДЫ")

    for number, expense in enumerate(expenses, start=1):
        print(
            f"{number}. {expense['name']} — "
            f"{expense['amount']:.2f} ₽ "
            f"({expense['category']})"
        )


def show_total():
    if not expenses:
        show_warning("Расходов пока нет.")
        return

    total = sum(expense["amount"] for expense in expenses)

    show_title("ОБЩАЯ СУММА РАСХОДОВ")
    print(f"Всего потрачено: {total:.2f} ₽")


def show_categories():
    if not expenses:
        show_warning("Расходов пока нет.")
        return

    categories = {}

    for expense in expenses:
        category = expense["category"]

        if category not in categories:
            categories[category] = 0

        categories[category] += expense["amount"]

    show_title("РАСХОДЫ ПО КАТЕГОРИЯМ")

    for category, amount in categories.items():
        print(f"{category}: {amount:.2f} ₽")


def delete_expense():
    if not expenses:
        show_warning("Расходов пока нет.")
        return

    show_expenses()

    try:
        number = int(
            input("\nВведите номер расхода для удаления: ")
        )

        if 1 <= number <= len(expenses):
            deleted_expense = expenses.pop(number - 1)
            save_expenses()

            show_success(
                f'Расход "{deleted_expense["name"]}" удалён!'
            )
        else:
            show_error("Такого номера нет.")

    except ValueError:
        show_error("Введите целое число.")


def expenses_menu():
    while True:
        show_title("МОИ РАСХОДЫ")

        print("1. Добавить расход")
        print("2. Показать расходы")
        print("3. Общая сумма")
        print("4. Расходы по категориям")
        print("5. Удалить расход")
        print("0. Назад")

        choice = input("\nВыберите пункт: ")

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
            show_error("Такого пункта нет.")