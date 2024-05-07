## New client to the company and created servers for him ##
## User intercractive 

import requests
import json

def display_menu():
    print("----Welcome to WarCrew Automated Tool-----")
    print("1. Create Servers")
    print("2. List Locations")
    print("3. Manage Client")
    print("4. Exit")
    choice = input("Enter your choice (1-4): ")
    return choice


def list_locations():
    list_of_locations = {
        "IL-RH": 400,
        "IL-PT": 700,
        "UX-TX": 900
    }
    print("\nList of Locations:")
    for location, value in list_of_locations.items():
        print(f"{location}: {value}")

def get_params():
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
            list_locations()
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

def create_servers():
    base_url = ""
    client = ""
    secret = ""
    url = base_url + "/service/server"
    headers = {
        "AuthClientId": client,
        "AuthSecret": secret,
        "Content-Type": "application/x-www-form-urlencoded"
    }

    num_servers = int(input("Enter the number of servers to create: "))
    valid_params = get_params()

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

def manage_client():
    power = "on"

def main():
    while True:
        choice = display_menu()
        if choice == "1":
            create_servers()
        elif choice == "2":
            list_locations()
        elif choice == "3":
            manage_client()
        elif choice == "4":
            print("----Thank You for using WarCrew Automated Tool-----")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
