import requests
import json

# API URL
base_url = "https://console.kamatera.com"

# Auth
client = "19c46c2899b11d00fe359f94a826bfc8"
secret = "d467c344850d233e7872f10561cd9505"

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