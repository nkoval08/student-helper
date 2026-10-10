
import subjects
import grades
import tasks
import schedule
import expenses

from interface import show_title, show_warning


def show_statistics():
    show_title("СТАТИСТИКА СТУДЕНТА")

    # Количество предметов
    subjects_count = len(subjects.subjects)
    print(f"\n📚 Предметов: {subjects_count}")

    # Средний балл
    all_grades = []

    for subject_grades in grades.grades.values():
        all_grades.extend(subject_grades)

    if all_grades:
        average = sum(all_grades) / len(all_grades)
        print(f"📊 Средний балл: {average:.2f}")
    else:
        show_warning("Оценок пока нет.")

    # Задачи
    completed_tasks = sum(
        1 for task in tasks.tasks if task["completed"]
    )

    uncompleted_tasks = len(tasks.tasks) - completed_tasks

    print(f"\n✅ Выполненных задач: {completed_tasks}")
    print(f"❌ Невыполненных задач: {uncompleted_tasks}")

    # Расписание
    lessons_count = len(schedule.schedule)
    print(f"\n📅 Занятий в расписании: {lessons_count}")

    # Расходы
    total_expenses = sum(
        expense["amount"] for expense in expenses.expenses
    )

    print(f"\n💰 Общая сумма расходов: {total_expenses:.2f} ₽")