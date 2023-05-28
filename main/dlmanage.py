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

# Define the user IDs of approved admins
approved_admins = ["966269150","291900788"]  

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

mods_basic_req = requests.get( mods_basic_end.replace( replace_ay, ay ) )
mods_basic = mods_basic_req.json() # List of dictionaries, each dictionary represents a module
modcodes = []
for i in mods_basic:
    modcodes.append( i["moduleCode"]) # List of all module codes

#############################################################################################################

#To greet the user haha        
def get_greeting(current_time):
    if current_time.hour < 12:
        return "Good morning"
    elif current_time.hour < 18:
        return "Good afternoon"
    else:
        return "Good evening"

##### MAIN MENU FUNCTION #####
@bot.message_handler( regexp = "Return to Main" )
def main( returntomain ):
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
    reply_text = f"{greeting} {returntomain.chat.first_name}. What would you like to do?\n"
    reply_text += "Please select the corresponding buttons.\n\n"
    reply_text += "1) Assignments Deadlines\n"
    reply_text += "2) Personal Planner\n"
    reply_text += "3) School Timetable\n"
    reply_text += "4) Exam Timetable\n"
    reply_text += "5) View Modules\n"
    reply_text += "6) Report Issues"
    bot.send_message( returntomain.chat.id , reply_text , reply_markup = markup )

##### START COMMAND ######
@bot.message_handler( commands = ["start"] ) # Handle /start command
def start( startmessage ):
    userid = str(startmessage.chat.id) # Obtain unique chat ID
    username = startmessage.chat.first_name # Obtain user's first name
    doc_ref = db.collection( "users" ).document( userid ) # Reference to check if User exists in DB
    doc = doc_ref.get()
    if doc.exists: # True if User exists
        main( startmessage ) # User is sent to the Main Menu
    else:
        data = { "username" : username } # Dictionary containing user's first name
        db.collection( "users" ).document( userid ).set( data ) # Create document for user with "data" as field
        db.collection( "users" ).document( userid ).collection( "all_mods" ).document( "all_mods" ).set({}) # Create all_mods document for User to be used later when adding/deleting modules
        response = "Hello " + username +", I am ManagementBot. I hope to assist you in better planning your schedule! \n"
        response += "You can choose what you want to do by opening the keyboard buttons and selecting the relevant options."
        bot.send_message( int(userid), response )
        bot.send_message( int(userid), "Before we begin, what modules are you taking this semester? ( Please enter the first module code. For example, CS1010S )" )

###################################################################################################################################
# FOR FUNCTION DEADLINE (1)
    
# Sample data for testing! (Only orbital deadline is real haha) Redo in future with proper databasing
dl_data = [
    {
        "title": "ST2131 Quiz 4",
        "due_date": "12/7/23 2359hrs",
        "status": "NOT COMPLETED"
    },
    {
        "title": "HSA1000 Individual Essay",
        "due_date": "13/7/23 2359hrs",
        "status": "NOT COMPLETED"
    },
    {
        "title": "DTK1234 Final DTJ",
        "due_date": "14/6/23 2359hrs",
        "status": "NOT COMPLETED"
    },
    {
        "title": "Orbital Milestone 1",
        "due_date": "29/5/23 1400hrs",
        "status": "NOT COMPLETED"
    },
    {
        "title": "Orbital Milestone 2",
        "due_date": "26/6/23 1400hrs",
        "status": "NOT COMPLETED"
    },
    {
        "title": "Orbital Milestone 3",
        "due_date": "24/7/23 1400hrs",
        "status": "NOT COMPLETED"
    }
]

#To add the sample data dl_data above into user_id
@bot.message_handler(func=lambda message: "add dl_data" in message.text)
def add_dl(message):
    username = message.chat.first_name
    user_id = str(message.from_user.id)
    set_dl(user_id, dl_data)
    bot.reply_to(message, f"DL_DATA added successfully for {username}")

def set_dl(user_id, dl_data):
    user_doc = db.collection("users").document(user_id)
    dl_collection = user_doc.collection("dl")

    for data in dl_data:
        assignment = {
            'id': dl_collection.document().id,  # Assign a unique ID to each assignment
            'title': data['title'],
            'due_date': data['due_date'],
            'status': data['status']
        }
        dl_collection.add(assignment)
        
