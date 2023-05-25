import requests
import json

test_token = "21450~ElLuAuUjDyKb5cTRLJ5mUiuTPOS6tNsKoFuO6MGApBLaoYyvqHUYrOTwWxNZ7SOG"

test_url = "https://canvas.instructure.com/api/v1/account_calendars?access_token=<ACCESS-TOKEN>".replace( "<ACCESS-TOKEN>", test_token )

test_get = requests.get( test_url )

test_response = test_get.json()