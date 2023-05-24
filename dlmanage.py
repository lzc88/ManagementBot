import os
import dotenv
import telebot
import firebase_admin
from firebase_admin import firestore
import datetime
import requests
import json
from datetime import datetime

dotenv.load_dotenv()

bottoken = os.getenv("bottoken")
bot = telebot.TeleBot(bottoken)

dbpath = os.getenv("dbpath")
cred = firebase_admin.credentials.Certificate(dbpath)
dbapp = firebase_admin.initialize_app( cred )
db = firestore.client()

replace = "{acadYear}"
mods_basic_end = os.getenv( "allmods" )

mods_basic_req = requests.get( mods_basic_end.replace( replace, "2022-2023") )
mods_basic = mods_basic_req.json() # List of dictionaries, each dictionary represents a module
modcodes = []
for i in mods_basic:
    modcodes.append( i["moduleCode"]) # List of all module codes

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
    reply_text = "Hello " + returntomain.chat.first_name + ", what would you like to do?"
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
    doc_ref = db.collection( "users" ).document( userid )
    doc = doc_ref.get()
    if doc.exists:
        main( startmessage )
    else:
        data = { "username" : username }
        db.collection( "users" ).document( userid ).set( data )
        bot.send_message( startmessage.chat.id, "Hello " + username +", I am ManagementBot. I hope to assist you in better planning your schedule!" )
        bot.send_message( startmessage.chat.id, "What modules are you taking this semester? (Please enter the first module code)" )

##### ADDING MODULE FUNCTION #####       
@bot.message_handler( func = lambda x: True if x.text.upper() in modcodes else False )
def add( mod_code ):
    userid = str( mod_code.chat.id )
    formtext = mod_code.text.upper()
    doc_ref = db.collection( "users" ).document( userid ).collection( "mods" ).document( "all_mods" )
    doc = doc_ref.get().to_dict()
    if formtext in doc.keys():
        doc = doc_ref.get().to_dict()
        bot.send_message( mod_code.chat.id, formtext + ": " + doc["title"] + ", is already in your list of modules." )
    else:
        db.collection( "users" ).document( userid ).collection( "mods" ).document( formtext ).set( {} )
        for i in mods_basic:
            if i["moduleCode"] == formtext:
                data = i
                mod_title = i["title"]
                db.collection("users").document( userid ).collection( "mods" ).document( "all_mods" ).set( {formtext: None}, merge = True )
                db.collection("users").document( userid ).collection( "mods" ).document( formtext ).collection( "module_info" ).document("basic_info").set(data)
                break # Break the for loop once done
        bot.send_message( mod_code.chat.id, "Ok, I have added " + formtext + ": " + mod_title + ", to your modules." )
    button1 = telebot.types.KeyboardButton( "Add module" )
    button2 = telebot.types.KeyboardButton( "Return to Main" )
    markup = telebot.types.ReplyKeyboardMarkup( resize_keyboard = True, one_time_keyboard = True )
    markup.add( button1 ).add( button2 )
    bot.send_message( mod_code.chat.id, "Please select the relevant options." , reply_markup = markup )

##### ADD ANOTHER MODULE FUNCTION #####
@bot.message_handler( regexp = "Add module" )
def add_another_module( add_another ):
    userid = add_another.chat.id
    bot.send_message( add_another.chat.id, "Please enter the module code." )

##### GO TO DELETE MODULE FUNCTION #####
@bot.message_handler( regexp = "Delete module" )
def go_delete_module( text ):
    userid = str( text.chat.id )
    doc_ref = db.collection( "users" ).document( userid ).collection( "mods" ).document( "all_mods" )
    doc = doc_ref.get()
    if doc.exists:
        doc = doc.to_dict()
        markup = telebot.types.ReplyKeyboardMarkup( resize_keyboard = True, one_time_keyboard = True )
        for mod_code in doc.keys():
            button = telebot.types.KeyboardButton( "Delete " + mod_code )
            markup.add( button )
        button = telebot.types.KeyboardButton( "Return to Main" )
        markup.add( button )
        bot.send_message( text.chat.id, "Please select an option.", reply_markup = markup )
    else:
        button1 = telebot.types.KeyboardButton( "Add module" )
        button2 = telebot.types.KeyboardButton( "Return to Main" )
        markup = telebot.types.ReplyKeyboardMarkup( resize_keyboard = True, one_time_keyboard = True )
        markup.add( button1 ).add( button2 )
        bot.send_message( text.chat.id, "You have no modules. Please procede to add modules.", reply_markup = markup )

class TextStartsFilter( telebot.custom_filters.AdvancedCustomFilter ):
    key: str = "text_startswith"
    def check( self, message, text ):
        return message.text.startswith( text )

bot.add_custom_filter( TextStartsFilter() )