#To delete the sample data dl_data above from user_id
@bot.message_handler(func=lambda message: message.text == "delete dl_data")
def delete_deadlines(message):
    username = message.chat.first_name
    user_id = str(message.from_user.id)
    delete_dl(user_id)
    bot.reply_to(message, f"DL_DATA have been deleted for {username}")

def delete_dl(user_id):
    user_doc = db.collection("users").document(user_id)
    dl_collection = user_doc.collection("dl")
    
    # Delete the existing dl collection
    docs = dl_collection.get()
    for doc in docs:
        doc.reference.delete()

#Main function for Assignment Deadlines
@bot.message_handler(func=lambda message: message.text == "Assignments Deadlines")
def assignments_deadline(message):
    user_id = str(message.from_user.id)
    deadlines = get_dl(user_id)

    if deadlines:
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        complete_button = telebot.types.KeyboardButton("Mark Assignments as complete")
        uncomplete_button = telebot.types.KeyboardButton("Mark Assignments as not completed")
        return_button = telebot.types.KeyboardButton("Return to Main")
        markup.row(complete_button)
        markup.row(uncomplete_button)
        markup.row(return_button)

        sorted_dl = sorted(deadlines, key=lambda x: (x['status'] == "COMPLETED", datetime.strptime(x['due_date'], "%d/%m/%y %H%Mhrs")))
        response = "These are your current deadlines:\n"
        for i, deadline in enumerate(sorted_dl, start=1):
            due_date = datetime.strptime(deadline['due_date'], "%d/%m/%y %H%Mhrs")
            current_date = datetime.now()

            time_remaining = due_date - current_date
            days_remaining = time_remaining.days
            hours_remaining = time_remaining.seconds // 3600

            if days_remaining > 0:
                time_left = f"{days_remaining} days and {hours_remaining} hours left."
            elif hours_remaining > 0:
                time_left = f"{hours_remaining} hours left."
            elif time_remaining > 0:
                time_left = "You have less than an hour left!"
            else:
                time_left = "The deadline for this assignment has passed"
            
            day_of_week = due_date.strftime("%A")

            response += f"{i}) {deadline['title']}:\nDue date: {day_of_week}, {deadline['due_date']} \nTime left: {time_left}\nStatus: {deadline['status']}\n\n"
        bot.send_message(message.chat.id, response, reply_markup=markup)
    else:
        response = "Yay! You have no pending deadlines, keep up the good work!"
        bot.send_message(message.chat.id, response)
        time.sleep(1)
        main(message)


# To allow users to mark as completion
@bot.message_handler(regexp="Mark Assignments as complete")
def mark_completed(message):
    user_id = str(message.from_user.id)
    deadlines = get_dl(user_id)

    if deadlines:
        response = "Please select the assignment you completed:\n"
        sorted_deadlines = sorted(deadlines, key=lambda x: datetime.strptime(x['due_date'], "%d/%m/%y %H%Mhrs"))
        pending_counter = 1
        pending_assignments = []
        for i, deadline in enumerate(sorted_deadlines, start=1):
            if deadline['status'] != "COMPLETED":
                response += f"{pending_counter}) {deadline['title']}\n"
                pending_assignments.append(deadline['id'])  # Include assignment ID
                pending_counter += 1

        if pending_counter == 1:
            response = "You do not have any assignments marked NOT COMPLETED left."
        else:
            response += "To return, please click on 'back'"
            keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            for i in range(1, pending_counter):
                keyboard.add(KeyboardButton(str(i)))
            keyboard.add(KeyboardButton('back'))
            bot.send_message(message.chat.id, response, reply_markup=keyboard)
            bot.register_next_step_handler(message, process_completed, pending_assignments)

        # Check if all deadlines are completed
        if all(deadline['status'] == "COMPLETED" for deadline in deadlines):
            response = "Yay! You have completed all deadlines, keep up the good work!"
            bot.send_message(message.chat.id, response)
            assignments_deadline(message)
            return
    else:
        response = "Yay! You have no pending deadlines, keep up the good work!"
        bot.reply_to(message, response)


