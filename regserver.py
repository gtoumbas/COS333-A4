"""
Authors: George Toumbas, Shanzay Waseem
"""
import sys
import os
import argparse
import socket


def handleSubmit(sock):
    server_sock = socket.socket()


def main():
    """
    Reads arguments from the command line and opens the GUI or the help message
    """
    if len(sys.argv) != 2:
        print("Usage: python %s host port file' % sys.argv[0]")
        sys.exit(2)

    parser = argparse.ArgumentParser(
        description='Server for the registrar application')
    parser.add_argument('port', metavar='port', type=int,
                        help='the port at which the server should listen')

    args = parser.parse_args()
    port = args.port

    try:
        port = int(sys.argv[1])
        server_sock = socket.socket()
        print('Opened server socket')
        if os.name != 'nt':
            server_sock.setsockopt(
                socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_sock.bind(('', port))
        print('Bound server socket to port')
        server_sock.listen()
        print('Listening')
        while True:
            try:
                sock, client_addr = server_sock.accept()
                with sock:
                    print('Accepted connection')
                    print('Opened socket')
                    print('Server IP addr and po ', sock.getsockname())
                    print('Client IP addr and po ', client_addr)
                    handle_client(sock)
            except Exception as ex:
                print(ex, file=sys.stderr)
    except Exception as ex:
        print(ex, file=sys.stderr)
        sys.exit(1)
