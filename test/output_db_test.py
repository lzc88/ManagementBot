# To test for outputs when fetching data from Firebase

import firebase_admin
from firebase_admin import firestore

cred = firebase_admin.credentials.Certificate("config\managementbot-72f56-firebase-adminsdk-7fs64-3c7bb1c603.json")
dbapp = firebase_admin.initialize_app( cred )
db = firestore.client()

my_id = "291900788"
days = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]

# Get user's main data

user = db.collection( "users" ).document( my_id ).get().to_dict()
print( user )

# Getting the titles of multiple Documents from a Collection

docs = db.collection( "users" ).document( my_id ).collection( "mods" ).document( "CS1010S" ).collection( "module_info" ).stream()

types = []

for doc in docs:
    types.append( doc.id )

print( types )

# Getting config lesson status of modules

docs2 = db.collection( "users" ).document( my_id ).collection( "mods" ).document( "all_mods" ).get()

docs2out = docs2.to_dict()

# Assignment output for Assignment Deadlines function

ass = db.collection( "users" ).document( my_id ).collection( "dl_data" ).document( "assignments" ).get().to_dict()

for i in ass:
    for x in i:
        print(x)

option = 'Orbital Milestone 2'
#db.collection( "users" ).document( my_id ).collection( "dl_data" ).document( "assignments" ).update( { 'Orbital Milestone 2.status' : True } )

# Lesson slots output

slots = db.collection( "users" ).document( my_id ).collection( "mods" ).document( "ST2131" ).collection( "lessons" ).document( "ST2131 Lecture" ).get().to_dict()["timings"]
print(slots)

# Lesson list output for school timetable function

userid = my_id
week_no = 4
week_ref = db.collection( "users" ).document( userid ).collection( "timetable" ).document( "this_week" )
this_week = week_ref.get().to_dict()
if week_no not in this_week:
    lesson_list = []
    mods = db.collection( "users" ).document( userid ).collection( "mods" ).stream()
    for mod in mods:
        lesson_types = db.collection( "users" ).document( userid ).collection( "mods" ).document( mod.id ).collection( "lessons" ).stream()
        for lesson in lesson_types:
            slots = db.collection( "users" ).document( userid ).collection( "mods" ).document( mod.id ).collection( "lessons" ).document( lesson.id ).get().to_dict()["timings"]
            for slot in slots:
                if week_no in slot["weeks"]:
                    lesson_list.append( slot )

sorted_tt = sorted(sorted( lesson_list, key=lambda x: x["startTime"] ), key = lambda x: days.index( x["day"] ) )
