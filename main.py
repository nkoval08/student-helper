import os

from subjects import subjects_menu, load_subjects
from grades import grades_menu, load_grades
from tasks import tasks_menu, load_tasks
from schedule import schedule_menu, load_schedule
from expenses import expenses_menu, load_expenses
from student_statistics import show_statistics
from interface import pause

RESET = "\033[0m"

GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
CYAN = "\033[96m"
WHITE = "\033[97m"
MAGENTA = "\033[95m"

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def show_header():
    print(CYAN + "=" * 40 + RESET)
    print(CYAN + "         STUDENT HELPER" + RESET)
    print(CYAN + "=" * 40 + RESET)

def pause():
    input(YELLOW + "\nНажмите Enter, чтобы продолжить..." + RESET)

load_subjects()
load_grades()
load_tasks()
load_schedule()
load_expenses()

while True:
    clear_screen()
    show_header()

    print()
    print(BLUE + "📚 1. Мои предметы" + RESET)
    print(GREEN + "📊 2. Мои оценки" + RESET)
    print(YELLOW + "✅ 3. Мои задачи" + RESET)
    print(CYAN + "📅 4. Расписание" + RESET)
    print(MAGENTA + "💰 5. Расходы" + RESET)
    print(WHITE + "📈 6. Статистика" + RESET)
    print(RED + "🚪 0. Выход" + RESET)

    choice = input("\nВыберите пункт: ")

    if choice == "1":
        clear_screen()
        subjects_menu()
        pause()

    elif choice == "2":
        clear_screen()
        grades_menu()
        pause()

    elif choice == "3":
        clear_screen()
        tasks_menu()
        pause()

    elif choice == "4":
        clear_screen()
        schedule_menu()
        pause()

    elif choice == "5":
        clear_screen()
        expenses_menu()
        pause()

    elif choice == "6":
        clear_screen()
        show_statistics()
        pause()

    elif choice == "0":
        clear_screen()
        print(GREEN + "До свидания! 👋" + RESET)
        break

    else:
        print(RED + "\n❌ Такого пункта нет." + RESET)
        pause()