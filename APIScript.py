## The code have 4 main classes: GetRequests, Postrequests, Putrequests, DeleteRequests ##
## Global access vars from main progrem will be the base url, headers, auth token ##
## auth token is genreates in auto.py using hash value of the key ##
## encrypt.py using AES & SHA256 ##


import requests
import json
from auth import authentication_token

class WarCrewTool:
   
   @staticmethod
   def display_menu():
        print("----Welcome to WarCrew Automated Tool-----")
        print("1. Create Servers")
        print("2. List Locations")
        print("3. Get Server ID")
        print("4. List Servers")
        print("5. Process status")
        print("6. View Notes")
        print("7. Exit")

        choice = input("Enter your choice (1-7): ")
        return choice

   @staticmethod
   def list_locations():
    list_of_locations = [
        "IL:0",
        "IL:0",
        "IL:0"
    ]

    print(f"List of Locations: {list_of_locations}")

# Class for all Get req
class GetRequests:

    def __init__(self, base_url, auth_headers, authentication_token, notes):
        self.base_url = base_url
        self.authentication_token = authentication_token
        self.auth_headers = auth_headers
        self.notes = notes 

    # Base Get Req
    def get(self, url, headers=None):
        if headers is None:
            headers = self.auth_headers
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            ok_data = response.json()
            return ok_data
        elif response.status_code == 500:  # For Debug
            print("Error 500:")
            print(response.content.decode("utf-8"))
        else:
            print("Error:", response.status_code)
        return response
    
    # GetServers API 
    # Valid requests - working
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
            print("----------------------------------------")
            print(f"No server found with the name '{server_name}'")

    def get_queue_status(self, queue_id):
        url = f"{self.base_url}/service/queue/{queue_id}"
        self.notes.add_note(f"Checking queue status for ID: {queue_id}")
        data = self.get(url)
        return data

    
    def print_queue_status(self, status):
        if status:
            print("Queue Status:")
            print(f"Queue ID: {status['id']}\nStatus: {status['status']}\nDescription: {status['description']}\nCompleted: {status['completed']}")
            print("----------------------------------------")
        else:
            print("No data found for the provided queue ID.")
        
    
# Class for all Post req
class PostRequest:
   def __init__(self, base_url, auth_headers, json_headers, auth_token, notes):
       self.base_url = base_url
       self.auth_token = auth_token
       self.auth_headers = auth_headers
       self.json_headers = json_headers
       self.notes = notes

   def post(self, url, data, headers=None):
    if headers is None:
        headers = self.auth_headers  # Use default headers
    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200:
        ok_data = response.json()
        return ok_data
    elif response.status_code == 405:  # For Debug
        print("Error 405:")
        print(response.content.decode("utf-8"))
    elif response.status_code == 500:  # For Debug
        print("Error 500:")
        print(response.content.decode("utf-8"))
    else:
        print("Error:", response.status_code)
    return response

   def post_menu(self):
        while True:
            print('''
                1. Create Server
                2. Clone Server(Req: Server ID): 
                3. Create New Disk For Server(Req: ID): 
                4. Create SnapShot For Server: 
                5. Clone Disk To HDlib
                6. Back to main menu
                7. Exit 
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
                #PostRequest(self.base_url, self.json_headers, authentication_token).create_disk()
                pass
            elif user_choice == "5":
                # Code for creating snapshot for server
                pass
            elif user_choice == "6":
                # Code for cloning disk to HDlib
                pass
            elif user_choice == "7":
                # Code for exit progrem
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

    # Post create server using func user_data_server
    # Varifed working
   def create_server(self):
    url = self.base_url + "/service/server"
    params = self.user_data_server()  # Call the method to get the parameters
    if params:  # Check if parameters were returned
        print("Creating the Server ...")
        post_id_server = self.post(url, data=params)
        self.notes.add_note(f"Creating Server: {post_id_server}")
        print(f"Queue ID: {post_id_server}")
    else:
        print("Server creation cancelled.")
   
   # API Post req to creating new disk
   def create_disk(self): 
       server_id = input("Enter server ID to create disk on: ")
       disk_size = input("Enter disk size(GB): ")
       url = self.base_url + f"/service/{server_id}/disk"
       
       data = {
            "size": disk_size,
            "provision": 0
        }
       # The actual req with JSON headers
       post_create_disk = self.post(url, headers=self.json_headers, data=data)
       print(post_create_disk)
       return None
       
   
class PutRequest:
   def __init__(self, base_url, auth_headers, xxxform_headers, json_headers, auth_token):
       self.base_url = base_url
       self.auth_token = auth_token
       self.xxxform_headers = xxxform_headers
       
    # Basic Put Req   
   def put(self, url, data):
        response = requests.put(url, headers=self.headers, data=data)
        if response.status_code == 200:
            ok_data = response.json()
            return ok_data
        elif response.status_code == 500: # For Debug
            print("Error 500:")
            print(response.content.decode("utf-8"))
        else:
            print("Error:", response.status_code)
        return response
    
   def server_power(self):
       return
   
class Notes:
    def __init__(self):
        self.notes = []

    def add_note(self, note):
        self.notes.append(note)

    def get_notes(self):
        return self.notes
            
    

def main():
    base_url = "https://console.kamatera.com"

    auth_headers = {
        "Authorization": "Bearer " + authentication_token
    }
    
    json_headers = {
        "Authorization": "Bearer " + authentication_token,
        "Content-Type": "application/json"
    }
    notes = Notes()

    while True:
        choice = WarCrewTool.display_menu()

        if choice == "1":
            post_request = PostRequest(base_url, auth_headers, json_headers, authentication_token, notes)
            post_request.create_server()
        elif choice == "2":
            WarCrewTool.list_locations()
        elif choice == "3": 
            GetRequests(base_url, auth_headers, authentication_token, notes).get_server_id_by_name()
        elif choice == "4":
            get_requests = GetRequests(base_url, auth_headers, authentication_token, notes)
            servers = get_requests.get_servers()
            get_requests.print_servers(servers)
        elif choice == "5":
            get_requests = GetRequests(base_url, auth_headers, authentication_token, notes)
            queue_id = input("Enter Queue ID: ")
            status = get_requests.get_queue_status(queue_id)
            get_requests.print_queue_status(status)
        elif choice == "6":
            saved_notes = notes.get_notes()
            if saved_notes:
                print("Notes:")
            for note in saved_notes:
                print(note)
            else:
                print("No notes saved yet.")

        elif choice == "7":
            print("----Thank You for using WarCrew Automated Tool-----")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
