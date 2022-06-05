from telegram import InlineKeyboardMarkup, InlineKeyboardButton

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
    '''Отправить сообщение проджект-менеджеру(?)'''
    context.bot.send_message(
        text='Клич о помощи',
        chat_id=update.effective_chat.id,
    )


def leave(update, context):
    '''Покинуть распределение проектов на данной неделе (удаление ученика из бд?)'''
    context.bot.send_message(
        text='Отказ от участия',
        chat_id=update.effective_chat.id,
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
