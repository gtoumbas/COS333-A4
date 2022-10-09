"""
Authors: George Toumbas, Shanzay Waseem
"""
import sys
import os
import argparse
import socket
import pickle

from reg_db import RegDB

# TODO add newlines to beginning of all error printing
def handleClient(sock, db):
    in_flo = sock.makefile(mode="rb")
    err = db.connect() # Opens connection to db 

    # Double check this. Might be writing to stderr twice
    if err:
        response = ["ERROR"]
        out_flo = sock.makefile(mode="wb")
        pickle.dump(response, out_flo)
        out_flo.flush()
        return
    
    inputs = pickle.load(in_flo)
    if inputs[0] == "SEARCH":
        results = db.search(inputs[1:])
        out_flo = sock.makefile(mode="wb")
        pickle.dump(results, out_flo)
        out_flo.flush()
    else :
        class_id = inputs[1]
        results = db.get_details(class_id)
        out_flo = sock.makefile(mode="wb")
        pickle.dump(results, out_flo)
        out_flo.flush()

    db.close()




def main():
    """
    Reads arguments from the command line and opens the GUI or the help message
    """
    db = RegDB()

    parser = argparse.ArgumentParser(
        description='Server for the registrar application')
    parser.add_argument('port', metavar='port', type=int,
                        help='the port at which the server should listen')

    args = parser.parse_args()

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
                    handleClient(sock, db)
                print('Closed socket')
            except Exception as ex:
                print(ex, file=sys.stderr)
    
    except Exception as ex:
        print(ex, file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()