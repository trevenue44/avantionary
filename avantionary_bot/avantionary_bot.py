import telebot
import os
from dotenv import load_dotenv
from avantionary_database import DataBase as db
load_dotenv()
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

API_KEY = os.environ.get("AVANTIONARY_API_KEY")

search = False
reverse = False
add_word, add_meaning, add_synonym, add_antonym = False
add = False

info_to_add = {}

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
    global search, reverse, add
    if call.data == "search":
        search = True
        avantionary_bot.send_message(call.message.chat.id, "Just text me the word!")
    if call.data == 'reverse':
        reverse = True
        search = True
        avantionary_bot.send_message(call.message.chat.id, "Reverse mode activated.\nSend me the word in reverse.\nI'll still send you its information")
    if call.data == 'add':
        avantionary_bot.send_message(call.message.chat.id, "Please fill the following form in the order with the required inputs.\n" + 
                                                           "\nNote: Any wrong information entered that is not identifiable by avantionary would be stored to memory as it is\n" +
                                                           "Caution: It is not advisable to edit the contents of a dictionary.")
        avantionary_bot.send_message(call.message.chat.id, "The following data will be required about the word." +
                                                            "\n\nThe Word\nThe meaning and any other information about the word\nAny synonyms (separate them with commas, if more than one)\nAny antonyms (separate them with commas, if more than one)")
        avantionary_bot.send_message(call.message.chat.id, "Let's start with the word: ")
        add = True

        


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
        avantionary_bot.reply_to(message, "Word: " + word)
    word_info = db.definitions(word)
    if word_info == "Word does not exist.":
        avantionary_bot.reply_to(message, "Word does not exist.")
    else:
        avantionary_bot.reply_to(message, f"MEANINGS:\n{word_info[0]}\n\nSYNONYMS:\n{word_info[1]}\n\nANTONYMS:\n{word_info[2]}")

def start_polling():
    avantionary_bot.polling(none_stop=True)

@avantionary_bot.message_handler(func=lambda:add and is_one_word())
def add_word(message):
    global info_to_add, add_meaning
    info_to_add["word"] = message.text.strip()
    avantionary_bot.send_message(message.chat.id, "Meaning of "+ info_to_add["word"])
    add_meaning = True

@avantionary_bot.message_handler(func=lambda:add_meaning)
def add_meaning(message):
    global info_to_add, add_synonym
    info_to_add["meaning"] = message.text.strip()
    avantionary_bot.send_message(message.chat.id, "Synonyms of "+ info_to_add["word"] + "\n Enter a dot(.) if there is none")
    add_synonym = True
 
@avantionary_bot.message_handler(func=lambda: add_synonym)
def add_synonym(message):
    global info_to_add, add_antonym
    info_to_add["synonyms"] = message.text.strip() if message.text.strip() != "." else ""
    avantionary_bot.send_message(message.chat.id, "Antonym of "+ info_to_add["word"] + "\n Enter a dot(.) if there is none")
    add_antonym = True

@avantionary_bot.message_handler(func=lambda: add_antonym)
def add_antonym(message):
    global info_to_add
    info_to_add["meaning"] = message.text.strip() if message.text.strip() != "." else ""
    avantionary_bot.send_message(message.chat.id, "Antonym of "+ info_to_add["word"] + "\n Enter a dot(.) if there is none")
    confirmation = False
    avantionary_bot.send_message(message.chat.id, "Are you sure you want to add the following data to the dictionary?")

    confirmation_markup = ReplyKeyboardMarkup()
    confirmation_markup.row(KeyboardButton("Yes"), KeyboardButton("No"))
