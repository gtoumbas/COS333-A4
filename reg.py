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
    # print(type(args))

    db = RegDB(DB_NAME)
    result = db.query(args)
    # print(result)


    # Check if the arguments are valid
    # if not args_are_valid(args):
        # exit(2)




if __name__ == '__main__':
    main()

