import requests
import json

# API URL
base_url = ""

# Auth
client = ""
secret = ""

def post_create_server(): # Warning, Valid Request
    url = base_url + "/service/server"

    # Authirztion
    # Adding Content-Type cuz somtimes the server using xxx-format
    headers = {
        "AuthClientId": client, 
        "AuthSecret": secret,
        "Content-Type": "application/x-www-form-urlencoded"
    }


    # Failed to use JSON for that.
    xxxform_data = {
        "name": "WarCrew-py-api-test",
        "cpu": "2D",
        "ram": 1024,
        "password": "Password123!",
        "billing": "monthly",
        "network_name_0": "wan",
        "network_ip_0": "192.168.100.1",
        "network_bits_0": 24,
        "disk_size_0": 50,
        "traffic": "t5000",
        "disk_src_0": "IL:Real-Number",
        "datacenter": "IL"
    }

    response = requests.post(url, headers=headers, data=xxxform_data)
    
    if response.status_code == 200:
        ok_data = response.json()
        print(f"Data for 200 OK Response: {ok_data}")
    elif response.status_code == 201: # After Succsus checking got 200. not sure why
        ok_data = response.json()
        print(f"Data for 201 Created Response: {ok_data}")
    elif response.status_code == 500: # For Debug
        print("Error 500 Internal Server Error. Response content:")
        print(response.content.decode("utf-8"))
    else:
       print("Error:", response.status_code)

    # Storing the ID Ticket in var for future use

    SucessID = str(ok_data)
    return None


post_create_server()
