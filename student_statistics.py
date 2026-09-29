import subjects
import grades
import tasks
import schedule
import expenses

def show_statistics():
    """Показывает общую статистику студента."""

    print("\n=== СТАТИСТИКА ===")

    # -------------------------
    # ПРЕДМЕТЫ
    # -------------------------

    subjects_count = len(subjects.subjects)

    print(f"\n📚 Предметов: {subjects_count}")

    # -------------------------
    # ОЦЕНКИ
    # -------------------------

    all_grades = []

    for subject_grades in grades.grades.values():
        all_grades.extend(subject_grades)

    if all_grades:
        average = sum(all_grades) / len(all_grades)
        print(f"📊 Средний балл: {average:.2f}")
    else:
        print("📊 Средний балл: пока нет оценок")

    # -------------------------
    # ЗАДАЧИ
    # -------------------------

    completed_tasks = 0
    uncompleted_tasks = 0

    for task in tasks.tasks:
        if task["completed"]:
            completed_tasks += 1
        else:
            uncompleted_tasks += 1

    print(f"\n✅ Выполненных задач: {completed_tasks}")
    print(f"❌ Невыполненных задач: {uncompleted_tasks}")

    # -------------------------
    # РАСПИСАНИЕ
    # -------------------------

    lessons_count = len(schedule.schedule)

    print(f"\n📅 Занятий в расписании: {lessons_count}")

    # -------------------------
    # РАСХОДЫ
    # -------------------------

    total_expenses = sum(
        expense["amount"]
        for expense in expenses.expenses
    )

    print(f"\n💰 Общая сумма расходов: {total_expenses:.2f} ₽")