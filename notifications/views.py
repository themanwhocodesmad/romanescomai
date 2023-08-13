from openpyxl.worksheet.filters import Filters
from romanesco.telegram import Update, Bot
from romanesco.telegram import Updater, MessageHandler, CallbackContext

updater = Updater(token='6403264388:AAH7wW54-pkLqSIX4UmFChcB5LsWEPC3VXw', use_context=True)


def register(update: Update, context: CallbackContext):
    msg = update.message.text.split()
    if len(msg) == 3:
        username, password = msg[1], msg[2]
        # Here you should add some logic to validate the username and password against your Django server
        # If they're valid, store the user's Telegram ID (update.message.chat_id) in your database
        context.bot.send_message(chat_id=update.effective_chat.id, text="You are now registered!")
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Please send your username and password.")


dispatcher = updater.dispatcher
register_handler = MessageHandler(Filters.text & (~Filters.command), register)
dispatcher.add_handler(register_handler)

updater.start_polling()


def notify_technician(jobNumber, assignedTechnician):
    bot = Bot(token='6403264388:AAH7wW54-pkLqSIX4UmFChcB5LsWEPC3VXw')
    bot.send_message(chat_id=CustomerUser.assignedTechnician.telegramChatID, text=f"{assignedTechnician} \n A new job has been assigned to you: {jobNumber}")
