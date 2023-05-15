# _*_ coding: utf-8 _*_
import re, time, pytz
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, Filters
from telegram.chataction import ChatAction
from PIL import Image
from time import sleep
from datetime import time

updater = Updater(
    token="TOKEN", use_context=True)

a = 0

def start(update, context):
    global a
    context.bot.send_chat_action(update.message.chat_id, ChatAction.TYPING)
    if update.message.chat_id == 5074618670:
        if a == 0:
            context.job_queue.run_daily(alarm,time(hour=9, minute=00, tzinfo=pytz.timezone('Asia/Tehran')),days=(0, 1, 2, 3, 4, 5, 6),context=update.message.chat_id)
            context.job_queue.run_daily(alarm,time(hour=13, minute=00, tzinfo=pytz.timezone('Asia/Tehran')),days=(0, 1, 2, 3, 4, 5, 6),context=update.message.chat_id)
            context.job_queue.run_daily(alarm,time(hour=17, minute=00, tzinfo=pytz.timezone('Asia/Tehran')),days=(0, 1, 2, 3, 4, 5, 6),context=update.message.chat_id)
            context.bot.sendMessage(chat_id=update.message.chat_id,text='The robot started')
            a = 1
        else:
            context.bot.sendMessage(chat_id=update.message.chat_id,text='The robot is running')
    else:
        context.bot.sendMessage(chat_id=update.message.chat_id,text='Hello World !')

def alarm(context):
    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton(text='create now', url='https://carbon.now.sh')]])
    context.bot.sendMessage(chat_id=5074618670,text='✅   Alarm !',reply_markup=keyboard)

def text(update, context):
    world = ['fohsh', 'no']
    if update.message.text in world:
            context.bot.deleteMessage(message_id=update.message.message_id, chat_id=update.message.chat_id)

print('The robot started')
updater.dispatcher.add_handler(CommandHandler("start", start, pass_job_queue=True))
updater.dispatcher.add_handler(MessageHandler(Filters.text, text))
updater.start_polling()
updater.idle()