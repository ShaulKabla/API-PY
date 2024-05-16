## The code have 4 main classes: GetRequests, Postrequests, Putrequests, DeleteRequests ##
## Global access vars from main progrem will be the base url, headers, auth token ##
## auth token is genreates in auto.py using hash value of the key ##
## encrypt.py using AES & SHA256 ## Going to change the method to pyc & input user


import requests
import json
import time
from auth import authentication_token


# Class for menu and maybe other things    
class WarCrewTool:
   
   # Must to find better way for the menu
   @staticmethod
   def display_menu():
        print("----Welcome to WarCrew Automated Tool-----")
        print("1. Create Servers")
        print("2. Clone Servers")
        print("2. List Locations")
        print("3. Get Server ID")
        print("4. List Servers")
        print("5. Process status")
        print("6. View Notes")
        print("7. Power On/Off server")
        print("8. Exit")

        choice = input("Enter your choice (1-7): ")
        return choice

# Class from API doc for the options
class Lists:
   @staticmethod
   def cpu_list():
      cpu_list = [
         "1A", "2A", "4A",
         "1B", "2B", "4B",
         "1T", "2T", "4T", "6T",
         "1D", "2D", "4D", "6D", "8D"
      ]
      return cpu_list
  
   @staticmethod
   def ram_list():
      ram_list = [256, 512, 1024, 2048, 3072, 4096, 6144, 8192, 10240, 122288, 16384]
      return ram_list
      
   @staticmethod
   def disk_size_list():
      disk_size_list = [5, 10, 15, 20, 30, 40, 50, 60, 80, 100, 150, 200, 250, 300, 350, 400, 450, 500, 600, 700, 800, 900, 1000, 1500, 2000, 3000, 4000]
      return disk_size_list

   # Using the first server from "GetServer" Etc: service_rancher
   # The disk_src is the image for the server.
   @staticmethod
   def disk_src_list():
      disk_src_list = {
   }
      return disk_src_list

    
# Classes for Errors. Not working yet    
class ErrorHandler:
    @staticmethod  
    def genral_error(error):
        print(f"Somthing Wrong... Exiting progrem. Error: {error}")
        
    def userinput_error(error):
        print("You Entered Invalid params")
class Errors(Exception):
    def exc():
        if Exception : pass        

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
        return response.json()
    
    # GetServers API 
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

    def get_server_id_by_name(self): # Get All server of the client API or Admin dep
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
        print(f"Response data: {queue_id}")  # debug
        print(f"Response data: {url}")  # debug
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
        if isinstance(ok_data, list) and len(ok_data) == 1: # Handle queue [] ID list
            ok_data = ok_data[0]
        return ok_data
    elif response.status_code == 404:  # For Debug
        print("Error 404:")
        print(response.content.decode("utf-8"))
    elif response.status_code == 500:  # For Debug
        print("Error 500:")
        print(response.content.decode("utf-8"))
    else:
        print("Error:", response.status_code)
        print(response.content.decode("utf-8"))
    return response


    # Post create server using fun user_data_server
   def create_server(self):
    url = self.base_url + "/service/server"
    params = UserInput.user_data_server()  # Call the method to get the parameters
    if params:  # Check if parameters were returned
        print("Creating the Server ...")
        post_id_server = self.post(url, data=params)
        self.notes.add_note(f"Creating Server: {post_id_server}")
        print(f"Queue ID: {post_id_server}")
    else:
        print("Server creation cancelled.")




   def clone_server(self):
    url = self.base_url + "/service/server/clone"
    params, clone_loop, base_clone_name = UserInput().user_clone_server()

    if params:
        print("Cloning the Servers ...")
        clone_loop = int(clone_loop)
        for i in range(clone_loop):
            params["name"] = f"{base_clone_name}.{i}"
            print(params)
            post_clone_server = self.post(url, data=params)
            if post_clone_server:
                queue_id = post_clone_server
                self.notes.add_note(f"Cloning Server {i}: {queue_id}")
                print(f"Server {i} Queue ID: {queue_id}")
                time.sleep(10)
                # Wait until the queue status is "complete"
                get_requests = GetRequests(self.base_url, self.auth_headers, self.auth_token, self.notes)
                while True:
                    queue_status = get_requests.get_queue_status(queue_id)
                    if queue_status["status"] == "complete":
                        print(f"{base_clone_name}.{i} cloning completed successfully.")
                        break
                    else:
                        print(f"Server {i} cloning is in progress. Status: {queue_status['status']}")
                        time.sleep(120)
    else:
        print("Server cloning failed.")
   
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
       
# Class for all Put req  
class PutRequest:
   def __init__(self, base_url, auth_headers, json_headers, auth_token):
       self.base_url = base_url
       self.auth_token = auth_token
       self.auth_headers = auth_headers
       
    # Basic Put Req   
   def put(self, url, data):
        response = requests.put(url, headers=self.auth_headers, data=data)
        if response.status_code == 200:
            ok_data = response.json()
            print("Success!")
            return ok_data
        elif response.status_code == 500: # For Debug
            print("Error 500:")
            print(response.content.decode("utf-8"))
        else:
            print("Error:", response.status_code)
            print(response.content.decode("utf-8"))
        return response
    
   def server_power(self):
       server_id = input("Enter valid server ID: ")
       url = f"{self.base_url}/service/server/{server_id}/power"
       power_choice = input("1.Power On/2.Power Off: ")
       
       if power_choice == '1':         
            data = {
                "power": "on"
            }
            print("Power Up...")
       elif power_choice == '2':
            data = {
                "power": "off"
            }
            print("ShutDown...")
       else:
           # Code for handle errors
           pass
       request = self.put(url, data)
       return request