##### DELETE MODULE FUNCTION #####
@bot.message_handler( text_startswith = "Delete " )
def delete_module( delete ):
    def delete_collection_db( collection_ref, batch_size ):
        docs_in_collection = collection_ref.list_documents( page_size = batch_size )
        for doc in docs_in_collection:
            doc.delete()
    userid = str( delete.chat.id )
    mod_to_delete = delete.text[ 7: ]
    db.collection( "users" ).document( userid ).collection( "mods" ).document( mod_to_delete ).delete()
    db.collection( "users" ).document( userid ).collection( "mods" ).document( "all_mods" ).update( { mod_to_delete : firestore.DELETE_FIELD } )
    button1 = telebot.types.KeyboardButton( "View modules" )
    button2 = telebot.types.KeyboardButton( "Return to Main" )
    markup = telebot.types.ReplyKeyboardMarkup( resize_keyboard = True, one_time_keyboard = True )
    markup.add( button1 ).add( button2 )
    bot.send_message( delete.chat.id, mod_to_delete + " has been deleted from your modules." )
    bot.send_message( delete.chat.id, "Please select the relevant options.", reply_markup = markup )

##### VIEW MODULES FUNCTION #####
@bot.message_handler( regexp = "View Modules" )
def view_modules( view ):
    userid = str(view.chat.id)
    doc_ref = db.collection( "users" ).document( userid ).collection( "mods" ).document("all_mods")
    doc = doc_ref.get().to_dict()
    if len(doc) > 0:
        doc = doc.to_dict()
        output = "Here are your modules: \n\n"
        for mod_code in doc.keys():
            output += mod_code + "\n"
        bot.send_message( view.chat.id, output )
        button1 = telebot.types.KeyboardButton( "Add module" )
        button2 = telebot.types.KeyboardButton( "Delete module" )
        button3 = telebot.types.KeyboardButton( "Return to Main" )
        markup = telebot.types.ReplyKeyboardMarkup( resize_keyboard = True, one_time_keyboard = True )
        markup.add( button1 ).add( button2 ).add( button3 )
        bot.send_message( view.chat.id, "What would you like to do?" , reply_markup = markup )
    else:
        button1 = telebot.types.KeyboardButton( "Add module" )
        button2 = telebot.types.KeyboardButton( "Return to Main" )
        markup = telebot.types.ReplyKeyboardMarkup( resize_keyboard = True, one_time_keyboard = True )
        markup.add(button1).add(button2)
        bot.send_message( view.chat.id, "You have no modules added, please procede to add modules.", reply_markup = markup )

@bot.message_handler()
def invalid_text( text ):
    bot.send_message( text.chat.id, "Invalid entry, you will be returned to the Main Menu." )
    main( text )
    
##############################################################################################
# FOR DEADLINE (1)
    
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
    else:
        response = "Yay! You have no pending deadlines, keep up the good work!"

    bot.reply_to(message, response)


# To allow users to mark as completion
@bot.message_handler(func=lambda message: message.text.lower() == "/completed")
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
                pending_assignments.append((deadline['id'], deadline['title']))  # Include assignment ID
                pending_counter += 1

        if pending_counter == 1:
            response = "You do not have any assignments marked NOT COMPLETED left."
        else:
            response += "To return, please reply 'back'"
            bot.send_message(message.chat.id, response)
            bot.register_next_step_handler(message, process_completed, pending_assignments)

        # Check if all deadlines are completed
        if all(deadline['status'] == "COMPLETED" for deadline in deadlines):
            response = "Yay! You have completed all deadlines, keep up the good work!"
            bot.send_message(message.chat.id, response)
    else:
        response = "Yay! You have no pending deadlines, keep up the good work!"
        bot.reply_to(message, response)

def process_completed(message, pending_assignments):
    user_id = str(message.from_user.id)
    text = message.text.lower()

    if text == "back":
        assignments_deadline(message)
    else:
        try:
            assignment_index = int(text) - 1

            if assignment_index in range(len(pending_assignments)):
                assignment_id, assignment_title = pending_assignments[assignment_index]  # Retrieve assignment ID and title
                deadlines = get_dl(user_id)

                for deadline in deadlines:
                    if deadline['id'] == assignment_id:
                        if deadline['status'] != "COMPLETED":
                            deadline['status'] = "COMPLETED"
                            update_dl(user_id, deadlines)
                            response = f"Congratulations on completing! I have marked '{assignment_title}' as COMPLETED."

                        else:
                            response = "This assignment has already been marked as COMPLETED."
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




# To mark as uncompleted
@bot.message_handler(func=lambda message: message.text == "/uncompleted")
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
        else:
            response += "To return, please reply 'back'"
        bot.send_message(message.chat.id, response)
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

bot.infinity_polling()