import requests

test = requests.get("https://<canvas-install-url>/login/oauth2/auth?client_id=111&response_type=code&redirect_uri=urn:ietf:wg:oauth:2.0:oob=<value_1>%20<value_2>%20<value_n>")