from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters
from telegram.ext import CommandHandler, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from functools import wraps
import asyncio
import json

API_TOKEN = '1249709268:AAFGgSTiQt1Jv7qnvvyttdiirdIHFsnfF-c' #change the API key for your bot

updater = Updater(API_TOKEN, use_context=True)

############################ Limit access #########################################
List_of_users = [] # needs change to an extenal file

def allowed_users():
    fileObject = open("list.json", "r") #list of users that can use the bot 
    jsonContent = fileObject.read()
    Users_List = json.loads(jsonContent)
    #print(Users_List)

    for i in range(len(Users_List)):
        #print (Users_List[i]['name'])
        List_of_users.append(Users_List[i]['chatid'])
        #print (List_of_users)

allowed_users()

def restricted(func):
    @wraps(func)
    #async def wrapped(update, context, *args, **kwargs):
    def wrapped(update, context, *args, **kwargs):
        user_id = update.effective_user.id
        if user_id not in List_of_users:
            print(f"Unauthorized access denied for {user_id}.")
            return
        #return await func(update, context, *args, **kwargs)
        return func(update, context, *args, **kwargs)
    return wrapped

############################ Command definition #########################################

@restricted
def start(update, context):
    update.message.reply_text(
        "Hi, Welcome to my test Bot.Please write /help to see the commands available.")
    update.message.reply_text(main_menu_message(),reply_markup=main_menu_keyboard())
    userid1 = str(update.message.chat_id) #get chatid from the user
   # print (userid1)

def help(update: Update, context: CallbackContext):
    update.message.reply_text("""Available Commands :-
    /Completar - Terminar pedido
    /Salir - Salir sin terminar pedido""")
    
def Completar(update, context):
    update.message.reply_text("Terminar pedido")
    
def Salir(update, context):
    update.message.reply_text("Salir sin terminar pedido")

############################ Menu definition #########################################
def main_menu(update,context):
  query = update.callback_query
  query.answer()
  query.edit_message_text(
                        text=main_menu_message(),
                        reply_markup=main_menu_keyboard())

def first_menu(update,context):
  query = update.callback_query
  query.answer()
  query.edit_message_text(
                        text=first_menu_message(),
                        reply_markup=first_menu_keyboard())

def second_menu(update,context):
  query = update.callback_query
  query.answer()
  query.edit_message_text(
                        text=second_menu_message(),
                        reply_markup=second_menu_keyboard())

############################ Sub Menu definitions #########################################
def first_submenu(bot, update):
  pass

def second_submenu(bot, update):
  pass

############################ Keyboards #########################################
def main_menu_keyboard():
  keyboard = [[InlineKeyboardButton('Option 1 🍄', callback_data='m1')], #Change product name
              [InlineKeyboardButton('Option 2 🙍', callback_data='m2')]] #Change product name
  return InlineKeyboardMarkup(keyboard)

def first_menu_keyboard():
  keyboard = [[InlineKeyboardButton('Submenu 1-1 👋', callback_data='m1_1')], #Change product size/amount
              [InlineKeyboardButton('Submenu 1-2 🔥', callback_data='m1_2')], #Change product size/amount
              [InlineKeyboardButton('Main menu', callback_data='main')]]
  return InlineKeyboardMarkup(keyboard)

def second_menu_keyboard():
  keyboard = [[InlineKeyboardButton('Submenu 2-1 🌌', callback_data='m2_1')], #Change product size/amount
              [InlineKeyboardButton('Submenu 2-2 🌈', callback_data='m2_2')], #Change product size/amount
              [InlineKeyboardButton('Main menu', callback_data='main')]]
  return InlineKeyboardMarkup(keyboard)

##If it's a long list, so you migth create a recursive functions to create menus

############################# Messages #########################################
def main_menu_message():
  return 'Choose the option in main menu:'

def first_menu_message():
  return 'Choose the submenu in first menu:'

def second_menu_message():
  return 'Choose the submenu in second menu:'

############################# Handle Commands #########################################

updater.dispatcher.add_handler(CommandHandler('Iniciar', start))
updater.dispatcher.add_handler(CommandHandler('help', help))
updater.dispatcher.add_handler(CommandHandler('Completar', Completar))
updater.dispatcher.add_handler(CommandHandler('Salir', Salir))

############################# Handle Menus #########################################
updater.dispatcher.add_handler(CallbackQueryHandler(main_menu, pattern='main'))
updater.dispatcher.add_handler(CallbackQueryHandler(first_menu, pattern='m1'))
updater.dispatcher.add_handler(CallbackQueryHandler(second_menu, pattern='m2'))
updater.dispatcher.add_handler(CallbackQueryHandler(second_menu, pattern='m2'))
updater.dispatcher.add_handler(CallbackQueryHandler(first_submenu,pattern='m1_1'))
updater.dispatcher.add_handler(CallbackQueryHandler(second_submenu,pattern='m2_1'))

############################# Handle errors #########################################
def unknown(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Sorry '%s' is not a valid command" % update.message.text)

def unknown_text(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Sorry I can't recognize you , you said '%s'" % update.message.text)


updater.start_polling()