def create_assignment_buttons(pending_assignments):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

    for i in range(1, len(pending_assignments) + 1):
        keyboard.add(KeyboardButton(str(i)))

    keyboard.add(KeyboardButton('back'))
    return keyboard


def process_completed(message, pending_assignments):
    user_id = str(message.from_user.id)
    text = message.text.lower()

    if text == "back":
        assignments_deadline(message)
    else:
        try:
            assignment_index = int(text) - 1

            if assignment_index in range(len(pending_assignments)):
                assignment_id = pending_assignments[assignment_index]  # Retrieve assignment ID
                deadlines = get_dl(user_id)
                pending_counter = 0

                for i, deadline in enumerate(deadlines):
                    if deadline['id'] == assignment_id and deadline['status'] != "COMPLETED":
                        deadline['status'] = "COMPLETED"
                        pending_counter += 1
                        response = f"Congratulations on completing! I have marked '{deadline['title']}' as COMPLETED."
                        break
                else:
                    response = "Failed to update the completion status. Please try again."

                if pending_counter > 0:
                    update_dl(user_id, deadlines)
            else:
                response = "Invalid assignment index. Please type in the number corresponding to the completed assignment.\n"
                response += "For example, if you want to mark 1) HW1, simply reply 1"
        except ValueError:
            response = "Invalid input."

        bot.reply_to(message, response)
        assignments_deadline(message)



# To mark as uncompleted
@bot.message_handler( regexp = "Mark Assignments as not completed")
def mark_uncompleted(message):
    user_id = str(message.from_user.id)
    deadlines = get_dl(user_id)

    if deadlines:
        response = "Please select the assignment to mark as NOT COMPLETED:\n"
        sorted_deadlines = sorted(deadlines, key=lambda x: datetime.strptime(x['due_date'], "%d/%m/%y %H%Mhrs"))
        completed_counter = 1
        completed_assignments = []
        for i, deadline in enumerate(sorted_deadlines, start=1):
            if deadline['status'] == "COMPLETED":
                response += f"{completed_counter}) {deadline['title']}\n"
                completed_assignments.append(deadline['id'])  # Include assignment ID
                completed_counter += 1

        if completed_counter == 1:
            response = "You do not have any assignments marked as COMPLETED."
            bot.send_message(message.chat.id, response)
            assignments_deadline(message)
            return
        else:
            response += "To return, please click on 'back'"
            keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            for i in range(1, completed_counter):
                keyboard.add(KeyboardButton(str(i)))
            keyboard.add(KeyboardButton('back'))
            bot.send_message(message.chat.id, response, reply_markup=keyboard)
            bot.register_next_step_handler(message, process_uncompleted, completed_assignments)
    else:
        response = "Yay! You have completed all your assignments for now, keep up the good work!"
        bot.reply_to(message, response)

def process_uncompleted(message, completed_assignments):
    user_id = str(message.from_user.id)
    text = message.text.lower()

    if text == "back":
        assignments_deadline(message)
    else:
        try:
            assignment_index = int(text) - 1

            if assignment_index in range(len(completed_assignments)):
                assignment_id = completed_assignments[assignment_index]  # Retrieve assignment ID
                deadlines = get_dl(user_id)

                for deadline in deadlines:
                    if deadline['id'] == assignment_id:
                        if deadline['status'] == "COMPLETED":
                            deadline['status'] = "NOT COMPLETED"
                            update_dl(user_id, deadlines)
                            response = f"Assignment '{deadline['title']}' has been marked as NOT COMPLETED."
                        else:
                            response = "This assignment is already marked as NOT COMPLETED."
                        break
                else:
                    response = "Failed to update the completion status. Please try again."
            else:
                response = "Invalid assignment index. Please type in the number corresponding to the completed assignment.\n"
                response += "For example, if you want to mark 1) HW1 , simply reply 1"
        except ValueError:
            response = "Invalid input."

        bot.reply_to(message, response)
        assignments_deadline(message)


