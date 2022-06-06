from telegram import InlineKeyboardMarkup, InlineKeyboardButton

from .db_processing import get_actual_projects, get_project_groups

def get_commands(update, context):
    '''Возвращает список команд и их участников (№-команды, имя, tg-link'''
    projects = get_actual_projects()

    for project in projects:
        groups = get_project_groups(project)

        message = 'Проект: ' + project.title + '\n'

        for group in groups:
            message = message + group.timecode.__str__() + '\n'
            for student in groups[group]:
                message = message + student.__str__()
                message = message + f' (Уровень: {student.level})\n'

    context.bot.send_message(
        text=message,
        chat_id=update.effective_chat.id,
    )

def pm_menu(update, context):
    '''Вывод меню роли'''
    keyboard = [
        [InlineKeyboardButton('Получить список команд', callback_data='pm_get_commands')]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    context.bot.send_message(text="Выберите действие", chat_id=update.effective_chat.id, reply_markup=reply_markup)
