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
is_confirmed = False
delete = False
to_delete = None
ADD_WORD = False
DELETE_WORD = False

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
    global search, reverse, add, delete
    # alllowing the user to search when 'search' is chosen from the inline keyboard
    if call.data == "search":
        search = True
        avantionary_bot.send_message(call.message.chat.id, "Just text me the word!")
    # activating reverse mode when 'reverse' is chosen from the inline keyboard
    if call.data == 'reverse':
        reverse = True
        search = True
        add = False
        delete = False
        avantionary_bot.send_message(call.message.chat.id, "Reverse mode activated.\nSend me the word in reverse.\nI'll still send you its information")
    # allowing the user to understand a series of items to be able to add to the dictionary
    if call.data == 'add':
        avantionary_bot.send_message(call.message.chat.id, "Please fill the following form in the order with the required inputs.\n" + 
                                                           "\nNote: Any wrong information entered that is not identifiable by avantionary would be stored to memory as it is\n" +
                                                           "Caution: It is not advisable to edit the contents of a dictionary.")
        avantionary_bot.send_message(call.message.chat.id, "The following data will be required about the word." +
                                                            "\n\nThe Word\nThe meaning and any other information about the word\nAny synonyms (separate them with commas, if more than one)\nAny antonyms (separate them with commas, if more than one)")
        avantionary_bot.send_message(call.message.chat.id, "Let's start with the word: ")
        add = True
        search = False
        delete = False
        reverse = False
    # initializing the process of deletion of word from dictionary
    if call.data == "delete":
        avantionary_bot.send_message(call.message.chat.id, "Please enter the word you want to delete")
        delete = True
        search = False
        reverse = False
        add = False

########################################################################################################################
######################################## Important Usable Functions ####################################################
########################################################################################################################

def make_confirmation_markup():
    """
    A funciton for creating a ReplyKeyboardMarkup and returning it
    """
    confirmation_markup = ReplyKeyboardMarkup()
    confirmation_markup.row(KeyboardButton("Yes"), KeyboardButton("No"))
    return confirmation_markup


########################################################################################################################
################################ Handling Searching and Reversed Searching #############################################
########################################################################################################################

# checking if message from the user contains only one word
def is_one_word(message):
    if " " not in message.text.strip() and search and not (add or delete):
        return True
    elif search and not (add or delete):
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
        avantionary_bot.reply_to(message, f"MEANING(S):\n{word_info[0]}\n\nSYNONYM(S):\n{word_info[1]}\n\nANTONYM(S):\n{word_info[2]}")

############################################################################################################
############################################### Word Addition ##############################################
############################################################################################################

def should_add_word(message):
    if add and not (search or delete or DELETE_WORD):
        return True
    else:
        return False

# allowing the user to enter the words when the user selects 'add'
@avantionary_bot.message_handler(func=should_add_word)
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

def should_add_meaning(message):
    if add_meaning and not(search or DELETE_WORD or delete):
        return True
    else:
        return False

# taking the meaning from the user after he enters word
@avantionary_bot.message_handler(func=should_add_meaning)
def add_meaning(message):
    global info_to_add, add_synonym, add_meaning
    info_to_add["meaning"] = message.text.strip()
    avantionary_bot.send_message(message.chat.id, "Synonym(s) of "+ info_to_add["word"] + "\nEnter a dot(.) if there is none")
    add_synonym = True
    add_meaning = False
 
def should_add_synonym(message):
    if add_synonym and not (search or delete or add or DELETE_WORD):
        return True
    else:
        return False

 # taking the synonyms from the user after he enters word
@avantionary_bot.message_handler(func=should_add_synonym)
def add_synonym(message):
    global info_to_add, add_antonym, add_synonym
    if message.text.strip() != ".":
        info_to_add["synonyms"] = message.text.strip().split(", ")
    else:
        info_to_add["synonyms"] = []
    avantionary_bot.send_message(message.chat.id, "Antonym(s) of "+ info_to_add["word"] + "\nEnter a dot(.) if there is none")
    add_antonym = True
    add_synonym = False


def should_add_antonym(message):
    if add_antonym and not (search or add or DELETE_WORD or delete):
        return True
    else:
        return False