def get_dl(user_id):
    dl_collection = db.collection("users").document(user_id).collection("dl")
    dl = dl_collection.get()

    dl_data = []
    for deadline in dl:
        dl_data.append({**deadline.to_dict(), 'id': deadline.id})  # Include assignment ID

    return dl_data

def update_dl(user_id, deadlines):
    user_doc = db.collection("users").document(user_id)
    dl_collection = user_doc.collection("dl")

    for deadline in deadlines:
        doc_id = deadline['id']
        dl_doc = dl_collection.document(str(doc_id))
        dl_doc.set(deadline)
        
        
# END OF FUNCTION DEADLINE

##############################################################################################################

# FOR FUNCTION Personal Planner (2)

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
        response += "e.g If you wish to delete 1) PW Meeting, please select 1\n"
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


#### End Of Personal Planner Code #####

###############################################################

#### Function VIEW MODULE CODES ########

##### VIEW MODULES FUNCTION #####
@bot.message_handler( regexp = "View Modules" )
def view_modules( view ):
    userid = str(view.chat.id) # User's unique ID
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
    else: # If the User has no modules to view
        button1 = telebot.types.KeyboardButton( "Add module" )
        button2 = telebot.types.KeyboardButton( "Return to Main" )
        markup = telebot.types.ReplyKeyboardMarkup( resize_keyboard = True, one_time_keyboard = True )
        markup.add(button1).add(button2)
        bot.send_message( int(userid), "You have no modules, please procede to add modules.", reply_markup = markup ) # Reply message with options to procede
        
##### GO TO ADD MODULE FUNCTION #####
@bot.message_handler( regexp = "Add module" )
def add_another_module( text ):
    bot.send_message( text.chat.id, "Please enter the module code." )

##### ADD MODULE FUNCTION #####   
@bot.message_handler( func = lambda x: True if x.text.upper() in modcodes else False )
def add_module( mod_code ):
    userid = str(mod_code.chat.id) # User's unique ID
    formtext = mod_code.text.upper() # Proper format of module code
    doc_ref = db.collection( "users" ).document( userid ).collection( "all_mods" ).document( "all_mods" ) # Reference to check if input module is in DB
    doc = doc_ref.get().to_dict() # Dictionary of all User's modules, can be empty
    if formtext in doc.keys(): # If module is already in User's modules
        title = doc[ formtext ] # Title of module
        bot.send_message( int(userid), formtext + ": " + title + ", is already in your list of modules." ) # Reply message
    else:
        db.collection( "users" ).document( userid ).collection( "mods" ).document( formtext ).set({}) # Create a document for the new module with empty dictionary as field
        mod_details_req = requests.get( mod_details_end.replace( replace_ay, ay ).replace( replace_mod, formtext ) ) # API request for details of input module
        mod_details = mod_details_req.json() # All details for input module
        title = mod_details["title"] # Title of module
        mod_tt = mod_details["semesterData"][semester]['timetable'] # All lesson types and slots of the module for the current semester
        mod_lesson_types = []
        for i in mod_tt: # mod_lesson_types will be a List of the different lesson types at the end of this For loop
            if i[ "lessonType" ] not in mod_lesson_types:
                mod_lesson_types.append( i["lessonType"] )
        db.collection( "users" ).document( userid ).collection( "all_mods" ).document( "all_mods" ).set( {formtext: title }, merge = True ) # Add module code and title to all_mods document
        for i in mod_lesson_types: # In the new module document, create a new collection and in this collection, create documents for each lesson type to store timings and venues in the future
            db.collection( "users" ).document( userid ).collection( "mods" ).document( formtext ).collection( "lessons" ).document( f'{formtext} {i}' ).set( {"config" : False} )
        bot.send_message( int(userid), "Ok, I have added " + formtext + ": " + title + ", to your modules." ) # Reply message
    button1 = telebot.types.KeyboardButton( "View modules" )
    button2 = telebot.types.KeyboardButton( "Add module" )
    button3 = telebot.types.KeyboardButton( "Delete module" )
    button4 = telebot.types.KeyboardButton( "Return to Main" )
    markup = telebot.types.ReplyKeyboardMarkup( resize_keyboard = True, one_time_keyboard = True )
    markup.add( button1 ).add( button2 ).add( button3 ).add( button4 )
    bot.send_message( int(userid), "What would you like to do?" , reply_markup = markup ) # Reply message with options to procede

