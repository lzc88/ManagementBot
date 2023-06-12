import os
import dotenv
import telebot
import telebot.types
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove
from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP
import firebase_admin
from firebase_admin import firestore
import datetime
import requests
from datetime import datetime
from datetime import timedelta
import time
import icalendar
import re
import threading
import pytz
import math

########## LOAD VARIABLES FROM .env ##########
dotenv.load_dotenv( dotenv_path = "config\.env" )

########## CREATING BOT INSTANCE ##########
""" bottoken = os.getenv("bottoken") """
bottoken = "6250045869:AAFzbpqRpxTfehyMOK5RHPgheiLLzBruAfk"
bot = telebot.TeleBot(bottoken)

########## INITIALISE DB ##########
cred = firebase_admin.credentials.Certificate("config\managementbot-72f56-firebase-adminsdk-7fs64-3c7bb1c603.json")
dbapp = firebase_admin.initialize_app( cred )
db = firestore.client()

########## Get all user_id ###############
def get_all_user_ids():
    user_ids = []

    # Query the database to retrieve all user documents
    users_collection = db.collection("users")
    user_docs = users_collection.get()

    # Extract user IDs from the documents
    for doc in user_docs:
        user_id = doc.id
        user_ids.append(user_id)

    return user_ids


########## ADMIN USER ID ########## **********Try to store this in the .env file so people won't see them
approved_admins = ["966269150","291900788"]  

########## NUSMOD API ENDPOINTS ##########
replace_ay = "{acadYear}"
replace_mod = "{moduleCode}"
mods_basic_end = os.getenv( "allmods" )
mod_details_end = os.getenv( "moddetails" )

########## TEST DATES AY 22/23 ##########
month_now = datetime.now().month
### SEMESTER ###
if month_now < 8:
    semester = 1
else:
    semester = 0
ay = "2022-2023"
### SEM START/END ###
if semester == 0:
    sem_start = datetime( 2022, 8, 8 )
    sem_end = datetime( 2022, 12, 3 )
else:
    sem_start = datetime( 2023, 1, 9 )
    sem_end = datetime( 2023, 5, 6 )
### RECESS WEEK START/END ###
if semester == 0:
    recess_start = datetime( 2022, 9, 17 )
    recess_end = datetime( 2022, 9, 25 )
else:
    recess_start = datetime( 2023, 2, 18 )
    recess_end = datetime( 2023, 2, 26 )
### READING WEEK START/END ###
if semester == 0:
    read_start = datetime( 2022, 11, 12 )
    read_end = datetime( 2022, 11, 18 )
else:
    read_start = datetime( 2023, 4, 15 )
    read_end = datetime( 2023, 4, 21 )

days = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]

############ To store user data ############
def get_user_data(user_id):
    user_ref = db.collection("users").document(user_id)
    user_doc = user_ref.get()

    if user_doc.exists:
        return user_doc.to_dict()
    else:
        return {}
    
def update_user_data(user_id, data):
    user_ref = db.collection("users").document(user_id)
    user_ref.set(data, merge=True)


    
########## GENERATE A LIST OF MODULE CODES ##########
mods_basic_req = requests.get( mods_basic_end.replace( replace_ay, ay ) )
mods_basic = mods_basic_req.json() # List of dictionaries, each dictionary represents a module
modcodes = []
for i in mods_basic:
    modcodes.append( i["moduleCode"]) # List of all module codes

####################################################################################################

########## FUNCTION TO DIRECT USER BASED ON OPTION SELECTED ##########
def choice( text, userid ):
    option = text.text
    if option == "View Modules":
        view_modules( text, userid )
    elif option == "Exam Timetable":
        view_exams( text, userid )
    elif option == "School Timetable":
        school_timetable( text, userid )
    elif option == "Assignments Deadlines":
        assignments_deadline( text, userid )
    elif option == "Personal Planner":
        personal_planner( text )
    elif option == "Report Issues":
        report_issues( text )
        
### Add for your functions here ###

########### FUNCTN TO GREET USER ##########      
def get_greeting(current_time):
    if current_time.hour < 12:
        return "Good morning"
    elif current_time.hour < 18:
        return "Good afternoon"
    else:
        return "Good evening"

########## MAIN MENU FUNCTION ##########
@bot.message_handler( regexp = "Return to Main" )
def main( text ):
    userid = str( text.chat.id )
    markup = telebot.types.ReplyKeyboardMarkup( resize_keyboard = True, one_time_keyboard = True )
    button1 = telebot.types.KeyboardButton( "Assignments Deadlines" )
    button2 = telebot.types.KeyboardButton( "Personal Planner" )
    button3 = telebot.types.KeyboardButton( "School Timetable" )
    button4 = telebot.types.KeyboardButton( "Exam Timetable" )
    button5 = telebot.types.KeyboardButton( "View Modules" )
    button6 = telebot.types.KeyboardButton( "Report Issues" )
    markup.add( button1 ).add( button2 ).add( button3 ).add( button4 ).add( button5 ).add( button6 )
    user_time = datetime.now().time()
    greeting = get_greeting(user_time)
    reply_text = f"{greeting} {text.chat.first_name}. What would you like to do?\n"
    reply_text += "Please select the corresponding buttons.\n\n"
    reply_text += "1) Assignments Deadlines\n"
    reply_text += "2) Personal Planner\n"
    reply_text += "3) School Timetable\n"
    reply_text += "4) Exam Timetable\n"
    reply_text += "5) View Modules\n"
    reply_text += "6) Report Issues"
    bot.send_message( int( userid ) , reply_text , reply_markup = markup )
    bot.register_next_step_handler( text, choice, userid )

########## START COMMAND (NEW USERS) ##########
@bot.message_handler( commands = ["start"] ) # Handle /start command
def start( startmessage ):
    userid = str(startmessage.chat.id) # Obtain unique chat ID
    username = startmessage.chat.first_name # Obtain user's first name
    doc_ref = db.collection( "users" ).document( userid ) # Reference to check if User exists in DB
    doc = doc_ref.get()
    if doc.exists: # True if User exists
        main(startmessage)
        check_deadline_reminders(userid)
        #check_pp_reminders(userid) #Implementing this next
    else: # If User is new
        data = { "username" : username } # Dictionary containing user's first name
        db.collection( "users" ).document( userid ).set( data ) # Create document for user with "data" as field
        db.collection( "users" ).document( userid ).collection( "all_mods" ).document( "all_mods" ).set({}) # Create all_mods document for User to be used later when adding/deleting modules
        db.collection( "users" ).document( userid ).collection( "timetable" ).document( "this_week" ).set({}) # Create this_week document for User to be used later to view timetable
        db.collection( "users" ).document( userid ).collection( "exam" ).document( "timings" ).set({}) # Create timings document for User to be used later to add exam timings
        response = "Hello " + username +", I am ManagementBot. I hope to assist you in better planning your schedule! \n"
        response += "You can choose what you want to do by opening the keyboard buttons and selecting the relevant options."
        check_deadline_reminders(userid)
        bot.send_message( int(userid), response )
        bot.send_message( int(userid), "Before we begin, what modules are you taking this semester?\n\n( Type and send module codes one at a time. Do wait for me to respond before sending another code! )" )
        go_to_addmodule( startmessage, userid )

###################################################################################################################################

# FUNCTION (1) Assignments Deadlines

########## HELPER FUNCTION FOR GETTING DL ##########    
def get_dl( userid ):
    user_doc = db.collection("users").document( userid )
    dl_data = []
    ics_data_doc = db.collection("users").document(userid).collection("CC_data").document("ics_data").get() # Retrieve .ics data from database
    if ics_data_doc.exists: # If .ics data exists
        ics_data = ics_data_doc.to_dict().get("data", [])

        for i, assignment in enumerate(ics_data, start=1):
            due_date_timestamp = assignment['due_date'].timestamp()
            due_date = datetime.fromtimestamp(due_date_timestamp)

            formatted_due_date = due_date.strftime("%A, %d/%m/%y %H%Mhrs")

            dl_data.append({
                'id': i,  # Assign a unique ID to each assignment
                'title': assignment['title'],
                'due_date': formatted_due_date,
                'status': assignment['status']
            })

    manually_typed_dl_docs = user_doc.collection("dl_data").stream() # Retrieve manually typed deadline data from database

    for i, doc in enumerate(manually_typed_dl_docs, start=len(dl_data)+1):
        dl = doc.to_dict()
        dl_data.append({
            'id': i,
            'title': dl['title'],
            'due_date': dl['due_date'].strftime("%A, %d/%m/%y %H%Mhrs"),
            'status': dl['status']
        })

    return dl_data

def check_deadline_reminders(user_id):
    last_reminder_timestamps = {}  # Dictionary to store the last reminder timestamp for each assignment

    while True:
        # Retrieve deadlines for the specific user
        deadlines = get_dl(user_id)

        # Check each deadline and send reminders if necessary
        for deadline in deadlines:
            if deadline['status'] == 'COMPLETED':
                continue  # Skip completed assignments

            title = deadline['title']
            due_date = datetime.strptime(deadline['due_date'], "%A, %d/%m/%y %H%Mhrs")
            current_date = datetime.now()
            time_remaining = due_date - current_date

            if time_remaining.total_seconds() <= 0:
                # Deadline has passed, send reminder if not already sent
                if title not in last_reminder_timestamps or last_reminder_timestamps[title] != 'due':
                    # Compose the reminder message
                    reminder_message = f"Your assignment '{title}' is due. (Due date: {due_date})."
                    bot.send_message(user_id, reminder_message)
                    last_reminder_timestamps[title] = 'due'

            elif time_remaining.total_seconds() <= 3600 and time_remaining.total_seconds() > 0:
                # Send reminder if not already sent at this interval
                if title not in last_reminder_timestamps or last_reminder_timestamps[title] != '1_hour':
                    reminder_message = f"Your assignment '{title}' will be due in 1 hour. (Due date: {due_date}). Don't forget to submit it!"
                    bot.send_message(user_id, reminder_message)
                    last_reminder_timestamps[title] = '1_hour'

            elif time_remaining.total_seconds() <= 6 * 3600 and time_remaining.total_seconds() > 0:
                # Send reminder if not already sent at this interval
                if title not in last_reminder_timestamps or last_reminder_timestamps[title] != '6_hours':
                    reminder_message = f"Your assignment '{title}' will be due in 6 hours. (Due date: {due_date}). Don't forget to finalize and submit your work!"
                    bot.send_message(user_id, reminder_message)
                    last_reminder_timestamps[title] = '6_hours'

            elif time_remaining.total_seconds() <= 24 * 3600 and time_remaining.total_seconds() > 0:
                # Send reminder if not already sent at this interval
                if title not in last_reminder_timestamps or last_reminder_timestamps[title] != '24_hours':
                    reminder_message = f"Your assignment '{title}' will be due in 24 hours. (Due date: {due_date}). Do begin on it if you haven't!"
                    bot.send_message(user_id, reminder_message)
                    last_reminder_timestamps[title] = '24_hours'

            elif time_remaining.total_seconds() <= 24 * 3600 * 3 and time_remaining.total_seconds() > 0:
                # Send reminder if not already sent at this interval
                if title not in last_reminder_timestamps or last_reminder_timestamps[title] != '3_days':
                    reminder_message = f"Your assignment '{title}' will be due in 3 days. (Due date: {due_date}). Do begin on it if you haven't!"
                    bot.send_message(user_id, reminder_message)
                    last_reminder_timestamps[title] = '3_days'

        # Wait for 1 minute before checking deadlines again
        time.sleep(60)
    
