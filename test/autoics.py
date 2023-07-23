import os
import dotenv
import telebot
import telebot.types
import firebase_admin
from firebase_admin import firestore
import datetime
import requests
from datetime import datetime
from datetime import timedelta

########## LOAD VARIABLES FROM .env ##########
dotenv.load_dotenv( dotenv_path = ".env" )

########## CREATING BOT INSTANCE ##########
bottoken = "6250045869:AAFzbpqRpxTfehyMOK5RHPgheiLLzBruAfk"
bot = telebot.TeleBot(bottoken)

########## INITIALISE DB ##########
""" cred = firebase_admin.credentials.Certificate("managementbot-72f56-firebase-adminsdk-7fs64-3c7bb1c603.json") """
cred = firebase_admin.credentials.Certificate("config\managementbot-72f56-firebase-adminsdk-7fs64-3c7bb1c603.json")
dbapp = firebase_admin.initialize_app( cred )
db = firestore.client()

month_now = (datetime.now() + timedelta(hours=8)).month
### SEMESTER ###
if month_now < 6:
    semester = 1
else:
    semester = 0
ay = "2023-2024"

replace_ay = "{acadYear}"
replace_mod = "{moduleCode}"
mods_basic_end = 'https://api.nusmods.com/v2/{acadYear}/moduleList.json'
mod_details_end = 'https://api.nusmods.com/v2/{acadYear}/modules/{moduleCode}.json'

def ics_configure_lessons_bychao( userid ):
    ics_timetable = db.collection( "users" ).document( userid ).collection( "nus_mods" ).document( "class_data" ).get().to_dict()
    manual_mods = db.collection( "users" ).document( userid ).collection( "all_mods" ).document( "all_mods" ).get().to_dict()
    for mod_lesson in ics_timetable:
        mod_code = mod_lesson.split( maxsplit = 1 )[0]
        if mod_code not in manual_mods:
            continue
        else:
            slot = ics_timetable[mod_lesson]["number"]
            mod_lesson = mod_lesson.split( maxsplit = 1 )[1][:-1]
            all_lessons_req = requests.get( mod_details_end.replace( replace_ay, ay ).replace( replace_mod, mod_code ) ).json()
            all_lessons = all_lessons_req["semesterData"][semester]['timetable'] # Retrieve all lesson slots of a module for the current semester
            for item in all_lessons: # For each lesson slot
                if item['classNo'] == slot and item['lessonType'] == mod_lesson: # To filter the lesson slot that corresponds to User's input
                    db.collection( "users" ).document( userid ).collection( "mods" ).document( mod_code ).collection( "lessons" ).document( f'{mod_code} {mod_lesson}' ).update( {"timings": firestore.ArrayUnion([item])})
                    db.collection( "users" ).document( userid ).collection( "mods" ).document( mod_code ).collection( "lessons" ).document( f'{mod_code} {mod_lesson}' ).update( {"config" : True} )