##### GO TO DELETE MODULE FUNCTION #####
@bot.message_handler( regexp = "Delete module" )
def go_delete_module( text ):
    userid = str(text.chat.id) # User's unique ID
    doc_ref = db.collection( "users" ).document( userid ).collection( "all_mods" ).document( "all_mods" ) # Reference to check if User has any modules to delete
    doc = doc_ref.get().to_dict() # Dictionary of all User's modules, can be empty
    if len(doc) > 0: # If User has modules to delete
        markup = telebot.types.ReplyKeyboardMarkup( resize_keyboard = True, one_time_keyboard = True )
        for mod_code in doc.keys():
            button = telebot.types.KeyboardButton( "Delete " + mod_code )
            markup.add( button )
        button = telebot.types.KeyboardButton( "Return to Main" )
        markup.add( button )
        bot.send_message( int(userid), "What would you like to do?", reply_markup = markup ) # Reply with options on what to delete, or Return to Main
    else: # User has no modules to delete
        button1 = telebot.types.KeyboardButton( "Add module" )
        button2 = telebot.types.KeyboardButton( "Return to Main" )
        markup = telebot.types.ReplyKeyboardMarkup( resize_keyboard = True, one_time_keyboard = True )
        markup.add( button1 ).add( button2 )
        bot.send_message( int(userid), "You have no modules, please procede to add modules.", reply_markup = markup ) # Reply with options to Add module or Return to Main

##### CUSTOM FILTER TO FILTER MESSAGES STARTING WITH ... #####

class TextStartsFilter( telebot.custom_filters.AdvancedCustomFilter ):
    key: str = "text_startswith"
    def check( self, message, text ):
        return message.text.startswith( text )

bot.add_custom_filter( TextStartsFilter() )

##### DELETE MODULE FUNCTION #####
@bot.message_handler( text_startswith = "Delete " )
def delete_module( mod_code ):
    userid = str(mod_code.chat.id) # User's unique ID
    mod_to_delete = mod_code.text[ 7: ] # Module code of module to delete, in  proper format
    title = db.collection( "users" ).document( userid ).collection( "all_mods" ).document( "all_mods" ).get().to_dict()[ mod_to_delete ] # Title of module
    db.collection( "users" ).document( userid ).collection( "mods" ).document( mod_to_delete ).delete()
    db.collection( "users" ).document( userid ).collection( "all_mods" ).document( "all_mods" ).update( { mod_to_delete : firestore.DELETE_FIELD } )
    button1 = telebot.types.KeyboardButton( "View modules" )
    button2 = telebot.types.KeyboardButton( "Add module" )
    button3 = telebot.types.KeyboardButton( "Delete module" )
    button4 = telebot.types.KeyboardButton( "Return to Main" )
    markup = telebot.types.ReplyKeyboardMarkup( resize_keyboard = True, one_time_keyboard = True )
    markup.add( button1 ).add( button2 ).add( button3 ).add( button4 )
    bot.send_message( int(userid), mod_to_delete + ": " + title + ", has been deleted from your modules." ) # Reply message
    bot.send_message( int(userid), "Please select the relevant options.", reply_markup = markup ) # Reply message with options to procede

##############################################################################################################
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


##############################################################################################################
# Function 6) Report Issues

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
    
#### End of Function 6 Report Issues

##############################################################################################################




##############################################################################################################
##### PLEASE ENSURE THIS STAYS AT THE BOTTOM OR FUNCTIONS WILL BREAK! #####
##### INVALID TEXT FUNCTION #####
@bot.message_handler()
def invalid_text( text ):
    bot.send_message( text.chat.id, "Invalid entry, you will be returned to the Main Menu." )
    main( text )
    

bot.infinity_polling()

##### PLEASE ENSURE THIS STAYS AT THE BOTTOM OR FUNCTIONS WILL BREAK! #####
# #############################################################################################################