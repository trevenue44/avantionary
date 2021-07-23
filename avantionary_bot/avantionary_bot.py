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
class ChatVariables():
    def __init__(self):
        self.search = False
        self.reverse = False
        self.add_word, self.add_meaning, self.add_synonym, self.add_antonym = (False, False, False, False)
        self.add = False
        self.info_to_add = {}
        self.is_confirmed = False
        self.delete = False
        self.to_delete = None
        self.ADD_WORD = False
        self.DELETE_WORD = False

ID_VARIABLES = {}

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
    ID_VARIABLES[message.chat.id] = ChatVariables()

# handling the data from the user. What the user enters after the welcome message
@avantionary_bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    global ID_VARIABLES
    # alllowing the user to search when 'search' is chosen from the inline keyboard
    if (call.message.chat.id in ID_VARIABLES) and call.data == "search":
        ID_VARIABLES[call.message.chat.id].search = True
        ID_VARIABLES[call.message.chat.id].reverse = False
        ID_VARIABLES[call.message.chat.id].add = False
        ID_VARIABLES[call.message.chat.id].delete = False
        avantionary_bot.send_message(call.message.chat.id, "Just text me the word!")
    # activating reverse mode when 'reverse' is chosen from the inline keyboard
    if (call.message.chat.id in ID_VARIABLES) and call.data == 'reverse':
        ID_VARIABLES[call.message.chat.id].reverse = True
        ID_VARIABLES[call.message.chat.id].search = True
        ID_VARIABLES[call.message.chat.id].add = False
        ID_VARIABLES[call.message.chat.id].delete = False
        avantionary_bot.send_message(call.message.chat.id, "Reverse mode activated.\nSend me the word in reverse.\nI'll still send you its information")
    # allowing the user to understand a series of items to be able to add to the dictionary
    if (call.message.chat.id in ID_VARIABLES) and call.data == 'add':
        avantionary_bot.send_message(call.message.chat.id, "Please fill the following form in the order with the required inputs.\n" + 
                                                           "\nNote: Any wrong information entered that is not identifiable by avantionary would be stored to memory as it is\n" +
                                                           "Caution: It is not advisable to edit the contents of a dictionary.")
        avantionary_bot.send_message(call.message.chat.id, "The following data will be required about the word." +
                                                            "\n\nThe Word\nThe meaning and any other information about the word\nAny synonyms (separate them with commas, if more than one)\nAny antonyms (separate them with commas, if more than one)")
        avantionary_bot.send_message(call.message.chat.id, "Let's start with the word: ")
        ID_VARIABLES[call.message.chat.id].add = True
        ID_VARIABLES[call.message.chat.id].search = False
        ID_VARIABLES[call.message.chat.id].delete = False
        ID_VARIABLES[call.message.chat.id].reverse = False
        print(call.message.chat.id)
    # initializing the process of deletion of word from dictionary
    if (call.message.chat.id in ID_VARIABLES) and call.data == "delete":
        avantionary_bot.send_message(call.message.chat.id, "Please enter the word you want to delete")
        ID_VARIABLES[call.message.chat.id].delete = True
        ID_VARIABLES[call.message.chat.id].search = False
        ID_VARIABLES[call.message.chat.id].reverse = False
        ID_VARIABLES[call.message.chat.id].add = False

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
    if (message.chat.id in ID_VARIABLES) and (" " not in message.text.strip()) and ID_VARIABLES[message.chat.id].search and not (ID_VARIABLES[message.chat.id].add or ID_VARIABLES[message.chat.id].delete):
        return True
    elif (message.chat.id in ID_VARIABLES) and ID_VARIABLES[message.chat.id].search and not (ID_VARIABLES[message.chat.id].add or ID_VARIABLES[message.chat.id].delete):
        avantionary_bot.reply_to(message, "Not a word.")
    else:
        return False

# handling the sending of word information when the user selects 'search' and enters a word
@avantionary_bot.message_handler(func=is_one_word)
def send_word_info(message):
    word = message.text.strip()
    # reversing the word in case reverse mode is activated by the user
    if (message.chat.id in ID_VARIABLES) and ID_VARIABLES[message.chat.id].reverse:
        word = word[::-1]
        avantionary_bot.reply_to(message, "Word: " + word)
    # getting the definitions from the avantionary database and displaying necessary output to the user
    word_info = db.definitions(word)
    if (message.chat.id in ID_VARIABLES) and (word_info == "Word does not exist."):
        avantionary_bot.reply_to(message, "Word does not exist.")
    else:
        avantionary_bot.reply_to(message, f"MEANING(S):\n{word_info[0]}\n\nSYNONYM(S):\n{word_info[1]}\n\nANTONYM(S):\n{word_info[2]}")

############################################################################################################
############################################### Word Addition ##############################################
############################################################################################################

def should_add_word(message):
    if (message.chat.id in ID_VARIABLES) and ID_VARIABLES[message.chat.id].add and not (ID_VARIABLES[message.chat.id].search or ID_VARIABLES[message.chat.id].delete or ID_VARIABLES[message.chat.id].DELETE_WORD):
        return True
    else:
        return False

