# Author: Trevor Rice
# Date: Mon Jul 22 21:52:06 EDT 2019
# Purpose: remove unwanted columns and anonymize the static ip column from
# the malicious domain data. This script will also create the database and insert
# our data using the access.py file in the MySQL directory. This script is meant
# to be ran once on the host computer and will never be ran again unless you
# need to recreate the entire database.

import pandas as pd
import sys
directoryPath = '/home/trevor/Documents/MaliciousDomainDetection'
sys.path.insert(1, directoryPath + '/Code/MySQL')
import access


def printProgressBar (iteration, total, prefix = 'Inserting Data', suffix = '', decimals = 1, length = 50, fill = '█'):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = '\r')
    # Print New Line on Complete
    if iteration == total:
        print()
    sys.stdout.flush()

def insert_data(readpath, chunksize, database, tablename):
    df = pd.read_csv(readpath, chunksize=chunksize, encoding = "ISO-8859-1", sep  =',', names = list(range(0,3)))
    for chunk in df: # for every chunk in the dataframe
        chunk = chunk.fillna(0) # checks for na values
        values = chunk.values.tolist() # converts chunk to a list()
        print(chunk)
        database.insert(tablename, 'staticip, domain, timestamp', values)

def get_sample(df, num_samples):
    return df.sample(n=num_samples, replace=True)





def process_and_insert_data(readpath, chunksize, database, tablename):
    """
    Reads the csv from readpath, removes unwanted columns, hashes the first
    column, and splits in into chunks of size @chunksize that are each inserted
    into the database
    @params:
        readpath: file path for the data
        chunksize: size of each chunk to be processed, if you raise the chunksize
        it will be faster, but use more memory
    """

    # calling function from access.py that creates a table
    #database.create_table(tablename, 'staticip varchar(75), domain varchar(75) primary key, timestamp datetime(2)')

    fileName = readpath[readpath.rfind('/') + 1:]
    print(fileName)
    print("Chunksize: " + str(chunksize))
    print("Calculating number of lines in "+fileName+"...")
    numlines = 0

    # reading the csv, limiting the columns to 5, some of our data had more than five columns
    df = pd.read_csv(readpath, chunksize=chunksize, encoding = "ISO-8859-1", sep  =',', names = list(range(0,5)))
    for chunk in pd.read_csv(readpath, chunksize=chunksize, encoding = "ISO-8859-1", sep  =',', names = list(range(0,5))):
        numlines += chunk.size/5 # size is rows times columns, thus nRow = size/nCol
    print('Total lines in',fileName + ':', int(numlines))

    linescompleted = 0
    for chunk in df: # for every chunk in the dataframe
        printProgressBar(linescompleted, numlines)

        # drop columns 1 and 4
        chunk = chunk.drop([chunk.columns[1], chunk.columns[4]], axis = 'columns')
        chunk[chunk.columns[0]] = chunk[chunk.columns[0]].apply(hash) # apply hash to first column
        chunk = chunk.fillna(0) # checks for na values
        values = chunk.values.tolist() # converts chunk to a list()

        # function in access.py to insert our list of values
        database.insert(tablename, 'staticip, domain, timestamp', values)

        linescompleted += chunksize
    printProgressBar(numlines, numlines)
