import os

from dotenv import load_dotenv
from telegram.ext import Updater
from telegram.ext import CommandHandler, CallbackQueryHandler, MessageHandler, Filters

from bot_users.bot_main import start
from bot_users.admin import admin_menu, request_time, generate_groups, send_info_to_students
from bot_users.student import student_menu, choose_time, change_time, call_pm, leave
from bot_users.project_manager import pm_menu, get_commands


if __name__ == "__main__":
    load_dotenv()
    bot_token = os.getenv("BOT-TOKEN")

    students = []
    project_managers = []
    admins = ["@HardRope", "@PaSeRouS"]

    updater = Updater(token=bot_token, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))

    dispatcher.add_handler(MessageHandler(Filters.all, admin_menu))
    dispatcher.add_handler(CallbackQueryHandler(request_time, pattern=r'admin_request_time'))
    dispatcher.add_handler(CallbackQueryHandler(generate_groups, pattern=r'admin_generate_groups'))
    dispatcher.add_handler(CallbackQueryHandler(send_info_to_students, pattern=r'admin_send_info'))

    dispatcher.add_handler(MessageHandler(Filters.all, pm_menu))
    dispatcher.add_handler(CallbackQueryHandler(get_commands, pattern=r'pm_get_commands'))

    dispatcher.add_handler(MessageHandler(Filters.all, student_menu))
    dispatcher.add_handler(CallbackQueryHandler(choose_time, pattern=r'student_choose_time'))
    dispatcher.add_handler(CallbackQueryHandler(change_time, pattern=r'student_change_time'))
    dispatcher.add_handler(CallbackQueryHandler(call_pm, pattern=r'student_call_pm'))
    dispatcher.add_handler(CallbackQueryHandler(leave, pattern=r'student_leave'))

    updater.start_polling()
    updater.idle()
