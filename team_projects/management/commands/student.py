import os

from telegram import InlineKeyboardMarkup, InlineKeyboardButton

from .db_processing import get_student

def choose_time(update, context):
    '''Генерирует кнопки с возможным временем созвона, возвращает список значений'''
    context.bot.send_message(
        text='Выбор времени',
        chat_id=update.effective_chat.id,
    )


def change_time(update, context):
    '''Очищает список возможного времени созвона, перенаправляет на choose_time'''
    context.bot.send_message(
        text='Изменение времени',
        chat_id=update.effective_chat.id,
    )


def call_pm(update, context):
    '''Отправить сообщение проджект-менеджеру'''

    student = get_student(update.effective_chat.id)

    projects = student.projects.all()
    last_project = projects.last()

    project_manager_id = last_project.mentor.telegram_id

    context.bot.send_message(
        text='Куратору отправлено сообщение, он свяжется с Вами, как только сможет',
        chat_id=update.effective_chat.id,
    )

    context.bot.send_message(
        text=f'Ученик @{update.effective_chat.username} хочет с Вами связаться',
        chat_id=project_manager_id,
    )


def leave(update, context):
    '''Отправка администратору сообщения об отказе от участия в проекте'''
    admin = os.getenv("ADMINS")

    context.bot.send_message(
        text='Сообщение администратору отправлено',
        chat_id=update.effective_chat.id,
    )

    context.bot.send_message(
        text=f'Cтудент @{update.effective_chat.username} хочет отказаться от участия в проекте',
        chat_id=admin,
    )


def student_menu(update, context):
    '''Вывод меню роли'''
    keyboard = [
        [InlineKeyboardButton('Выбор времени созвона', callback_data='student_choose_time')],
        [InlineKeyboardButton('Изменить выбранное время', callback_data='student_change_time')],
        [InlineKeyboardButton('Написать проджект-менеджеру', callback_data='student_call_pm')],
        [InlineKeyboardButton('Отказаться от участия', callback_data='student_leave')],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    context.bot.send_message(text="Выберите действие", chat_id=update.effective_chat.id, reply_markup=reply_markup)