########## MAIN FUNCTION FOR ASSIGNMENT DEADLINES ##########
def assignments_deadline( message, userid ):
    user_data = get_user_data( userid )
    deadlines = get_dl( userid )

    if deadlines:
        page_size = 8  # Number of assignments per page

        current_page = user_data.get("current_page", 1) # Retrieve the current page from user data (default to the first page)

        start_index = (current_page - 1) * page_size # Calculate the start index for current page
        end_index = start_index + page_size # Calculate the end index for current page

        assignments_to_delete = [] # List to store titles of expired assignments to be deleted

        for assignment in deadlines: # Iterate through deadlines and check for assignments to be deleted
            due_date = datetime.strptime(assignment['due_date'], "%A, %d/%m/%y %H%Mhrs")
            current_date = datetime.now()
            time_remaining = due_date - current_date

            if time_remaining.total_seconds() <= 0 and time_remaining.total_seconds() <= -24 * 3600: # If the assignment is past due and due for more than 24 hours
                assignments_to_delete.append(assignment['title'])

        for title in assignments_to_delete: # Process the deletion of assignments
            auto_delete_assignment( userid, title )

        deadlines = get_dl( userid ) # Retrieve the updated deadlines after deletion

        sorted_deadlines = sorted(deadlines, key=lambda x: (x['status'] == 'COMPLETED', datetime.strptime(x['due_date'], "%A, %d/%m/%y %H%Mhrs"))) # Sort deadlines by due date

        current_assignments = sorted_deadlines[start_index:end_index] # Retrieve the assignments for the current page

        # Generate the response message for the current page
        response = "These are your current deadlines:\n\n"
        for index, assignment in enumerate(current_assignments, start=start_index + 1):
            due_date = datetime.strptime(assignment['due_date'], "%A, %d/%m/%y %H%Mhrs")
            current_date = datetime.now()
            time_remaining = due_date - current_date

            # Check if the assignment is past due
            if time_remaining.total_seconds() <= 0:
                # Check if the assignment is due (not completed)
                if assignment['status'] != 'COMPLETED':
                    # Check if the assignment is overdue by more than 24 hours
                    if time_remaining.total_seconds() <= -24 * 3600:
                        # Delete the assignment from cc_data and dl_data
                        auto_delete_assignment(user_id, assignment['title'])
                        continue  # Skip deleted assignment

                time_left = "This Assignment is Due"
            else:
                days_remaining = time_remaining.days
                hours_remaining = time_remaining.seconds // 3600

                if days_remaining > 0:
                    time_left = f"{days_remaining} days and {hours_remaining} hours left."
                elif hours_remaining > 0:
                    time_left = f"{hours_remaining} hours left."
                elif time_remaining.total_seconds() > 0:
                    time_left = "You have less than an hour left!"
                else:
                    time_left = "This Assignment is Due"

            day_of_week = due_date.strftime("%A")
            assignment_info = f"{index}) {assignment['title']}:\nDue date: {day_of_week}, {due_date.strftime('%d/%m/%y %H%Mhrs')}\nTime left: {time_left}\nStatus: {assignment['status']}\n\n"
            response += assignment_info


        # Create keyboard markup for pagination
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        if current_page > 1 and end_index < len(deadlines):
            response += "Please click on the 'Next' button to view more deadlines and 'Previous' button to return to the previous page"
            previous_button = telebot.types.KeyboardButton("Previous")
            next_button = telebot.types.KeyboardButton("Next")
            markup.row(previous_button, next_button)
        elif current_page > 1:
            response += " Please click on the 'Previous' button to return to the previous page."
            previous_button = telebot.types.KeyboardButton("Previous")
            markup.row(previous_button)
        elif end_index < len(deadlines):
            response += " Please click on the 'Next' button to view more deadlines."
            next_button = telebot.types.KeyboardButton("Next")
            markup.row(next_button)

        complete_button = telebot.types.KeyboardButton("Mark Assignments as complete")
        uncomplete_button = telebot.types.KeyboardButton("Mark Assignments as not completed")
        manage_deadlines_button = telebot.types.KeyboardButton("Manage Deadlines Data")
        add_cal_button = telebot.types.KeyboardButton("Manage Calendar Data")
        return_button = telebot.types.KeyboardButton("Return to Main")
        markup.row(complete_button)
        markup.row(uncomplete_button)
        markup.row(manage_deadlines_button)
        markup.row(add_cal_button)
        markup.row(return_button)

        bot.send_message(message.chat.id, response, reply_markup=markup, parse_mode="HTML")

        # Update user data with the current page
        update_user_data(userid, {"current_page": current_page})

    else:
        response = "Your deadlines list is empty. Please add in deadlines to use this function.\n\n"
        response += "Please click on 'Manage Calendar Data' to import in Canvas Calendar data. You may also click on 'Manage Deadlines Data' to manually add in your own deadlines."
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        complete_button = telebot.types.KeyboardButton("Mark Assignments as complete")
        uncomplete_button = telebot.types.KeyboardButton("Mark Assignments as not completed")
        manage_deadlines_button = telebot.types.KeyboardButton("Manage Deadlines Data")
        add_cal_button = telebot.types.KeyboardButton("Manage Calendar Data")
        return_button = telebot.types.KeyboardButton("Return to Main")
        markup.row(complete_button)
        markup.row(uncomplete_button)
        markup.row(manage_deadlines_button)
        markup.row(add_cal_button)
        markup.row(return_button)
        bot.send_message(message.chat.id, response, reply_markup=markup)
        
# To view next page of deadlines (if len > 8)
@bot.message_handler(func=lambda message: message.text == "Next")
def handle_next_button(message):
    user_id = str(message.from_user.id)
    user_data = get_user_data(user_id)
    current_page = user_data.get("current_page", 1)
    user_data["current_page"] = current_page + 1
    update_user_data(user_id, user_data)
    assignments_deadline(message)

@bot.message_handler(func=lambda message: message.text == "Previous")
def handle_previous_button(message):
    user_id = str(message.from_user.id)
    user_data = get_user_data(user_id)
    current_page = user_data.get("current_page", 1)
    user_data["current_page"] = current_page - 1
    update_user_data(user_id, user_data)
    assignments_deadline(message)
        
@bot.message_handler(regexp="Manage Deadlines Data")
def manage_deadlines_data(message):
    # Display the options for managing deadlines
    response = "Please select an option to manage deadlines:\n"
    response += "1) Add Deadline\n"
    response += "2) Delete Deadline\n"
    response += "3) Return to Assignment deadlines"

    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    add_deadline_button = telebot.types.KeyboardButton("Add Deadline")
    delete_deadline_button = telebot.types.KeyboardButton("Delete Deadline")
    return_button = telebot.types.KeyboardButton("Return to Assignment deadlines")
    markup.row(add_deadline_button)
    markup.row(delete_deadline_button)
    markup.row(return_button)

    bot.send_message(message.chat.id, response, reply_markup=markup)


@bot.message_handler(func=lambda message: message.text.lower() == "return to assignment deadlines")
def handle_back_adl(message):
    assignments_deadline(message)     

@bot.message_handler(regexp="Add Deadline")        
def add_dl(message):
    markup = telebot.types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id, "Please enter the deadline name.", reply_markup=markup)
    bot.register_next_step_handler(message, add_dl_name)

def add_dl_name(message):
    dl_name = message.text
    response = "Please enter the deadline date and time in 24H format (e.g. DD/MM HHMM)\n\n"
    bot.send_message(message.chat.id, response)
    bot.register_next_step_handler(message, add_dl_datetime, dl_name)

def add_dl_datetime(message, dl_name):
    dl_datetime = message.text.replace(":", "")  # Remove the colon from the time format

    try:
        # Try parsing as "DD/MM/YYYY HHMM" format
        dl_time = datetime.strptime(dl_datetime, "%d/%m/%Y %H%M")
        current_time = datetime.now()

        if dl_time < current_time:
            # The entered time is in the past
            bot.send_message(message.chat.id, "You need to enter a future date and time.")
            # Prompt the user again to enter a valid time
            bot.register_next_step_handler(message, lambda msg: add_dl_datetime(msg, dl_name))
        else:
            # The entered time is valid
            save_dl_details(message, dl_name, dl_time)

    except ValueError:
        try:
            # Try parsing as "DD/MM HHMM" format
            dl_date, dl_time = dl_datetime.split(" ")
            current_year = datetime.now().year

            dl_time_full = f"{dl_date}/{current_year} {dl_time}"
            dl_time_full = datetime.strptime(dl_time_full, "%d/%m/%Y %H%M")

            if dl_time_full < datetime.now():
                # The entered time is in the past
                bot.send_message(message.chat.id, "You need to enter a future date and time.")
                # Prompt the user again to enter a valid time
                bot.register_next_step_handler(message, lambda msg: add_dl_datetime(msg, dl_name))
            else:
                # The entered time is valid
                save_dl_details(message, dl_name, dl_time_full)

        except ValueError:
            # The entered time format is invalid
            response = "Invalid date and time format. Please enter the date and time in 24H format.\n"
            response += "e.g., for 5 May 11pm, please type 05/05 2300\n"
            bot.send_message(message.chat.id, response)
            # Prompt the user again to enter a valid time
            bot.register_next_step_handler(message, lambda msg: add_dl_datetime(msg, dl_name))   
        
def save_dl_details(message, dl_name, dl_datetime):
    user_id = message.from_user.id
    dl_ref = db.collection('users').document(str(user_id)).collection('dl_data').document()
    dl_ref.set({
        'title': dl_name,
        'due_date': dl_datetime,
        'status': "NOT COMPLETED"
    })

    bot.send_message(user_id, "Deadline added to your Assignment Deadlines!")
    assignments_deadline(message)

def auto_delete_assignment(user_id,title):
    deadline_title = title
    found = False

    user_doc = db.collection("users").document(user_id)
    dl_data_col = user_doc.collection("dl_data")

    # Search for the deadline with the given title in dl_data collection
    dl_data_query = dl_data_col.where("title", "==", deadline_title).limit(1).stream()

    for doc in dl_data_query:
        doc.reference.delete()
        response = f"The deadline '{doc.get('title')}' has been deleted."
        found = True
        break

    if not found:
        cc_data_doc = user_doc.collection("CC_data").document("ics_data")
        cc_data_snapshot = cc_data_doc.get()

        if cc_data_snapshot.exists:
            cc_data = cc_data_snapshot.to_dict().get("data", [])

            # Search for the deadline with the given title in cc_data list
            for deadline in cc_data:
                if deadline.get('title') == deadline_title:
                    cc_data.remove(deadline)
                    found = True
                    break

            # Update the deadline data in Firestore
            cc_data_doc.set({"data": cc_data}, merge=True)
    


#To delete deadlines        
@bot.message_handler(regexp="Delete Deadline")
def delete_deadline(message):
    user_id = str(message.from_user.id)
    deadlines = get_dl(user_id)

    if deadlines:
        response = "Please select the deadline you want to delete:\n"
        sorted_deadlines = sorted(deadlines, key=lambda x: datetime.strptime(x['due_date'], "%A, %d/%m/%y %H%Mhrs"))
        for i, deadline in enumerate(sorted_deadlines, start=1):
            response += f"{i}) {deadline['title']} - {deadline['due_date']}\n"
        
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        for deadline in sorted_deadlines:
            keyboard.add(KeyboardButton(deadline['title']))
        keyboard.add(KeyboardButton('back'))
        response += "\n\nIf you wish to delete All deadlines (INCLUDES CALENDAR DATA), please manually type 'delete_all_deadlines' "
        bot.send_message(message.chat.id, response, reply_markup=keyboard)
        bot.register_next_step_handler(message, process_delete)
    else:
        response = "You have no deadlines to delete."
        bot.reply_to(message, response)
        assignments_deadline(message)
        


