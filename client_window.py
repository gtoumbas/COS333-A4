import sys
import socket

from PyQt5 import QtWidgets
class ClientWindow:

    def __init__(self, argv):
        self.host = argv[1]
        self.port = argv[2]
        self.app = QtWidgets.QApplication(argv)
        self.window = QtWidgets.QMainWindow()
    


    def createWindow(self):
        self.window.setWindowTitle("Princeton University Class Search")
        frame = QtWidgets.QFrame()
        layout = QtWidgets.QGridLayout()
        
        # Dept label and text 
        deptLabel = QtWidgets.QLabel("Dept:")
        self.deptLine = QtWidgets.QLineEdit("")
        layout.addWidget(self.deptLabel, 0, 0)
        layout.addWidget(self.deptLine, 0, 1)

        # Number label and text 
        numberLabel = QtWidgets.QLabel("Number:")
        self.numberLine = QtWidgets.QLineEdit("")
        layout.addWidget(self.numberLabel, 1, 0)
        layout.addWidget(self.numberLine, 1, 1)

        # Area label and text 
        areaLabel = QtWidgets.QLabel("Area:")
        self.reaLine = QtWidgets.QLineEdit("")
        layout.addWidget(self.areaLabel, 2, 0)
        layout.addWidget(self.areaLine, 2, 1)

        # Title label and text 
        titleLabel = QtWidgets.QLabel("Title:")
        self.titleLine = QtWidgets.QLineEdit("")
        layout.addWidget(self.titleLabel, 3, 0)
        layout.addWidget(self.titleLine, 3, 1)

        layout.setRowStretch(0, 0)
        layout.setRowStretch(1, 1)
        layout.setRowStretch(2, 0)
        layout.setRowStretch(3, 0)

        self.submit_btton = QtWidgets.QPushButton("Submit")
        layout.addWidget(self.submit_btton, 0, 2, 4, 1)
        self.submit_btton.clicked.connect(
            self.submitClicked(self.host, self.port))

        # Adding list widget
        listWidget = QtWidgets.QListWidget()
        layout.addWidget(listWidget, 4, 0, 1, 3)

        # deptLine, numberLine, areaLine, titleLine is where the 
        # inputs are instead of args and so self needs to be made
        # of those instead of args 

        frame.setLayout(layout)

        # Set size of window to a quarter of the screen
        screen = QtWidgets.QDesktopWidget().screenGeometry()
        self.window.resize(int(screen.width() / 2), int(screen.height() / 2))
        self.window.setCentralWidget(frame)
        self.window.show()

    def connectToServer(self):
        pass

    def sendRequest(self):
        pass

    def receiveResponse(self):
        pass

    def clicked(self):
        pass

    def closeApp(self):
        pass

    def submitClicked(self, host, port):
        inputs = [
            self.deptLine.text(),
            self.numberLine.text(),
            self.areaLine.text(),
            self.titleLine.text()
        ]

        try:
            with socket.socket() as sock:
                sock.connect((host, port))
                out_flo = sock.makefile(mode="w", encoding="utf-8")

                for i in inputs:
                    out_flo.write(i + "\n")
                    out_flo.flush()

        except Exception as ex:
            print(ex, file=sys.stderr)
            sys.exit(1)

