import getpass
import subprocess
from collections import Counter
import re
import json
import csv
from urllib.request import urlopen, Request
import pyfiglet
import os
import openpyxl
import mysql.connector
import requests




nam = input("What is your name? ")
ascii_art = pyfiglet.figlet_format(nam)
print(ascii_art)


############              GET IP ADDRESS              #############
def get_public_ip():
    try:
        response = requests.get('https://api.ipify.org/?format=json')
        ip_data = response.json()
        public_ip = ip_data['ip']
        return public_ip
    except requests.exceptions.RequestException as e:
        print('Error: ', e)
        return None
# Call the function to get the public IP address
public_ip = get_public_ip()
# Print the public IP address
if public_ip:
    print('Your Public IP Address Is:', public_ip)
else:
    print('Failed to retrieve public IP address.')

print()
############   This is for execute the tshark command and put output in a file     #####

capfile = input("Please Enter your .cap file name with extension: ")
if os.path.isfile(capfile):

    command = ['tshark', '-r', capfile, '-T', 'fields', '-e', 'ip.addr']
    output_file = 'extractcapfiles.txt' 
 
    try:
        with open(output_file, 'w') as file:
            subprocess.call(command, stdout=file)
        print("-------------------------------------------------------------")
        print("                     GOOD TO GO WITH OPTIONS  ")
    except subprocess.CalledProcessError as e:
        print(f"Command execution failed: {e}")

    ip_list = []

    with open(output_file, "r") as file:
        lines = file.readlines()
    for line in lines:
        if line.strip():
            ips = line.split(",")
            ip1 = ips[0].strip()
            ip2 = ips[1].strip()
            ip_list.append(ip1)
            ip_list.append(ip2)

    ################################################   Funcations only   #####################################################

    def mainips():
        unique_ips = list(set(ip_list))
        ip_counts = Counter(unique_ips)
        total_ips = len(ip_counts)
        print()
        print("Total number of IPs:", total_ips)
        # print(unique_ips)  It will show like json output.
        for showallips in unique_ips:
            print(showallips)

        print() 
        response = input("Do you want to store those ips in a file? (yes/no): ")
        if response.lower() in ["y", "yes"]:
            enter = input("Enter your file name: ")
            outputips = f"{enter}.txt"
            with open(outputips, 'w') as file:
                for showallips in unique_ips:
                    file.write(showallips + "\n")
            print("IPs output has been saved in", outputips)
        else:
            print("ips is not save in a file")


        ##########         With comma to the ips there are showing some error. I took output in a file with quato and comma   ##########################
        response = input('Do you want those ips like ("185.13.88.201",)  yes/no: ')
        if response.lower() in ["y", "yes"]:
            enter = input("Enter your file name: ")
            output1_file = f"{enter}.txt"
            with open(output1_file, 'w') as file:
                for showallips in unique_ips:
                    result = re.sub(r"([^\n]+)", r'"\1",', showallips).strip()
                    file.write(result + "\n")
            print("Output saved in", output1_file)
        else:
            print("You don't want that")


        ##########        Duplicate ips         ############
        print()
        response = input("Do you want to see the duplicate ips, means How many times some ips are being repeated? (yes/no): ")
        if response.lower() in ["y", "yes"]:
            ip_counts = Counter(ip_list)
            duplicate_ips = {ip: count for ip, count in ip_counts.items() if count > 1}
            print("Duplicate IPs are:")
            for ipcounts, count in duplicate_ips.items():
                print(f"{ipcounts}: {count} times")
        else:
            print("Ok, won't show duplicate ips")


    def duplicateips():
            ip_counts = Counter(ip_list)
            duplicate_ips = {ip: count for ip, count in ip_counts.items() if count > 1}
            print()
            print("Duplicate IPs and are being repeated:")
            for ipcounts, count in duplicate_ips.items():
                print(f"{ipcounts}: {count} times")


    def ipsinexcel():
        unique_ips = list(set(ip_list))
        ip_counts = Counter(unique_ips)
        total_ips = len(ip_counts)
        print("Total number of IPs:", total_ips)
        # ip-api endpoint URL
        # see http://ip-api.com/docs/api:batch for documentation
        endpoint = 'http://ip-api.com/batch'

        # Prepare the request data
        request_data = json.dumps(unique_ips).encode('utf-8')

        # Prepare the request headers
        headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'Batch-Example/1.0'
        }
        # Create the request object
        request = Request(endpoint, data=request_data, headers=headers)

        # Send the request and get the response
        with urlopen(request) as response:
            # Read the response data
            response_data = response.read().decode('utf-8')

            # Parse the JSON response
            data = json.loads(response_data)

            # Create a new Excel workbook and select the active sheet
            workbook = openpyxl.Workbook()
            sheet = workbook.active
            # Write the header row
            header = [
                'IP', 'Status', 'Country', 'Country Code', 'Region', 'Region Name',
                'City', 'ZIP', 'Latitude', 'Longitude', 'Timezone', 'ISP', 'Organization',
                'ASN', 'Query'
            ]
            sheet.append(header)
            # Write the IP information to the Excel file
        # Write the IP information to the Excel file
            for result in data:
                row = [
                    result.get('query', ''), 
                    result.get('status', ''), 
                    result.get('country', ''), 
                    result.get('countryCode', ''), 
                    result.get('region', ''), 
                    result.get('regionName', ''), 
                    result.get('city', ''), 
                    result.get('zip', ''), 
                    result.get('lat', ''), 
                    result.get('lon', ''), 
                    result.get('timezone', ''), 
                    result.get('isp', ''), 
                    result.get('org', ''), 
                    result.get('as', ''), 
                    result.get('query', '')
                ]
                sheet.append(row)

            name = input("Please Keep a file name: ")
            # Save the Excel file
            workbook.save(f"{name}.xlsx")
            print(f"Details have been inserted in {name}.xlsx")


    def ipsincsv():
        unique_ips = list(set(ip_list))
        ip_counts = Counter(unique_ips)
        total_ips = len(ip_counts)
        print("Total number of IPs:", total_ips)
        # ip-api endpoint URL
        # see http://ip-api.com/docs/api:batch for documentation
        endpoint = 'http://ip-api.com/batch'

        # Prepare the request data
        request_data = json.dumps(unique_ips).encode('utf-8')

        # Prepare the request headers
        headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'Batch-Example/1.0'
        }

        # Create the request object
        request = Request(endpoint, data=request_data, headers=headers)

        # Send the request and get the response
        with urlopen(request) as response:
            # Read the response data
            response_data = response.read().decode('utf-8')

            # Parse the JSON response
            data = json.loads(response_data)

        # Save the IP information as a CSV file
        name = input("Please keep the file csv file name: ")
        output_file = (f"{name}.csv")

        with open(output_file, 'w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow([
                'IP', 'Status', 'Country', 'CountryCode', 'Region', 'RegionName',
                'City', 'ZIP', 'Latitude', 'Longitude', 'Timezone', 'ISP', 'Organization',
                'ASN', 'Query'
            ])

            for result in data:
                row = [
                    result.get('query', ''), 
                    result.get('status', ''), 
                    result.get('country', ''), 
                    result.get('countryCode', ''), 
                    result.get('region', ''), 
                    result.get('regionName', ''), 
                    result.get('city', ''), 
                    result.get('zip', ''), 
                    result.get('lat', ''), 
                    result.get('lon', ''), 
                    result.get('timezone', ''), 
                    result.get('isp', ''), 
                    result.get('org', ''), 
                    result.get('as', ''), 
                    result.get('query', '')
                ]
                writer.writerow(row)
        print(f"Details have been saved in {output_file}")


    def ipsinjson():
        unique_ips = list(set(ip_list))
        ip_counts = Counter(unique_ips)
        total_ips = len(ip_counts)
        # see http://ip-api.com/docs/api:batch for documentation
        endpoint = 'http://ip-api.com/batch'

        # Prepare the request data
        request_data = json.dumps(unique_ips).encode('utf-8')

        # Prepare the request headers
        headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'Batch-Example/1.0'
        }
        # Create the request object
        request = Request(endpoint, data=request_data, headers=headers)

        wan = input("Type your file name to get json format output: ")
        # Send the request and get the response
        with urlopen(request) as response:
            # Read the response data
            response_data = response.read().decode('utf-8')

            # Parse the JSON response
            data = json.loads(response_data)
            with open(wan+'.txt', 'w') as file:
                for result in data:
                    file.write(json.dumps(result) + '\n')


    def httprequests(cap_file):
        # Run TShark command to extract HTTP protocol data
        command = ['tshark', '-r', cap_file, '-Y', 'http', '-T', 'fields', '-e', 'http.request.full_uri']
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        
        # Capture and decode the output
        output, _ = process.communicate()
        output = output.decode().strip()

        # Return a list of extracted HTTP requests
        return output.split('\n')
    def mainhttprequests():
        cap_file = capfile
        http_requests = httprequests(cap_file)
        for request in http_requests:
            print(request)


    def postorget(cap_file):
        # Run TShark command to extract HTTP requests
        command = ['tshark', '-r', cap_file, '-Y', 'http.request', '-T', 'fields', '-e', 'http.request.method', '-e', 'http.request.uri']
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        
        # Capture and decode the output
        output, _ = process.communicate()
        output = output.decode().strip()

        # Split the output into individual requests
        requests = output.split('\n')
        # Return the list of extracted HTTP requests
        return requests
    def mainpostget():
        cap_file = capfile
        http_requests = postorget(cap_file)
        for request in http_requests:
            method, uri = request.split('\t')
            print("Method:", method)
            print("URI:", uri)
            print()

    
    def datainsert():
        unique_ips = list(set(ip_list))
        ip_counts = Counter(unique_ips)
        total_ips = len(ip_counts)
        # ip-api endpoint URL
        # see http://ip-api.com/docs/api:batch for documentation
        endpoint = 'http://ip-api.com/batch'

        # Prepare the request data
        request_data = json.dumps(unique_ips).encode('utf-8')

        # Prepare the request headers
        headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'Batch-Example/1.0'
        }

        # Create the request object
        request = Request(endpoint, data=request_data, headers=headers)

        # Send the request and get the response
        with urlopen(request) as response:
            # Read the response data
            response_data = response.read().decode('utf-8')

            # Parse the JSON response
            data = json.loads(response_data)

        # Save the IP information as a CSV file
        # name = input("Please keep the file csv file name: ")
        output_file = ("savehere123savehere.csv")

        with open(output_file, 'w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow([
                'IP', 'Status', 'Country', 'CountryCode', 'Region', 'RegionName',
                'City', 'ZIP', 'Latitude', 'Longitude', 'Timezone', 'ISP', 'Organization',
                'ASN', 'Query'
            ])

            for result in data:
                row = [
                    result.get('query', ''), 
                    result.get('status', ''), 
                    result.get('country', ''), 
                    result.get('countryCode', ''), 
                    result.get('region', ''), 
                    result.get('regionName', ''), 
                    result.get('city', ''), 
                    result.get('zip', ''), 
                    result.get('lat', ''), 
                    result.get('lon', ''), 
                    result.get('timezone', ''), 
                    result.get('isp', ''), 
                    result.get('org', ''), 
                    result.get('as', ''), 
                    result.get('query', '')
                ]
                writer.writerow(row)
    def maindatainsert():
        # GET BASIC DETAILS
        print()
        print("Please type server details for inserting full details of those ips")
        print()
        serverIP = input("Enter your server IP? ")
        username = input("What is your mysql server username? ")
        userpass = getpass.getpass("Put the password: ")
        print()
        print("To create a database or table, just provide their names.")
        print()
        databasename = input("Type the desired name for the DATABASE: ")
        tablename = input("Type the desired name for the TABLE: ")

        config = {
            'host': serverIP,
            'user': username,
            'password': userpass,
            'autocommit': True  # Add autocommit option
        }

        # Create database
        database_name = databasename
        create_database_query = f"CREATE DATABASE {database_name}"

        # Establish connection to MySQL server
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()
        cursor.execute(create_database_query)
        print()
        print(f"Database '{database_name}' created successfully!")

        # Switch to the created database
        cursor.execute(f"USE {database_name}")

        # Column names for the table
        column_names = [
            'IP',
            'Status',
            'Country',
            'CountryCode',
            'Region',
            'RegionName',
            'City',
            'ZIP',
            'Latitude',
            'Longitude',
            'Timezone',
            'ISP',
            'Organization',
            'ASN',
            'Query'
        ]

        datainsert()

        # Open the CSV file
        csv_file_path = 'savehere123savehere.csv'
        with open(csv_file_path, 'r') as file:
            # Check if the table exists, create it if necessary
            table_name = tablename
            cursor.execute(f"SHOW TABLES LIKE '{table_name}'")
            result = cursor.fetchone()

            if not result:
                # Create the table
                columns = ', '.join([f'{column} VARCHAR(255)' for column in column_names])
                create_table_query = f"CREATE TABLE {table_name} ({columns})"
                cursor.execute(create_table_query)
                print(f"Table '{table_name}' created successfully!")

            # Read the CSV file
            csv_data = csv.reader(file)
            next(csv_data)  # Skip the header row if it exists

            # Iterate over each row in the CSV file
            for row in csv_data:
                # Extract the data from the CSV row
                data = tuple(row)

                # Prepare the SQL query
                query = f"INSERT INTO {table_name} ({', '.join(column_names)}) VALUES ({', '.join(['%s'] * len(column_names))})"

                # Execute the query
                cursor.execute(query, data)

            # Close the MySQL connection
            cursor.close()
            conn.close()
        os.remove("savehere123savehere.csv")
        print(f"Data inserted successfully into this '{table_name}' TABLE of this '{database_name}' DATABASE")


    def default():
        if option == '0':
            os.remove("extractcapfiles.txt")
            exit()
        else:
            print("Invalid option selected")
    ################################################   Funcations upper   #####################################################



    while True:   
        print("---------------------------------------------------------------")     
        option = input( "1> Read .cap file or extracted the ips, We can have output in a file as well.\n"
                        "2> Show me duplicate ips, How many times those are being repeated\n"
                        "3> Get ips All details in a excel file\n"
                        "4> Get ips All details in a csv file\n"
                        "5> Get ips details in text file as json format\n"
                        "6> To see all http protocal request and which websites\n"
                        "7> To See POST or GET requests\n"
                        "8> For inserting all ips details to MYSQL Database\n"
                        "0> Exit\n\n"
                        "Enter your choice: ")

        # Create a dictionary with option handlers
        option_handlers = {
            "1": mainips,
            "2": duplicateips,
            "3": ipsinexcel,
            "4": ipsincsv,
            "5": ipsinjson,
            "6": mainhttprequests,
            "7": mainpostget,
            "8": maindatainsert,
        }

        # Execute the appropriate handler based on the option
        option_handlers.get(option, default)()
        print()


else:
    print()
    print("Hello "+nam)
    print(f"The file '{capfile}' does not exist in the directory.")
    print("Good Bye!!")
    exit()




 