def delete_all_deadlines(message):
    user_id = str(message.from_user.id)

    # Delete all deadlines from dl_data
    user_doc = db.collection("users").document(user_id)
    dl_data_collection = user_doc.collection("dl_data")

    # Get all documents in dl_data collection
    dl_data_docs = dl_data_collection.get()

    for doc in dl_data_docs:
        doc.reference.delete()

    # Delete ics_data document
    ics_data_doc = user_doc.collection("CC_data").document("ics_data")
    ics_data_doc.delete()

    response = "All deadlines have been deleted."
    bot.reply_to(message, response)

    # Reset the current page to 1
    user_data = get_user_data(user_id)
    user_data["current_page"] = 1
    update_user_data(user_id, user_data)

    assignments_deadline(message)


def process_delete(message):
    user_id = str(message.from_user.id)
    text = message.text

    if text == 'back':
        assignments_deadline(message)
    elif text.lower() == 'delete_all_deadlines':
        delete_all_deadlines(message)
    else:
        deadline_title = text
        found = False

        user_doc = db.collection("users").document(user_id)
        dl_data_col = user_doc.collection("dl_data")

        # Search for the deadline with the given title in dl_data collection
        dl_data_query = dl_data_col.where("title", "==", deadline_title).limit(1).stream()

        for doc in dl_data_query:
            doc.reference.delete()
            response = f"The deadline '{doc.get('title')}' has been deleted."
            found = True
            break

        if not found:
            cc_data_doc = user_doc.collection("CC_data").document("ics_data")
            cc_data_snapshot = cc_data_doc.get()

            if cc_data_snapshot.exists:
                cc_data = cc_data_snapshot.to_dict().get("data", [])

                # Search for the deadline with the given title in cc_data list
                for deadline in cc_data:
                    if deadline.get('title') == deadline_title:
                        cc_data.remove(deadline)
                        response = f"The deadline '{deadline['title']}' has been deleted."
                        found = True
                        break

                # Update the deadline data in Firestore
                cc_data_doc.set({"data": cc_data}, merge=True)

        if not found:
            response = f"Failed to find the deadline with title '{deadline_title}'. Please try again."

        bot.reply_to(message, response)
        assignments_deadline(message)
   
        
# To allow users to mark as completion
@bot.message_handler(regexp="Mark Assignments as complete")
def mark_completed(message):
    user_id = str(message.from_user.id)
    deadlines = get_dl(user_id)

    if deadlines:
        response = "Please select the assignment to mark as COMPLETED:\n"
        completed_assignments = []
        index = 1
        for deadline in deadlines:
            if deadline['status'] != "COMPLETED":
                response += f"{index}) {deadline['title']}\n"
                completed_assignments.append(deadline['title'])
                index += 1

        if not completed_assignments:
            response = "You do not have any assignments marked as NOT COMPLETED."
            bot.send_message(message.chat.id, response)
            assignments_deadline(message)
            return
        else:
            response += "To return, please click on 'back'"
            keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            for assignment_title in completed_assignments:
                keyboard.add(KeyboardButton(f"{assignment_title}"))
            keyboard.add(KeyboardButton('back'))
            bot.send_message(message.chat.id, response, reply_markup=keyboard)
            bot.register_next_step_handler(message, process_completed, completed_assignments)
    else:
        response = "Yay! You have completed all your assignments for now. Keep up the good work!"
        button = telebot.types.KeyboardButton( "Return to Main" )
        markup = telebot.types.ReplyKeyboardMarkup( resize_keyboard = True, one_time_keyboard = True )
        markup.add( button )
        bot.send_message( user_id, response, reply_markup = markup )


def process_completed(message, pending_assignments):
    user_id = str(message.from_user.id)
    text = message.text

    if text == "back":
        assignments_deadline(message)
    elif text in pending_assignments:
        user_doc = db.collection("users").document(user_id)
        cc_data_doc = user_doc.collection("CC_data").document("ics_data")
        dl_data_docs = user_doc.collection("dl_data").stream()

        cc_data_snapshot = cc_data_doc.get()
        cc_data = cc_data_snapshot.to_dict().get("data", []) if cc_data_snapshot.exists else []

        dl_data = []

        # Retrieve dl_data from Firestore
        for doc in dl_data_docs:
            dl = doc.to_dict()
            dl_data.append(dl)

        # Search for the assignment with the given title in cc_data and dl_data
        for assignment in cc_data + dl_data:
            if assignment.get('title') == text:
                if assignment['status'] != "COMPLETED":
                    assignment['status'] = "COMPLETED"

                    if assignment in cc_data:
                        cc_data_doc.set({"data": cc_data}, merge=True)
                    else:
                        dl_doc = user_doc.collection("dl_data").document(doc.id)
                        dl_doc.set(assignment, merge=True)

                    response = f"Congratulations on completing! I have marked '{assignment['title']}' as COMPLETED."
                else:
                    response = f"The assignment '{assignment['title']}' is already marked as COMPLETED."
                break
        else:
            response = f"Failed to find the assignment with title '{text}'. Please try again."

        bot.reply_to(message, response)
        assignments_deadline(message)
    else:
        response = "Invalid assignment selection. Please select an assignment from the given options."
        bot.reply_to(message, response)
        mark_completed(message)


# To mark as uncompleted
@bot.message_handler(regexp="Mark Assignments as not completed")
def mark_uncompleted(message):
    user_id = str(message.from_user.id)
    deadlines = get_dl(user_id)

    if deadlines:
        response = "Please select the assignment to mark as NOT COMPLETED:\n"
        completed_assignments = []
        index = 1
        for deadline in deadlines:
            if deadline['status'] == "COMPLETED":
                response += f"{index}) {deadline['title']}\n"
                completed_assignments.append(deadline['title'])
                index += 1

        if not completed_assignments:
            response = "You do not have any assignments marked as COMPLETED."
            bot.send_message(message.chat.id, response)
            assignments_deadline(message)
            return
        else:
            response += "To return, please click on 'back'"
            keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            for assignment_title in completed_assignments:
                keyboard.add(KeyboardButton(f"{assignment_title}"))
            keyboard.add(KeyboardButton('back'))
            bot.send_message(message.chat.id, response, reply_markup=keyboard)
            bot.register_next_step_handler(message, process_uncompleted, completed_assignments)
    else:
        response = "Yay! You have completed all your assignments for now. Keep up the good work!"
        bot.reply_to(message, response)


def process_uncompleted(message, completed_assignments):
    user_id = str(message.from_user.id)
    text = message.text

    if text == "back":
        assignments_deadline(message)
    else:
        assignment_title = text
        if assignment_title in completed_assignments:
            user_doc = db.collection("users").document(user_id)
            cc_data_doc = user_doc.collection("CC_data").document("ics_data")
            dl_data_docs = user_doc.collection("dl_data").stream()

            cc_data_snapshot = cc_data_doc.get()
            cc_data = cc_data_snapshot.to_dict().get("data", []) if cc_data_snapshot.exists else []

            dl_data = []

            # Retrieve dl_data from Firestore
            for doc in dl_data_docs:
                dl = doc.to_dict()
                dl_data.append(dl)

            assignment_found = False

            # Search for the assignment with the given title in cc_data and dl_data
            for assignment in cc_data + dl_data:
                if assignment.get('title', '') == assignment_title:
                    if assignment['status'] != "NOT COMPLETED":
                        assignment['status'] = "NOT COMPLETED"

                        if assignment in cc_data:
                            cc_data_doc.set({"data": cc_data}, merge=True)
                        else:
                            dl_doc = user_doc.collection("dl_data").document(doc.id)
                            dl_doc.set(assignment, merge=True)

                        response = f"I have marked '{assignment['title']}' as NOT COMPLETED."
                    else:
                        response = f"The assignment '{assignment['title']}' is already marked as NOT COMPLETED."
                    assignment_found = True
                    break

            if not assignment_found:
                response = f"Failed to find the assignment with title '{assignment_title}'. Please try again."

        else:
            response = "Invalid assignment. Please select an assignment from the given options."

        bot.reply_to(message, response)
        assignments_deadline(message)


# Function to prompt the user to upload .ics file or provide the link
@bot.message_handler(regexp="Manage Calendar Data")
def prompt_calendar_data(message):
    user_id = str(message.from_user.id)
    user_doc = db.collection("users").document(user_id)
    state = {"user_doc": user_doc}

    # Check if .ics data exists
    if user_doc.collection("CC_data").document("ics_data").get().exists and len("CC_data") > 0:
        markup = ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True)
        update_button = KeyboardButton("Update .ics data")
        delete_button = KeyboardButton("Delete .ics data")
        back_button = KeyboardButton("Back")
        markup.add(update_button, delete_button, back_button)

        response = "The .ics data already exists. What would you like to do?\n\n"
        response += "Do note that providing calendar data will not affect deadlines which you have manually entered through 'Manage Deadlines data'. However, "
        response += "all deadlines imported from previous .ics file will be overridden if you update .ics data.\n\n"
        response += "To retrieve .ics data from Canvas, please go to canvas -> calendar (on the left side) -> Calendar feed (Bottom Right) \n"
        response += "The .ics link is in the textbox, select 'Provide .ics link' and copy paste the link for the bot."
        response += " Else, if you click on 'Click to view Calendar Feed', you will download .ics file, select 'Upload .ics file' and upload the .ics file to the bot.\n\n"
        response += 'Please ensure that your .ics file is not corrupted, else you will get an error. This issue may rise if there are no valid deadlines on your canvas calendar '
        response += 'or all assignments in your canvas calendar all are past the due date.'
        bot.send_message(user_id, response, reply_markup=markup)
        bot.register_next_step_handler(message, handle_existing_ics_data, state)
    else:
        markup = ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True)
        upload_button = KeyboardButton("Upload .ics file")
        link_button = KeyboardButton("Provide .ics link")
        back_button = KeyboardButton("Back")
        markup.add(upload_button, link_button)
        markup.add(back_button)

        response = "Please select an option to provide the calendar data.\n\n"
        response += "Do note that providing calendar data will not affect deadlines which you have manually entered through 'Manage Deadlines data'.\n\n"
        response += "To retrieve .ics data from Canvas, please go to canvas -> calendar (on the left side) -> Calendar feed (Bottom Right) \n"
        response += "The .ics link is in the textbox, select 'Provide .ics link' and copy paste the link for the bot."
        response += " Else, if you click on 'Click to view Calendar Feed', you will download .ics file, select 'Upload .ics file' and upload the .ics file to the bot.\n\n"
        response += 'Please ensure that your .ics file is not corrupted, else you will get an error. This issue may rise if there are no valid deadlines on your canvas calendar '
        response += 'or all assignments in your canvas calendar all are past the due date.'
        bot.send_message(user_id, response, reply_markup=markup)
        bot.register_next_step_handler(message, handle_calendar_data_input, state)

