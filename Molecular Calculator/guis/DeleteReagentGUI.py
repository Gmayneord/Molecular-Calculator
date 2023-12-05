from PyQt5 import QtWidgets, QtCore


class DeleteReagentGUI(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.create_gui()
        self.add_elements()
        self.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.WindowStaysOnTopHint)

    def create_gui(self):
        self.setWindowTitle("Delete items")
        self.resize(400, 120)
        self.window_widget = QtWidgets.QWidget()

    def add_elements(self):
        v_layout = QtWidgets.QVBoxLayout()

        # =========================================================================
        h_layout = QtWidgets.QHBoxLayout()

        label = QtWidgets.QLabel("Delete item:")
        h_layout.addWidget(label)

        self.dropdown_menu = QtWidgets.QComboBox()
        self.dropdown_menu.setFixedSize(QtCore.QSize(150, 20))
        h_layout.addWidget(self.dropdown_menu)

        self.delete_button = QtWidgets.QPushButton("Delete...")
        h_layout.addWidget(self.delete_button)

        v_layout.addLayout(h_layout)

        # =========================================================================
        h_layout = QtWidgets.QHBoxLayout()

        self.close_button = QtWidgets.QPushButton("Close")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.close_button.sizePolicy().hasHeightForWidth())
        self.close_button.setSizePolicy(sizePolicy)
        h_layout.addWidget(self.close_button)

        v_layout.addLayout(h_layout)

        # =========================================================================
        self.window_widget.setLayout(v_layout)
        self.setCentralWidget(self.window_widget)
        self.window_widget.setContentsMargins(10, 10, 10, 10)
        # =========================================================================