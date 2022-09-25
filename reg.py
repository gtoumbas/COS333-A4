""" 
Authors: George Toumbas, Shanzay Wazeem

Description: TODO 

"""
import argparse
from regDB import RegDB

DB_NAME = 'reg.sqlite'

def main():
    # Information from https://docs.python.org/3/howto/argparse.html

    parser = argparse.ArgumentParser(allow_abbrev=False, description="Registrar application: show overviews of classes")
    parser.add_argument('-d', metavar='dest', help="Show only those classes whose department contains dept", type = str)
    parser.add_argument('-n', metavar='num',  help="Show only those classes whose course number contains num", type = str) 
    parser.add_argument('-a', metavar='area',  help="Show only those classes whose distrib area contains area", type = str) 
    parser.add_argument('-t', metavar='title',  help="Show only those classes whose course title contains title", type = str) 

    args = parser.parse_args()

    # Need to check for valid args (either here or in regDB) 
    # Probably best to do it in regDB 

    db = RegDB()
    db.search(args)
    db.close()


if __name__ == '__main__':
    main()

