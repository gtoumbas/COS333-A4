"""
Authors: George Toumbas, Shanzay Waseem
"""
import sys

from PyQt5 import QtWidgets 
import argparse
from reg_db import RegDB

def main():
    """
    Reads arguments from the command line and opens the GUI or the help message
    """
    if len(sys.argv) != 3:
        print("Usage: python %s host port file’ % sys.argv[0]")
        sys.exit(2)

    parser = argparse.ArgumentParser(description='Client for the registrar application')
    parser.add_argument(metavar='host', type=int,
                    help='the host on which the server is running')
    parser.add_argument(metavar='port', type=int,
                    help='the port at which the server is listening')

    args = parser.parse_args()

    try:
        host =  sys.argv[1]
        port =  sys.argv[2]
        app = QtWidgets.QApplication(sys.argv)
        window = QtWidgets.QMainWindow()
        window.setWindowTitle("Princeton University Class Search")
        frame = QtWidgets.QFrame()
        layout = QtWidgets.QGridLayout()
        
        # Dept label and text 
        deptLabel = QtWidgets.QLabel("Dept:")
        deptLine = QtWidgets.QLineEdit("")
        layout.addWidget(deptLabel, 0, 0)
        layout.addWidget(deptLine, 1, 0)

        # Number label and text 
        numberLabel = QtWidgets.QLabel("Number:")
        numberLine = QtWidgets.QLineEdit("")
        layout.addWidget(numberLabel, 0, 1)
        layout.addWidget(numberLine, 1, 1)

        # Area label and text 
        areaLabel = QtWidgets.QLabel("Area:")
        areaLine = QtWidgets.QLineEdit("")
        layout.addWidget(areaLabel, 0, 2)
        layout.addWidget(areaLine, 1, 2)

        # Title label and text 
        titleLabel = QtWidgets.QLabel("Title:")
        titleLine = QtWidgets.QLineEdit("")
        layout.addWidget(titleLabel, 0, 3)
        layout.addWidget(titleLine, 1, 3)

        layout.setRowStretch(0, 0)
        layout.setRowStretch(1, 1)
        layout.setRowStretch(2, 0)
        layout.setRowStretch(3, 0)

        button = QtWidgets.QPushButton("Submit")
        layout.addWidget(button, 2, 0)

        # deptLine, numberLine, areaLine, titleLine is where the 
        # inputs are instead of args and so self needs to be made
        # of those instead of args 

        frame.setLayout(layout)
        window.show()

        inputs = [deptLine, numberLine, areaLine, titleLine] 
        registrar_db = RegDB()
        registrar_db.search(inputs)
        registrar_db.close()

        sys.exit(app.exec_())


    except Exception as ex:
        print(ex, file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()

    