# allowing the user to enter the words when the user selects 'add'
@avantionary_bot.message_handler(func=should_add_word)
def add_word(message):
    global ID_VARIABLES
    if (" " not in message.text.strip()) and not message.text.strip().isnumeric():
        if db.definitions(message.text.strip()) == "Word does not exist.":
            ID_VARIABLES[message.chat.id].info_to_add[message.chat.id] = {"word": message.text.strip()}
            avantionary_bot.reply_to(message, "Meaning of "+ ID_VARIABLES[message.chat.id].info_to_add[message.chat.id]["word"])
            ID_VARIABLES[message.chat.id].add_meaning = True
            ID_VARIABLES[message.chat.id].add = False
        else:
            avantionary_bot.reply_to(message, "Word already in avantionary.")
            return
    else:
        avantionary_bot.reply_to(message, "Not one word. Please try again.")

def should_add_meaning(message):
    if (message.chat.id in ID_VARIABLES) and ID_VARIABLES[message.chat.id].add_meaning and not(ID_VARIABLES[message.chat.id].search or ID_VARIABLES[message.chat.id].DELETE_WORD or ID_VARIABLES[message.chat.id].delete):
        return True
    else:
        return False

# taking the meaning from the user after he enters word
@avantionary_bot.message_handler(func=should_add_meaning)
def add_meaning(message):
    global ID_VARIABLES
    ID_VARIABLES[message.chat.id].info_to_add[message.chat.id]["meaning"] = message.text.strip()
    avantionary_bot.reply_to(message, "Synonym(s) of "+ ID_VARIABLES[message.chat.id].info_to_add[message.chat.id]["word"] + "\nEnter a dot(.) if there is none")
    ID_VARIABLES[message.chat.id].add_synonym = True
    ID_VARIABLES[message.chat.id].add_meaning = False
 
def should_add_synonym(message):
    if (message.chat.id in ID_VARIABLES) and ID_VARIABLES[message.chat.id].add_synonym and not (ID_VARIABLES[message.chat.id].search or ID_VARIABLES[message.chat.id].delete or ID_VARIABLES[message.chat.id].add or ID_VARIABLES[message.chat.id].DELETE_WORD):
        return True
    else:
        return False

 # taking the synonyms from the user after he enters word
@avantionary_bot.message_handler(func=should_add_synonym)
def add_synonym(message):
    global ID_VARIABLES
    if message.text.strip() != ".":
        ID_VARIABLES[message.chat.id].info_to_add[message.chat.id]["synonyms"] = message.text.strip().split(", ")
    else:
        ID_VARIABLES[message.chat.id].info_to_add[message.chat.id]["synonyms"] = []
    avantionary_bot.reply_to(message, "Antonym(s) of "+ ID_VARIABLES[message.chat.id].info_to_add[message.chat.id]["word"] + "\nEnter a dot(.) if there is none")
    ID_VARIABLES[message.chat.id].add_antonym = True
    ID_VARIABLES[message.chat.id].add_synonym = False


def should_add_antonym(message):
    if (message.chat.id in ID_VARIABLES) and ID_VARIABLES[message.chat.id].add_antonym and not (ID_VARIABLES[message.chat.id].search or ID_VARIABLES[message.chat.id].add or ID_VARIABLES[message.chat.id].DELETE_WORD or ID_VARIABLES[message.chat.id].delete):
        return True
    else:
        return False

# taking the antonyms from the user after he enters word
@avantionary_bot.message_handler(func=should_add_antonym)
def add_antonym(message):
    global ID_VARIABLES
    if message.text.strip() != ".":
        ID_VARIABLES[message.chat.id].info_to_add[message.chat.id]["antonyms"] = message.text.strip().split(", ")
    else:
        ID_VARIABLES[message.chat.id].info_to_add[message.chat.id]["antonyms"] = []
    ID_VARIABLES[message.chat.id].add_antonym = False
    ID_VARIABLES[message.chat.id].ADD_WORD = True
    
    # asking the user for confirmation
    avantionary_bot.reply_to(message, "Are you sure you want to add the following data to the dictionary?\n\nYes or No", reply_markup=make_confirmation_markup())


# checking the result of the confirmation markup
def add_confirmation(message):
    global ID_VARIABLES
    if (message.chat.id in ID_VARIABLES) and message.text.strip().lower() == "yes" and ID_VARIABLES[message.chat.id].ADD_WORD and not (ID_VARIABLES[message.chat.id].is_confirmed or ID_VARIABLES[message.chat.id].delete or ID_VARIABLES[message.chat.id].search or ID_VARIABLES[message.chat.id].DELETE_WORD):
        avantionary_bot.reply_to(message, "Confirmed.", reply_markup=ReplyKeyboardRemove())
        ID_VARIABLES[message.chat.id].is_confirmed = True
        return True
    elif (message.chat.id in ID_VARIABLES) and message.text.strip().lower() == "no" and ID_VARIABLES[message.chat.id].ADD_WORD and not (ID_VARIABLES[message.chat.id].is_confirmed or ID_VARIABLES[message.chat.id].delete or ID_VARIABLES[message.chat.id].search or ID_VARIABLES[message.chat.id].DELETE_WORD):
        avantionary_bot.reply_to(message, "Action aborted.")
        ID_VARIABLES[message.chat.id].is_confirmed = True
        return False
    elif (message.chat.id in ID_VARIABLES) and not (ID_VARIABLES[message.chat.id].is_confirmed or ID_VARIABLES[message.chat.id].delete or ID_VARIABLES[message.chat.id].DELETE_WORD or ID_VARIABLES[message.chat.id].search) and ID_VARIABLES[message.chat.id].ADD_WORD:
        avantionary_bot.reply_to(message, "Invalid choice. Please try again.", reply_markup=make_confirmation_markup())


