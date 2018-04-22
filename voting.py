import json
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from bot import query



def vote(bot, update):
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
        
        return result

    with open('data.json', 'w') as f:
        json.dump(DATA, f, indent=2)

       