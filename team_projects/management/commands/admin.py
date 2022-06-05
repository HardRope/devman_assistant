from telegram import InlineKeyboardMarkup, InlineKeyboardButton

def request_time(update, context):
    '''Отправляет запрос ученикам о необходимости выбрать время'''
    context.bot.send_message(
        text='Запрос ученикам',
        chat_id=update.effective_chat.id,
    )


def generate_groups(update, context):
    '''Запускает формирование групп'''
    context.bot.send_message(
        text='Генератор групп',
        chat_id=update.effective_chat.id,
    )


def send_info_to_students(update, context):
    '''Рассылает ученикам(кураторам?) информацию о группах, времени и дате(?) созвона'''
    context.bot.send_message(
        text='Рассылка',
        chat_id=update.effective_chat.id,
    )


def admin_menu(update, context):
    '''Вывод меню роли'''
    keyboard = [
        [InlineKeyboardButton('Запрос времени у учеников', callback_data='admin_request_time')],
        [InlineKeyboardButton('Сформировать группы', callback_data='admin_generate_groups')],
        [InlineKeyboardButton('Рассылка информации ученикам', callback_data='admin_send_info')],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    context.bot.send_message(text="Выберите действие", chat_id=update.effective_chat.id, reply_markup=reply_markup)
