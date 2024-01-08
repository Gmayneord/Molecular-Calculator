from PyQt5 import QtWidgets, QtCore, QtGui

from data.constants import MW_FIELD_MIN_VAL, MW_FIELD_MAX_VAL, MW_FIELD_DECIMAL_NO

class EditReagentGUI(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.create_gui()
        self.add_elements()
        self.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.WindowStaysOnTopHint)

    def create_gui(self):
        self.setWindowTitle("Edit items")
        self.resize(400, 250)
        self.window_widget = QtWidgets.QWidget()

    def add_elements(self):
        v_layout = QtWidgets.QVBoxLayout()

        # =========================================================================
        h_layout = QtWidgets.QHBoxLayout()
        label = QtWidgets.QLabel("Select a reagent:")
        h_layout.addWidget(label)
        self.dropdown_menu = QtWidgets.QComboBox()
        h_layout.addWidget(self.dropdown_menu)

        v_layout.addLayout(h_layout)

        # =========================================================================
        h_layout = QtWidgets.QHBoxLayout()
        label = QtWidgets.QLabel("Reagent name:")
        h_layout.addWidget(label)

        self.reagent_input = QtWidgets.QLineEdit()
        self.reagent_input.setFixedSize(QtCore.QSize(150, 20))
        h_layout.addWidget(self.reagent_input)

        v_layout.addLayout(h_layout)

        # =========================================================================
        h_layout = QtWidgets.QHBoxLayout()
        label = QtWidgets.QLabel("Reagent MW:")
        h_layout.addWidget(label)

        self.mw_input = QtWidgets.QLineEdit()
        self.mw_input.setFixedSize(QtCore.QSize(150, 20))
        self.mw_input.setValidator(QtGui.QDoubleValidator(bottom=MW_FIELD_MIN_VAL,
                                                          top=MW_FIELD_MAX_VAL,
                                                          decimals=MW_FIELD_DECIMAL_NO,
                                                          notation=QtGui.QDoubleValidator.StandardNotation))
        h_layout.addWidget(self.mw_input)

        v_layout.addLayout(h_layout)

        # =========================================================================
        h_layout = QtWidgets.QHBoxLayout()
        label = QtWidgets.QLabel("Product code (Optional):")
        h_layout.addWidget(label)

        self.product_code_input = QtWidgets.QLineEdit()
        self.product_code_input.setFixedSize(QtCore.QSize(150, 20))
        h_layout.addWidget(self.product_code_input)

        v_layout.addLayout(h_layout)

        # =========================================================================
        h_layout = QtWidgets.QHBoxLayout()
        label = QtWidgets.QLabel("Supplier (Optional):")
        h_layout.addWidget(label)

        self.supplier_input = QtWidgets.QLineEdit()
        self.supplier_input.setFixedSize(QtCore.QSize(150, 20))
        h_layout.addWidget(self.supplier_input)

        v_layout.addLayout(h_layout)

        # =========================================================================
        h_layout = QtWidgets.QHBoxLayout()
        label = QtWidgets.QLabel("H Codes (Optional):")
        h_layout.addWidget(label)

        self.h_code_input = QtWidgets.QLineEdit()
        self.h_code_input.setFixedSize(QtCore.QSize(150, 20))
        h_layout.addWidget(self.h_code_input)

        v_layout.addLayout(h_layout)

        # =========================================================================
        h_layout = QtWidgets.QHBoxLayout()
        self.add_item_button = QtWidgets.QPushButton("Update item...")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.add_item_button.sizePolicy().hasHeightForWidth())
        self.add_item_button.setSizePolicy(sizePolicy)
        h_layout.addWidget(self.add_item_button)

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