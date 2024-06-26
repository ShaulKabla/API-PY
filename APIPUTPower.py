import requests
import json

# API URL
# Py server test
base_url = ""
test_server_id = "Real-server-ID"

# Auth keys - *Problem* - Will secure it.
client = ""
secret = ""

def put_power(): # Warning, Valid Request
    url = f"{base_url}/service/server/{test_server_id}/power"

    # Authirztion
    # Adding Content-Type cuz somtimes the server using xxx-format
    headers = {
        "AuthClientId": client, 
        "AuthSecret": secret,
        "Content-Type": "application/x-www-form-urlencoded"
    }


    # On/Off.
    xxxform_data = {
        "power": "off",
    }

    response = requests.put(url, headers=headers, data=xxxform_data)
    
    if response.status_code == 200:
        ok_data = response.json()
        print(f"Data for 200 OK Response: {ok_data}")
    elif response.status_code == 500: # For Debug
        print("Error 500 Internal Server Error. Response content:")
        print(response.content.decode("utf-8"))
    else:
       print("Error:", response.status_code)


    SucessID = str(ok_data)
    return None


put_power()