# Handler for processing the selected option when .ics data exists
def handle_existing_ics_data(message, state):
    user_doc = state["user_doc"]

    if message.text == "Back":
        assignments_deadline(message)

    elif message.text == "Update .ics data":
        markup = ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True)
        upload_button = KeyboardButton("Upload .ics file")
        link_button = KeyboardButton("Provide .ics link")
        back_button = KeyboardButton("Back")
        markup.add(upload_button, link_button)
        markup.add(back_button)

        user_id = str(message.from_user.id)
        user_data = get_user_data(user_id)
        user_data["current_page"] = 1
        update_user_data(user_id, user_data)
    
        bot.send_message(message.chat.id, "Please select an option to update the calendar data:", reply_markup=markup)
        bot.register_next_step_handler(message, handle_update_calendar_data_input, state)
    elif message.text == "Delete .ics data":
        ics_data_doc = user_doc.collection("CC_data").document("ics_data")
        ics_data_doc.delete()

        # Reset the current page to 1
        user_id = str(message.from_user.id)
        user_data = get_user_data(user_id)
        user_data["current_page"] = 1
        update_user_data(user_id, user_data)

        bot.send_message(message.chat.id, "The .ics data has been deleted.")
        assignments_deadline(message)
    else:
        bot.send_message(message.chat.id, "Invalid option. Please try again.")

# Handler for processing the selected option to update the .ics data when no .ics data is found
def handle_update_calendar_data_input(message, state):
    user_doc = state["user_doc"]

    if message.text == "Back":
        assignments_deadline(message)
    elif message.text == "Upload .ics file":
        bot.send_message(message.chat.id, "Please upload the new .ics file.")
        bot.register_next_step_handler(message, handle_ics_file_upload, user_doc)
    elif message.text == "Provide .ics link":
        bot.send_message(message.chat.id, "Please provide the new .ics link.")
        bot.register_next_step_handler(message, handle_ics_link_input, user_doc)
    else:
        bot.send_message(message.chat.id, "Invalid option. Please try again.")


# Handler for processing the selected option and obtaining the calendar data
def handle_calendar_data_input(message, state):
    user_doc = state["user_doc"]

    if message.text == "Back":
        assignments_deadline(message)
    elif message.text == "Upload .ics file":
        bot.send_message(message.chat.id, "Please upload the .ics file.")
        bot.register_next_step_handler(message, handle_ics_file_upload, user_doc)
    elif message.text == "Provide .ics link":
        bot.send_message(message.chat.id, "Please provide the .ics link.")
        bot.register_next_step_handler(message, handle_ics_link_input, user_doc)
    else:
        bot.send_message(message.chat.id, "Invalid option. Please try again.")

# Handler for processing the uploaded .ics file
def handle_ics_file_upload(message, user_doc):
    if message.document:
        file_info = bot.get_file(message.document.file_id)
        file_url = f"https://api.telegram.org/file/bot{bottoken}/{file_info.file_path}"

        # Process the .ics file data
        ics_data = process_ics_file(file_url)

        if ics_data:
            # Convert date objects to datetime objects
            for assignment in ics_data:
                assignment['due_date'] = datetime.combine(assignment['due_date'], datetime.min.time())

            # Store the .ics data under the user's document
            user_doc.collection("CC_data").document("ics_data").set({'data': ics_data})
            bot.send_message(message.chat.id, "Calendar data has been successfully stored.")
        else:
            bot.send_message(message.chat.id, "Failed to process the .ics file.")
            assignments_deadline(message)  
        
        assignments_deadline(message)  # Send the user back to assignments_deadline()
    else:
        bot.send_message(message.chat.id, "No file uploaded. Please try again.")


# Handler for processing the provided .ics link
def handle_ics_link_input(message, user_doc):
    if message.text == "Back":
        assignments_deadline(message)
        
    ics_link = message.text.strip()

    # Process the .ics file data from the link
    ics_data = process_ics_file(ics_link)

    if ics_data:
        # Store the .ics data under the user's document
        user_doc.collection("CC_data").document("ics_data").set({'data': ics_data})

        bot.send_message(message.chat.id, "Calendar data has been successfully stored.")
        assignments_deadline(message)
    else:
        bot.send_message(message.chat.id, "Failed to process the .ics link.")
        assignments_deadline(message)  


# Function to process the .ics file data and extract the required fields
def process_ics_file(file_url):
    try:
        response = requests.get(file_url)
        response.raise_for_status()

        ics_content = response.text

        # Parse the .ics content
        cal = icalendar.Calendar.from_ical(ics_content)

        # Extract the required fields from the .ics file
        extracted_data = []

        for event in cal.walk('vevent'):
            title = str(event.get('summary'))
            due_date = event.get('dtstart').dt

            assignment = {
                'title': title,
                'due_date': due_date,
                'status': 'NOT COMPLETED'
            }

            extracted_data.append(assignment)

        return extracted_data
    except requests.exceptions.RequestException as e:
        print(f"Error retrieving .ics file: {e}")
        return None


# END OF FUNCTION (1) Assignment Deadlines

###################################################################################################################################

# FUNCTION (2) Personal Planner

# To Delete Personal Planner
@bot.message_handler(regexp="Delete_all_personal_planner")
def delete_personal_planner(message):
    user_id = str(message.from_user.id)
    pp_ref = db.collection('users').document(user_id).collection('personal_planner')

    # Delete all documents in the personal planner collection
    docs = pp_ref.get()
    for doc in docs:
        doc.reference.delete()

    response = "All events in your Personal Planner has been deleted.\n"
    response += "You will be sent back to the main menu."
    bot.send_message(message.chat.id, response)
    main(message)
    
#Main Function 
@bot.message_handler(regexp="Personal Planner")
def personal_planner(message):
    user_id = str(message.from_user.id)
    pp_ref = db.collection('users').document(user_id).collection('personal_planner')

    pp_data = pp_ref.get()
    if pp_data:
        event_list = []
        for doc in pp_data:
            event_data = doc.to_dict()
            event_data['date'] = datetime.strptime(event_data['date'], "%d/%m/%Y %H%M")
            event_list.append(event_data)

        # Sort the event list based on the 'date' field in ascending order
        sorted_events = sorted(event_list, key=lambda x: x['date'])

        response = "Your Personal Planner:\n\n"
        for index, event_data in enumerate(sorted_events, start=1):
            formatted_date = event_data['date'].strftime("%A %d/%m/%Y %H%Mhrs")
            response += f"{index}) {event_data['title']}\n"
            response += f"Date: {formatted_date}\n"
            response += f"Additional Notes: {event_data['notes']}\n\n"
    else:
        response = "Your Personal Planner is currently empty. Please add an event to begin."

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(KeyboardButton("Add Events"))
    keyboard.add(KeyboardButton("Delete Events"))
    keyboard.add(KeyboardButton("Return to Main"))

    bot.send_message(message.chat.id, response, reply_markup=keyboard)
    bot.register_next_step_handler(message, handle_personal_planner_menu)

def handle_personal_planner_menu(message):
    user_reply = message.text.lower()

    if user_reply == 'add events':
        add_event(message)
    elif user_reply == 'delete events':
        delete_event(message)
    elif user_reply == 'return to main':
        main(message)
    else:
        bot.send_message(message.chat.id, "Invalid option. Please select a valid option.")

# To Add Event
def add_event(message):
    bot.send_message(message.chat.id, "Please enter the event name:")
    bot.register_next_step_handler(message, add_event_name)


def add_event_name(message):
    event_name = message.text
    response = "Please enter the event date and time in 24H format (e.g DD/MM HHMM )\n\n"
    response += "However, if you wish to add a future year, please key in format DD/MM/YYYY HHMM instead"
    bot.send_message(message.chat.id, response)
    bot.register_next_step_handler(message, add_event_datetime, event_name)
        
def add_event_datetime(message, event_name):
    event_datetime = message.text.replace(":", "")  # Remove the colon from the time format

    try:
        # Try parsing as "DD/MM/YYYY HHMM" format
        event_time = datetime.strptime(event_datetime, "%d/%m/%Y %H%M")
        current_time = datetime.now()

        if event_time < current_time:
            # The entered time is in the past
            bot.send_message(message.chat.id, "You gonna need a time machine for this event. Please enter a future date and time.")
            # Prompt the user again to enter a valid time
            bot.register_next_step_handler(message, add_event_datetime, event_name)
        else:
            # The entered time is valid
            # Call handle_additional_comments to present the buttons for adding or skipping comments
            handle_additional_comments(message, event_name, event_datetime)
    except ValueError:
        try:
            # Try parsing as "DD/MM HHMM" format
            event_date, event_time = event_datetime.split(" ")
            current_year = datetime.now().year

            event_time_full = f"{event_date}/{current_year} {event_time}"
            event_time_full = datetime.strptime(event_time_full, "%d/%m/%Y %H%M")

            if event_time_full < datetime.now():
                # The entered time is in the past
                bot.send_message(message.chat.id, "You gonna need a time machine for this event. Please enter a future date and time.")
                # Prompt the user again to enter a valid time
                bot.register_next_step_handler(message, add_event_datetime, event_name)
            else:
                # The entered time is valid
                # Call handle_additional_comments to present the buttons for adding or skipping comments
                handle_additional_comments(message, event_name, event_time_full.strftime("%d/%m/%Y %H%M"))
        except ValueError:
            # The entered time format is invalid
            response = "Invalid date and time format. Please enter the date and time in 24H format.\n"
            response += "e.g., for 5 May 11pm, please type 05/05 2300 \n\n"
            response += "However, if you are attempting to key in a future year, please enter the date in DD/MM/YYYY HHMM\n\n"
            response += "e.g, for 6 June 2026 12pm, please type 06/06/2026 1200"
            bot.send_message(message.chat.id, response)
            # Prompt the user again to enter a valid time
            bot.register_next_step_handler(message, add_event_datetime, event_name)


def handle_additional_comments(message, event_name, event_datetime):
    # Present the buttons for adding or skipping comments
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(KeyboardButton("Add comment"))
    keyboard.add(KeyboardButton("Skip comment"))
    bot.send_message(message.chat.id, "Do you want to add additional comments?", reply_markup=keyboard)
    bot.register_next_step_handler(message, handle_additional_comments_choice, event_name, event_datetime)

    # Prompt to use the buttons if an invalid response is received
    bot.send_message(message.chat.id, "Please use the buttons to select your option. Subsequently you may also reply 'yes' or 'no'.")

def handle_additional_comments_choice(message, event_name, event_datetime):
    choice = message.text.lower()

    if choice == 'add comment' or choice == 'yes':
        # Remove the keyboard
        remove_keyboard = ReplyKeyboardRemove()
        bot.send_message(message.chat.id, "Please enter the additional comments:", reply_markup=remove_keyboard)
        bot.register_next_step_handler(message, save_event_with_comments, event_name, event_datetime)
    elif choice == 'skip comment' or choice == 'no':
        # User chooses to skip adding comments
        event_notes = ""
        save_event_details(message, event_name, event_datetime, event_notes)
    else:
        # Invalid response, prompt to select again
        bot.send_message(message.chat.id, "Please use the buttons to select your option.")
        bot.register_next_step_handler(message, handle_additional_comments_choice, event_name, event_datetime)


def save_event_with_comments(message, event_name, event_datetime):
    event_notes = message.text
    save_event_details(message, event_name, event_datetime, event_notes)


