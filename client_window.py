import sys
import platform
import socket
import pickle 

from PyQt5 import QtWidgets, QtGui, QtCore
class ClientWindow:

    def __init__(self, argv):
        self.host = argv[1]
        self.port = int(argv[2])
        self.app = QtWidgets.QApplication(argv)
        self.window = QtWidgets.QMainWindow()    


    def create_window(self):
        font = QtGui.QFont("Courier", 10)
        self.app.setFont(font)
        self.window.setWindowTitle("Princeton University Class Search")
        frame = QtWidgets.QFrame()
        layout = QtWidgets.QGridLayout()
        
        # Dept label and text 
        deptLabel = QtWidgets.QLabel("Dept:")
        self.deptLine = QtWidgets.QLineEdit("")
        self.deptLine.returnPressed.connect(self.submit_clicked)
        layout.addWidget(deptLabel, 0, 0)
        layout.addWidget(self.deptLine, 0, 1)

        # Number label and text 
        numberLabel = QtWidgets.QLabel("Number:")
        self.numberLine = QtWidgets.QLineEdit("")
        self.numberLine.returnPressed.connect(self.submit_clicked)
        layout.addWidget(numberLabel, 1, 0)
        layout.addWidget(self.numberLine, 1, 1)

        # Area label and text 
        areaLabel = QtWidgets.QLabel("Area:")
        self.areaLine = QtWidgets.QLineEdit("")
        self.areaLine.returnPressed.connect(self.submit_clicked)
        layout.addWidget(areaLabel, 2, 0)
        layout.addWidget(self.areaLine, 2, 1)

        # Title label and text 
        titleLabel = QtWidgets.QLabel("Title:")
        self.titleLine = QtWidgets.QLineEdit("")
        self.titleLine.returnPressed.connect(self.submit_clicked)
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
        # Display all results initially
        self.submit_clicked()
        self.listWidget.itemDoubleClicked.connect(self.class_clicked)
        #  Change to cmd+o for mac
        if platform.system() == "Darwin":
            enterShortcut = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+O"), self.listWidget)
        else:
            enterShortcut = QtWidgets.QShortcut(QtGui.QKeySequence("Return"), self.listWidget)
        enterShortcut.setContext(QtCore.Qt.WidgetShortcut)
        enterShortcut.activated.connect(lambda: self.class_clicked(self.listWidget.currentItem()))

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

        # Clear list widget
        self.listWidget.clear() 

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
        

    def display_search_results(self, results):
        try:
            for r in results:
                class_id, dept, number, area, title = r
                self.listWidget.addItem(f"{class_id:>5} {dept:>3} {number:>4} {area:>3} {title}")
                self.listWidget.setCurrentRow(0)
        except Exception as err:
            QtWidgets.QMessageBox.critical(self.window, "Server Error", str(err))

        # Activate the first item in the list




    def class_clicked(self, item):
        print("clicked")
        print(type(item))
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
                if results[0] == "InavlidClassId":
                    self.display_ClassId_err(class_id)
                    return
                
                self.display_class_details(results)
                

        except Exception as err:
            QtWidgets.QMessageBox.critical(self.window, "Server Error", str(err))


    def display_class_details(self, results):
        try:
            info_box = QtWidgets.QMessageBox.information(
                self.window, 
                "Class Details", 
                results, 
                buttons=QtWidgets.QMessageBox.Ok,
                defaultButton=QtWidgets.QMessageBox.Ok
                )
        except Exception as err:
            QtWidgets.QMessageBox.critical(self.window, "Server Error", str(err))


    def display_ClassId_err(self, classId):
        try:
            QtWidgets.QMessageBox.critical(self.window, "Error", "no class with classId %s exists" % classId)
        except Exception as err:
            QtWidgets.QMessageBox.critical(self.window, "Server Error", str(err))
