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

    parser = argparse.ArgumentParser(description='Client for the registrar application')
    parser.add_argument('host', metavar='host', type=int,
                    help='the host on which the server is running')
    parser.add_argument('port', metavar='port', type=int,
                    help='the port at which the server is listening')

    args = parser.parse_args()
    print(sys.argv)

    try:

        host =  args.host
        port =  args.port
        app = QtWidgets.QApplication(sys.argv)
        window = QtWidgets.QMainWindow()
        window.setWindowTitle("Princeton University Class Search")
        frame = QtWidgets.QFrame()
        layout = QtWidgets.QGridLayout()
        
        # Dept label and text 
        deptLabel = QtWidgets.QLabel("Dept:")
        deptLine = QtWidgets.QLineEdit("")
        layout.addWidget(deptLabel, 0, 0)
        layout.addWidget(deptLine, 0, 1)

        # Number label and text 
        numberLabel = QtWidgets.QLabel("Number:")
        numberLine = QtWidgets.QLineEdit("")
        layout.addWidget(numberLabel, 1, 0)
        layout.addWidget(numberLine, 1, 1)

        # Area label and text 
        areaLabel = QtWidgets.QLabel("Area:")
        areaLine = QtWidgets.QLineEdit("")
        layout.addWidget(areaLabel, 2, 0)
        layout.addWidget(areaLine, 2, 1)

        # Title label and text 
        titleLabel = QtWidgets.QLabel("Title:")
        titleLine = QtWidgets.QLineEdit("")
        layout.addWidget(titleLabel, 3, 0)
        layout.addWidget(titleLine, 3, 1)

        layout.setRowStretch(0, 0)
        layout.setRowStretch(1, 1)
        layout.setRowStretch(2, 0)
        layout.setRowStretch(3, 0)

        submit_btton = QtWidgets.QPushButton("Submit")
        layout.addWidget(submit_btton, 0, 2, 4, 1)

        # Adding list widget
        listWidget = QtWidgets.QListWidget()
        layout.addWidget(listWidget, 4, 0, 1, 3)

        # deptLine, numberLine, areaLine, titleLine is where the 
        # inputs are instead of args and so self needs to be made
        # of those instead of args 

        frame.setLayout(layout)

        # Set size of window to a quarter of the screen
        screen = QtWidgets.QDesktopWidget().screenGeometry()
        window.resize(int(screen.width() / 2), int(screen.height() / 2))
        window.setCentralWidget(frame)
        window.show()

        inputs = [deptLine, numberLine, areaLine, titleLine] 
        inputs = ["COS", "", "", ""]
        registrar_db = RegDB()
        results = registrar_db.search(inputs)
        print(results)
        registrar_db.close()

        sys.exit(app.exec_())


    except Exception as ex:
        print(ex, file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()



class ClientWindow:

