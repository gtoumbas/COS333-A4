from inspect import classify_class_attrs
import sys
import socket
import pickle 

from PyQt5 import QtWidgets, QtGui
class ClientWindow:

    def __init__(self, argv):
        self.host = argv[1]
        self.port = int(argv[2])
        self.app = QtWidgets.QApplication(argv)
        self.window = QtWidgets.QMainWindow()
    


    def create_window(self):
        self.window.setWindowTitle("Princeton University Class Search")
        frame = QtWidgets.QFrame()
        layout = QtWidgets.QGridLayout()
        
        # Dept label and text 
        deptLabel = QtWidgets.QLabel("Dept:")
        self.deptLine = QtWidgets.QLineEdit("")
        layout.addWidget(deptLabel, 0, 0)
        layout.addWidget(self.deptLine, 0, 1)

        # Number label and text 
        numberLabel = QtWidgets.QLabel("Number:")
        self.numberLine = QtWidgets.QLineEdit("")
        layout.addWidget(numberLabel, 1, 0)
        layout.addWidget(self.numberLine, 1, 1)

        # Area label and text 
        areaLabel = QtWidgets.QLabel("Area:")
        self.areaLine = QtWidgets.QLineEdit("")
        layout.addWidget(areaLabel, 2, 0)
        layout.addWidget(self.areaLine, 2, 1)

        # Title label and text 
        titleLabel = QtWidgets.QLabel("Title:")
        self.titleLine = QtWidgets.QLineEdit("")
        layout.addWidget(titleLabel, 3, 0)
        layout.addWidget(self.titleLine, 3, 1)

        layout.setRowStretch(0, 0)
        layout.setRowStretch(1, 1)
        layout.setRowStretch(2, 0)
        layout.setRowStretch(3, 0)

        self.submit_btton = QtWidgets.QPushButton("Submit")
        layout.addWidget(self.submit_btton, 0, 2, 4, 1)
        self.submit_btton.clicked.connect(self.submit_clicked)

        # Adding list widget
        self.listWidget = QtWidgets.QListWidget()
        layout.addWidget(self.listWidget, 4, 0, 1, 3)
        self.listWidget.itemDoubleClicked.connect(self.class_clicked)

        # deptLine, numberLine, areaLine, titleLine is where the 
        # inputs are instead of args and so self needs to be made
        # of those instead of args 

        frame.setLayout(layout)

        # Set size of window to a quarter of the screen
        screen = QtWidgets.QDesktopWidget().screenGeometry()
        self.window.resize(int(screen.width() / 2), int(screen.height() / 2))
        self.window.setCentralWidget(frame)
        self.window.show()
        sys.exit(self.app.exec_())

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

    def submit_clicked(self):
        inputs = [
            self.deptLine.text(),
            self.numberLine.text(),
            self.areaLine.text(),
            self.titleLine.text()
        ]
        inputs.insert(0, "SEARCH")

        try:
            with socket.socket() as sock:
                sock.connect((self.host, self.port))
                out_flo = sock.makefile(mode="wb")
                print(out_flo)
                pickle.dump(inputs, out_flo)

                out_flo.flush()

                in_flo = sock.makefile(mode="rb")
                results = pickle.load(in_flo)
                self.display_search_results(results)

        except Exception as ex:
            print(ex, file=sys.stderr)
            sys.exit(1)
        

    def display_search_results(self, results):
        for r in results:
            # class_id, dept, number, area, title = r
            # self.listWidget.addItem(f"{class_id:>5} {dept:>4} {number:>6} {area:>4} {title}")
            # self.listWidget.addItem("%5s%4s%5s%4s %s" % r)
            font = QtGui.QFont("Courier", 10)
            # r.setFont(font)
            self.listWidget.addItem("%5s%4s%5s%4s %s" % r)

    def class_clicked(self, item):
        # Classid is number before first space
        class_id = item.text().split()[0]
        print(class_id)
        inputs = ["DETAILS", class_id]

        try:
            with socket.socket() as sock:
                sock.connect((self.host, self.port))
                out_flo = sock.makefile(mode="wb")
                print(out_flo)
                pickle.dump(inputs, out_flo)

                out_flo.flush()

                in_flo = sock.makefile(mode="rb")
                results = pickle.load(in_flo)
                self.display_class_details(results)
                

        except Exception as ex:
            print(ex, file=sys.stderr)
            sys.exit(1)


    def display_class_details(self, results):
        info_box = QtWidgets.QMessageBox()
        info_box.setTitle("Class Details")
        info_box.setText(results)
        info_box.setIcon(QtWidgets.QMessageBox.Information)
        info_box.setStandardButtons(QtWidgets.QMessageBox.Ok)


        sys.exit(info_box.exec_())

        


        

        




