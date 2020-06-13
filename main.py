import os
directoryPath = os.path.dirname(os.path.realpath(__file__))
import json
import MySQLdb
import sys
import subprocess
from os import path
from colorama import init
init()
from colorama import Fore, Back, Style
# print(Fore.RED + 'some red text')
# print(Back.GREEN + 'and with a green background')
# print(Style.DIM + 'and in dim text')
# print(Style.RESET_ALL)
# print('back to normal now')
# sys.path.insert(1, directoryPath + '/Code')
import MySQL.access as access
# import DataProcessing.process as process
import CUDA.matcher
# import pandas as pd
# import time
# import CUDA.info as info
# import RDG.generator as gen


def check_libraries():
    print(Fore.CYAN + 'Checking if the necessary libraries are installed...')
    libraries_not_found = []
    try:
        import os
    except ImportError:
        libraries_not_found.append('os')
    
    try:
        import json
    except ImportError:
        libraries_not_found.append('json')

    try:
        import MySQLdb
    except ImportError:
        libraries_not_found.append('MySQLdb')

    try:
        import sys
    except ImportError:
        libraries_not_found.append('sys')

    try:
        import subprocess
    except ImportError:
        libraries_not_found.append('subprocess')
    
    try:
        import colorama
    except ImportError:
        libraries_not_found.append('colorama')
        
    try:
        import time
    except ImportError:
        libraries_not_found.append('time')

    try:
        import csv
    except ImportError:
        libraries_not_found.append('csv')

    if len(libraries_not_found) > 0:
        print(Fore.RED + 'You need to install the following libraries:')
        for library in libraries_not_found:
            print('   *' + Fore.RED + library)
        print()
        return False
    print(Fore.GREEN + 'All libraries installed')
    return True


def read_db_info():
    path_to_db_info = directoryPath + '\dbinfo.json'
    if not path.exists(path_to_db_info):
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
        return False
    print(Fore.GREEN + "Connection Successful!\n")

    return database

def create_local_data(db):
    print(Fore.CYAN + 'Attempting to copy database into local csv...')
    path_to_data = directoryPath + '\localdata.csv'
    print(Fore.YELLOW + 'Attempting to write to ' + path_to_data)
    data = read_db_info()
    database_name = data['name']

    db.to_csv('dataset', path_to_data)
    print(Fore.GREEN + 'Successfully wrote data to localdata.csv\n')

def create_matcher():
    path_to_data = directoryPath + '\localdata.csv'
    matcher = CUDA.matcher.Matcher(path_to_data)
    return matcher

def main():
    print(Fore.YELLOW + 'Starting setup...\n')
    db = check_db_connection()
    reqs = check_libraries()
    if not (db and reqs):
        sys.exit(1)
    print()

    create_local_data(db)
    
    matcher = create_matcher()
    matcher.load_gpu()

    while (True):
        sample_domain = input(Fore.YELLOW + 'Enter a domain to be checked: ')
        result = matcher.is_malicious(sample_domain)

        if (result == 1):
            print(Fore.YELLOW + f'"{sample_domain}" is malicious')
        else:
            print(Fore.YELLOW + f'"{sample_domain}" is benign')
        print()

if __name__ == "__main__":
    main()