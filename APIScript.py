## The code have 4 main classes: GetRequests, Postrequests, Putrequests, DeleteRequests ##
## Global access vars from main progrem will be the base url, headers, auth token ##
## auth token is genreates in auto.py using hash value of the key ##


import requests
import json
from auth import authentication_token

class WarCrewTool:
   def __init__(self, base_url, authentication_token):
       self.base_url = base_url

   @staticmethod
   def display_menu():
    print("----Welcome to WarCrew Automated Tool-----")
    print("1. Create Servers")
    print("2. List Locations")
    print("3. Manage Client")
    print("4. List Servers")
    print("5. Exit")

    choice = input("Enter your choice (1-5): ")
    return choice

   @staticmethod
   def list_locations():
       list_of_locations = [
           "IL:0"
           "IL:0"
           "IL:0"
       ]

       print("\nList of Locations:")

class GetRequests:
    def __init__(self, base_url, headers, authentication_token):
        self.base_url = base_url
        self.authentication_token = authentication_token
        self.headers = headers

    def get(self, url):
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            ok_data = response.json()
            return ok_data
        elif response.status_code == 201:
            ok_data = response.json()
            print(response.content.decode("utf-8"))
        else:
            print("Error:", response.status_code)
        return response

    def get_servers(self):
        url = self.base_url + "/service/servers"
        servers = self.get(url)

        # Formating the response into clear text
        if servers:
            print("\nList of Servers:")
            for server in servers:
                print(f"Server ID: {server['id']}, Name: {server['name']}, DC: {server['datacenter']}, Power: {server['power']}")
                print(f"\n----------------------------------------")

class PostRequest:
   def __init__(self, base_url, auth_token):
       self.base_url = base_url
       self.auth_token = auth_token

   def put_request(self):
       # Code for PUT request
       pass

   def post_request(self):
       list_of_option = [
           "1. Create Server",
           "2. Power on/off",
           "3. Clone Server(Req: Source Server ID): ",
           "4. Create New Disk For Server(Req ID): ",
           "5. Create SnapShot For Server: ",
           "6. Clone Disk To HDlib: "
       ]

       user_choice = input("Choose Action: ")

       if user_choice == "1":
           # Code for creating server
           pass
       elif user_choice == "2":
           data = self.server_power()
           # Code for power on/off
           pass

       response = requests.post(url, headers=headers, data=data)

   def server_power(self):  # Post Call Func for user choice
       power = input("1.Power On/2.Power off: ")
       if power == "1":
           data = {
               "power": "on"
           }
       elif power == "2":
           data = {
               "power": "off"
           }
       return data

   def get_params_create_server(self):
       name_server = input("Enter the name of the server: ")
       cpu = input("Enter CPU: ")
       ram = input("Enter Ram: ")
       password = input("Enter Password: ")
       billing = input("Billing (monthly/hourly): ")
       network_name = "wan"
       network_ip = "192.168.100.1"
       network_bits = "24"
       disk_size = input("Enter Disk Size: ")
       traffic = input("Choose Traffic(1.World/2.Asia): ")
       if traffic == "1":
           traffic = "t5000"
       else:
           traffic = "t1000"
       disk_src = input("Enter Disk Source: ")

       while True:
           datacenter = input("Enter DataCenter (type 'help' for list): ")
           if datacenter == "help":
               WarCrewTool.list_locations()
           else:
               break
       if datacenter == "help":
           return None
       else:
           params = {
               "name": name_server,
               "cpu": cpu,
               "ram": ram,
               "password": password,
               "billing": billing,
               "network_name_0": network_name,
               "network_ip_0": network_ip,
               "network_bits_0": network_bits,
               "disk_size_0": disk_size,
               "traffic": traffic,
               "disk_src_0": disk_src,
               "datacenter": datacenter
           }

           return params

   def create_servers(self):
       url = self.base_url + "/service/server"

       headers = {
           "AuthClientId": client,
           "AuthSecret": secret,
           "Content-Type": "application/x-www-form-urlencoded"
       }

       num_servers = int(input("Enter the number of servers to create: "))

       valid_params = self.get_params_create_server()

       if not valid_params:
           print("Invalid parameters. Exiting Script.")
           return

       for _ in range(num_servers):
           response = requests.post(url, headers=headers, data=valid_params)
           if response.status_code == 200:
               ok_data = response.json()
               print(f"Data for 200 OK Response: {ok_data}")
           elif response.status_code == 201:
               ok_data = response.json()
               print(f"Data for 201 Created Response: {ok_data}")
           elif response.status_code == 500:
               print("Error 500 Internal Server Error. Response content:")
               print(response.content.decode("utf-8"))
           else:
               print("Error:", response.status_code)

       print("All servers created successfully.")

def main():
    base_url = "https://console.kamatera.com"

    headers = {
        "Authorization": "Bearer " + authentication_token,
    }

    while True:
        choice = WarCrewTool.display_menu()

        if choice == "1":
            PostRequest(base_url,headers, authentication_token).create_servers()
        elif choice == "2":
            WarCrewTool.list_locations()
        elif choice == "3":
            # Code for managing client
            pass
        elif choice == "4":
            get_requests = GetRequests(base_url, headers, authentication_token)
            get_requests.get_servers()
        elif choice == "5":
            print("----Thank You for using WarCrew Automated Tool-----")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
   main()
