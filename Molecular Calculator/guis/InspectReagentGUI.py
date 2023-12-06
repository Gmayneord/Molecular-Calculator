from PyQt5 import QtWidgets, QtGui, QtCore
from gui_functions.CommonFunctions import create_line

class InspectReagentGUI(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.create_gui()
        self.add_elements()
        self.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.WindowStaysOnTopHint)

    def create_gui(self):
        self.setWindowTitle("Reagent")
        self.resize(400, 250)
        self.window_widget = QtWidgets.QWidget()

    def add_elements(self):
        v_layout = QtWidgets.QVBoxLayout()

        bold_text = QtGui.QFont()
        bold_text.setBold(True)

        # =========================================================================
        h_layout = QtWidgets.QHBoxLayout()
        label = QtWidgets.QLabel("Reagent name: ")
        label.setFont(bold_text)
        h_layout.addWidget(label)

        self.name_label = QtWidgets.QLabel()
        h_layout.addWidget(self.name_label)

        v_layout.addLayout(h_layout)
        line = create_line("h")
        v_layout.addWidget(line)

        # =========================================================================
        h_layout = QtWidgets.QHBoxLayout()
        label = QtWidgets.QLabel("Reagent MW: ")
        label.setFont(bold_text)
        h_layout.addWidget(label)

        self.mw_label = QtWidgets.QLabel()
        h_layout.addWidget(self.mw_label)

        v_layout.addLayout(h_layout)
        line = create_line("h")
        v_layout.addWidget(line)

        # =========================================================================
        h_layout = QtWidgets.QHBoxLayout()
        label = QtWidgets.QLabel("Product Code: ")
        label.setFont(bold_text)
        h_layout.addWidget(label)

        self.product_code_label = QtWidgets.QLabel()
        h_layout.addWidget(self.product_code_label)

        v_layout.addLayout(h_layout)
        line = create_line("h")
        v_layout.addWidget(line)

        # =========================================================================
        h_layout = QtWidgets.QHBoxLayout()
        label = QtWidgets.QLabel("Supplier: ")
        label.setFont(bold_text)
        h_layout.addWidget(label)

        self.supplier_label = QtWidgets.QLabel()
        h_layout.addWidget(self.supplier_label)

        v_layout.addLayout(h_layout)
        line = create_line("h")
        v_layout.addWidget(line)

        # =========================================================================
        h_layout = QtWidgets.QHBoxLayout()
        label = QtWidgets.QLabel("H codes: ")
        label.setFont(bold_text)
        h_layout.addWidget(label)

        self.h_code_label = QtWidgets.QLabel()
        h_layout.addWidget(self.h_code_label)

        v_layout.addLayout(h_layout)
        line = create_line("h")
        v_layout.addWidget(line)

        # =========================================================================
        h_layout = QtWidgets.QHBoxLayout()
        self.close_button = QtWidgets.QPushButton("Close")
        self.close_button.setFixedSize(100, 25)
        h_layout.addWidget(self.close_button)
        v_layout.addLayout(h_layout)

        # =========================================================================
        self.window_widget.setLayout(v_layout)
        self.setCentralWidget(self.window_widget)
        self.window_widget.setContentsMargins(10, 10, 10, 10)
        # =========================================================================