def save_event_details(message, event_name, event_datetime, event_notes):
    user_id = message.from_user.id
    pp_ref = db.collection('users').document(str(user_id)).collection('personal_planner')
    new_event_ref = pp_ref.document()
    new_event_ref.set({
        'title': event_name,
        'date': event_datetime,
        'notes': event_notes
    })

    bot.send_message(user_id, "Event added to your Personal Planner!")
    personal_planner(message)

# To Delete Events
@bot.message_handler(regexp="Delete Events")
def delete_event(message):
    user_id = str(message.from_user.id)
    pp_ref = db.collection('users').document(user_id).collection('personal_planner')
    pp_data = pp_ref.get()

    if pp_data:
        response = "Select the event to delete:\n"
        response += "Please select the corresponding index to your event title\n"
        response += "e.g If you wish to delete 1) Orbital Meeting, please select 1\n"
        button_array = []
        event_docs = [doc for doc in pp_data]
        for index, doc in enumerate(event_docs, start=1):
            event_title = doc.to_dict().get('title')
            response += f"\n{index}) {event_title}"
            button = KeyboardButton(str(index))
            button_array.append(button)

        response += "\n\nIf you wish to delete all events. Please type in 'Delete_all_personal_planner'"
        button_array.append(KeyboardButton("back"))

        keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        keyboard.add(*button_array)

        bot.send_message(message.chat.id, response, reply_markup=keyboard)
        bot.register_next_step_handler(message, process_delete_event, event_docs)
    else:
        bot.send_message(message.chat.id, "You do not have any events available to delete.")
        personal_planner(message)

def process_delete_event(message, event_docs):
    user_id = str(message.from_user.id)
    event_index = message.text
    text = message.text.lower()
    
    if text == "back":
        personal_planner(message)
        
    elif text == "delete_all_personal_planner":
        delete_personal_planner(message)

    elif event_index.isdigit():
        event_index = int(event_index) - 1

        if event_index in range(len(event_docs)):
            event_doc = event_docs[event_index]
            event_title = event_doc.to_dict().get('title')
            event_doc.reference.delete()
            bot.send_message(message.chat.id, f"Event '{event_title}' has been deleted from your Personal Planner.")
            personal_planner(message)  # Call personal_planner after successful deletion
        else:
            # Invalid event index
            response = "Invalid event index. Please select a valid event to delete.\n"
            response += "Please use the buttons to select the event you wish to delete"
            bot.send_message(message.chat.id, response)
            # Prompt the user again to select a valid event
            bot.register_next_step_handler(message, process_delete_event, event_docs)
    else:
        # Invalid input, not a numeric value
        response = "Invalid input. Please enter a numeric value for event index.\n"
        response += "Please use the buttons to select the event you wish to delete"
        bot.send_message(message.chat.id, response)
        # Prompt the user again to enter a valid input
        bot.register_next_step_handler(message, process_delete_event, event_docs)


# END OF FUNCTION (2) Personal Planner

###################################################################################################################################

# FUNCTION (3) School Timetable

########## FUNCTION TO DIRECT USER BASED ON OPTION SELECTED IN EXAM TIMETABLE ##########
def choice3( message, userid ): # Choice options for School Timetable function
    option = message.text
    if option == "Add module":
        go_to_addmodule( message, userid )
    elif option == "School Timetable":
        school_timetable( message, userid )
    elif option == "Return to Main":
        main( message )

def choice3a( message, userid, unconfigured_list ): 
    option = message.text
    if option == "Configure lessons":
        prompt_config_lesson( message, userid, unconfigured_list )
    elif option == "Unconfigure lessons":
        prompt_unconfig( message, userid )
    elif option == "Ignore and proceed to view school timetable":
        view_timetable( message, userid )
    elif option == "Return to Main":
        main( message )

########## FUNCTION TO PROMPT USER TO CONFIG/UNCONFIG LESSON/VIEW TT ##########
def school_timetable( message, userid ):
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
        if unconfigured == "": # If all User's lessons are configured, proceed to view timetable
             view_timetable( message, userid )
        else: # If User has unconfigured lessons, can choose to configure, ignore and proceed to view, or return to main
            button1 = telebot.types.KeyboardButton( "Configure lessons" )
            button2 = telebot.types.KeyboardButton( "Unconfigure lessons" )
            button3 = telebot.types.KeyboardButton( "Ignore and proceed to view school timetable" )
            button4 = telebot.types.KeyboardButton( "Return to Main" )
            markup = telebot.types.ReplyKeyboardMarkup( resize_keyboard = True, one_time_keyboard = True )
            markup.add( button1 ).add( button2 ).add( button3 ).add( button4 )
            bot.send_message( int(userid), "You have not configured the timings for these lessons. Would you like to configure them now? The lesson slot numbers are required.\n\n" + unconfigured, reply_markup = markup )
            bot.register_next_step_handler( message, choice3a, userid, unconfigured_list )
    else: # If User has no mods
        button1 = telebot.types.KeyboardButton( "Add modules" )
        button2 = telebot.types.KeyboardButton( "Return to Main" )
        markup = telebot.types.ReplyKeyboardMarkup( resize_keyboard = True, one_time_keyboard = True )
        markup.add(button1).add(button2)
        bot.send_message( int(userid), "You have no modules, please proceed to add modules.",reply_markup = markup )
        bot.register_next_step_handler( message, choice3, userid ) # Next step based on User's choice

########## FUNCTION TO SELECT LESSON TO CONFIGURE ##########
def prompt_config_lesson( message, userid, unconfigured_list ):
    markup = telebot.types.ReplyKeyboardMarkup( resize_keyboard = True, one_time_keyboard = True )
    for item in unconfigured_list:
        button = telebot.types.KeyboardButton( item )
        markup.add( button )
    bot.send_message( int(userid), "Which lesson would you like to configure?", reply_markup = markup )
    bot.register_next_step_handler( message, config_lesson1, userid, unconfigured_list )

########## FUNCTION TO CONFIGURE LESSON (1) ##########
def config_lesson1( message, userid, unconfigured_list ):
    lesson = message.text
    if lesson in unconfigured_list:
        bot.send_message( int(userid), f'What is your lesson slot number for {lesson}? \n\nFor lectures/tutorials with only one slot, please key in 1. Otherwise, please key in your allocated slot number. \n\nFor odd/even lessons, please key in the full lesson slot number as seen on NUSMods. For example: \nE23, D09, E9 etc. \n\nFor all other lessons, please key in the numbers only. For example: \nSEC-09 will be 09.' )
        bot.register_next_step_handler( message, config_lesson2, userid, lesson )
    else:
        bot.send_message( message.chat.id, "That is an invalid lesson. Please try again.")
        school_timetable( message, userid )

########## FUNCTION TO CONFIGURE LESSON (2) ##########
def config_lesson2( message, userid, lesson ):
    lesson_list = lesson.split( maxsplit = 1 )
    mod_code, lesson_type = lesson_list[0], lesson_list[1]
    lesson_no = message.text.upper()
    all_lessons_req = requests.get( mod_details_end.replace( replace_ay, ay ).replace( replace_mod, mod_code ) ).json()
    all_lessons = all_lessons_req["semesterData"][semester]['timetable'] # Retrieve all lesson slots of a module for the current semester
    for item in all_lessons: # For each lesson slot
        if item['classNo'] == lesson_no and item['lessonType'] == lesson_type: # To filter the lesson slot that corresponds to User's input
            db.collection( "users" ).document( userid ).collection( "mods" ).document( mod_code ).collection( "lessons" ).document( lesson ).update( {"timings": firestore.ArrayUnion([item])})
            db.collection( "users" ).document( userid ).collection( "mods" ).document( mod_code ).collection( "lessons" ).document( lesson ).update( {"config" : True} )
    check_ref = db.collection( "users" ).document( userid ).collection( "mods" ).document( mod_code ).collection( "lessons" ).document( lesson ).get().to_dict()
    if check_ref["config"]:
        bot.send_message( int(userid), f'Your timing for {lesson} has been configured!')
        regenerate( message )
        school_timetable( message, userid )
    else:
        button1 = telebot.types.KeyboardButton( "School Timetable" )
        button2 = telebot.types.KeyboardButton( "Return to Main" )
        markup = telebot.types.ReplyKeyboardMarkup( resize_keyboard = True, one_time_keyboard = True )
        markup.add( button1 ).add( button2 )
        bot.send_message( int(userid), "Your lesson slot could not be found. Please return to School Timetable to try again. If error persists, kindly feedback this issue to us via the Main menu, thank you!", reply_markup = markup )
        bot.register_next_step_handler( message, choice3, userid )

########## FUNCTION TO SELECT LESSON TO UNCONFIGURE ##########
def prompt_unconfig( message, userid ):
    mods = db.collection( "users" ).document( userid ).collection( "mods" ).stream()
    configlist = []
    for mod in mods:
        lessons = db.collection( "users" ).document( userid ).collection( "mods" ).document( mod.id ).collection( "lessons" ).stream()
        for lesson in lessons:
            lesson_status = db.collection( "users" ).document( userid ).collection( "mods" ).document( mod.id ).collection( "lessons" ).document( lesson.id ).get().to_dict()[ "config" ]
            if lesson_status:
                configlist.append( lesson.id )
    if not configlist:
        bot.send_message( int(userid), "You have no configured lessons, please proceed to configure them." )
        school_timetable( message, userid )
    else:
        markup = telebot.types.ReplyKeyboardMarkup( resize_keyboard = True, one_time_keyboard = True )
        for lesson in configlist:
            button = telebot.types.KeyboardButton( lesson )
            markup.add( button )
        bot.send_message( int(userid), "Which lesson would you like to unconfigure?", reply_markup = markup )
        bot.register_next_step_handler( message, unconfig, userid )

########## FUNCTION TO UNCONFIGURE LESSON ##########
def unconfig( message, userid ):
    dummy = message.text.split( maxsplit = 1 )
    mod_code = dummy[0]
    db.collection( "users" ).document( userid ).collection( "mods" ).document( mod_code ).collection( "lessons" ).document( message.text ).set( {"config": False} )
    regenerate( message )
    bot.send_message( int(userid), f"{message.text} has been unconfigured!" )
    school_timetable( message, userid )

########## DATE FOR TESTING ##########
test_date = datetime( 2023, 2, 28 )
######################################

