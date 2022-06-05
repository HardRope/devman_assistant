import os

from .admin import admin_menu
from .project_manager import pm_menu
from .student import student_menu


def start(update, context):
    '''Запуск бота, определение роли, вывод нужного меню'''

    students = os.getenv("STUDENTS")
    project_managers = os.getenv("PROJECT_MANAGERS")
    admins = os.getenv("ADMINS")

    user_name = update.effective_user.name

    context.bot.send_message(
        text=f"Добро пожаловать в бота Devman, {user_name}",
        chat_id=update.effective_chat.id,
    )

    if user_name in students:
        student_menu(update, context)
    if user_name in project_managers:
        pm_menu(update, context)
    if user_name in admins:
        admin_menu(update, context)
