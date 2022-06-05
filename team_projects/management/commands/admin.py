import os
from textwrap import dedent
from time import strptime

from telegram import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup

from .db_processing import get_actual_projects, get_participants, get_timecodes_buttons 
from .db_processing import save_timecode, get_current_timecodes
from .db_processing import GroupCorrectionError, ProjectFinishedError
from .distribution import sort_students

def request_time(update, context):
    '''Отправляет запрос ученикам о необходимости выбрать время'''
    projects = get_actual_projects()

    for project in projects:
        students = get_participants(project)

        for student in students:
            if not get_current_timecodes(student, project):
                student_timecodes = []
                row_buttons = []

                try:
                    timecodes_buttons = get_timecodes_buttons(student, project)

                    for button in timecodes_buttons[student]:
                        row_buttons.append(button)

                        if len(row_buttons) == 2:
                            student_timecodes.append(row_buttons)
                            row_buttons = []

                    if row_buttons:
                        student_timecodes.append(row_buttons)

                    reply_markup = ReplyKeyboardMarkup (
                        keyboard=student_timecodes,
                        resize_keyboard=True,
                        one_time_keyboard=True,
                    )

                    message = f'''Привет, {student.first_name} {student.last_name}.
Выбери удобное для тебя время для созвона во время проекта из представленных 
ниже.'''

                    context.bot.send_message(
                        text=message,
                        chat_id=student.telegram_id,
                        reply_markup=reply_markup
                    )

                except GroupCorrectionError:
                    message = f'''Группы в проекте "{project}" уже сформированы.
                
Дальнейшие корректировки невозможны.'''

                    context.bot.send_message(
                        text=message,
                        chat_id=student.telegram_id
                    )

                except ProjectFinishedError:
                    message = f'''"{project}" завершен.
                
Дальнейшие корректировки невозможны.'''
                             
                    context.bot.send_message(
                        text=message,
                        chat_id=student.telegram_id
                    )


def generate_groups(update, context):
    '''Запускает формирование групп'''
    projects = get_actual_projects()

    for project in projects:
        students_no_time = False

        students = get_participants(project)

        for student in students:
            if not get_current_timecodes(student, project) and students_no_time == False:
                context.bot.send_message(
                    text='''Не все ученики выбрали время! 
Запросите время у учеников ещё раз.''',
                    chat_id=update.effective_chat.id,
                )

                students_no_time = True

        if students_no_time == False:
            sort_students(project)

            context.bot.send_message(
                    text='''Группы сформированы.''',
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
    user_name = update.effective_user.name
    admins = os.getenv("ADMINS")

    if user_name in admins:
        keyboard = [
            [InlineKeyboardButton('Запрос времени у учеников', callback_data='admin_request_time')],
            [InlineKeyboardButton('Сформировать группы', callback_data='admin_generate_groups')],
            [InlineKeyboardButton('Рассылка информации ученикам', callback_data='admin_send_info')],
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        context.bot.send_message(text="Выберите действие:", chat_id=update.effective_chat.id, reply_markup=reply_markup)
    elif update.message.text:
        projects = get_actual_projects()

        for project in projects:
            students = get_participants(project)

            for student in students:
                if student.telegram_id == update.effective_chat.id:
                    student_timecodes = []
                    row_buttons = []

                    try:
                        timecodes_buttons = get_timecodes_buttons(
                            student,
                            project
                        )

                        for button in timecodes_buttons[student]:
                            if button == update.message.text:
                                timecode = save_timecode(
                                    button[0:8],
                                    student,
                                    project
                                )
                            
                                if button[14] == '0':
                                    convinient_time = button[0:2] + ':30:00'
                                elif button[14] == '3':
                                    convinient_time = button[11:13] + ':00:00'

                                timecode = save_timecode(
                                    convinient_time, 
                                    student, 
                                    project
                                )

                    except GroupCorrectionError:
                        message = f'''Группы в проекте "{project}" уже сформированы.
            
Дальнейшие корректировки невозможны.'''

                        context.bot.send_message(
                            text=message,
                            chat_id=student.telegram_id
                        )
                    except ProjectFinishedError:
                        message = f'''"{project}" завершен.
            
Дальнейшие корректировки невозможны.'''
                         
                        context.bot.send_message(
                            text=message,
                            chat_id=student.telegram_id
                        )