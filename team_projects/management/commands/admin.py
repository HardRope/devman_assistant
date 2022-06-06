import os
from textwrap import dedent
from time import strptime

from django.core.exceptions import ObjectDoesNotExist
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup

from .db_processing import get_actual_projects, get_participants, get_timecodes_buttons 
from .db_processing import confirm_groups, get_current_timecodes, save_timecode
from .db_processing import get_current_student_group
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

                    message = f'Привет, {student.first_name} {student.last_name}.\n'
                    message = message + 'Выбери удобное для тебя время для созвона'
                    message = message + 'во время проекта из представленных ниже.'
                    
                    context.bot.send_message(
                        text=message,
                        chat_id=student.telegram_id,
                        reply_markup=reply_markup
                    )

                except GroupCorrectionError:
                    message = f'Группы в проекте "{project}" уже сформированы.'
                    message = message + 'Дальнейшие корректировки невозможны.'

                    context.bot.send_message(
                        text=message,
                        chat_id=student.telegram_id
                    )

                except ProjectFinishedError:
                    message = f'"{project}" завершен.'
                    message = message + 'Дальнейшие корректировки невозможны.'
                             
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
                message = 'Не все ученики выбрали время!'
                message = message + 'Запросите время у учеников ещё раз.'

                context.bot.send_message(
                    text=message,
                    chat_id=update.effective_chat.id,
                )

                students_no_time = True

        if students_no_time == False:
            groups, students_out = sort_students(project)

            message = 'Сформированные группы: \n'

            for timecode in groups:
                message = message + 'Время: ' + timecode.__str__() + '\n'
                message = message + 'Уровень: '+ groups[timecode]['level'].__str__() + '\n'
                message = message + 'Ученики: \n'

                for student in groups[timecode]['students']:
                    message = message + student.__str__() + '\n'

                message = message + '\n'

            message = message + 'Неотсортированные ученики' + '\n'
            for student in students_out:
                    message = message + student.__str__() + '\n'

            keyboard = [
                [InlineKeyboardButton('Подтвердить группы', callback_data='admin_confirm_groups')],
            ]

            reply_markup = InlineKeyboardMarkup(keyboard)

            context.bot.send_message(
                    text=message,
                    chat_id=update.effective_chat.id,
                    reply_markup = reply_markup
                )


def send_info_to_students(update, context):
    '''Рассылает ученикам(кураторам?) информацию о группах, времени и дате(?) созвона'''
    projects = get_actual_projects()

    for project in projects:
        students = get_participants(project)
        
        for student in students:
            try:
                group = get_current_student_group(student, project)

                message = 'Привет! Созвон с командой будет в '
                message = message + group.timecode.__str__() + '.\n\n'
                message = message + 'Вот описание проекта: '
                message = message + project.briefing

                context.bot.send_message(
                    text=message,
                    chat_id=student.telegram_id,
                )
            except ObjectDoesNotExist:
                continue


def admin_confirm_groups(update, context):
    '''Создаёт группы после подтверждения'''
    try:
        projects = get_actual_projects()

        for project in projects:
            groups, students = sort_students(project)
            if confirm_groups(project, groups, students):
                keyboard = [
                    [InlineKeyboardButton('Оповестить учеников', callback_data='admin_send_info')],
                ]

                reply_markup = InlineKeyboardMarkup(keyboard)

                context.bot.send_message(
                    text='Студенты расформированы по группам',
                    chat_id=update.effective_chat.id,
                    reply_markup = reply_markup
                )
            else:
                message = 'Сформировать группы не получилось\n'
                message = message + 'Проверьте логи об ошибках'

                context.bot.send_message(
                    text=message,
                    chat_id=update.effective_chat.id,
                )

    except GroupCorrectionError:
        message = f'Группы в проекте "{project}" уже сформированы.\n'
        message = message + 'Дальнейшие корректировки невозможны.'

        context.bot.send_message(
            text=message,
            chat_id=student.telegram_id
        )

    except ProjectFinishedError:
        message = f'"{project}" завершен.'
        message = message + 'Дальнейшие корректировки невозможны.'
                             
        context.bot.send_message(
            text=message,
            chat_id=student.telegram_id
        )


def admin_menu(update, context):
    '''Вывод меню роли'''
    user_name = update.effective_user.name
    admins = os.getenv("ADMINS")

    if user_name in admins and update.message.text == '/start':
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
                        message = f'Группы в проекте "{project}" уже сформированы.'
                        message = message + 'Дальнейшие корректировки невозможны.'

                        context.bot.send_message(
                            text=message,
                            chat_id=student.telegram_id
                        )
                    except ProjectFinishedError:
                        message = f'"{project}" завершен.'
                        message = message + 'Дальнейшие корректировки невозможны.'
                         
                        context.bot.send_message(
                            text=message,
                            chat_id=student.telegram_id
                        )