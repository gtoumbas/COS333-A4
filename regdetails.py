"""
Authors: George Toumbas, Shanzay Waseem
"""
import argparse
from reg_db import RegDB


def main():
    """
    Reads arguments (classid) from the command
    line and searches the registrar database.
    """
    # Information from https://docs.python.org/3/howto/argparse.html

    # Parser Setup
    parser = argparse.ArgumentParser(
        allow_abbrev=False,
        description="Registrar application: show details about a class")
    parser.add_argument(
        'classID', metavar='classid', type=int,
        help="the id of the class whose details should be shown")

    # Parse the arguments
    args = parser.parse_args()

    registrar_db = RegDB()
    registrar_db.get_details(args)
    registrar_db.close()


if __name__ == '__main__':
    main()
