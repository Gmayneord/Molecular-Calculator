from PyQt5 import QtCore, QtGui, QtWidgets

from gui_functions.CommonFunctions import create_line
from data.constants import REAGENT_FIELD_MIN_VAL, REAGENT_FIELD_MAX_VAL, REAGENT_FIELD_DECIMALS_NO

class MainGUI(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.create_gui()
        self.add_elements()

    def create_gui(self):
        self.resize(440, 349)
        self.setWindowTitle("Molecular Calculator")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setFixedSize(QtCore.QSize(440, 349))

    def add_elements(self):
        self.tab_object = QtWidgets.QTabWidget(self)
        self.tab_object.setGeometry(QtCore.QRect(10, 10, 420, 300))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tab_object.sizePolicy().hasHeightForWidth())
        self.tab_object.setSizePolicy(sizePolicy)
        self.tab_object.setFixedSize(QtCore.QSize(420, 300))

        self.add_mass_tab()
        self.add_vol_tab()
        self.add_conc_tab()
        self.add_reagent_inspection_tab()

        self.close_button = QtWidgets.QPushButton("Close", self)
        self.close_button.setGeometry(QtCore.QRect(160, 314, 113, 32))
        self.close_button.setFixedSize(QtCore.QSize(113, 32))

        self.setStyleSheet('''
                           QTabWidget::tab-bar {
                               alignment: center;
                           }''')

        self.tab_object.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(self)

    def add_reagent_inspection_tab(self):
        self.reagent_inspect_tab = QtWidgets.QWidget()
        v_layout_widget = QtWidgets.QWidget(self.reagent_inspect_tab)
        v_layout_widget.setGeometry(QtCore.QRect(0, 0, 411, 271))
        v_layout = QtWidgets.QVBoxLayout(v_layout_widget)
        v_layout.setContentsMargins(10, 10, 10, 10)

        h_layout = QtWidgets.QHBoxLayout()

        select_reagent_label = QtWidgets.QLabel("Select a reagent: ", v_layout_widget)
        select_reagent_label.setFixedSize(QtCore.QSize(107, 26))
        h_layout.addWidget(select_reagent_label)

        self.i_reagent_dropdown = QtWidgets.QComboBox(v_layout_widget)
        self.i_reagent_dropdown.setFixedSize(QtCore.QSize(185, 26))
        h_layout.addWidget(self.i_reagent_dropdown)

        self.i_mw_label = QtWidgets.QLabel("MW:--", v_layout_widget)
        self.i_mw_label.setFixedSize(QtCore.QSize(85, 26))
        h_layout.addWidget(self.i_mw_label)

        v_layout.addLayout(h_layout)

        h_layout = QtWidgets.QHBoxLayout()

        self.inspect_reagent_button = QtWidgets.QPushButton("Inspect item", v_layout_widget)
        self.inspect_reagent_button.setFixedSize(QtCore.QSize(195, 32))
        h_layout.addWidget(self.inspect_reagent_button)

        v_layout.addLayout(h_layout)

        # Add in a few spacer items to make the location more in line with the rest of the interface.
        for i in range(3):
            h_layout = QtWidgets.QHBoxLayout()
            spacer = QtWidgets.QLabel("", v_layout_widget)
            h_layout.addWidget(spacer)
            v_layout.addLayout(h_layout)

        self.tab_object.addTab(self.reagent_inspect_tab, "Reagents")


    def add_mass_tab(self):
        mass_tab = QtWidgets.QWidget()
        v_layout_widget = QtWidgets.QWidget(mass_tab)
        v_layout_widget.setGeometry(QtCore.QRect(0, 0, 411, 271))
        v_layout = QtWidgets.QVBoxLayout(v_layout_widget)
        v_layout.setContentsMargins(10, 10, 10, 10)
        # =========================================================================
        h_layout = QtWidgets.QHBoxLayout()

        select_reagent_label = QtWidgets.QLabel("Select a reagent: ", v_layout_widget)
        select_reagent_label.setFixedSize(QtCore.QSize(107, 26))
        h_layout.addWidget(select_reagent_label)

        self.m_reagent_dropdown = QtWidgets.QComboBox(v_layout_widget)
        self.m_reagent_dropdown.setFixedSize(QtCore.QSize(185, 26))
        h_layout.addWidget(self.m_reagent_dropdown)

        self.m_mw_label = QtWidgets.QLabel("MW:--", v_layout_widget)
        self.m_mw_label.setFixedSize(QtCore.QSize(85, 26))
        h_layout.addWidget(self.m_mw_label)

        v_layout.addLayout(h_layout)

        # =========================================================================
        h_layout = QtWidgets.QHBoxLayout()

        conc_label = QtWidgets.QLabel("Concentration: ", v_layout_widget)
        h_layout.addWidget(conc_label)

        self.m_conc_textbox = QtWidgets.QLineEdit(v_layout_widget)
        self.m_conc_textbox.setFixedSize(QtCore.QSize(190, 21))
        self.m_conc_textbox.setValidator(QtGui.QDoubleValidator(bottom=REAGENT_FIELD_MIN_VAL,
                                                                top=REAGENT_FIELD_MAX_VAL,
                                                                decimals=REAGENT_FIELD_DECIMALS_NO,
                                                                notation=QtGui.QDoubleValidator.StandardNotation))
        h_layout.addWidget(self.m_conc_textbox)

        self.m_conc_dropdown = QtWidgets.QComboBox(v_layout_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.m_conc_dropdown.sizePolicy().hasHeightForWidth())
        self.m_conc_dropdown.setSizePolicy(sizePolicy)
        self.m_conc_dropdown.setFixedSize(QtCore.QSize(80, 26))
        h_layout.addWidget(self.m_conc_dropdown)

        v_layout.addLayout(h_layout)

        # =========================================================================
        h_layout = QtWidgets.QHBoxLayout()

        vol_label = QtWidgets.QLabel("Volume: ", v_layout_widget)
        h_layout.addWidget(vol_label)

        self.m_vol_textbox = QtWidgets.QLineEdit(v_layout_widget)
        self.m_vol_textbox.setFixedSize(QtCore.QSize(190, 21))
        self.m_vol_textbox.setValidator(QtGui.QDoubleValidator(bottom=REAGENT_FIELD_MIN_VAL,
                                                                top=REAGENT_FIELD_MAX_VAL,
                                                                decimals=REAGENT_FIELD_DECIMALS_NO,
                                                                notation=QtGui.QDoubleValidator.StandardNotation))
        h_layout.addWidget(self.m_vol_textbox)

        self.m_vol_dropdown = QtWidgets.QComboBox(v_layout_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.m_vol_dropdown.sizePolicy().hasHeightForWidth())
        self.m_vol_dropdown.setSizePolicy(sizePolicy)
        self.m_vol_dropdown.setFixedSize(QtCore.QSize(80, 26))
        h_layout.addWidget(self.m_vol_dropdown)

        v_layout.addLayout(h_layout)

        # =========================================================================
        h_layout = QtWidgets.QHBoxLayout()

        self.m_calc_button = QtWidgets.QPushButton("Calculate", v_layout_widget)
        self.m_calc_button.setFixedSize(QtCore.QSize(195, 32))
        h_layout.addWidget(self.m_calc_button)

        self.m_clear_calc_button = QtWidgets.QPushButton("Clear Calculation", v_layout_widget)
        self.m_clear_calc_button.setEnabled(False)
        self.m_clear_calc_button.setFixedSize(QtCore.QSize(194, 32))
        h_layout.addWidget(self.m_clear_calc_button)

        v_layout.addLayout(h_layout)

        # =========================================================================
        line = create_line("h")
        v_layout.addWidget(line)

        # =========================================================================
        self.m_output = QtWidgets.QLabel(v_layout_widget)
        self.m_output.setFixedSize(QtCore.QSize(391, 37))
        self.m_output.setText("")
        self.m_output.setWordWrap(True)
        self.m_output.setAlignment(QtCore.Qt.AlignCenter)
        v_layout.addWidget(self.m_output)

        # =========================================================================
        line = create_line("h")
        v_layout.addWidget(line)

        # =========================================================================
        self.tab_object.addTab(mass_tab, "Mass")
        # =========================================================================

    def add_vol_tab(self):
        vol_tab = QtWidgets.QWidget()

        v_layout_widget = QtWidgets.QWidget(vol_tab)
        v_layout_widget.setGeometry(QtCore.QRect(0, 0, 411, 271))

        v_layout = QtWidgets.QVBoxLayout(v_layout_widget)
        v_layout.setContentsMargins(10, 10, 10, 10)

        # =========================================================================
        h_layout = QtWidgets.QHBoxLayout()

        select_reagent_label = QtWidgets.QLabel("Select a reagent: ", v_layout_widget)
        select_reagent_label.setFixedSize(QtCore.QSize(107, 26))
        h_layout.addWidget(select_reagent_label)

        self.v_reagent_dropdown = QtWidgets.QComboBox(v_layout_widget)
        self.v_reagent_dropdown.setFixedSize(QtCore.QSize(185, 26))
        h_layout.addWidget(self.v_reagent_dropdown)

        self.v_mw_label = QtWidgets.QLabel("MW:--", v_layout_widget)
        self.v_mw_label.setFixedSize(QtCore.QSize(85, 26))
        h_layout.addWidget(self.v_mw_label)

        v_layout.addLayout(h_layout)

        # =========================================================================
        h_layout = QtWidgets.QHBoxLayout()

        conc_label = QtWidgets.QLabel("Concentration: ", v_layout_widget)
        h_layout.addWidget(conc_label)

        self.v_conc_textbox = QtWidgets.QLineEdit(v_layout_widget)
        self.v_conc_textbox.setFixedSize(QtCore.QSize(190, 21))
        self.v_conc_textbox.setValidator(QtGui.QDoubleValidator(bottom=REAGENT_FIELD_MIN_VAL,
                                                                top=REAGENT_FIELD_MAX_VAL,
                                                                decimals=REAGENT_FIELD_DECIMALS_NO,
                                                                notation=QtGui.QDoubleValidator.StandardNotation))
        h_layout.addWidget(self.v_conc_textbox)

        self.v_conc_dropdown = QtWidgets.QComboBox(v_layout_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.v_conc_dropdown.sizePolicy().hasHeightForWidth())
        self.v_conc_dropdown.setSizePolicy(sizePolicy)
        self.v_conc_dropdown.setFixedSize(QtCore.QSize(80, 26))
        h_layout.addWidget(self.v_conc_dropdown)

        v_layout.addLayout(h_layout)

        # =========================================================================
        h_layout = QtWidgets.QHBoxLayout()

        mass_label = QtWidgets.QLabel("Mass:", v_layout_widget)
        h_layout.addWidget(mass_label)

        self.v_mass_textbox = QtWidgets.QLineEdit(v_layout_widget)
        self.v_mass_textbox.setFixedSize(QtCore.QSize(190, 21))
        self.v_mass_textbox.setValidator(QtGui.QDoubleValidator(bottom=REAGENT_FIELD_MIN_VAL,
                                                                top=REAGENT_FIELD_MAX_VAL,
                                                                decimals=REAGENT_FIELD_DECIMALS_NO,
                                                                notation=QtGui.QDoubleValidator.StandardNotation))
        h_layout.addWidget(self.v_mass_textbox)

        self.v_mass_dropdown = QtWidgets.QComboBox(v_layout_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.v_mass_dropdown.sizePolicy().hasHeightForWidth())
        self.v_mass_dropdown.setSizePolicy(sizePolicy)
        self.v_mass_dropdown.setFixedSize(QtCore.QSize(80, 26))
        h_layout.addWidget(self.v_mass_dropdown)

        v_layout.addLayout(h_layout)

        # =========================================================================
        h_layout = QtWidgets.QHBoxLayout()

        self.v_calc_button = QtWidgets.QPushButton("Calculate", v_layout_widget)
        self.v_calc_button.setFixedSize(QtCore.QSize(195, 32))
        h_layout.addWidget(self.v_calc_button)

        self.v_clear_calc_button = QtWidgets.QPushButton("Clear Calculation", v_layout_widget)
        self.v_clear_calc_button.setEnabled(False)
        self.v_clear_calc_button.setFixedSize(QtCore.QSize(194, 32))
        h_layout.addWidget(self.v_clear_calc_button)

        v_layout.addLayout(h_layout)

        # =========================================================================
        line = QtWidgets.QFrame(v_layout_widget)
        line.setFrameShape(QtWidgets.QFrame.HLine)
        line.setFrameShadow(QtWidgets.QFrame.Sunken)
        v_layout.addWidget(line)

        self.v_output = QtWidgets.QLabel(v_layout_widget)
        self.v_output.setFixedSize(QtCore.QSize(391, 37))
        self.v_output.setText("")
        self.v_output.setWordWrap(True)
        self.v_output.setAlignment(QtCore.Qt.AlignCenter)
        v_layout.addWidget(self.v_output)

        line = QtWidgets.QFrame(v_layout_widget)
        line.setFrameShape(QtWidgets.QFrame.HLine)
        line.setFrameShadow(QtWidgets.QFrame.Sunken)
        v_layout.addWidget(line)

        # =========================================================================
        self.tab_object.addTab(vol_tab, "Volume")
        # =========================================================================

    def add_conc_tab(self):
        conc_tab = QtWidgets.QWidget()
        v_layout_widget = QtWidgets.QWidget(conc_tab)
        v_layout_widget.setGeometry(QtCore.QRect(0, 0, 411, 271))
        v_layout = QtWidgets.QVBoxLayout(v_layout_widget)
        v_layout.setContentsMargins(10, 10, 10, 10)

        # =========================================================================
        h_layout = QtWidgets.QHBoxLayout()

        select_reagent_label = QtWidgets.QLabel("Select a reagent: ", v_layout_widget)
        select_reagent_label.setFixedSize(QtCore.QSize(107, 26))
        h_layout.addWidget(select_reagent_label)

        self.c_reagent_dropdown = QtWidgets.QComboBox(v_layout_widget)
        self.c_reagent_dropdown.setFixedSize(QtCore.QSize(185, 26))
        h_layout.addWidget(self.c_reagent_dropdown)

        self.c_mw_label = QtWidgets.QLabel("MW:--", v_layout_widget)
        self.c_mw_label.setFixedSize(QtCore.QSize(85, 26))
        h_layout.addWidget(self.c_mw_label)

        v_layout.addLayout(h_layout)

        # =========================================================================
        h_layout = QtWidgets.QHBoxLayout()

        vol_label= QtWidgets.QLabel("Volume:", v_layout_widget)
        h_layout.addWidget(vol_label)

        self.c_vol_textbox = QtWidgets.QLineEdit(v_layout_widget)
        self.c_vol_textbox.setFixedSize(QtCore.QSize(190, 21))
        self.c_vol_textbox.setValidator(QtGui.QDoubleValidator(bottom=REAGENT_FIELD_MIN_VAL,
                                                                top=REAGENT_FIELD_MAX_VAL,
                                                                decimals=REAGENT_FIELD_DECIMALS_NO,
                                                                notation=QtGui.QDoubleValidator.StandardNotation))
        h_layout.addWidget(self.c_vol_textbox)

        self.c_vol_dropdown = QtWidgets.QComboBox(v_layout_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.c_vol_dropdown.sizePolicy().hasHeightForWidth())
        self.c_vol_dropdown.setSizePolicy(sizePolicy)
        self.c_vol_dropdown.setFixedSize(QtCore.QSize(80, 26))
        h_layout.addWidget(self.c_vol_dropdown)

        v_layout.addLayout(h_layout)

        # =========================================================================
        h_layout = QtWidgets.QHBoxLayout()

        mass_label = QtWidgets.QLabel("Mass:", v_layout_widget)
        h_layout.addWidget(mass_label)

        self.c_mass_textbox = QtWidgets.QLineEdit(v_layout_widget)
        self.c_mass_textbox.setFixedSize(QtCore.QSize(190, 21))
        self.c_mass_textbox.setValidator(QtGui.QDoubleValidator(bottom=REAGENT_FIELD_MIN_VAL,
                                                                top=REAGENT_FIELD_MAX_VAL,
                                                                decimals=REAGENT_FIELD_DECIMALS_NO,
                                                                notation=QtGui.QDoubleValidator.StandardNotation))
        h_layout.addWidget(self.c_mass_textbox)

        self.c_mass_dropdown = QtWidgets.QComboBox(v_layout_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.c_mass_dropdown.sizePolicy().hasHeightForWidth())
        self.c_mass_dropdown.setSizePolicy(sizePolicy)
        self.c_mass_dropdown.setFixedSize(QtCore.QSize(80, 26))
        h_layout.addWidget(self.c_mass_dropdown)

        v_layout.addLayout(h_layout)

        # =========================================================================
        h_layout = QtWidgets.QHBoxLayout()

        self.c_calc_button = QtWidgets.QPushButton("Calculate", v_layout_widget)
        self.c_calc_button.setFixedSize(QtCore.QSize(195, 32))
        h_layout.addWidget(self.c_calc_button)

        self.c_clear_calc_button = QtWidgets.QPushButton("Clear Calculation", v_layout_widget)
        self.c_clear_calc_button.setEnabled(False)
        self.c_clear_calc_button.setFixedSize(QtCore.QSize(194, 32))
        h_layout.addWidget(self.c_clear_calc_button)

        v_layout.addLayout(h_layout)

        # =========================================================================
        line = create_line("h")
        v_layout.addWidget(line)

        self.c_output = QtWidgets.QLabel(v_layout_widget)
        self.c_output.setFixedSize(QtCore.QSize(391, 37))
        self.c_output.setText("")
        self.c_output.setWordWrap(True)
        self.c_output.setAlignment(QtCore.Qt.AlignCenter)
        v_layout.addWidget(self.c_output)

        line = create_line("h")
        v_layout.addWidget(line)

        # =========================================================================
        self.tab_object.addTab(conc_tab, "Concentration")
        # =========================================================================
