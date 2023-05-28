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

@bot.message_handler( regexp = "School Timetable" )
def school_timetable( message ):
    userid = str( message.chat.id ) # User's unique ID
    doc_ref = db.collection( "users" ).document( userid ).collection( "all_mods" ).document( "all_mods" ) # Reference to check if User's mods are configured / If User has any modules
    doc = doc_ref.get().to_dict() # Dictionary containing all of User's mods, can be empty
    if len(doc) > 0: # If User has mods
        bot.send_message( int(userid), "Please wait a moment...")
        docs = db.collection( "users" ).document( userid ).collection("mods").stream()
        unconfigured = ""
        unconfigured_list = []
        for doc in docs:
            docs2 = db.collection( "users" ).document( userid ).collection( "mods" ).document( doc.id ).collection( "lessons" ).stream()
            for doc2 in docs2:
                doc_ref = db.collection( "users" ).document( userid ).collection( "mods" ).document( doc.id ).collection( "lessons" ).document( doc2.id )
                config_status = doc_ref.get().to_dict()[ "config" ]
                if not config_status:
                    unconfigured += f'{doc2.id} \n\n'
                    unconfigured_list.append( doc2.id )
        if unconfigured == "":
            bot.send_message( int(userid), "Here is your school timetable!" )
        else:
            button1 = telebot.types.KeyboardButton( "Configure lessons" )
            button2 = telebot.types.KeyboardButton( "Ignore and procede to view school timetable" )
            button3 = telebot.types.KeyboardButton( "Return to Main" )
            markup = telebot.types.ReplyKeyboardMarkup( resize_keyboard = True, one_time_keyboard = True )
            markup.add( button1 ).add( button2 ).add( button3 )
            bot.send_message( int(userid), "You have not configured the timings for these lessons. Would you like to configure them now? The lesson slot numbers are required.\n\n" + unconfigured, reply_markup = markup )
            bot.register_next_step_handler( message, prompt_config_lesson, unconfigured_list )
    else: # If User has no mods
        button1 = telebot.types.KeyboardButton( "Add modules" )
        button2 = telebot.types.KeyboardButton( "Return to Main" )
        markup = telebot.types.ReplyKeyboardMarkup( resize_keyboard = True, one_time_keyboard = True )
        markup.add(button1).add(button2)
        bot.send_message( int(userid), "You currently do not have any modules, please procede to Add modules or Return to Main.",reply_markup = markup )

def prompt_config_lesson( message, unconfigured_list ):
    if message.text == "Configure lessons":
        markup = telebot.types.ReplyKeyboardMarkup( resize_keyboard = True, one_time_keyboard = True )
        for item in unconfigured_list:
            button = telebot.types.KeyboardButton( item )
            markup.add( button )
        bot.send_message( message.chat.id, "Which lesson would you like to configure?", reply_markup = markup )
        bot.register_next_step_handler( message, config_lesson1, unconfigured_list )
    else:
        bot.send_message( message.chat.id, "That is an invalid input." )
        school_timetable( message )

def config_lesson1( message, unconfigured_list ):
    lesson = message.text
    if lesson in unconfigured_list:
        bot.send_message( message.chat.id, f'What is your lesson slot number for {lesson}? \n\n For lesson slot numbers for odd/even lessons, please key in the full lesson slot number. For example: \n\n D23, E9 \n\n For all other lessons, please key in the numbers only. For example: \n\n LEC-1, SEC-09 will be 1 and 9 respectively.' )
        bot.register_next_step_handler( message, config_lesson2, lesson )
    else:
        bot.send_message( message.chat.id, "That is an invalid lesson.")
        school_timetable( message )

def config_lesson2( message, lesson ):
    userid = str(message.chat.id)
    lesson_list = lesson.split( maxsplit = 1 )
    mod_code, lesson_type = lesson_list[0], lesson_list[1]
    lesson_no = message.text.upper()
    all_lessons_req = requests.get( mod_details_end.replace( replace_ay, ay ).replace( replace_mod, mod_code ) ).json()
    all_lessons = all_lessons_req["semesterData"][semester]['timetable']
    for item in all_lessons:
        if item['classNo'] == lesson_no and item['lessonType'] == lesson_type:
            db.collection( "users" ).document( userid ).collection( "mods" ).document( mod_code ).collection( "lessons" ).document( lesson ).update( {"timings": firestore.ArrayUnion([item])})
            db.collection( "users" ).document( userid ).collection( "mods" ).document( mod_code ).collection( "lessons" ).document( lesson ).update( {"config" : True} )
    check_ref = db.collection( "users" ).document( userid ).collection( "mods" ).document( mod_code ).collection( "lessons" ).document( lesson ).get().to_dict()
    if check_ref["config"]:
        bot.send_message( int(userid), f'Your timing for {lesson} has been configured!')
        school_timetable( message )
    else:
        button1 = telebot.types.KeyboardButton("School Timetable")
        button2 = telebot.types.KeyboardButton( "Return to Main" )
        markup = telebot.types.ReplyKeyboardMarkup( resize_keyboard = True, one_time_keyboard = True )
        markup.add( button1 ).add( button2 )
        bot.send_message( int(userid), "Your lesson slot could not be found. Please return to School Timetable to try again. If error persists, kindly feedback this issue to us via the Main menu, thank you!", reply_markup = markup )

#################################################

def view_timetable( message ):
    userid = str(message.chat.id)
    diff = test_date - sem_start
    week = math.ceil( diff.days/7 )
    output = ""
    docs = db.collection( "users" ).document( userid ).collection( "mods" ).stream()
    for doc in docs:
        lessons = db.collection( "users" ).document( userid ).collection( "mods" ).document( doc.id ).collection( "module_info" ).stream()
        for lesson in lessons:
            timing = db.collection( "users" ).document( userid ).collection( "mods" ).document( doc.id ).collection( "module_info" ).document( lesson.id ).get().to_dict()
            for classes in timing["timings"]:
                if week in classes["weeks"]:
                    None


bot.infinity_polling()