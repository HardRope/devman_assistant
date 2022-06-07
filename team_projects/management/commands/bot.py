from django.core.management.base import BaseCommand
from environs import Env
from telegram.ext import (CallbackQueryHandler, CommandHandler, Filters,
                          MessageHandler, Updater)

from .admin import (admin_confirm_groups, admin_menu, generate_groups,
                    request_time, send_info_to_students)
from .bot_main import start
from .project_manager import get_commands, pm_menu
from .student import call_pm, leave, student_menu


class Command(BaseCommand):
    help = "Telegram bot"

    def handle(self, *args, **kwargs):
        env = Env()
        env.read_env()
        telegram_bot_token = env.str("TELEGRAM_BOT_TOKEN")

        updater = Updater(token=telegram_bot_token, use_context=True)
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
        dispatcher.add_handler(CallbackQueryHandler(call_pm, pattern=r'student_call_pm'))
        dispatcher.add_handler(CallbackQueryHandler(leave, pattern=r'student_leave'))

        updater.start_polling()
        updater.idle()
