import logging
import json
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          CallbackQueryHandler)
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import voting

updater = Updater(token='357811653:AAFaLB_tXns3LchYECBNyy-Swa6h4FbGEDc')
dispatcher = updater.dispatcher


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)
logger = logging.getLogger(__name__)


updater.start_polling()


# command /start give usear a message
def start(bot, update):
    bot.send_message(
        chat_id=update.message.chat_id,
        text='Hola {}!'.format(update.message.from_user.first_name))

def button(bot,update):
    query = update.callback_query
    keyboard = [[InlineKeyboardButton("Si!", callback_data="si"),
                InlineKeyboardButton("Nop", callback_data="no")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query = update.callback_query
    return query
    

def vote(bot, update,query):
    DATA = json.load(open('data.json'))

    for project_name, project in DATA['projects'].items():
        update.message.reply_text(
        'Te interesa el proyecto: {}?'.format(project_name),
                                    )

        if query.data == "si":
            result = 'Te interesa el proyecto: {}!'.format(project_name)
            project['votes'].append(update.message.from_user.username)

        else:
            result = 'No te interesa el proyecto: {}!'.format(project_name)

        bot.edit_message_text(text=result,
                          chat_id=query.message.chat_id,
                          message_id=query.message.message_id)

    with open('data.json', 'w') as f:
        json.dump(DATA, f, indent=2)
    


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)

# repeat all messages user send to bot
def echo(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=update.message.text)
    

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

echo_handler = MessageHandler(Filters.text, echo)
dispatcher.add_handler(echo_handler)

query = updater.dispatcher.add_handler(CallbackQueryHandler(button))
updater.dispatcher.add_handler(CommandHandler('vote', vote(bot,updater,query=query)))
updater.dispatcher.add_error_handler(error)
