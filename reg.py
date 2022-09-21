""" 
Authors: George Toumbas, Shanzay Wazeem

Description: TODO 

"""
import argparse
import sqlite3
from regDB import RegDB

DB_NAME = 'reg.sqlite'

def main():
    # Information from https://docs.python.org/3/howto/argparse.html

    # Parser Setup allow verbose = false
    parser = argparse.ArgumentParser(allow_abbrev=False, description="Registrar application: show overviews of classes")
    parser.add_argument('-d', metavar='dest', help="Show only those classes whose department contains dept")
    parser.add_argument('-n', metavar='num',  help="Show only those classes whose course number contains num") 
    parser.add_argument('-a', metavar='area',  help="Show only those classes whose distrib area contains area") 
    parser.add_argument('-t', metavar='title',  help="Show only those classes whose course title contains title") 


    # Parse the arguments
    args = parser.parse_args()

    # Need to check for valid args (either here or in regDB)

    db = RegDB(DB_NAME)
    # db.search(args)
    db.get_details(8321) # TODO write this into reg details

    db.close()




if __name__ == '__main__':
    main()

