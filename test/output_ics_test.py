import requests
import icalendar
import datetime

link = "https://canvas.nus.edu.sg/feeds/calendars/user_4E3lALnX0FFXPIZF7obDSz0oGbXRkXEyBBJDf5u9.ics"

link2 = "https://calendar.google.com/calendar/ical/limzhichao88%40gmail.com/private-afa12df71c6b509a7d6a0547cc95545d/basic.ics"

response = requests.get(link).text

cal = icalendar.Calendar.from_ical( response )

for i in cal.walk('vevent'):
   title = str( i.get("summary") )
   due_date = datetime.datetime.fromtimestamp(i.get( "dtstart" ).dt.timestamp()) # Due date is a datetime object
   ol = [ title, due_date ]
   print(ol)

def process_ics_link(file_url):
    try:
        response = requests.get(file_url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error retrieving .ics file: {e}")
        return None
    
print( process_ics_link( "a" ) )