# taking the antonyms from the user after he enters word
@avantionary_bot.message_handler(func=should_add_antonym)
def add_antonym(message):
    global info_to_add, add_antonym, ADD_WORD
    if message.text.strip() != ".":
        info_to_add["antonyms"] = message.text.strip().split(", ")
    else:
        info_to_add["antonyms"] = []
    add_antonym = False
    ADD_WORD = True
    
    # asking the user for confirmation
    avantionary_bot.send_message(message.chat.id, "Are you sure you want to add the following data to the dictionary?\n\nYes or No", reply_markup=make_confirmation_markup())


# checking the result of the confirmation markup
def add_confirmation(message):
    global is_confirmed
    if message.text.strip().lower() == "yes" and ADD_WORD and not (is_confirmed or delete or search or DELETE_WORD):
        avantionary_bot.send_message(message.chat.id, "Confirmed.", reply_markup=ReplyKeyboardRemove())
        is_confirmed = True
        return True
    elif message.text.strip().lower() == "no" and ADD_WORD and not (is_confirmed or delete or search or DELETE_WORD):
        avantionary_bot.send_message(message.chat.id, "Action aborted.")
        is_confirmed = True
        return False
    elif not (is_confirmed or delete or DELETE_WORD or search) and ADD_WORD:
        avantionary_bot.send_message(message.chat.id, "Invalid choice. Please try again.", reply_markup=make_confirmation_markup())


# checking for confirmation before adding word to the dictionary
@avantionary_bot.message_handler(func=add_confirmation)
def add_word_confirmed(message):
    global ADD_WORD
    if ADD_WORD:
        feedback = add_word(info_to_add)
        avantionary_bot.send_message(message.chat.id, feedback)
    else:
        return

def add_word(info):
    global ADD_WORD
    """
    A funciton for handling the addition of the words and its info taken from the user to the database
    """
    ADD_WORD = False
    return db.add_to_dictionary(info)


##########################################################################################################################
############################################# Deletion of Word ###########################################################
##########################################################################################################################

def should_delete_word(message):
    if delete and not (search or add or ADD_WORD):
        return True
    else:
        return False

# a function for handling the deletion of a word
@avantionary_bot.message_handler(func=should_delete_word)
def delete_word(message):
    global delete, to_delete, DELETE_WORD, is_confirmed
    if (" " not in message.text.strip()) and not message.text.strip().isnumeric():
        if db.definitions(message.text.strip()) != "Word does not exist.":
            delete = False
            DELETE_WORD = True
            to_delete = message.text.strip().upper()
            is_confirmed = False
            avantionary_bot.reply_to(message, "Are you sure you want to delete " + message.text.strip().upper(), reply_markup=make_confirmation_markup())
        else:
            avantionary_bot.reply_to(message, "Word not in dictionary")
            return
    else:
        avantionary_bot.reply_to(message, "Not a word. Please try again.")


def delete_confirmation(message):
    global is_confirmed
    if (message.text.strip().lower() == "yes") and DELETE_WORD and not (is_confirmed or delete or search or add or ADD_WORD):
        avantionary_bot.send_message(message.chat.id, "Confirmed.", reply_markup=ReplyKeyboardRemove())
        is_confirmed = True
        return True
    elif (message.text.strip().lower() == "no") and DELETE_WORD and not (is_confirmed or delete or search or add or ADD_WORD):
        avantionary_bot.send_message(message.chat.id, "Action aborted.")
        is_confirmed = True
        return False
    elif not (is_confirmed or add or ADD_WORD or search) and DELETE_WORD:
        avantionary_bot.send_message(message.chat.id, "Invalid choice. Please try again.", reply_markup=make_confirmation_markup())


@avantionary_bot.message_handler(func=delete_confirmation)
def delete_word_confirmed(message):
    global DELETE_WORD, to_delete
    if DELETE_WORD:
        feedback = db.delete_from_dictionary(to_delete)
        avantionary_bot.send_message(message.chat.id, feedback)
        DELETE_WORD = False
    else:
        return

####################################################################################################################

def start_polling():
    """
    A function to allow external access to the bot. To be able to poll from another file
    """
    avantionary_bot.polling(none_stop=True)