########## FUNCTION TO VIEW TIMETABLE ##########
def view_timetable( message, userid ):
    if recess_start < test_date < recess_end:
        button = telebot.types.KeyboardButton( "Return to Main")
        markup = telebot.types.ReplyKeyboardMarkup( resize_keyboard = True, one_time_keyboard = True )
        markup.add( button )
        bot.send_message( int(userid), "It is recess week, have a good rest! :)", reply_markup = markup )
    elif read_start < test_date < read_end:
        button = telebot.types.KeyboardButton( "Return to Main")
        markup = telebot.types.ReplyKeyboardMarkup( resize_keyboard = True, one_time_keyboard = True )
        markup.add( button )
        bot.send_message( int(userid), "It is reading week, have a good rest! :)", reply_markup = markup )
    elif read_end < test_date:
        button = telebot.types.KeyboardButton( "Return to Main")
        markup = telebot.types.ReplyKeyboardMarkup( resize_keyboard = True, one_time_keyboard = True )
        markup.add( button )
        bot.send_message( int(userid), "You have no more classes, all the best for your exams!", reply_markup = markup )
    elif sem_end < test_date:
        button = telebot.types.KeyboardButton( "Return to Main")
        markup = telebot.types.ReplyKeyboardMarkup( resize_keyboard = True, one_time_keyboard = True )
        markup.add( button )
        bot.send_message( int(userid), "The semester has ended, have a good break! :)", reply_markup = markup )
    else:
        week_no = math.floor(((test_date - sem_start).days)/7 + 1) # The current week number
        if recess_end < test_date:
            week_no -= 1
        week_ref = db.collection( "users" ).document( userid ).collection( "timetable" ).document( "this_week" )
        this_week = week_ref.get().to_dict()
        if str(week_no) not in this_week: # If this week's timetable does not match with current week's number
            bot.send_message( int(userid) , f"Please hold on while I generate your timetable for week {week_no}, thank you!" )
            lesson_list = []
            mods = db.collection( "users" ).document( userid ).collection( "mods" ).stream()
            for mod in mods:
                lesson_types = db.collection( "users" ).document( userid ).collection( "mods" ).document( mod.id ).collection( "lessons" ).stream()
                for lesson in lesson_types:
                    slots = db.collection( "users" ).document( userid ).collection( "mods" ).document( mod.id ).collection( "lessons" ).document( lesson.id ).get().to_dict()
                    if slots["config"]:
                        for slot in slots["timings"]:
                            if week_no in slot["weeks"]:
                                slot[ "name" ] = lesson.id
                                lesson_list.append( slot )
            db.collection( "users" ).document( userid ).collection( "timetable" ).document( "this_week" ).set( { str(week_no) : lesson_list } )
            view_timetable( message, userid )
        else:
            bot.send_message( int(userid), f"Please hold on while I fetch your timetable for week {week_no}, thank you!" )
            tt_ref = db.collection( "users" ).document( userid ).collection( "timetable" ).document( "this_week" )
            tt = tt_ref.get().to_dict()
            for lesson in tt[str(week_no)]:
                day = lesson["day"]
                if days.index( day ) < test_date.weekday():
                    tt_ref.update( { str(week_no) : firestore.ArrayRemove( [lesson] ) } )
            upd_tt = db.collection( "users" ).document( userid ).collection( "timetable" ).document( "this_week" ).get().to_dict()
            tt_list = []
            for lesson in upd_tt[str(week_no)]:
                tt_list.append( lesson )
            tt_dic = {}
            for lesson in tt_list:
                if lesson['day'] not in tt_dic:
                    tt_dic[ lesson['day'] ] = [ lesson ]
                else:
                    tt_dic[ lesson['day'] ].append( lesson )
            for day in tt_dic:
                tt_dic[day] = sorted( tt_dic[day], key = lambda x: x["startTime"] )
            tt_days = sorted( tt_dic, key = lambda x: days.index(x) ) # Sorted list of dictionary keys
            text = ""
            for day in tt_days:
                days_passed = (week_no-1)*7 + days.index( day )
                date = (sem_start + timedelta( days = days_passed )).strftime( "%d/%m/%Y" )
                text += f"{day.upper()}, {date}\n\n"
                for lesson in tt_dic[day]:
                    text += f'{lesson["name"]}\nStart: {lesson["startTime"]}\nEnd: {lesson["endTime"]}\nVenue: {lesson["venue"]}\n\n'
                text += "\n"
            if text == "":
                bot.send_message( int(userid) , f"You have no more lessons for week {week_no}. Have a good rest!" )
                main( message )
            else:
                button1 = telebot.types.KeyboardButton( "Unconfigure lessons" )
                button2 = telebot.types.KeyboardButton( "Return to Main" )
                markup = telebot.types.ReplyKeyboardMarkup( resize_keyboard = True, one_time_keyboard = True )
                markup.add( button1 ).add( button2 )
                bot.send_message( int(userid), f"Here is your time table for week {week_no}!" )
                bot.send_message( int(userid), text, reply_markup = markup )
                bot.register_next_step_handler( message, choice3a, userid, None )

########## FUNCTION TO RESTART WEEKLY TIMETABLE ##########
def regenerate( message ):
    userid = str( message.chat.id )
    db.collection( "users" ).document( userid ).collection( "timetable" ).document( "this_week" ).set({})

# END OF FUNCTION (3) School Timetable

###################################################################################################################################

# FUNCTION (4) Exam Timetable

########## FUNCTION TO DIRECT USER BASED ON OPTION SELECTED IN EXAM TIMETABLE ##########
def choice4( message, userid ):
    option = message.text
    if option == "Add module":
        go_to_addmodule( message, userid )
    elif option == "Delete module":
        go_delete_module( message, userid )
    elif option == "Return to Main":
        main( message )

########## VIEW EXAM FUNCTION ##########
def view_exams( message, userid ):
    if sem_end < test_date:
        button = telebot.types.KeyboardButton( "Return to Main")
        markup = telebot.types.ReplyKeyboardMarkup( resize_keyboard = True, one_time_keyboard = True )
        markup.add( button )
        bot.send_message( int(userid), "The semester has ended, have a good break! :)", reply_markup = markup )
    else:
        doc_ref = db.collection( "users" ).document( userid ).collection( "exam" ).document( "timings" )
        doc = doc_ref.get().to_dict() # Returns a dictionary where the keys are module codes and items are the respective exam timings. Can be empty
        output = ""
        exam_list = []
        for mod_code in doc:
            exam_list.append( mod_code )
        exam_list = sorted( exam_list, key = lambda x: doc[x][0][5:7] )
        for mod_code in exam_list:
            dd = doc[mod_code][0][8:10] # Day of exam
            mm = doc[mod_code][0][5:7]
            yy = doc[mod_code][0][:4]
            date = f'{dd}/{mm}/{yy}'
            duration = doc[mod_code][1] # Duration of exam
            cd = (datetime( int(yy), int(mm), int(dd) ) - test_date).days
            if cd >= 0:
                output += f'{mod_code} Finals\nDate: { date }\nDuration: { duration } minutes\nCountdown: {cd} days\n\n'
        if output == "": # If the User does not have any exams
            all_mods = db.collection( "users" ).document( userid ).collection( "all_mods" ).document( "all_mods" ).get().to_dict()
            if len( all_mods ) > 0:
                button = telebot.types.KeyboardButton( "Return to Main" )
                markup = telebot.types.ReplyKeyboardMarkup( resize_keyboard = True, one_time_keyboard = True )
                markup.add(button)
                bot.send_message( int(userid), "You have no examinations! :)", reply_markup = markup )
            else:
                button1 = telebot.types.KeyboardButton( "Add module" )
                button2 = telebot.types.KeyboardButton( "Return to Main" )
                markup = telebot.types.ReplyKeyboardMarkup( resize_keyboard = True, one_time_keyboard = True )
                markup.add( button1 ).add( button2 )
                bot.send_message( int(userid), "You have no modules, please proceed to add modules.", reply_markup = markup )
                bot.register_next_step_handler( message, choice4, userid ) # Next step based on User's choice
        else:
            button1 = telebot.types.KeyboardButton( "Add module" )
            button2 = telebot.types.KeyboardButton( "Delete module" )
            button3 = telebot.types.KeyboardButton( "Return to Main" )
            markup = telebot.types.ReplyKeyboardMarkup( resize_keyboard = True, one_time_keyboard = True )
            markup.add( button1 ).add( button2 ).add( button3 )
            bot.send_message( int(userid), f"Here are your exam dates for AY {ay.replace( '-', '/' )} Semester {semester+1}:\n\n{output}", reply_markup = markup )
            bot.register_next_step_handler( message, choice4, userid )


# END OF FUNCTION (4) Exam Timetable

###################################################################################################################################

# FUNCTIONS (5) View Modules, Add module, and Delete module

########## HELPER FUNCTION FOR ADDING EXAM TIMING, TO BE USED IN ADD MODULE ##########
def add_exam( userid, mod_code, sem ):
    mod_details_req = requests.get( mod_details_end.replace( replace_ay, ay ).replace( replace_mod, mod_code ) )
    mod_details = mod_details_req.json()['semesterData'][sem]
    if 'examDate' in mod_details:
        db.collection( "users" ).document( userid ).collection( "exam" ).document( "timings" ).update( { mod_code : [ mod_details['examDate'], mod_details['examDuration'] ] } )

########## HELPER FUNCTION FOR REMOVING EXAM TIMING, TO BE USED IN DEL MODULE ##########
def remove_exam( userid, mod_code ):
    db.collection( "users" ).document( userid ).collection( "exam" ).document( "timings" ).update( { mod_code : firestore.DELETE_FIELD} )

########## FUNCTION TO DIRECT USER BASED ON OPTION SELECTED IN VIEW MODULES ##########
def choice5( message, userid ):
    option = message.text
    if option == "Add module":
        go_to_addmodule( message, userid )
    elif option == "Delete module":
        go_delete_module( message, userid )
    elif option == "View modules":
        view_modules( message, userid )
    elif option == "Return to Main":
        main( message )

########## VIEW MODULES FUNCTION ##########
def view_modules( message, userid ):
    doc_ref = db.collection( "users" ).document( userid ).collection( "all_mods" ).document( "all_mods" ) # Reference to check if User has any modules to view
    doc = doc_ref.get().to_dict() # Dictionary of all User's modules, can be empty
    if len(doc) > 0: # If the User has modules to view
        output = "Here are your modules: \n\n"
        for mod_code in doc.keys(): # Keys of dictionary are the module codes
            output += mod_code + ", " + doc[mod_code] + "\n"
        bot.send_message( int(userid), output ) # Output message for User to view modules
        button1 = telebot.types.KeyboardButton( "Add module" )
        button2 = telebot.types.KeyboardButton( "Delete module" )
        button3 = telebot.types.KeyboardButton( "Return to Main" )
        markup = telebot.types.ReplyKeyboardMarkup( resize_keyboard = True, one_time_keyboard = True ) # Reply message with options to procede
        markup.add( button1 ).add( button2 ).add( button3 )
        bot.send_message( int(userid), "What would you like to do?" , reply_markup = markup )
        bot.register_next_step_handler( message, choice5, userid ) # Next step based on User's choice
    else: # If the User has no modules to view
        button1 = telebot.types.KeyboardButton( "Add module" )
        button2 = telebot.types.KeyboardButton( "Return to Main" )
        markup = telebot.types.ReplyKeyboardMarkup( resize_keyboard = True, one_time_keyboard = True )
        markup.add(button1).add(button2)
        bot.send_message( int(userid), "You have no modules, please proceed to add modules.", reply_markup = markup ) # Reply message with options to procede
        bot.register_next_step_handler( message, choice5, userid ) # Next step based on User's choice
        
########## ADD MODULE FUNCTION ##########
def go_to_addmodule( message, userid ):
    bot.send_message( userid, "Please enter the module code." )
    bot.register_next_step_handler( message, add_module, userid )

