## The code have 4 main classes: GetRequests, Postrequests, Putrequests, DeleteRequests ##
## Global access vars from main progrem will be the base url, headers, auth token ##
## auth token is genreates in auto.py using hash value of the key ##


import requests
import json
from auth import authentication_token

class WarCrewTool:
   
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
        "IL:0",
        "IL:0",
        "IL:0"
    ]

    print(f"\nList of Locations: {list_of_locations}")

# Checked and varifed.
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
        elif response.status_code == 500:  # For Debug
            print("Error 500:")
            print(response.content.decode("utf-8"))
        else:
            print("Error:", response.status_code)
        return response

    def get_servers(self):
        url = self.base_url + "/service/servers"
        servers = self.get(url)
        return servers

    def print_servers(self, servers):
        if servers:
            print("List of Servers:")
            for server in servers:
                print(f"Server ID: {server['id']}, Name: {server['name']}, DC: {server['datacenter']}, Power: {server['power']}")
                print(f"----------------------------------------")
        else:
            print("No servers found.")

    def get_server_id_by_name(self):
        server_name = input("Enter Server Name: ")
        servers = self.get_servers()
        matching_servers = [server for server in servers if server['name'] == server_name]
        if matching_servers:
            print("----------------------------------------")
            for server in matching_servers:
                print(f"Server ID for '{server_name}': {server['id']}")
                print("----------------------------------------")
        else:
            print(f"No server found with the name '{server_name}'")




class PostRequest:
   def __init__(self, base_url, headers, auth_token):
       self.base_url = base_url
       self.auth_token = auth_token
       self.headers = headers

   def post(self, url, data):
        response = requests.post(url, headers=self.headers, data=data)
        if response.status_code == 200:
            ok_data = response.json()
            return ok_data
        elif response.status_code == 500: # For Debug
            print("Error 500:")
            print(response.content.decode("utf-8"))
        else:
            print("Error:", response.status_code)
        return response

   def post_request(self):
        while True:
            print('''
                1. Create Server
                2. Power on/off 
                3. Clone Server(Req: Server ID): 
                4. Create New Disk For Server(Req: ID): 
                5. Create SnapShot For Server: 
                6. Clone Disk To HDlib 
            ''')

            user_choice = input("Choose Action: ")
            if user_choice == "1":
                # Code for creating server
                pass
            elif user_choice == "2":
                data = self.server_power()
                # Code for power on/off
                pass
            elif user_choice == "3":
                # Code for cloning server
                pass
            elif user_choice == "4":
                # Code for creating new disk for server
                pass
            elif user_choice == "5":
                # Code for creating snapshot for server
                pass
            elif user_choice == "6":
                # Code for cloning disk to HDlib
                pass
            else:
                print("Invalid choice. Please select a valid option.")

## Taking input from the user for creating a server
## 

   def user_data_server(self):
    name_server = input("Enter the name of the server: ")
    disk_src = input("Enter Disk Source: ") # Still not sure how the storage orginzed
    cpu = input("Enter CPU: ")
    ram = input("Enter Ram: ")
    password = input("Enter Password: ")
    billing = input("Billing (monthly/hourly): ")
    network_name = input("Network name(wan/la-1-**lan-network-name**): ") # wan for automated process
    
    if network_name == "wan": # wan auto conf (can't blank - api)
        network_ip = "192.168.100.1"
    else:
        network_ip = input("Enter valid IP: ")

    network_bits = "24"
    disk_size = input("Enter Disk Size: ")
    traffic = input("Choose Traffic(1.World/2.Asia): ")
    if traffic == "1":
        traffic = "t5000"
    else:
        traffic = "t1000"

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


   def create_server(self):
       url = self.base_url + "/service/server"


       response = requests.post(url, headers=headers, data=data)

def main():
    base_url = "https://console.kamatera.com"

    headers = {
        "Authorization": "Bearer " + authentication_token,
    }

    while True:
        choice = WarCrewTool.display_menu()

        if choice == "1":
            PostRequest(base_url, headers, authentication_token).create_servers()
        elif choice == "2":
            WarCrewTool.list_locations()
        elif choice == "3":
            GetRequests(base_url, headers, authentication_token).get_server_id_by_name()
        elif choice == "4":
            get_requests = GetRequests(base_url, headers, authentication_token)
            servers = get_requests.get_servers()
            get_requests.print_servers(servers)
        elif choice == "5":
            print("----Thank You for using WarCrew Automated Tool-----")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
