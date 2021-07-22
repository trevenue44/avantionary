# DOCUMENTATION
# This is a python module of avantionary_bot to allow access from other files
# Used mainly pyTelegramBotAPI package to control the actions of avantionary_bot

import telebot
import os
from dotenv import load_dotenv
from avantionary_database import DataBase as db
load_dotenv()
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

# loading in the environment variable
API_KEY = os.environ.get("AVANTIONARY_API_KEY")

# some global variables for easy navigation when inputs are given
search = False
reverse = False
add_word, add_meaning, add_synonym, add_antonym = (False, False, False, False)
add = False
info_to_add = {}

# creating the avantionary_bot
avantionary_bot = telebot.TeleBot(API_KEY)

# handling the welcome message. When the bot is started
@avantionary_bot.message_handler(commands=["start"])
def start(message):
    # creating an inline keyboard with the necessary buttons
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
    # creating the inline markup using the keyboard above and displaying it to the user
    inline_markup = InlineKeyboardMarkup(keyboard)
    avantionary_bot.reply_to(message, "Hello there!\n" +
                             "This is Avantionary.\n" + 
                             "A bot to give you your word's meanings, synonyms and antonyms.", 
                             reply_markup=inline_markup)


# handling the data from the user. What the user enters after the welcome message
@avantionary_bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    global search, reverse, add
    # alllowing the user to search when 'search' is chosen from the inline keyboard
    if call.data == "search":
        search = True
        avantionary_bot.send_message(call.message.chat.id, "Just text me the word!")
    # activating reverse mode when 'reverse' is chosen from the inline keyboard
    if call.data == 'reverse':
        reverse = True
        search = True
        avantionary_bot.send_message(call.message.chat.id, "Reverse mode activated.\nSend me the word in reverse.\nI'll still send you its information")
    # allowing the user to under a series of items to be able to add to the dictionary
    if call.data == 'add':
        avantionary_bot.send_message(call.message.chat.id, "Please fill the following form in the order with the required inputs.\n" + 
                                                           "\nNote: Any wrong information entered that is not identifiable by avantionary would be stored to memory as it is\n" +
                                                           "Caution: It is not advisable to edit the contents of a dictionary.")
        avantionary_bot.send_message(call.message.chat.id, "The following data will be required about the word." +
                                                            "\n\nThe Word\nThe meaning and any other information about the word\nAny synonyms (separate them with commas, if more than one)\nAny antonyms (separate them with commas, if more than one)")
        avantionary_bot.send_message(call.message.chat.id, "Let's start with the word: ")
        add = True

# checking if message from the user contains only one word
def is_one_word(message):
    if " " not in message.text.strip() and search and not add:
        return True
    elif search and not add:
        avantionary_bot.reply_to(message, "Not a word.")
    else:
        return False

# handling the sending of word information when the user selects 'search' and enters a word
@avantionary_bot.message_handler(func=is_one_word)
def send_word_info(message):
    word = message.text.strip()
    # reversing the word in case reverse mode is activated by the user
    if reverse:
        word = word[::-1]
        avantionary_bot.reply_to(message, "Word: " + word)
    # getting the definitions from the avantionary database and displaying necessary output to the user
    word_info = db.definitions(word)
    if word_info == "Word does not exist.":
        avantionary_bot.reply_to(message, "Word does not exist.")
    else:
        avantionary_bot.reply_to(message, f"**MEANING(S)**:\n{word_info[0]}\n\n**SYNONYM(S)**:\n{word_info[1]}\n\n**ANTONYM(S)**:\n{word_info[2]}")

# allowing the user to enter the words when the user selects 'add'
@avantionary_bot.message_handler(func=lambda _: True if add else False)
def add_word(message):
    global info_to_add, add_meaning, add
    if (" " not in message.text.strip()) and not message.text.strip().isnumeric():
        if db.definitions(message.text.strip()) == "Word does not exist.":
            info_to_add["word"] = message.text.strip()
            avantionary_bot.send_message(message.chat.id, "Meaning of "+ info_to_add["word"])
            add_meaning = True
            add = False
        else:
            avantionary_bot.reply_to(message, "Word already in avantionary.")
            return
    else:
        avantionary_bot.reply_to(message, "Not one word. Please try again.")

# taking the meaning from the user after he enters word
@avantionary_bot.message_handler(func=lambda _: True if add_meaning else False)
def add_meaning(message):
    global info_to_add, add_synonym, add_meaning
    info_to_add["meaning"] = message.text.strip()
    avantionary_bot.send_message(message.chat.id, "Synonyms of "+ info_to_add["word"] + "\n Enter a dot(.) if there is none")
    add_synonym = True
    add_meaning = False
 
 # taking the synonyms from the user after he enters word
@avantionary_bot.message_handler(func=lambda _: True if add_synonym else False)
def add_synonym(message):
    global info_to_add, add_antonym, add_synonym
    info_to_add["synonyms"] = message.text.strip() if message.text.strip() != "." else ""
    avantionary_bot.send_message(message.chat.id, "Antonym of "+ info_to_add["word"] + "\n Enter a dot(.) if there is none")
    add_antonym = True
    add_synonym = False

# taking the antonyms from the user after he enters word
@avantionary_bot.message_handler(func=lambda _: True if add_antonym else False)
def add_antonym(message):
    global info_to_add, add_antonym
    info_to_add["antonyms"] = message.text.strip() if message.text.strip() != "." else ""
    add_antonym = False
    
    # asking the user for confirmation
    avantionary_bot.send_message(message.chat.id, "Are you sure you want to add the following data to the dictionary?\n\nYes or No", reply_markup=make_confirmation_markup())


def make_confirmation_markup():
    """
    A funciton for creating a ReplyKeyboardMarkup and returning it
    """
    confirmation_markup = ReplyKeyboardMarkup()
    confirmation_markup.row(KeyboardButton("Yes"), KeyboardButton("No"))
    return confirmation_markup

# checking the result of the confirmation markup
def confirmation(message):
    if message.text.strip().lower() == "yes":
        avantionary_bot.send_message(message.chat.id, "Confirmed.", reply_markup=ReplyKeyboardRemove())
        return True
    elif message.text.strip().lower() == "no":
        avantionary_bot.send_message(message.chat.id, "Action aborted.")
        return False
    else:
        avantionary_bot.send_message(message.chat.id, "Invalid choice. Please try again.", reply_markup=make_confirmation_markup())

# checking for confirmation before adding word to the dictionary
@avantionary_bot.message_handler(func=confirmation)
def add_word_confirmed(message):
    feedback = add_word(info_to_add)
    avantionary_bot.send_message(message.chat.id, feedback)


def add_word(info):
    """
    A funciton for handling the addition of the words and its info taken from the user to the database
    """
    print(info)
    return "Word Printed"

def start_polling():
    """
    A function to allow external access to the bot. To be able to poll from another file
    """
    avantionary_bot.polling(none_stop=True)