def add_module( message, userid ):
    formtext = message.text.upper() # Proper format of module code
    if formtext in modcodes: # If the input module is a valid module code
        doc_ref = db.collection( "users" ).document( userid ).collection( "all_mods" ).document( "all_mods" ) # Reference to check if input module is in DB
        doc = doc_ref.get().to_dict() # Dictionary of all User's modules, can be empty
        if formtext in doc: # If module is already in User's modules
            title = doc[ formtext ] # Title of module
            bot.send_message( int(userid), formtext + ": " + title + ", is already in your list of modules." ) # Reply message
        else: # If module is not in User's modules
            db.collection( "users" ).document( userid ).collection( "mods" ).document( formtext ).set({}) # Create a document for the new module with empty dictionary as field
            mod_details_req = requests.get( mod_details_end.replace( replace_ay, ay ).replace( replace_mod, formtext ) ) # API request for details of input module
            mod_details = mod_details_req.json() # All details for input module
            title = mod_details["title"] # Title of module
            try:
                mod_sem = mod_details['semesterData'][semester]['semester']
                mod_tt = mod_details['semesterData'][semester]['timetable']
            except:
                mod_sem = mod_details['semesterData'][0]['semester']
                mod_tt = mod_details['semesterData'][0]['timetable']
            if mod_sem == semester+1:
                mod_lesson_types = []
                for i in mod_tt: # mod_lesson_types will be a List of the different lesson types at the end of this For loop
                    if i[ "lessonType" ] not in mod_lesson_types:
                        mod_lesson_types.append( i["lessonType"] )
                db.collection( "users" ).document( userid ).collection( "all_mods" ).document( "all_mods" ).set( {formtext: title }, merge = True ) # Add module code and title to all_mods document
                for i in mod_lesson_types: # In the new module document, create a new collection and in this collection, create documents for each lesson type to store timings and venues in the future
                    db.collection( "users" ).document( userid ).collection( "mods" ).document( formtext ).collection( "lessons" ).document( f'{formtext} {i}' ).set( {"config" : False} ) # Create document for each lesson type input module has
                try:
                    add_exam( userid, formtext, semester ) # Using helper function to add exam timing for input module to DB
                except:
                    add_exam( userid, formtext, 0)
                bot.send_message( int(userid), "Ok, I have added " + formtext + ": " + title + ", to your modules." ) # Reply message
            else:
                bot.send_message( int(userid), f"{formtext}: {title}, is not available in Semester {mod_sem}." )
        button1 = telebot.types.KeyboardButton( "View modules" )
        button2 = telebot.types.KeyboardButton( "Add module" )
        button3 = telebot.types.KeyboardButton( "Delete module" )
        button4 = telebot.types.KeyboardButton( "Return to Main" )
        markup = telebot.types.ReplyKeyboardMarkup( resize_keyboard = True, one_time_keyboard = True )
        markup.add( button1 ).add( button2 ).add( button3 ).add( button4 )
        bot.send_message( int(userid), "What would you like to do?" , reply_markup = markup ) # Reply message with options to procede
        bot.register_next_step_handler( message, choice5, userid ) # Next step based on User's choice
    else: # Input module is an invalid module code
        bot.send_message( int(userid), "That is an invalid module code, please try again." )
        view_modules( message, userid ) # Prompt User to add module again

########## DELETE MODULE FUNCTION ##########
def go_delete_module( message, userid ):
    doc_ref = db.collection( "users" ).document( userid ).collection( "all_mods" ).document( "all_mods" ) # Reference to check if User has any modules to delete
    doc = doc_ref.get().to_dict() # Dictionary of all User's modules, can be empty
    if len(doc) > 0: # If User has modules to delete
        markup = telebot.types.ReplyKeyboardMarkup( resize_keyboard = True, one_time_keyboard = True )
        for mod_code in doc:
            button = telebot.types.KeyboardButton( "Delete " + mod_code )
            markup.add( button )
        button = telebot.types.KeyboardButton( "Return to Main" )
        markup.add( button )
        bot.send_message( int(userid), "What would you like to do?", reply_markup = markup ) # Reply with options on what to delete, or Return to Main
        bot.register_next_step_handler( message, delete_module, userid ) # Next step based on User's choice
    else: # User has no modules to delete
        button1 = telebot.types.KeyboardButton( "Add module" )
        button2 = telebot.types.KeyboardButton( "Return to Main" )
        markup = telebot.types.ReplyKeyboardMarkup( resize_keyboard = True, one_time_keyboard = True )
        markup.add( button1 ).add( button2 )
        bot.send_message( int(userid), "You have no modules, please procede to add modules.", reply_markup = markup ) # Reply with options to Add module or Return to Main
        bot.register_next_step_handler( message, choice5, userid ) # Next step based on User's choice

def delete_module( message, userid ):
    option = message.text
    if option == "Return to Main":
        main( message )
    else:
        mod_to_delete = message.text[ 7: ] # Module code of module to delete, in  proper format
        title = db.collection( "users" ).document( userid ).collection( "all_mods" ).document( "all_mods" ).get().to_dict()[ mod_to_delete ] # Title of module
        db.collection( "users" ).document( userid ).collection( "mods" ).document( mod_to_delete ).delete()
        db.collection( "users" ).document( userid ).collection( "all_mods" ).document( "all_mods" ).update( { mod_to_delete : firestore.DELETE_FIELD } )
        regenerate( message )
        remove_exam( userid, mod_to_delete )
        button1 = telebot.types.KeyboardButton( "View modules" )
        button2 = telebot.types.KeyboardButton( "Add module" )
        button3 = telebot.types.KeyboardButton( "Delete module" )
        button4 = telebot.types.KeyboardButton( "Return to Main" )
        markup = telebot.types.ReplyKeyboardMarkup( resize_keyboard = True, one_time_keyboard = True )
        markup.add( button1 ).add( button2 ).add( button3 ).add( button4 )
        bot.send_message( int(userid), mod_to_delete + ": " + title + ", has been deleted from your modules." ) # Reply message
        bot.send_message( int(userid), "What would you like to do?", reply_markup = markup ) # Reply message with options to procede
        bot.register_next_step_handler( message, choice5, userid ) # Next step based on User's choice


# END OF FUNCTIONS (5) View Modules, Add module and Delete module

###################################################################################################################################

# FUNCTION (6) Report Issues

@bot.message_handler(regexp="Report Issues")
def report_issues(message):
    user_id = str(message.from_user.id)
    user_name = message.chat.first_name

    # Welcome message and question
    welcome_message = f"Hello {user_name}, welcome to the report issue section.\n"
    welcome_message += "May I know whether you want to report an issue such as bugs or provide feedback and suggestions?"

    # Buttons for bug report, feedback, and return to main
    buttons = [
        [KeyboardButton("Report Bug")],
        [KeyboardButton("Provide Feedback")],
        [KeyboardButton("Return to Main")],
    ]
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for button_row in buttons:
        keyboard.add(*button_row)

    bot.send_message(message.chat.id, welcome_message, reply_markup=keyboard)
    bot.register_next_step_handler(message, handle_report_issues_choice)


def handle_report_issues_choice(message):
    user_id = str(message.from_user.id)
    user_name = message.from_user.username
    choice = message.text.lower()

    if choice == 'report bug':
        # Ask for bug report details
        bot.send_message(message.chat.id, "Please provide details of the bug report:")
        bot.register_next_step_handler(message, confirm_bug_report, user_id, user_name)
    elif choice == 'provide feedback':
        # Ask for feedback details
        bot.send_message(message.chat.id, "Please provide your feedback and suggestions:")
        bot.register_next_step_handler(message, confirm_feedback, user_id, user_name)
    elif choice == 'return to main':
        # Return to main menu
        main(message)
    else:
        # Invalid choice, prompt again
        bot.send_message(message.chat.id, "Invalid choice. Please select either 'Report Bug', 'Provide Feedback', or 'Return to Main'.")
        bot.register_next_step_handler(message, handle_report_issues_choice)

def confirm_bug_report(message, user_id, user_name):
    bug_report = message.text

    # Confirmation message
    confirmation_message = f"Hello {user_name}, may I check whether this is the bug you wish to report?\n\n"
    confirmation_message += bug_report

    # Buttons for confirmation
    buttons = [
        KeyboardButton("Yes"),
        KeyboardButton("Edit"),
    ]
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(*buttons)

    bot.send_message(message.chat.id, confirmation_message, reply_markup=keyboard)
    bot.register_next_step_handler(message, handle_bug_report_confirmation, user_id, user_name, bug_report)

def handle_bug_report_confirmation(message, user_id, user_name, bug_report):
    choice = message.text.lower()

    if choice == 'yes':
        # Save bug report to Firestore
        issues_ref = db.collection('Issues')
        issue_doc_ref = issues_ref.document()
        issue_doc_ref.set({
            'user_id': user_id,
            'user_name': user_name,
            'reports': {
                'bug_report': bug_report,
                'timestamp': firestore.SERVER_TIMESTAMP
            }
        })

        bot.send_message(message.chat.id, "Bug report has been successfully submitted. Thank you!")
        report_issues(message)
    elif choice == 'edit':
        # Prompt user to edit bug report
        bot.send_message(message.chat.id, "Please provide the edited bug report:")
        bot.register_next_step_handler(message, confirm_bug_report, user_id, user_name)
    else:
        # Invalid choice, prompt again
        bot.send_message(message.chat.id, "Invalid choice. Please select either 'Yes' or 'Edit'.")
        bot.register_next_step_handler(message, handle_bug_report_confirmation, user_id, user_name, bug_report)
        
        
def confirm_feedback(message, user_id, user_name):
    feedback = message.text

    # Confirmation message
    confirmation_message = f"Hello {user_name}, may I check whether this is the feedback you wish to provide?\n\n"
    confirmation_message += feedback

    # Buttons for confirmation
    buttons = [
        KeyboardButton("Yes"),
        KeyboardButton("Edit"),
    ]
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(*buttons)

    bot.send_message(message.chat.id, confirmation_message, reply_markup=keyboard)
    bot.register_next_step_handler(message, handle_feedback_confirmation, user_id, user_name, feedback)
    
    
def handle_feedback_confirmation(message, user_id, user_name, feedback):
    choice = message.text.lower()

    if choice == 'yes':
        # Save feedback to Firestore
        issues_ref = db.collection('Issues')
        issue_doc_ref = issues_ref.document()
        issue_doc_ref.set({
            'user_id': user_id,
            'user_name': user_name,
            'reports': {
                'feedback': feedback,
                'timestamp': firestore.SERVER_TIMESTAMP
            }
        })

        bot.send_message(message.chat.id, "Feedback has been successfully submitted. Thank you!")
        report_issues(message)
    elif choice == 'edit':
        # Prompt user to edit feedback
        bot.send_message(message.chat.id, "Please provide the edited feedback:")
        bot.register_next_step_handler(message, confirm_feedback, user_id, user_name)
    else:
        # Invalid choice, prompt again
        bot.send_message(message.chat.id, "Invalid choice. Please select either 'Yes' or 'Edit'.")
        bot.register_next_step_handler(message, handle_feedback_confirmation, user_id, user_name, feedback)


# To retrieve the reports made
issues = []

