from telegram import InlineKeyboardMarkup, InlineKeyboardButton

def get_commands(update, context):
    '''Возвращает список команд и их участников (№-команды, имя, tg-link'''
    context.bot.send_message(
        text='Список команд',
        chat_id=update.effective_chat.id,
    )

def pm_menu(update, context):
    '''Вывод меню роли'''
    keyboard = [
        [InlineKeyboardButton('Получить список команд', callback_data='pm_get_commands'),],
            # [InlineKeyboardButton('', callback_data=),],
            # [InlineKeyboardButton('', callback_data=),],
            # [InlineKeyboardButton('', callback_data=),],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    context.bot.send_message(text="Выберите действие", chat_id=update.effective_chat.id, reply_markup=reply_markup)
