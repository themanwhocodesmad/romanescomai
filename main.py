from typing_extensions import Final
from telegram import Update
from telegram.ext import filters, Application, CommandHandler, MessageHandler, ContextTypes

from authentication.models import CustomUser

TOKEN: Final = "6403264388:AAH7wW54-pkLqSIX4UmFChcB5LsWEPC3VXw"
BOT_USERNAME: Final = "@MRE_Bot"


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /start is issued."""
    update.message.reply_text(
        'Hello! Please send me your username and mobile number separated by a comma: "username,012345789"')


async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /start is issued."""
    update.message.reply_text('This is a custom command')


def handle_response(text: str, update:Update) -> str:
    processed: str = text.lower()

    try:
        username, mobile_number = [item.strip() for item in processed.split(',')]
        user = CustomUser.objects.get(username=username, cell_number=mobile_number)
        user.telegram_ChatID = update.message.chat_id
        user.save()
        return 'Successfully authenticated and chatID saved!'

    except CustomUser.DoesNotExist:

        return 'Authentication failed. Please make sure you sent the correct username and mobile number.'

    except ValueError:
        return 'Please send your username and mobile number separated by a comma.'

