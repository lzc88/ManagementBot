import os
import dotenv
import telebot
import firebase_admin
from firebase_admin import firestore

dotenv.load_dotenv()

bottoken = os.getenv("bottoken")
bot = telebot.TeleBot(bottoken)

dbpath = os.getenv("dbpath")
cred = firebase_admin.credentials.Certificate("dbpath")
dbapp = firebase_admin.initialize_app( cred )
db = firestore.client()

@bot.message_handler( commands = ["start",] )
def start( text ):
    userid = str(text.chat.id)
    username = text.chat.first_name
    doc_ref = db.collection( "users" ).document( userid )
    doc = doc_ref.get()
    if doc.exists:
        markup = telebot.types.ReplyKeyboardMarkup( resize_keyboard = True, one_time_keyboard = True )
        button1 = telebot.types.KeyboardButton( "View timetable" )
        button2 = telebot.types.KeyboardButton( "View personal planner" )
        button3 = telebot.types.KeyboardButton( "View exam timetable" )
        button4 = telebot.types.KeyboardButton( "View modules" )
        markup.add( button1 ).add( button2 ).add( button3 ).add( button4 )
        bot.reply_to( text, "Hello " + username + ". What would you like to do?", reply_markup = markup )
    else:
        data = {}
        db.collection( "users" ).document( userid ).set( data )
        bot.reply_to( text, "Hello " + username +", I am ManagementBot. I hope I can assist you in better planning your scedule!" )
        bot.send_message( text.chat.id, "What modules are you taking this semester? (Please enter the module codes)" )

bot.infinity_polling()