# Class for all User Input die in hell        
class UserInput:
      def user_data_server():
         name_server = input("Enter the name of the server: ")
         
         # Using the first server from "GetServer" Etc: service_rancher
         
         while True:
            datacenter = input("Enter DataCenter: ")
            if datacenter.upper() not in Lists.disk_src_list().keys():
                  print("Invalid")
                  continue
            else:
                  break
         
         while True:
            disk_src = input("Enter Disk Source: ")
            if disk_src not in Lists.disk_src_list().values():
                  print("Invalid")
                  continue
            else:
                  break

         while True:
            cpu = input("Enter CPU: ")
            if cpu.upper() not in Lists.cpu_list():
                  print("Invalid.")
                  continue
            else:
                  break
               
         while True:
            disk_size = input("Enter Disk Size(GB): ")
            disk_size = int(disk_size)
            if disk_size not in Lists.disk_size_list():
               print("Invalid.")
               continue
            else:
               break


         while True:
            ram = input("Enter Ram(MB): ")
            if ram not in [str(r) for r in Lists.ram_list()]:
                  print("Invalid.")
            else:
                  break

         while True:
            password = input("Enter Password: ")
            if len(password) >= 12 and any(char.isupper() for char in password) and any(char.isdigit() for char in password) and any(char in "!@#$%^&*()-_=+`~,.<>/\\?|{}[]" for char in password):
                  break
            else:
                  print("Weak Password")

         while True:
            billing = input("Enter Billing Method(1.Monthly/2.Hourly): ")
            if billing == "1":
                  billing = "monthly"
                  break
            elif billing == "2":
                  billing = "hourly"
                  break
            else:
                  print("Invalid Method")
            
         while True:
            traffic = input("Choose Traffic(1.World/2.Asia): ")
            if traffic == "1":
               traffic = "t5000"
               break
            elif traffic =="2":
               traffic = "t1000"
               break
            else:
               print("Invalid Input")


         while True:
            network_name = input("Network name(1.Wan/2.Lan): ")
            if network_name == "1":
                  network_name = "wan"
                  params = {
                     "disk_src_0": disk_src,
                     "datacenter": datacenter,
                     "name": name_server,
                     "cpu": cpu,
                     "ram": ram,
                     "password": password,
                     "billing": billing,
                     "network_name_0": network_name,
                     "disk_size_0": disk_size,
                     "traffic": traffic
                  }
                  
                  return params
            
            elif network_name == "2":
                  params = {
                     "disk_src_0": disk_src,
                     "datacenter": datacenter,
                     "name": name_server,
                     "cpu": cpu,
                     "ram": ram,
                     "password": password,
                     "billing": billing,
                     "traffic": traffic,
                  }
                  

                  num_lans = int(input("How many LANs do you want to create?: "))

                  while True:
                    lan_net_bits = input("Enter Network Bits for all LANs: ")
                    if lan_net_bits.isdigit() and int(lan_net_bits) in range(20, 31):
                        lan_net_bits = int(lan_net_bits)
                        break
                    else:
                        print("Invalid input. 20-30")

                  while True:
                    num_lans = int(input("How many LANs do you want to create?: "))
                    if num_lans.isdigit() and int(num_lans) in range(231): #prefix 24 with reserved Ip's
                        num_lans = int(num_lans)
                        break
                    else:
                        print("Invalid input.")
                  
                  lan_name_base = input("Enter Lan Network Name: ")

                  for i in range(num_lans):
                     lan_name = f"lan-{lan_name_base}"
                     lan_ip = input(f"Enter IP{i} for the server:{name_server}{i}: ")

                     octets = lan_ip.split('.')
                     octets[-1] = str(int(octets[-1]) + i)
                     lan_ip = '.'.join(octets)

                     params[f"network_name_{i}"] = lan_name
                     params[f"network_ip_{i}"] = lan_ip
                     params[f"network_bits_{i}"] = lan_net_bits

                  return params
            else:
                  print("Invalid Choose")



      def user_clone_server(self):  
        clone_source_id = input("Enter server ID to clone: ")  # Will create fun to check id with get serverid
        base_clone_name = input("Enter base name for the clones: ")

        # to not overload CWM Limiting to 10 clones per request
        while True:
            clone_loop = input("How many clones you want to create? (Max: 7): ")
            if clone_loop.isdigit() and int(clone_loop) in range(1, 8):
                clone_loop = int(clone_loop)
                break
            else:
                print("Invalid input. Please enter a number between 1 and 7.")

        while True:
            password = input("Enter Password: ")
            if len(password) >= 12 and any(char.isupper() for char in password) and any(
                    char.isdigit() for char in password) and any(
                char in "!@#$%^&*()-_=+`~,.<>/\\?|{}[]" for char in password):
                break
            else:
                print("Weak Password")

        while True:
            billing = input("Enter Billing Method (1.Monthly/2.Hourly): ")
            if billing == "1":
                billing = "monthly"
                break
            elif billing == "2":
                billing = "hourly"
                break
            else:
                print("Invalid Method")

        params = {
            "source": clone_source_id,
            "name": base_clone_name,
            "password": password,
            "billing": billing,
        }

        return params, clone_loop, base_clone_name  # Returning base_clone_name

      
# Class for Notes
class Notes:
    def __init__(self):
        self.notes = []

    def add_note(self, note):
        self.notes.append(note)

    def get_notes(self):
        return self.notes
            

def main():
    base_url = ""

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
            post_request = PostRequest(base_url, auth_headers, json_headers, authentication_token, notes)
            post_request.clone_server()
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
            get_requests = PutRequest(base_url, auth_headers, authentication_token, notes).server_power()
        elif choice == "8":
            print("----Thank You for using WarCrew Automated Tool-----")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
