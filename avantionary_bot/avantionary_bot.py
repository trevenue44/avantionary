import telebot
import os
from dotenv import load_dotenv
from avantionary_database import DataBase as db
load_dotenv()
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

API_KEY = os.environ.get("AVANTIONARY_API_KEY")

avantionary_bot = telebot.TeleBot(API_KEY)

@avantionary_bot.message_handler(commands=["start"])
def start(message):

    keyboard = [
        [
            InlineKeyboardButton("Update", callback_data='1'),
            InlineKeyboardButton("Add", callback_data='1')
        ],
        [
            InlineKeyboardButton("Delete", callback_data='1'),
            InlineKeyboardButton("Search", callback_data="1")
        ], 
        [
            InlineKeyboardButton("Anagram", callback_data='1')
        ]
    ]
    gen_markup = InlineKeyboardMarkup(keyboard)
    avantionary_bot.reply_to(message, "Hello there!\n" +
                             "This is Avantionary.\n" + 
                             "A bot to give you your word's meanings, synonyms and antonyms." +
                             "\nJust text me the word!", reply_markup=gen_markup)


def is_one_word(message):
    if " " not in message.text.strip():
        return True
    else:
        avantionary_bot.reply_to(message, "Not a word.")
        return False

@avantionary_bot.message_handler(func=is_one_word)
def send_word_info(message):
    word = message.text.strip()
    word_info = db.definitions(word)
    if word_info == "Word does not exist.":
        avantionary_bot.reply_to(message, "Word does not exist.")
    else:
        avantionary_bot.reply_to(message, f"MEANINGS:\n{word_info[0]}\n\nSYNONYMS:\n{word_info[1]}\n\nANTONYMS:\n{word_info[2]}")


def start_polling():
    avantionary_bot.polling()
