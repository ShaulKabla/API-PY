import requests
import json

# API URL
# Py server test
base_url = "https://console.kamatera.com"
test_server_id = "564d0f9c-b51e-a483-5463-cd528c32d226"

# Auth keys - *Problem* - Will secure it.
client = "19c46c2899b11d00fe359f94a826bfc8"
secret = "d467c344850d233e7872f10561cd9505"

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

    # Storing the ID Ticket in var for future use

    SucessID = str(ok_data)
    return None


put_power()