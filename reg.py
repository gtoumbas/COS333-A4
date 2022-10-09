"""
Authors: George Toumbas, Shanzay Waseem
"""
import sys
import argparse
from PyQt5 import QtWidgets
from client_window import ClientWindow

def main():
    """
    Reads arguments from the command line and
    opens the GUI or the help message
    """

    parser = argparse.ArgumentParser(description=
    'Client for the registrar application')
    parser.add_argument('host', metavar='host', type=str,
                    help='the host on which the server is running')
    parser.add_argument('port', metavar='port', type=int,
                    help='the port at which the server is listening')

    _ = parser.parse_args()
    print(sys.argv)

    try:
        client_window = ClientWindow(sys.argv)
        client_window.create_window()

    except Exception as ex:
        print(ex, file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
