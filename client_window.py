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
        self.window.setFont(font)
        self.window.setWindowTitle("Princeton University Class Search")
        frame = QtWidgets.QFrame()
        layout = QtWidgets.QGridLayout()

        # Dept label and text
        dept_label = QtWidgets.QLabel("Dept:")
        self.dept_line = QtWidgets.QLineEdit("")
        self.dept_line.returnPressed.connect(self.submit_clicked(inputs))
        layout.addWidget(dept_label, 0, 0)
        layout.addWidget(self.dept_line, 0, 1)

        # Number label and text
        number_label = QtWidgets.QLabel("Number:")
        self.number_line = QtWidgets.QLineEdit("")
        self.number_line.returnPressed.connect(self.submit_clicked(inputs))
        layout.addWidget(number_label, 1, 0)
        layout.addWidget(self.number_line, 1, 1)

        # Area label and text
        area_label = QtWidgets.QLabel("Area:")
        self.area_line = QtWidgets.QLineEdit("")
        self.area_line.returnPressed.connect(self.submit_clicked(inputs))
        layout.addWidget(area_label, 2, 0)
        layout.addWidget(self.area_line, 2, 1)

        # Title label and text
        title_label = QtWidgets.QLabel("Title:")
        self.title_line = QtWidgets.QLineEdit("")
        self.title_line.returnPressed.connect(self.submit_clicked(inputs))
        layout.addWidget(title_label, 3, 0)
        layout.addWidget(self.title_line, 3, 1)

        layout.setRowStretch(0, 0)
        layout.setRowStretch(1, 1)
        layout.setRowStretch(2, 0)
        layout.setRowStretch(3, 0)

        # Submit button
        self.submit_btton = QtWidgets.QPushButton("Submit")
        layout.addWidget(self.submit_btton, 0, 2, 4, 1)
        self.submit_btton.clicked.connect(self.submit_clicked)

        # Adding list widget
        self.list_widget = QtWidgets.QListWidget()
        layout.addWidget(self.list_widget, 4, 0, 1, 3)
        self.list_widget.itemDoubleClicked.connect(self.class_clicked)
        #  Get details from enter key or from cmd+o(mac)
        if platform.system() == "Darwin":
            enter_shortcut = QtWidgets.QShortcut(
                QtGui.QKeySequence("Ctrl+O"), self.list_widget)
        else:
            enter_shortcut = QtWidgets.QShortcut(
                QtGui.QKeySequence("Return"), self.list_widget)
        enter_shortcut.setContext(QtCore.Qt.WidgetShortcut)
        enter_shortcut.activated.connect(
            lambda: self.class_clicked(self.list_widget.currentItem()))

        frame.setLayout(layout)

        # Set size of window to a quarter of the screen
        screen = QtWidgets.QDesktopWidget().screenGeometry()
        self.window.resize(
            int(screen.width() / 2), int(screen.height() / 2))
        self.window.setCentralWidget(frame)
        self.window.show()

        # Display all results initially
        self.submit_clicked()


        sys.exit(self.app.exec_())

    def send_request(self, request):
        try:
            with socket.socket() as sock:
                sock.connect((self.host, self.port))
                out_flo = sock.makefile('wb')
                pickle.dump(request, out_flo)
                out_flo.flush()

                # Receive response
                in_flo = sock.makefile('rb')
                response = pickle.load(in_flo)
                response_ok = self.check_response(response)
                if not response_ok:
                    return None

                return response

        except Exception as ex:
            QtWidgets.QMessageBox.critical(
                self.window, "Server Error", str(ex),
                buttons=QtWidgets.QMessageBox.Ok)
            return None

    def check_response(self, response):
        if len(response) == 0:
            return True
        if response[0] == "ERROR":
            QtWidgets.QMessageBox.critical(
                self.window, "Server Error",
                "A server error occurred. \
                    Please contact the system administrator.",
                buttons=QtWidgets.QMessageBox.Ok)
            return False
        if response[0] == "INVALID_CLASSID":
            QtWidgets.QMessageBox.critical(
                self.window, "Error",
                f"No Class With classId {response[1]} Exists",
                buttons=QtWidgets.QMessageBox.Ok)
            return False

        return True

    # submit clicked is for when you are grabbing the queries
    def submit_clicked(self, inputs):
        inputs.insert(0, "SEARCH")

        # Clear list widget
        self.list_widget.clear()
        response = self.send_request(inputs)
        if response:
            self.display_search_results(response)


    def display_search_results(self, results):
        for currresult in results:
            class_id, dept, number, area, title = currresult
            self.list_widget.addItem(
                f"{class_id:>5} {dept:>3}\
                     {number:>4} {area:>3} {title}")
        self.list_widget.setCurrentRow(0) # Set focus on first item


    def class_clicked(self, item):
        # Classid is number before first space
        class_id = item.text().split()[0]
        inputs = ["DETAILS", class_id]

        # Send request to server
        response = self.send_request(inputs)
        if response:
            self.display_class_details(response)


    def display_class_details(self, results):
        _ = QtWidgets.QMessageBox.information(
            self.window,
            "Class Details",
            results,
            buttons=QtWidgets.QMessageBox.Ok,
            defaultButton=QtWidgets.QMessageBox.Ok
        )