@bot.message_handler(regexp="retrieve_issues_reported")
def retrieve_issues_reported(message):
    user_id = str(message.from_user.id)

    # Check if the user is an approved admin
    if user_id not in approved_admins:
        bot.send_message(message.chat.id, "You are not authorized to access this function.")
        return

    issues_ref = db.collection('Issues')
    issues_data = issues_ref.stream()

    # Reset the issues list
    issues.clear()

    for issue in issues_data:
        issue_data = issue.to_dict()
        user_name = issue_data.get('user_name')
        bug_report = issue_data.get('reports', {}).get('bug_report')
        feedback = issue_data.get('reports', {}).get('feedback')
        timestamp = issue_data.get('reports', {}).get('timestamp')
        status = issue_data.get('reports', {}).get('status', 'NOT RESOLVED')  # Set default status to "NOT RESOLVED"
        notes = issue_data.get('reports', {}).get('notes', '')  # Empty string by default

        if bug_report:
            issues.append({
                'Type': 'Bug Report',
                'Report': bug_report,
                'User_reported': user_name,
                'Time Reported': timestamp,
                'Status': status,
                'Notes': notes,
                'DocRef': issue.id  # Store the document reference for resolving the issue
            })
        elif feedback:
            issues.append({
                'Type': 'Feedback',
                'Report': feedback,
                'User_reported': user_name,
                'Time Reported': timestamp,
                'Status': status,
                'Notes': notes,
                'DocRef': issue.id  # Store the document reference for resolving the issue
            })

    response = "Reports:\n\n"

    response += "Bugs Reported:\n"
    bug_reports = [issue for issue in issues if issue['Type'] == 'Bug Report']
    if bug_reports:
        for i, bug_report in enumerate(bug_reports, start=1):
            response += f"{i}) Bug Report: {bug_report['Report']}\n"
            response += f"   User_reported: {bug_report['User_reported']}\n"
            response += f"   Time Reported: {bug_report['Time Reported'].strftime('%Y-%m-%d %H:%M:%S')}\n"
            response += f"   Status: {bug_report['Status']}\n"
            response += f"   Notes: {bug_report['Notes']}\n\n"
    else:
        response += "No bug reports found.\n\n"

    response += "Feedback Given:\n"
    feedbacks = [issue for issue in issues if issue['Type'] == 'Feedback']
    if feedbacks:
        for i, feedback in enumerate(feedbacks, start=1):
            response += f"{i}) Feedback: {feedback['Report']}\n"
            response += f"   User_reported: {feedback['User_reported']}\n"
            response += f"   Time Reported: {feedback['Time Reported'].strftime('%Y-%m-%d %H:%M:%S')}\n"
            response += f"   Status: {feedback['Status']}\n"
            response += f"   Notes: {feedback['Notes']}\n\n"
    else:
        response += "No feedbacks found.\n\n"

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(KeyboardButton("Mark issues as RESOLVED"))
    keyboard.add(KeyboardButton("Mark issues as NOT RESOLVED"))
    keyboard.add(KeyboardButton("Edit Issue Notes"))
    keyboard.add(KeyboardButton("Return to Main"))

    bot.send_message(message.chat.id, response, reply_markup=keyboard)
 



@bot.message_handler(regexp="Mark issues as RESOLVED")
def mark_resolve(message):
    user_id = str(message.from_user.id)

    # Check if the user is an approved admin
    if user_id not in approved_admins:
        bot.send_message(message.chat.id, "You are not authorized to access this function.")
        return

    # Separate issues into resolved and unresolved categories
    unresolved_issues = [issue for issue in issues if issue['Status'] == 'NOT RESOLVED']
    resolved_issues = [issue for issue in issues if issue['Status'] == 'RESOLVED']

    if not unresolved_issues:
        bot.send_message(message.chat.id, "No unresolved issues found.")
        return

    # Create a keyboard markup for selecting the unresolved issue to mark as resolved
    markup = ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True)

    for i, issue in enumerate(unresolved_issues, start=1):
        markup.add(KeyboardButton(f"{i}) {issue['Type']}: {issue['Report']}"))

    bot.send_message(message.chat.id, "Select the issue to mark as resolved:", reply_markup=markup)

    # Set the next handler to process the selected issue and pass the unresolved_issues list
    bot.register_next_step_handler(message, process_selected_issue, unresolved_issues)


def process_selected_issue(message, issues):
    try:
        selected_index = int(message.text.split(")")[0]) - 1
        selected_issue = issues[selected_index]

        # Update the status of the selected issue
        issue_doc_ref = db.collection('Issues').document(selected_issue['DocRef'])
        issue_doc_ref.update({'reports.status': 'RESOLVED'})

        # Remove the resolved issue from the list
        issues.remove(selected_issue)

        bot.send_message(message.chat.id, "Issue marked as resolved successfully.", reply_markup=ReplyKeyboardRemove())
    except (ValueError, IndexError):
        bot.send_message(message.chat.id, "Invalid selection. Please try again.")

    # Call the retrieve_issues_reported function to display the updated list
    retrieve_issues_reported(message)
    
@bot.message_handler(regexp="Mark issues as NOT RESOLVED")
def mark_unresolve(message):
    user_id = str(message.from_user.id)

    # Check if the user is an approved admin
    if user_id not in approved_admins:
        bot.send_message(message.chat.id, "You are not authorized to access this function.")
        return

    # Separate issues into resolved and unresolved categories
    unresolved_issues = [issue for issue in issues if issue['Status'] == 'NOT RESOLVED']
    resolved_issues = [issue for issue in issues if issue['Status'] == 'RESOLVED']

    if not resolved_issues:
        bot.send_message(message.chat.id, "No resolved issues found.")
        return

    # Create a keyboard markup for selecting the resolved issue to mark as unresolved
    markup = ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True)

    for i, issue in enumerate(resolved_issues, start=1):
        markup.add(KeyboardButton(f"{i}) {issue['Type']}: {issue['Report']}"))

    bot.send_message(message.chat.id, "Select the issue to mark as unresolved:", reply_markup=markup)

    # Set the next handler to process the selected issue and pass the resolved_issues list
    bot.register_next_step_handler(message, process_selected_issue_unresolve, resolved_issues)

def process_selected_issue_unresolve(message, resolved_issues):
    try:
        selected_index = int(message.text.split(")")[0]) - 1
        selected_issue = resolved_issues[selected_index]

        # Update the status of the selected issue
        issue_doc_ref = db.collection('Issues').document(selected_issue['DocRef'])
        issue_doc_ref.update({'reports.status': 'NOT RESOLVED'})

        # Remove the resolved status from the issue
        selected_issue['Status'] = 'NOT RESOLVED'

        bot.send_message(message.chat.id, "Issue marked as unresolved successfully.", reply_markup=ReplyKeyboardRemove())
    except (ValueError, IndexError):
        bot.send_message(message.chat.id, "Invalid selection. Please try again.")

    # Call the retrieve_issues_reported function to display the updated list
    retrieve_issues_reported(message)



@bot.message_handler(regexp="Edit Issue Notes")
def edit_issues(message):
    user_id = str(message.from_user.id)
    state = {}  # Create a state dictionary for the user

    # Check if the user is an approved admin
    if user_id not in approved_admins:
        bot.send_message(message.chat.id, "You are not authorized to access this function.")
        return

    issues_ref = db.collection('Issues')
    issues_data = issues_ref.get()
    issues = []

    if issues_data:
        for issue in issues_data:
            issue_data = issue.to_dict()
            user_name = issue_data.get('user_name')
            bug_report = issue_data.get('reports', {}).get('bug_report')
            feedback = issue_data.get('reports', {}).get('feedback')
            timestamp = issue_data.get('reports', {}).get('timestamp')
            status = issue_data.get('reports', {}).get('status', 'NOT RESOLVED')
            notes = issue_data.get('reports', {}).get('notes', '')  # Empty string by default

            if bug_report:
                issues.append({
                    'Type': 'Bug Report',
                    'Report': bug_report,
                    'User_reported': user_name,
                    'Time Reported': timestamp,
                    'Status': status,
                    'Notes': notes,
                    'DocRef': issue.id  # Store the document reference for resolving the issue
                })
            elif feedback:
                issues.append({
                    'Type': 'Feedback',
                    'Report': feedback,
                    'User_reported': user_name,
                    'Time Reported': timestamp,
                    'Status': status,
                    'Notes': notes,
                    'DocRef': issue.id  # Store the document reference for resolving the issue
                })

    # Check if there are any issues
    if len(issues) == 0:
        bot.send_message(message.chat.id, "No issues found.")
        return

    # Create a keyboard markup for selecting the issues
    markup = ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True)
    for i, issue in enumerate(issues, start=1):
        markup.add(KeyboardButton(f"{i}) {issue['Type']}: {issue['Report']}"))

    bot.send_message(message.chat.id, "Select the issue to edit its notes:", reply_markup=markup)

    # Store the issues data and the user's state in the state dictionary
    state['issues'] = issues
    state['user_id'] = user_id

    # Register the next step handler to handle the selected issue
    bot.register_next_step_handler(message, handle_selected_issue, state)


def handle_selected_issue(message, state):
    selected_option = message.text
    issues = state['issues']

    # Extract the index from the selected option
    try:
        selected_index = int(selected_option.split(')')[0]) - 1
    except ValueError:
        bot.send_message(message.chat.id, "Invalid issue selection.")
        return

    # Check if the selected index is valid
    if selected_index < 0 or selected_index >= len(issues):
        bot.send_message(message.chat.id, "Invalid issue selection.")
        return

    # Retrieve the selected issue
    selected_issue = issues[selected_index]
    state['selected_issue'] = selected_issue

    # Prompt the user to enter the new notes
    bot.send_message(message.chat.id, "Please enter the new notes:")

    # Register the next step handler to handle the user's input
    bot.register_next_step_handler(message, handle_notes_input, state)


def handle_notes_input(message, state):
    feedback = message.text
    state['feedback'] = feedback

    # Confirmation message
    confirmation_message = f"Hello, may I check whether this is the feedback you wish to provide?\n\n"
    confirmation_message += feedback

    # Create a keyboard markup for confirmation
    buttons = [
        KeyboardButton("Yes"),
        KeyboardButton("Edit"),
    ]
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(*buttons)

    # Remove the previous keyboard
    remove_keyboard = ReplyKeyboardRemove()

    # Send the confirmation message with the keyboard
    bot.send_message(message.chat.id, confirmation_message, reply_markup=keyboard)

    # Register the next step handler to handle the confirmation
    bot.register_next_step_handler(message, handle_confirmation, state)


def handle_confirmation(message, state):
    confirmation = message.text.lower()

    if confirmation == "yes":
        # Update the notes of the selected issue
        selected_issue = state['selected_issue']
        selected_issue['Notes'] = state['feedback']

        # Update the issue in the database
        update_issue_notes(selected_issue)

        bot.send_message(message.chat.id, "Notes updated successfully.")
        retrieve_issues_reported(message)
    elif confirmation == "edit":
        bot.send_message(message.chat.id, "Please re-enter the new notes:")
        bot.register_next_step_handler(message, handle_notes_input, state)
    else:
        bot.send_message(message.chat.id, "Invalid confirmation response.")


def update_issue_notes(issue):
    doc_ref = db.collection('Issues').document(issue['DocRef'])
    doc_ref.update({'reports.notes': issue['Notes']})
    
# END OF FUNCTION (6) Report Issues

###################################################################################################################################



###################################################################################################################################
##### PLEASE ENSURE THIS STAYS AT THE BOTTOM OR FUNCTIONS WILL BREAK! #####
##### INVALID TEXT FUNCTION #####
@bot.message_handler()
def invalid_text( text ):
    bot.send_message( text.chat.id, "Invalid entry, you will be returned to the Main Menu." )
    main( text )
    
""" def send_restart_instructions():
    all_user_ids = get_all_user_ids()
    for user_id in all_user_ids:
        restart_message = "The server has restarted. To reinitialize the bot functionality, please send the /start command."
        bot.send_message(user_id, restart_message) """
        
#Implement this only when the server is active, if not local testing is just spam fest to all users

def start_bot():
    # Send restart instructions to users
    """ send_restart_instructions() """
    # Start the infinite polling
    bot.infinity_polling()
    
start_bot()

##### PLEASE ENSURE THIS STAYS AT THE BOTTOM OR FUNCTIONS WILL BREAK! #####
###################################################################################################################################