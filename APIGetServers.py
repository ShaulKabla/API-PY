import requests
import json

# API URL
base_url = ""

# Auth
client = ""
secret = ""

def get_servers():
    url = base_url + "/service/servers"

    # Authirztion
    headers = {
        "AuthClientId": client, 
        "AuthSecret": secret
    }

    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        ok_json_data = response.json()
        print(f"Json Data: {ok_json_data}")
    else:
       print("Error:", response.status_code)
    return None


get_servers()
