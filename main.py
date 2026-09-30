import os

from subjects import subjects_menu, load_subjects
from grades import grades_menu, load_grades
from tasks import tasks_menu, load_tasks
from schedule import schedule_menu, load_schedule
from expenses import expenses_menu, load_expenses
from student_statistics import show_statistics

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def show_header():
    print("=" * 40)
    print("         STUDENT HELPER")
    print("=" * 40)

def pause():
    input("\nНажмите Enter, чтобы продолжить...")

load_subjects()
load_grades()
load_tasks()
load_schedule()
load_expenses()


while True:
    clear_screen()
    show_header()

    print("\n📚 1. Мои предметы")
    print("📊 2. Мои оценки")
    print("✅ 3. Мои задачи")
    print("📅 4. Расписание")
    print("💰 5. Расходы")
    print("📈 6. Статистика")
    print("🚪 0. Выход")

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
        print("До свидания! 👋")
        break

    else:
        print("\n❌ Такого пункта нет.")
        pause()