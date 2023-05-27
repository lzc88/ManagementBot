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
from datetime import datetime
import time

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
    semester = 0
else:
    semester = 1
ay = "2022-2023"

mods_basic_req = requests.get( mods_basic_end.replace( replace_ay, ay ) )
mods_basic = mods_basic_req.json() # List of dictionaries, each dictionary represents a module
modcodes = []
for i in mods_basic:
    modcodes.append( i["moduleCode"]) # List of all module codes

def add_lesson( lesson_no, mod_code, lesson_type): # Adding a particular lesson for a particular module to DB based on User's input
    userid = str(lesson_no.chat.id) # User's unique ID
    formtext = lesson_no.text.upper() # Lesson number in proper format
    mod_details_req = requests.get( mod_details_end.replace( replace_ay, ay ).replace( replace_mod, mod_code ) ) # Request to NUSMods API for module details
    mod_lesson_details = mod_details_req.json()["semesterData"][semester]['timetable'] # List of different lessons, each item is a dictionary representing a particular lesson
    for class_no in mod_lesson_details:
        if class_no["classNo"] == formtext:
            user_lesson = class_no
            db.collection( "users" ).document( userid ).collection( "mods" ).document( mod_code ).collection( "module_info" ).document( lesson_type ).set( user_lesson )
            bot.send_message( int(userid), "Ok, I have added " + lesson_type + ": " + formtext + "for " + mod_code + " to your School Timetable." )
            return None
    ### If User's input does not match any Lesson number ###
    bot.send_message( int(userid), "That is an invalid " + lesson_type + " number, please try again.")
    bot.register_next_step_handler( lesson_no, add_lesson, mod_code, lesson_type )

def config_timetable( text, mod_code, title ):
    userid = str(text.chat.id) # User's unique ID
    all_mods = db.collection( "users" ).document( userid ).collection( "mods" ).document( mod_code ).collection( "module_info" ).stream() # Returns documents whose ID are the different lesson types
    lesson_types = []
    for mod in all_mods: # lesson_types will be a list of User's lesson types at the end of For loop
        lesson_types.append( mod.id )
    markup = telebot.types.ReplyKeyboardMarkup( resize_keyboard = True, one_time_keyboard = True )
    for lesson_type in lesson_types:
        button = telebot.types.KeyboardButton( lesson_type )
        markup.add(button)
    bot.send_message( int(userid), "Which lesson type would you like to configure?", reply_markup = markup )
    bot.register_next_step_handler( text, config_timetable_2 )

def config_timetable_2( lesson_type ):
    lesson = lesson_type.chat.id
    bot.send_message( lesson_type.chat.id, "What is your slot numnber for " + lesson + "?" )
    bot.register_next_step_handler( lesson_type, add_lesson, )

#db.collection( "users" ).document( userid ).collection( "mods" ).document( "all_mods" ).update( {mod_code : [ title, True ]} )
#bot.send_message( int(userid), "Ok, all your lessons for " + mod_code + " have been set!" )

########## CALL BACK FUNCTION ##########
def yes_or_no( yn, mod_code, title ):
    formtext = yn.text.upper()
    if formtext == "YES":
        config_timetable( yn, mod_code, title )
########################################

@bot.message_handler( regexp = "School Timetable" )
def school_timetable( stt ):
    userid = str( stt.chat.id ) # User's unique ID
    doc_ref = db.collection( "users" ).document( userid ).collection( "mods" ).document( "all_mods" ) # Reference to check if User's mods are configured / If User has any modules
    doc = doc_ref.get().to_dict() # Dictionary containing all of User's mods, can be empty
    if len(doc) > 0: # If User has mods
        false_mods = ""
        false_mods_no = 0
        for mod_code in doc: # For each module User has, check if lessons for that module has been configured
            title = doc[mod_code][0]
            status = doc[mod_code][1]
            if not status: # If timetable for module is not yet configured
                false_mods += f'{mod_code}, {title} \n\n'
                false_mods_no += 1
        if false_mods_no != 0:
            bot.send_message( int(userid), "You have not indicated any lesson slots for:\n\n" + false_mods + "Would you like to indicate now? The lesson slot numbers are required." )
            bot.register_next_step_handler( stt, yes_or_no, mod_code, title )
        else:
            bot.send_message( int(userid), "Here is your school timetable!" )
    else: # If User has no mods
        bot.send_message( int(userid), "You currently do not have any modules, please procede to Add modules!" )

bot.infinity_polling()