""" 
Authors: George Toumbas, Shanzay Wazeem

Description: TODO 

"""
import argparse
import sqlite3

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

    # Check if the arguments are valid
    if not argsAreValid(args):
        exit(2)




if __name__ == '__main__':
    main()


def argsAreValid(args):
    """ 
    Returns True if the arguments are valid, False otherwise. 
    """
    # TODO Implement
    return True


def argsToSQL(args):
    """ 
    Returns a SQL query based on the arguments. 
    """
    # TODO Implement
    return ""


def printResults(results):
    """ 
    Prints the results of the query. 
    """
    # TODO Implement
    pass


# Need to be able to search by department, course number, distrib area, course title
# Should also create a function which displays results in a table
# Could to single function that queries databse E.g
# searchDB(args)

# Could also have a function for each search type
