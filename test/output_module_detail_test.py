import os
import dotenv
import requests
from datetime import datetime

dotenv.load_dotenv( dotenv_path = "config\.env" )

current_month = datetime.now().month 
if current_month < 8:
    semester = 1
else:
    semester = 0

replace = "{acadYear}"
replace2 = "{moduleCode}"
mods_basic_end = os.getenv( "allmods" )
mod_details_end = os.getenv( "moddetails" )

mod_details_req = requests.get( mod_details_end.replace( replace, "2022-2023" ).replace( replace2, "FIN3703B") )
mod_details = mod_details_req.json()["semesterData"]

unique_lesson_types = []
for i in mod_details:
    if i['lessonType'] not in unique_lesson_types:
        unique_lesson_types.append( i['lessonType'] )


mods_basic_req = requests.get( mods_basic_end.replace( replace, "2022-2023") )
mods_basic = mods_basic_req.json()