import os

from django.core.management.base import BaseCommand
from dotenv import load_dotenv
from telegram.ext import CommandHandler, CallbackQueryHandler, Filters
from telegram.ext import MessageHandler, Updater

from .admin import admin_menu, generate_groups, request_time, send_info_to_students
from .admin import admin_confirm_groups
from .bot_main import start
from .project_manager import get_commands, pm_menu
from .student import call_pm, change_time, choose_time, leave, student_menu
# from team_projects.models import Student

class Command(BaseCommand):
    help = "Telegram bot"

    def handle(self, *args, **kwargs):
        load_dotenv()
        bot_token = os.getenv("BOT-TOKEN")

        updater = Updater(token=bot_token, use_context=True)
        dispatcher = updater.dispatcher

        dispatcher.add_handler(CommandHandler('start', start))

        dispatcher.add_handler(MessageHandler(Filters.all, admin_menu))
        dispatcher.add_handler(CallbackQueryHandler(request_time, pattern=r'admin_request_time'))
        dispatcher.add_handler(CallbackQueryHandler(generate_groups, pattern=r'admin_generate_groups'))
        dispatcher.add_handler(CallbackQueryHandler(send_info_to_students, pattern=r'admin_send_info'))
        dispatcher.add_handler(CallbackQueryHandler(admin_confirm_groups, pattern=r'admin_confirm_groups'))

        dispatcher.add_handler(MessageHandler(Filters.all, pm_menu))
        dispatcher.add_handler(CallbackQueryHandler(get_commands, pattern=r'pm_get_commands'))

        dispatcher.add_handler(MessageHandler(Filters.all, student_menu))
        # dispatcher.add_handler(CallbackQueryHandler(choose_time, pattern=r'student_choose_time'))
        # dispatcher.add_handler(CallbackQueryHandler(change_time, pattern=r'student_change_time'))
        dispatcher.add_handler(CallbackQueryHandler(call_pm, pattern=r'student_call_pm'))
        dispatcher.add_handler(CallbackQueryHandler(leave, pattern=r'student_leave'))

        updater.start_polling()
        updater.idle()

    # def ask_for_timecode(student: Student,
    #                      necessary_timecodes: list,
    #                      buttons: list):
    #     row_buttons = []

    #     for button in timecodes_buttons[student]:
    #         row_buttons.append(button)

    #         if len(row_buttons) == 2:
    #             student_timecodes.append(row_buttons)
    #             row_buttons = []

    #         if row_buttons:
    #             student_timecodes.append(row_buttons)

    #         reply_markup = ReplyKeyboardMarkup (
    #             keyboard=student_timecodes,
    #             resize_keyboard=True,
    #             one_time_keyboard=True,
    #         )

    #         message = f'Привет, {student.first_name} {student.last_name}.'

    #         context.bot.send_message(
    #             text=message,
    #             chat_id=student.telegram_id,
    #             reply_markup=reply_markup
    #         )