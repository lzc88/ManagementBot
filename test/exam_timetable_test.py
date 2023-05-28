import os
import dotenv
import telebot
import telebot.types
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove
from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP #pip install python-telegram-bot-calendar
import firebase_admin
from firebase_admin import firestore
import datetime
import requests
import time
from datetime import datetime
import math

dotenv.load_dotenv( dotenv_path = "config\.env" )

bottoken = os.getenv("bottoken")
bot = telebot.TeleBot(bottoken)

cred = firebase_admin.credentials.Certificate("config\managementbot-72f56-firebase-adminsdk-7fs64-3c7bb1c603.json")
dbapp = firebase_admin.initialize_app( cred )
db = firestore.client()

replace_ay = "{acadYear}"
replace_mod = "{moduleCode}"
mods_basic_end = os.getenv( "allmods" )
mod_details_end = os.getenv( "moddetails" )

month_now = datetime.now().month
if month_now < 8:
    semester = 1
else:
    semester = 0
ay = "2022-2023"

if semester == 0:
    sem_start = datetime( 2022, 8, 8 )
    sem_end = datetime( 2022, 11, 18 )
else:
    sem_start = datetime( 2023, 1, 9 )
    sem_end = datetime( 2023, 4, 14 )

days = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]

test_date = datetime( 2023, 2, 3 )

mods_basic_req = requests.get( mods_basic_end.replace( replace_ay, ay ) )
mods_basic = mods_basic_req.json() # List of dictionaries, each dictionary represents a module
modcodes = []
for i in mods_basic:
    modcodes.append( i["moduleCode"]) # List of all module codes

@bot.message_handler( "Exam timetable" )
def exam_timetable( message ):
    