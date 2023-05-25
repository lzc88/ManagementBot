# To test for outputs when fetching data from Firebase

import firebase_admin
from firebase_admin import firestore

cred = firebase_admin.credentials.Certificate("config\managementbot-72f56-firebase-adminsdk-7fs64-3c7bb1c603.json")
dbapp = firebase_admin.initialize_app( cred )
db = firestore.client()

my_id = "291900788"

# Getting the titles of multiple Documents from a Collection

docs = db.collection( "users" ).document( my_id ).collection( "mods" ).document( "CS1010S" ).collection( "module_info" ).stream()

types = []

for doc in docs:
    types.append( doc.id )

print( types )