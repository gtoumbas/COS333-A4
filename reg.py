"""
Authors: George Toumbas, Shanzay Waseem
"""
import argparse
from reg_db import RegDB

DB_NAME = 'reg.sqlite'


def main():
    """
    Reads arguments from the command line and searches the registrar database.
    """
    # Information from https://docs.python.org/3/howto/argparse.html

    parser = argparse.ArgumentParser(
        allow_abbrev=False,
        description =
        "Registrar application: show overviews of classes")
    parser.add_argument(
        '-d', metavar='dest',
        help="Show only those classes whose department contains dept",
        type=str)
    parser.add_argument(
        '-n', metavar='num',
        help="Show only those classes whose course number contains num",
        type=str)
    parser.add_argument(
        '-a', metavar='area',
        help="Show only those classes whose distrib area contains area",
        type=str)
    parser.add_argument(
        '-t', metavar='title',
        help=
        "Show only those classes whose course title contains title",
        type=str)

    args = parser.parse_args()

    registrar_db = RegDB()
    registrar_db.search(args)
    registrar_db.close()


if __name__ == '__main__':
    main()
