import logging
import json
from pprint import pprint
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          CallbackQueryHandler)
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import token_secure


updater = Updater(token=token_secure.TOKEN)
dispatcher = updater.dispatcher


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)
logger = logging.getLogger(__name__)


updater.start_polling()

#Global info
vote_auth = False
DATA = json.load(open('data.json'))
autorizados = ["WinnaZ","sofide", "ArthurMarduk"]

# command /start give usear a message
def start(bot, update):
    bot.send_message(
        chat_id=update.message.chat_id,
        text='Hola ' + update.message.from_user.first_name + '! Bienvenidx')


start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)


# repeat all messages user send to bot
def echo(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=update.message.text)
    print ("---------------------------------------------------------------")
    print ("usuario: " + update.message.from_user.username)
    print ("texto: " + update.message.text )
    
    
echo_handler = MessageHandler(Filters.text, echo)
dispatcher.add_handler(echo_handler)




def empezar_votacion(bot, update):
    global vote_auth
    if vote_auth == False:    
        if update.message.from_user.username in autorizados:    
            update.message.reply_text("Autorizado")
            update.message.reply_text("Votación Abierta")
            vote_auth = True
        else:
            update.message.reply_text("No estas Autorizadx para hacer esta acción")
    else:
        update.message.reply_text("La votacion ya estaba abierta")



def vote(bot, update):
    if vote_auth:
        update.message.reply_text(
            'Te interesa el proyecto:'
        )
        for project_name, project in DATA['projects'].items():
            keyboard = [[InlineKeyboardButton("Si!" , callback_data="si"),
                        InlineKeyboardButton("Nop", callback_data="no")]]

            reply_markup = InlineKeyboardMarkup(keyboard)

            update.message.reply_text(
                text= project_name,
                reply_markup=reply_markup
            )
    else:
        update.message.reply_text("Votación Cerrada")
        


def button(bot, update):
    query = update.callback_query
    print (query)
    if query.data == "si":
        project = query.message['text']
        user = query.message['chat']['username']
        result = 'Interesadx en: ' + project
        print (project,user)
        DATA['projects'][project]['votes'].append(user)
    else:
        result = 'No te interesa el proyecto' 


    bot.edit_message_text(text=result,
                          chat_id=query.message.chat_id,
                          message_id=query.message.message_id)

def terminar_votacion(bot, update):
    if update.message.from_user.username in autorizados:    
        with open('data.json', 'w') as f:
            json.dump(DATA, f, indent=2)
        update.message.reply_text("Autorizado")
        update.message.reply_text("Información Cargada, votación cerrada")
        vote_auth = False
    else:
        update.message.reply_text("No estas Autorizadx para hacer esta ación")


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


updater.dispatcher.add_handler(CommandHandler('empezar_votacion', empezar_votacion))
updater.dispatcher.add_handler(CommandHandler('vote', vote))
updater.dispatcher.add_handler(CommandHandler('terminar_votacion', terminar_votacion))
updater.dispatcher.add_handler(CallbackQueryHandler(button))
updater.dispatcher.add_error_handler(error)