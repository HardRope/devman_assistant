from .admin import admin_menu
from .db_processing import get_actual_projects, get_mentors, get_participants
from .project_manager import pm_menu
from .student import student_menu
from environs import Env


def start(update, context):
    '''Запуск бота, определение роли, вывод нужного меню'''
    env = Env()
    env.read_env()

    admins = env.list("ADMIN")

    user_name = update.effective_user.name
    user_id = update.effective_user.id

    context.bot.send_message(
        text=f"Добро пожаловать в бота Devman, {user_name}",
        chat_id=update.effective_chat.id,
    )

    projects = get_actual_projects()
    students_id = []
    mentors_id = []

    for project in projects:
        students = get_participants(project)
        mentors = get_mentors()

        for student in students:
            students_id.append(student.telegram_id)

        for mentor in mentors:
            mentors_id.append(mentor.telegram_id)
    print(admins)
    if str(user_id) in admins:
        admin_menu(update, context)
    elif user_id in mentors_id:
        pm_menu(update, context)
    elif user_id in students_id:
        student_menu(update, context)
    else:
        context.bot.send_message(
            text=f"Сейчас у вас нет актуальных проектов",
            chat_id=update.effective_chat.id,
        )
