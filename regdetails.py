import argparse
from regDB import RegDB


def main():
    # Information from https://docs.python.org/3/howto/argparse.html

    # Parser Setup
    parser = argparse.ArgumentParser(allow_abbrev=False, description="Registrar application: show details about a class")
    parser.add_argument('classID', metavar='classid', type=int, help="the id of the class whose details should be shown")

    # Parse the arguments
    args = parser.parse_args()


    db = RegDB()
    db.get_details(args) 

    db.close()




if __name__ == '__main__':
    main()
