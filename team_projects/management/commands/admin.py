import os
from textwrap import dedent

from django.core.exceptions import ObjectDoesNotExist
from telegram import (InlineKeyboardButton, InlineKeyboardMarkup,
                      ReplyKeyboardMarkup)

from team_projects.models import AvailableTimecode

from .db_processing import (GroupCorrectionError, ProjectFinishedError,
                            confirm_groups, get_actual_projects, get_available_timecode,
                            get_current_student_group, get_current_timecodes,
                            get_participants, get_timecodes_buttons,
                            save_timecode)
from .distribution import sort_students


def request_time(update, context):
    '''Отправляет запрос ученикам о необходимости выбрать время'''
    projects = get_actual_projects()
    user_id = update.effective_user.id
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

                    message = dedent(
                        f"""
                        Привет, {student.first_name}!

                        Выбери удобное для тебя время для созвона из представленных ниже.
                        """
                    )
                    
                    context.bot.send_message(
                        text=message,
                        chat_id=student.telegram_id,
                        reply_markup=reply_markup
                    )

                except GroupCorrectionError as error:
                    context.bot.send_message(text=error, chat_id=user_id)

                except ProjectFinishedError as error:
                    context.bot.send_message(text=error, chat_id=user_id)
                

def generate_groups(update, context):
    '''Запускает формирование групп'''
    projects = get_actual_projects()

    for project in projects:
        students_no_time = False

        students = get_participants(project)

        for student in students:
            if not get_current_timecodes(student, project) and students_no_time == False:
                message = dedent(
                    """
                    Не все ученики выбрали время!
                    Запросите время у учеников ещё раз.
                    """
                )
                
                context.bot.send_message(
                    text=message,
                    chat_id=update.effective_chat.id,
                )

                students_no_time = True

        if students_no_time == False:
            groups, students_out = sort_students(project)

            message = dedent(
                """Сформированные группы:
                """
            )

            for timecode in groups:
                message += dedent(
                    f"""
                    Время: {timecode.__str__()}
                    Ученики:
                    """
                )
                
                for student in groups[timecode]['students']:
                    message += dedent(
                        f"""{student} ({student.level})
                        """
                    )

            message += dedent(
                """
                Неотсортированные ученики:
                """
            )
            for student in students_out:
                    message += dedent(
                        f"""{student} ({student.level})
                        """
                    )
            keyboard = [
                [InlineKeyboardButton('Подтвердить группы', callback_data='admin_confirm_groups')],
                [InlineKeyboardButton('Запрос времени у учеников', callback_data='admin_request_time')],
                [InlineKeyboardButton('Сформировать группы', callback_data='admin_generate_groups')],
                [InlineKeyboardButton('Рассылка информации ученикам', callback_data='admin_send_info')],
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

                message = dedent(
                    f"""
                    Привет! Созвон с командой будет в {group.timecode}.

                    Бриф проекта: {project.briefing}
                    """
                )
                
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
        user_id = update.effective_user.id
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
                message = dedent(
                    """
                    Сформировать группы не получилось.
                    Проверьте логи об ошибках
                    """
                )

                context.bot.send_message(
                    text=message,
                    chat_id=update.effective_chat.id,
                )

    except GroupCorrectionError as error:
        context.bot.send_message(text=error, chat_id=user_id)

    except ProjectFinishedError as error:
        context.bot.send_message(text=error, chat_id=user_id)


def admin_menu(update, context):
    '''Вывод меню роли'''
    user_id = update.effective_user.id
    admins = os.getenv("ADMIN")
    if str(user_id) in admins and update.message.text == '/start':
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
                                first_time = button.split(" - ")[0]
                                hour, minute, _ = first_time.split(":")
                                available_timecode = get_available_timecode(int(hour), int(minute))
                                first_timecode = save_timecode(
                                    available_timecode,
                                    student,
                                    project
                                )
                                
                                if minute == '30':
                                    hour = int(hour) + 1
                                    minute = 0
                                else:
                                    hour = int(hour)
                                    minute = 30
                                
                                available_timecode = get_available_timecode(hour, minute)
                                second_timecode = save_timecode(
                                    available_timecode, 
                                    student, 
                                    project
                                )

                    except GroupCorrectionError as error:
                        context.bot.send_message(text=error, chat_id=user_id)

                    except ProjectFinishedError as error:
                        context.bot.send_message(text=error, chat_id=user_id)