# checking for confirmation before adding word to the dictionary
@avantionary_bot.message_handler(func=add_confirmation)
def add_word_confirmed(message):
    global ID_VARIABLES
    if (message.chat.id in ID_VARIABLES) and ID_VARIABLES[message.chat.id].ADD_WORD:
        feedback = db.add_to_dictionary(ID_VARIABLES[message.chat.id].info_to_add[message.chat.id])
        avantionary_bot.reply_to(message, feedback)
        ID_VARIABLES[message.chat.id].ADD_WORD = False
    else:
        return


# ##########################################################################################################################
# ############################################# Deletion of Word ###########################################################
# ##########################################################################################################################

def should_delete_word(message):
    if (message.chat.id in ID_VARIABLES) and ID_VARIABLES[message.chat.id].delete and not (ID_VARIABLES[message.chat.id].search or ID_VARIABLES[message.chat.id].add or ID_VARIABLES[message.chat.id].ADD_WORD):
        return True
    else:
        return False

# a function for handling the deletion of a word
@avantionary_bot.message_handler(func=should_delete_word)
def delete_word(message):
    global ID_VARIABLES
    if (message.chat.id in ID_VARIABLES) and (" " not in message.text.strip()) and not message.text.strip().isnumeric():
        if db.definitions(message.text.strip()) != "Word does not exist.":
            ID_VARIABLES[message.chat.id].delete = False
            ID_VARIABLES[message.chat.id].DELETE_WORD = True
            ID_VARIABLES[message.chat.id].to_delete = message.text.strip().upper()
            ID_VARIABLES[message.chat.id].is_confirmed = False
            avantionary_bot.reply_to(message, "Are you sure you want to delete " + message.text.strip().upper(), reply_markup=make_confirmation_markup())
        else:
            avantionary_bot.reply_to(message, "Word not in dictionary")
            return
    elif not (message.chat.id in ID_VARIABLES):
        return
    else:
        avantionary_bot.reply_to(message, "Not a word. Please try again.")


def delete_confirmation(message):
    global ID_VARIABLES
    if (message.chat.id in ID_VARIABLES) and (message.text.strip().lower() == "yes") and ID_VARIABLES[message.chat.id].DELETE_WORD and not (ID_VARIABLES[message.chat.id].is_confirmed or ID_VARIABLES[message.chat.id].delete or ID_VARIABLES[message.chat.id].search or ID_VARIABLES[message.chat.id].add or ID_VARIABLES[message.chat.id].ADD_WORD):
        avantionary_bot.send_message(message.chat.id, "Confirmed.", reply_markup=ReplyKeyboardRemove())
        is_confirmed = True
        return True
    elif (message.chat.id in ID_VARIABLES) and (message.text.strip().lower() == "no") and ID_VARIABLES[message.chat.id].DELETE_WORD and not (ID_VARIABLES[message.chat.id].is_confirmed or ID_VARIABLES[message.chat.id].delete or ID_VARIABLES[message.chat.id].search or ID_VARIABLES[message.chat.id].add or ID_VARIABLES[message.chat.id].ADD_WORD):
        avantionary_bot.send_message(message.chat.id, "Action aborted.")
        ID_VARIABLES[message.chat.id].is_confirmed = True
        return False
    elif (message.chat.id in ID_VARIABLES) and not (ID_VARIABLES[message.chat.id].is_confirmed or ID_VARIABLES[message.chat.id].add or ID_VARIABLES[message.chat.id].ADD_WORD or ID_VARIABLES[message.chat.id].search) and ID_VARIABLES[message.chat.id].DELETE_WORD:
        avantionary_bot.send_message(message.chat.id, "Invalid choice. Please try again.", reply_markup=make_confirmation_markup())


@avantionary_bot.message_handler(func=delete_confirmation)
def delete_word_confirmed(message):
    global ID_VARIABLES
    if (message.chat.id in ID_VARIABLES) and ID_VARIABLES[message.chat.id].DELETE_WORD:
        feedback = db.delete_from_dictionary(ID_VARIABLES[message.chat.id].to_delete)
        avantionary_bot.send_message(message.chat.id, feedback)
        ID_VARIABLES[message.chat.id].DELETE_WORD = False
    else:
        return

####################################################################################################################

def start_polling():
    """
    A function to allow external access to the bot. To be able to poll from another file
    """
    avantionary_bot.polling(none_stop=True)
