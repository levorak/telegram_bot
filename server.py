import telegram
from telegram.ext.updater import Updater
from telegram.ext.callbackcontext import CallbackContext
from telegram.update import Update
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters
from telegram.ext import CommandHandler, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from functools import wraps
import asyncio
import json
import csv
import numpy as np

############################ Initialize bot and updater #########################################
API_TOKEN = '' #change the API key for your bot
updater = Updater(API_TOKEN, use_context=True)
dispatcher = updater.dispatcher

############################ Initialize  global variables #########################################
sub_options = [
    [
        ["💐Bouquet", "🪷Flowers - Bouquet added to the order"],
        ["🎍Basket", "🪷Flowers - Basket added to the order"]
    ],
    [
        ["🌱Seeds", "🌿Herbs - Seeds added to the order"],
        ["🪴Potted", "🌿Herbs - Potted added to the order"]
    ]
]

order = []
List_of_users = []
clear_message ="Order cleared"

############################ Limit access #########################################

def allowed_users():
    fileObject = open("list.json", "r") #list of users that can use the bot
    jsonContent = fileObject.read()
    Users_List = json.loads(jsonContent)

    for i in range(len(Users_List)):
        List_of_users.append(Users_List[i]['chatid'])

allowed_users()

def restricted(func):
    @wraps(func)
    def wrapped(update, context, *args, **kwargs):
        user_id = update.effective_user.id
        if user_id not in List_of_users:
            print(f"Unauthorized access denied for {user_id}.")
            return
        #return await func(update, context, *args, **kwargs)
        return func(update, context, *args, **kwargs)
    return wrapped
@restricted

############################ Command definition #########################################

def start(update, context):
    reply_markup = main_menu_keyboard()
    message = context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome! Please select a category from the menu below, or type /help", reply_markup=reply_markup)
    context.user_data['messages'] = [message.message_id]

def confirm(update, context):
    message = "Current order: "
    for o in order:
        message += o + " "
    update.message.reply_text(message) # comment this if you dont want to keep the order on the chat
    order.append(str(update.effective_user.id ))
    save_to_csv(order)
    global clear_message
    clear_message= 'Thanks, bye'
    clear(update, context)

def clear(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,text=clear_message)
    context.bot.delete_message(chat_id=update.message.chat_id, message_id=context.user_data['messages'][-1])
    context.bot.delete_message(chat_id=update.message.chat_id, message_id=context.user_data['messages'][-2])

def help(update, context):
    message = "List of available commands: \n"
    message += "/start - Welcome message with options \n"
    message += "/confirm - Confirm and send order \n"
    message += "/clear - Clear order \n"
    message += "/help - List of available commands"
    update.message.reply_text(message)

############################ Menu definition #########################################

def main_menu_keyboard():
    keyboard = [[InlineKeyboardButton("Flowers", callback_data='1'),
                 InlineKeyboardButton("Herbs", callback_data='2')]]
    return InlineKeyboardMarkup(keyboard)

def main_menu(update, context):
  query = update.callback_query
  query.answer()
  query.edit_message_text(
                        text="Please select a product or type /help",
                        reply_markup=main_menu_keyboard())

def sub_menu(update, context, sub_menu_num):
    query = update.callback_query
    keyboard = []
    query = update.callback_query
    for i in range(len(sub_options[sub_menu_num])):
        keyboard.append([InlineKeyboardButton(sub_options[sub_menu_num][i][0], callback_data=f'{sub_menu_num+1}-{i+1}')])
    keyboard.append([InlineKeyboardButton("Return to main menu", callback_data='main')])
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(text="Please select a product, the type /confirm to send your order or /clear to restart", reply_markup=reply_markup)

############################ Handle menu options #########################################

def button(update, context):
    query = update.callback_query
    if query.data == '1':
#        context.user_data['messages'].append(message.message_id)
        sub_menu(update,context, 0)
    elif query.data == '2':
#        context.user_data['messages'].append(message.message_id)
        sub_menu(update,context, 1)
    elif query.data == "main":
#        context.user_data['messages'].append(message.message_id)
        main_menu(update,context)    
    else:
        #context.user_data['messages'].append(context.message.message_id)
        sub_menu_num,sub_option_num = [int(x) for x in query.data.split("-")]
        query.answer(sub_options[sub_menu_num-1][sub_option_num-1][1])
        order.append(sub_options[sub_menu_num-1][sub_option_num-1][0])

############################# Handle Commands #########################################
        
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

confirm_handler = CommandHandler('confirm', confirm)
dispatcher.add_handler(confirm_handler)

help_handler = CommandHandler('help', help)
dispatcher.add_handler(help_handler)

clear_handler = CommandHandler('clear', clear)
dispatcher.add_handler(clear_handler)

dispatcher.add_handler(CallbackQueryHandler(main_menu, pattern='main'))

callback_handler = CallbackQueryHandler(button)
dispatcher.add_handler(callback_handler)

############################# Start the bot #########################################
updater.start_polling()

############################# Save to csv #########################################
def save_to_csv(options):
    with open("sample.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["New order"])
        for option in options:
            writer.writerow([option])