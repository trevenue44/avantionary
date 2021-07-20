import telebot
import os
from dotenv import load_dotenv
from avantionary_database import DataBase as db
load_dotenv()
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

API_KEY = os.environ.get("AVANTIONARY_API_KEY")

search = False
reverse = False

avantionary_bot = telebot.TeleBot(API_KEY)

@avantionary_bot.message_handler(commands=["start"])
def start(message):

    keyboard = [
        [
            InlineKeyboardButton("Search", callback_data='search'),
            InlineKeyboardButton("Add", callback_data='add')
        ],
        [
            InlineKeyboardButton("Update", callback_data='update'),
            InlineKeyboardButton("Delete", callback_data="delete")
        ], 
        [
            InlineKeyboardButton("Reversed", callback_data='reverse')
        ]
    ]
    gen_markup = InlineKeyboardMarkup(keyboard)
    avantionary_bot.reply_to(message, "Hello there!\n" +
                             "This is Avantionary.\n" + 
                             "A bot to give you your word's meanings, synonyms and antonyms.", 
                             reply_markup=gen_markup)


@avantionary_bot.callback_query_handler(func= lambda call: True)
def callback_query(call):
    global search, reverse
    if call.data == "search":
        search = True
        avantionary_bot.send_message(call.message.chat.id, "Just text me the word!")
    if call.data == 'reverse':
        reverse = True
        search = True
        avantionary_bot.send_message(call.message.chat.id, "Reverse mode activated.\nSend me the word in reverse.\nI'll still send you its information")
        


def is_one_word(message):
    if " " not in message.text.strip() and search:
        return True
    elif search:
        avantionary_bot.reply_to(message, "Not a word.")
    else:
        return False

@avantionary_bot.message_handler(func=is_one_word)
def send_word_info(message):
    word = message.text.strip()
    if reverse:
        word = word[::-1]
    word_info = db.definitions(word)
    if word_info == "Word does not exist.":
        avantionary_bot.reply_to(message, "Word does not exist.")
    else:
        avantionary_bot.reply_to(message, f"MEANINGS:\n{word_info[0]}\n\nSYNONYMS:\n{word_info[1]}\n\nANTONYMS:\n{word_info[2]}")


def start_polling():
    avantionary_bot.polling(none_stop=True)

