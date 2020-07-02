'''
Script to add domains from a directory of csv files
'''

import sys, getopt
import os
from colorama import init
init()
from colorama import Fore, Back, Style
path = os.getcwd()
sys.path.append('..\\')
from MySQL import access
import json
def add(dirpath):
    files = os.listdir(dirpath)

    for file in files:
        insert_file_to_db(dirpath + '\\' + file)

def read_db_info():
    directoryPath = os.path.dirname(os.path.realpath(__file__))
    directoryPath = directoryPath[0 :directoryPath.rfind('\\')]
    path_to_db_info = directoryPath + '\dbinfo.json'
    if not os.path.exists(path_to_db_info):
        print(Fore.RED + "dbinfo.json doesn't exist in this directory. Please refer to the documentation in README.md to set up this file.")
        return False
    with open(path_to_db_info) as f:
        data = json.load(f)
    return data

def check_db_connection():
    data = read_db_info()
    address = data['address']
    username = data['username']
    password = data['password']
    database_name = data['name']
    print(f'{Fore.CYAN}Attempting to connect to database "{database_name}" on server "{address}" using username "{username}" and password "{password}"')
    try:
        database = access.Connection(address, username, password, database_name)
    except (MySQLdb.Error) as e:
        print(Fore.RED + 'While attempting to connect, the following exceptions occured: ')
        print(e)
        sys.exit(1)
    print(Fore.GREEN + "Connection Successful!\n")

    return database

db = check_db_connection()

def insert_file_to_db(filepath):
    

    with open(filepath, 'r') as file:
        values = file.readlines()
        for line in values: 
            line = line.strip('\n')
            db.insert('dataset', 'staticip, domain, timestamp', ['Null', line, 'Null'])



def main(argv):
    print(argv)
    path = argv[0]

    if os.path.isdir(path):
        add(path)
    else:
        print(Fore.RED + 'Enter a valid directory')
        return 0
if __name__ == "__main__":
   main(sys.argv[1:])