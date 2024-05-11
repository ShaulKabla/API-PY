import requests
from encrypt import decrypt_api, load_key_from_file, encrypted_client, encrypted_secret

base_url = "https://console.kamatera.com"

key = load_key_from_file("keys.txt")

# Decrypt the encrypted client ID and secret
decrypted_client = decrypt_api(key, encrypted_client)
decrypted_secret = decrypt_api(key, encrypted_secret)

def post_create_server():
    url = base_url + "/service/authenticate"

    # Auth not working when added ID's to the header
    headers = {
        "Content-Type": "application/json"
    }

    # JSON data using the decrypted vars
    json_data = {
        "clientId": decrypted_client,  
        "secret": decrypted_secret   
    }

    # Send POST request with JSON auth data
    response = requests.post(url, headers=headers, json=json_data)
    
    if response.status_code == 200:
        ok_data = response.json()
        authentication_token = ok_data['authentication']
        expires = ok_data['expires']
        print("Authentication token:", authentication_token)
        return authentication_token
    elif response.status_code == 500: # For Debug
        print("Error 500 Internal Server Error. Response content:")
        print(response.content.decode("utf-8"))
    else:
       print("Error:", response.status_code)
       return None

authentication_token = post_create_server()
