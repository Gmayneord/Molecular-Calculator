"""
Created on Tue Dec 13 08:38:33 2022

@author: g.mayneord
"""

from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from os import path, mkdir
from json import dump, load

# =====================================================================
# Parameters:
# =====================================================================
# Storage location of file:
DATA_STORAGE_FILE_LOC = "Stored_data.json"

# ===============================
# Cycle of tabs
# ===============================
GUI_TABS = ["m", "c", "v"]

# ===============================
# Range of units
# ===============================

CONC_SCALER_DICT = {"M": 1,
                    "mM": 0.001,
                    "uM": 0.000001,
                    "nM": 0.000000001,
                    }

VOL_SCALER_DICT = {"L": 1,
                   "mL": 0.001,
                   "uL": 0.000001,
                   "nL": 0.000000001,
                   }

MASS_SCALER_DICT = {"kg": 1000,
                    "g": 1,
                    "mg": 0.001,
                    "ug": 0.000001,
                    "ng": 0.000000001,
                    }

CONC_SCALER_DEFAULT = "mM"
VOL_SCALER_DEFAULT = "mL"
MASS_SCALER_DEFAULT = "g"

# Text for commands from text boxes
ADD_NEW_ITEM_TEXT = "Add new item..."
DELETE_ITEM_TEXT = "Delete item..."
EDIT_ITEM_TEXT = "Edit item..."


# =====================================================================
# Processing functions:
# =====================================================================
def populateDropdownBox(dropdown_box_object, list_to_populate, additional_opt=False, sort_list=True):
    dropdown_box_object.clear()
    if sort_list:
        list_to_populate = sorted(list_to_populate, key=str.lower)

    # If we want to add the options to the dropdown box...
    if additional_opt:
        list_to_populate.append(ADD_NEW_ITEM_TEXT)
        list_to_populate.append(DELETE_ITEM_TEXT)
        list_to_populate.append(EDIT_ITEM_TEXT)

    for each_item in list_to_populate:
        dropdown_box_object.addItem(each_item)


def errorHighlight(field_to_change):
    field_to_change.setStyleSheet("background: red")


def errorReset(field_to_change):
    field_to_change.setStyleSheet("background: None")


def createDirPath(path_for_creation):
    real_dir = False
    existing_path = path_for_creation
    directories_to_create = []
    while real_dir is False:
        if path.isdir(existing_path):
            real_dir = True
        else:
            directories_to_create.append(path.basename(existing_path))
            existing_path = path.dirname(existing_path)
    directories_to_create.reverse()

    for each_dir in directories_to_create:
        existing_path = path.join(existing_path, each_dir)
        mkdir(existing_path)


def initialRun():
    # Run if no data file is detected. Will sort out making the file.xw
    file_data = {"Reagents": {}}
    with open(DATA_STORAGE_FILE_LOC, "w") as file_obj:
        dump(file_data, file_obj)
    file_obj.close()
    return file_data


# =====================================================================
# GUI elements:
# =====================================================================
# Allow dialog scaling on high resolution displays (e.g. 4K)
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)


class MainWindow():
    def __init__(self):
        self.Gui = GenerateMainGUI()

        if path.isfile(DATA_STORAGE_FILE_LOC) is False:
            self.stored_data = initialRun()
            for each_tab in GUI_TABS:
                exec(f"self.Gui.{each_tab}_output.setText('First runtime detected... A new data storage file has been created!')")

        else:
            self.stored_data = self.readFromStorage(DATA_STORAGE_FILE_LOC)

        self.dialog_busy = False
        self.fillDropdownMenus()
        self.connectButtons()

    def connectButtons(self):
        Gui = self.Gui
        Gui.close_button.clicked.connect(self.closeButtonAction)

        Gui.m_calc_button.clicked.connect(self.m_calculateButtonAction)
        Gui.m_clear_calc_button.clicked.connect(lambda: self.clearCalculationAction(Gui.m_output, Gui.m_calc_button, Gui.m_clear_calc_button))

        Gui.v_calc_button.clicked.connect(self.v_calculateButtonAction)
        Gui.v_clear_calc_button.clicked.connect(lambda: self.clearCalculationAction(Gui.v_output, Gui.v_calc_button, Gui.v_clear_calc_button))

        Gui.c_calc_button.clicked.connect(self.c_calculateButtonAction)
        Gui.c_clear_calc_button.clicked.connect(lambda: self.clearCalculationAction(Gui.c_output, Gui.c_calc_button, Gui.c_clear_calc_button))

    def fillDropdownMenus(self):
        def fillScalingDropdown(dropdown_obj, population_dict, default_val):
            populateDropdownBox(dropdown_obj,
                                list(population_dict),
                                sort_list=False)
            dropdown_obj.setCurrentIndex(dropdown_obj.findText(default_val))

        def fillReagentDropdown(dropdown_obj, mw_label_obk):
            populateDropdownBox(dropdown_obj, list(self.stored_data['Reagents'].keys()), additional_opt=True)
            if len(list(self.stored_data["Reagents"].keys())) != 0:
                self.reagentSelectedAction(dropdown_obj, mw_label_obk)
            # Also set up action for when dropdown menu item is selected
            dropdown_obj.activated[str].connect(lambda: self.reagentSelectedAction(dropdown_obj, mw_label_obk))

        Gui = self.Gui
        # Assign dropdown menus in Mass tab:
        fillScalingDropdown(Gui.m_conc_dropdown, CONC_SCALER_DICT, CONC_SCALER_DEFAULT)
        fillScalingDropdown(Gui.m_vol_dropdown, VOL_SCALER_DICT, VOL_SCALER_DEFAULT)
        fillReagentDropdown(Gui.m_reagent_dropdown, Gui.m_mw_label)

        # Assign dropdown menus to Volume tab:
        fillScalingDropdown(Gui.v_conc_dropdown, CONC_SCALER_DICT, CONC_SCALER_DEFAULT)
        fillScalingDropdown(Gui.v_mass_dropdown, MASS_SCALER_DICT, MASS_SCALER_DEFAULT)
        fillReagentDropdown(Gui.v_reagent_dropdown, Gui.v_mw_label)

        fillScalingDropdown(Gui.c_vol_dropdown, VOL_SCALER_DICT, VOL_SCALER_DEFAULT)
        fillScalingDropdown(Gui.c_mass_dropdown, MASS_SCALER_DICT, MASS_SCALER_DEFAULT)
        fillReagentDropdown(Gui.c_reagent_dropdown, Gui.c_mw_label)

    def reagentSelectedAction(self, dropdown_obj, mw_label_obj):
        if self.dialog_busy is False:
            self.current_dropdown_text = dropdown_obj.currentText()
            if self.current_dropdown_text == ADD_NEW_ITEM_TEXT:
                self.add_item_window = AddWindow(dropdown_obj)
                self.add_item_window.show()
                # Need to write add new item class
            elif self.current_dropdown_text == DELETE_ITEM_TEXT:
                self.delete_new_window = DeleteWindow(dropdown_obj)
                self.delete_new_window.show()
            # Also need to write this
            elif self.current_dropdown_text == EDIT_ITEM_TEXT:
                self.edit_window = EditWindow(dropdown_obj)
                self.edit_window.show()
            else:
                # Update the molecular weight label with the current selected item
                reagent_choice = self.stored_data["Reagents"][self.current_dropdown_text]
                self.updateMWLabel(mw_label_obj, reagent_choice)

    def clearCalculationAction(self, text_to_reset, calc_button, clear_button):
        text_to_reset.setText(" ")
        calc_button.setDisabled(False)
        clear_button.setDisabled(True)

    def m_calculateButtonAction(self):
        Gui = self.Gui
        errorReset(Gui.m_conc_textbox)
        errorReset(Gui.m_vol_textbox)
        reagent_selection_box = Gui.m_reagent_dropdown

        conc_textbox = Gui.m_conc_textbox
        conc_scaler = Gui.m_conc_dropdown
        vol_textbox = Gui.m_vol_textbox
        vol_scaler = Gui.m_vol_dropdown

        # Check for blank fields
        if conc_textbox.text() == "":
            errorHighlight(conc_textbox)

        if vol_textbox.text() == "":
            errorHighlight(vol_textbox)

        if reagent_selection_box.currentText() == ADD_NEW_ITEM_TEXT:
            errorHighlight(reagent_selection_box)

        if conc_textbox.text() != "" and vol_textbox.text() != "" and reagent_selection_box.currentText() != ADD_NEW_ITEM_TEXT:
            concentration = float(conc_textbox.text())
            volume = float(vol_textbox.text())
            molecular_weight = float(self.stored_data["Reagents"][reagent_selection_box.currentText()])
            self.massCalculationAndDisplay(input_conc=concentration,
                                           input_vol=volume,
                                           inputMW=molecular_weight,
                                           vol_scaler=vol_scaler.currentText(),
                                           conc_scaler=conc_scaler.currentText(),
                                           reagent_name=reagent_selection_box.currentText())

    def v_calculateButtonAction(self):
        Gui = self.Gui
        errorReset(Gui.v_conc_textbox)
        errorReset(Gui.v_mass_textbox)
        reagent_selection_box = Gui.v_reagent_dropdown

        conc_textbox = Gui.v_conc_textbox
        conc_scaler = Gui.v_conc_dropdown
        mass_textbox = Gui.v_mass_textbox
        mass_scaler = Gui.v_mass_dropdown

        # Check for blank fields
        if conc_textbox.text() == "":
            errorHighlight(conc_textbox)

        if mass_textbox.text() == "":
            errorHighlight(mass_textbox)

        if reagent_selection_box.currentText() == ADD_NEW_ITEM_TEXT:
            errorHighlight(reagent_selection_box)

        if conc_textbox.text() != "" and mass_textbox.text() != "" and reagent_selection_box.currentText() != ADD_NEW_ITEM_TEXT:
            concentration = float(conc_textbox.text())
            mass = float(mass_textbox.text())
            molecular_weight = float(self.stored_data["Reagents"][reagent_selection_box.currentText()])

            self.volCalculationAndDisplay(input_conc=concentration,
                                          conc_scaler=conc_scaler.currentText(),
                                          input_mass=mass,
                                          mass_scaler=mass_scaler.currentText(),
                                          inputMW=molecular_weight,
                                          reagent_name=reagent_selection_box.currentText())

    def c_calculateButtonAction(self):
        Gui = self.Gui
        mass_textbox = Gui.c_mass_textbox
        vol_textbox = Gui.c_vol_textbox

        errorReset(vol_textbox)
        errorReset(mass_textbox)
        reagent_selection_box = Gui.c_reagent_dropdown

        vol_scaler = Gui.c_vol_dropdown
        mass_scaler = Gui.c_mass_dropdown

        # Check for blank fields
        if vol_textbox.text() == "":
            errorHighlight(vol_textbox)

        if mass_textbox.text() == "":
            errorHighlight(mass_textbox)

        if reagent_selection_box.currentText() == ADD_NEW_ITEM_TEXT:
            errorHighlight(reagent_selection_box)

        if vol_textbox.text() != "" and mass_textbox.text() != "" and reagent_selection_box.currentText() != ADD_NEW_ITEM_TEXT:
            vol = float(vol_textbox.text())
            mass = float(mass_textbox.text())
            molecular_weight = float(self.stored_data["Reagents"][reagent_selection_box.currentText()])

            self.concCalculationAndDisplay(input_mass=mass,
                                           mass_scaler=mass_scaler.currentText(),
                                           input_vol=vol,
                                           vol_scaler=vol_scaler.currentText(),
                                           inputMW=molecular_weight,
                                           reagent_name=reagent_selection_box.currentText())

    def closeButtonAction(self):
        self.Gui.close()

    def updateMWLabel(self, mw_label_obj, molecular_weight):
        mw_label_obj.setText("MW: " + str(molecular_weight))

    def massCalculationAndDisplay(self, input_conc, conc_scaler, input_vol, vol_scaler, inputMW, reagent_name):
        conc_scale_factor = CONC_SCALER_DICT[conc_scaler]
        vol_scale_factor = VOL_SCALER_DICT[vol_scaler]

        scaled_conc = input_conc * conc_scale_factor
        scaled_vol = input_vol * vol_scale_factor

        calc_mass = scaled_conc * scaled_vol * inputMW

        adj_calc_mass = None

        # Work out magnitude for output number
        for mass_mag in MASS_SCALER_DICT:
            # Calculated value starts off small, and increases with each iteration. When it is above 1 we know we're on the right scale (e.g. mg)
            if calc_mass / MASS_SCALER_DICT[mass_mag] > 1:
                adj_calc_mass = str.format('{0:.2f}', calc_mass / MASS_SCALER_DICT[mass_mag])
                break
        if adj_calc_mass is None:
            self.Gui.m_output.setText("The current calculation is out of bounds of the pre-defined scaling parameters. Please consider increasing scaling parameters to fix this")
        else:
            self.Gui.m_output.setText(f"For {input_vol}{vol_scaler} of {input_conc}{conc_scaler} use {adj_calc_mass}{mass_mag} of {reagent_name}")
            self.Gui.m_calc_button.setDisabled(True)
            self.Gui.m_clear_calc_button.setDisabled(False)

    def volCalculationAndDisplay(self, input_conc, conc_scaler, input_mass, mass_scaler, inputMW, reagent_name):
        mass_scale_factor = MASS_SCALER_DICT[mass_scaler]
        conc_scale_factor = CONC_SCALER_DICT[conc_scaler]

        scaled_mass = input_mass * mass_scale_factor
        scaled_conc = input_conc * conc_scale_factor

        calc_vol = (scaled_mass / inputMW) / scaled_conc

        adj_calc_vol = None

        # Work out magnitude for output number
        for vol_mag in VOL_SCALER_DICT:
            # Calculated value starts off small, and increases with each iteration. When it is above 1 we know we're on the right scale (e.g. mg)
            if calc_vol / VOL_SCALER_DICT[vol_mag] > 1:
                adj_calc_vol = str.format('{0:.2f}', calc_vol / VOL_SCALER_DICT[vol_mag])
                break

        if adj_calc_vol is None:
            self.Gui.v_output.setText("The current calculation is out of bounds of the pre-defined scaling parameters. Please consider increasing scaling parameters to fix this")
        else:
            self.Gui.v_output.setText(f"For {input_conc}{conc_scaler} using {input_mass}{mass_scaler} of {reagent_name}, use a total volume of {adj_calc_vol}{vol_mag}")
            self.Gui.v_calc_button.setDisabled(True)
            self.Gui.v_clear_calc_button.setDisabled(False)

    def concCalculationAndDisplay(self, input_mass, mass_scaler, input_vol, vol_scaler, inputMW, reagent_name):
        mass_scale_factor = MASS_SCALER_DICT[mass_scaler]
        vol_scale_factor = VOL_SCALER_DICT[vol_scaler]

        scaled_mass = input_mass * mass_scale_factor
        scaled_vol = input_vol * vol_scale_factor

        calc_conc = (scaled_mass / inputMW) / scaled_vol

        adj_calc_conc = None

        # Work out magnitude for output number
        for conc_mag in CONC_SCALER_DICT:
            # Calculated value starts off small, and increases with each iteration. When it is above 1 we know we're on the right scale (e.g. mg)
            if calc_conc / CONC_SCALER_DICT[conc_mag] > 1:
                adj_calc_conc = str.format('{0:.2f}', calc_conc / CONC_SCALER_DICT[conc_mag])
                break

        if adj_calc_conc is None:
            self.Gui.c_output.setText("The current calculation is out of bounds of the pre-defined scaling parameters. Please consider increasing scaling parameters to fix this")
        else:
            self.Gui.c_output.setText(f"With {input_mass}{mass_scaler} of {reagent_name} in {input_vol}{vol_scaler} you will have {adj_calc_conc}{conc_mag}")
            self.Gui.c_calc_button.setDisabled(True)
            self.Gui.c_clear_calc_button.setDisabled(False)

    def readFromStorage(self, file_to_read, specific_section=None):
        with open(file_to_read, "r") as file_obj:
            stored_data = load(file_obj)
        file_obj.close()

        if specific_section is None:
            return stored_data
        else:
            return stored_data[specific_section]

    def writeToStorage(self, section_to_update, selected_element, del_item=False):
        if del_item:
            del self.stored_data[section_to_update][selected_element]
        else:
            self.stored_data[section_to_update][selected_element["name"]] = selected_element["data"]

        # Write this new edited data into the file.
        with open(DATA_STORAGE_FILE_LOC, "w") as file_obj:
            dump(self.stored_data, file_obj)
        file_obj.close()

        if del_item:
            self.updateReagentDropdowns(None)
        else:
            self.updateReagentDropdowns(selected_element["name"])

    def updateReagentDropdowns(self, reagent_selected):
        reagent_data = self.stored_data["Reagents"]
        dropdown_list = [self.Gui.m_reagent_dropdown,
                         self.Gui.v_reagent_dropdown,
                         self.Gui.c_reagent_dropdown]

        mw_label_list = [self.Gui.m_mw_label,
                         self.Gui.v_mw_label,
                         self.Gui.c_mw_label]

        for obj_no in range(len(dropdown_list)):
            dropdown_obj = dropdown_list[obj_no]
            populateDropdownBox(dropdown_obj, reagent_data, additional_opt=True)

            if reagent_selected is None:
                dropdown_index = 0
            else:
                dropdown_index = dropdown_obj.findText(reagent_selected)
            dropdown_obj.setCurrentIndex(dropdown_index)

            if len(reagent_data) > 0:
                self.updateMWLabel(mw_label_list[obj_no],
                                   reagent_data[dropdown_obj.currentText()])
            else:
                self.updateMWLabel(mw_label_list[obj_no],
                                   "--")


class DeleteWindow(QtWidgets.QMainWindow):
    def __init__(self, dropdown_obj):
        super().__init__()
        main.dialog_busy = True
        self.createGUI()
        self.connectButtons()
        self.reset_main_dropbox = True
        self.dropdown_obj = dropdown_obj

    def createGUI(self):
        self.setWindowTitle("Delete items")
        self.resize(300, 100)
        v_layout = QtWidgets.QVBoxLayout()
        h_layout = QtWidgets.QHBoxLayout()
        label = QtWidgets.QLabel("Delete item:")
        h_layout.addWidget(label)
        self.dropdown_menu = QtWidgets.QComboBox()
        self.dropdown_menu.setMinimumSize(QtCore.QSize(150, 20))
        self.dropdown_menu.setMaximumSize(QtCore.QSize(150, 20))
        # Populate the list with items stored from the main data storage
        populateDropdownBox(self.dropdown_menu, list(main.stored_data["Reagents"]))

        h_layout.addWidget(self.dropdown_menu)
        self.delete_button = QtWidgets.QPushButton("Delete...")
        h_layout.addWidget(self.delete_button)

        v_layout.addLayout(h_layout)

        h_layout = QtWidgets.QHBoxLayout()
        self.close_button = QtWidgets.QPushButton("Close")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.close_button.sizePolicy().hasHeightForWidth())
        self.close_button.setSizePolicy(sizePolicy)

        h_layout.addWidget(self.close_button)
        v_layout.addLayout(h_layout)

        widget = QtWidgets.QWidget()
        widget.setLayout(v_layout)
        self.setCentralWidget(widget)
        widget.setContentsMargins(10, 10, 10, 10)

    def connectButtons(self):
        self.close_button.clicked.connect(self.closeButtonAction)
        self.delete_button.clicked.connect(self.deleteButtonAction)

    # ===================================
    # GUI actions:
    # ===================================
    def closeButtonAction(self):
        if self.reset_main_dropbox is True:
            self.dropdown_obj.setCurrentIndex(0)
        main.dialog_busy = False
        self.close()

    def deleteButtonAction(self):
        errorReset(self.dropdown_menu)
        if self.dropdown_menu.currentText() != "":
            self.reset_main_dropbox = False
            # Turn off button to avoid accidental multiple activations
            self.delete_button.setEnabled(False)
            # Remove it and write the change to the file
            main.writeToStorage("Reagents", self.dropdown_menu.currentText(), del_item=True)

            # Also update the dropdown box in the delete window GUI.
            populateDropdownBox(self.dropdown_menu, list(main.stored_data["Reagents"]), additional_opt=False)

            # Wait a moment to avoid multiple clicks
            QtCore.QTimer.singleShot(1000, lambda: self.delete_button.setEnabled(True))
        else:
            errorHighlight(self.dropdown_menu)


class AddWindow(QtWidgets.QMainWindow):
    def __init__(self, dropdown_obj):
        super().__init__()
        main.dialog_busy = True
        self.createGUI()
        self.connectButtons()
        self.reset_main_dropbox = True
        # Save where we currently spawned this from, so we can go back to it later
        self.dropdown_obj = dropdown_obj

    def createGUI(self):
        self.setWindowTitle("Add items")
        self.resize(300, 100)
        v_layout = QtWidgets.QVBoxLayout()
        h_layout = QtWidgets.QHBoxLayout()
        label = QtWidgets.QLabel("Reagent name:")
        h_layout.addWidget(label)
        self.reagent_input = QtWidgets.QLineEdit()
        self.reagent_input.setMinimumSize(QtCore.QSize(150, 20))
        self.reagent_input.setMaximumSize(QtCore.QSize(150, 20))
        h_layout.addWidget(self.reagent_input)
        v_layout.addLayout(h_layout)

        h_layout = QtWidgets.QHBoxLayout()
        label = QtWidgets.QLabel("Reagent MW:")
        h_layout.addWidget(label)
        self.reagent_MW = QtWidgets.QLineEdit()
        self.reagent_MW.setMinimumSize(QtCore.QSize(150, 20))
        self.reagent_MW.setMaximumSize(QtCore.QSize(150, 20))
        h_layout.addWidget(self.reagent_MW)
        v_layout.addLayout(h_layout)

        h_layout = QtWidgets.QHBoxLayout()
        self.add_item_button = QtWidgets.QPushButton("Add item...")
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

        widget = QtWidgets.QWidget()
        widget.setLayout(v_layout)
        self.setCentralWidget(widget)
        widget.setContentsMargins(10, 10, 10, 10)

    def connectButtons(self):
        self.add_item_button.clicked.connect(self.add_item_action)
        self.close_button.clicked.connect(self.closeButtonAction)

    # ===================================
    # GUI actions:
    # ===================================
    def closeButtonAction(self):
        if self.reset_main_dropbox is True:
            self.dropdown_obj.setCurrentIndex(0)
        main.dialog_busy = False
        self.close()

    def add_item_action(self):
        errorReset(self.reagent_input)
        errorReset(self.reagent_MW)
        errorReset(self.dropdown_obj)

        if self.reagent_input != "" and self.reagent_MW != "":
            self.reset_main_dropbox = False
            # Remove it and write the change to the file
            main.writeToStorage("Reagents",
                                {"name": self.reagent_input.text(),
                                 "data": float(self.reagent_MW.text())})

            # Set the index on the dropdown box to be the new item...
            # self.dropdown_obj.setCurrentIndex(self.dropdown_obj.findText(self.reagent_input.text()))
            # Close the dialog
            self.closeButtonAction()
        else:
            if self.reagent_input == "":
                errorHighlight(self.reagent_input)
            if self.reagent_MW == "":
                errorHighlight(self.reagent_MW)


class EditWindow(QtWidgets.QMainWindow):
    def __init__(self, dropdown_obj):
        super().__init__()
        main.dialog_busy = True
        self.create_GUI()
        self.connectButtons()
        self.reset_main_dropbox = True
        self.dropdown_obj = dropdown_obj

    def create_GUI(self):
        self.setWindowTitle("Edit items")
        self.resize(300, 100)
        v_layout = QtWidgets.QVBoxLayout()

        h_layout = QtWidgets.QHBoxLayout()
        label = QtWidgets.QLabel("Select a reagent:")
        h_layout.addWidget(label)
        self.dropdown_menu = QtWidgets.QComboBox()
        h_layout.addWidget(self.dropdown_menu)
        # Populate the list with items stored from the main data storage
        populateDropdownBox(self.dropdown_menu, list(main.stored_data["Reagents"]))
        v_layout.addLayout(h_layout)

        h_layout = QtWidgets.QHBoxLayout()
        label = QtWidgets.QLabel("Reagent name:")
        h_layout.addWidget(label)
        self.reagent_input = QtWidgets.QLineEdit()
        self.reagent_input.setMinimumSize(QtCore.QSize(150, 20))
        self.reagent_input.setMaximumSize(QtCore.QSize(150, 20))
        h_layout.addWidget(self.reagent_input)
        v_layout.addLayout(h_layout)

        h_layout = QtWidgets.QHBoxLayout()
        label = QtWidgets.QLabel("Reagent MW:")
        h_layout.addWidget(label)
        self.reagent_MW = QtWidgets.QLineEdit()
        self.reagent_MW.setMinimumSize(QtCore.QSize(150, 20))
        self.reagent_MW.setMaximumSize(QtCore.QSize(150, 20))
        h_layout.addWidget(self.reagent_MW)
        v_layout.addLayout(h_layout)

        h_layout = QtWidgets.QHBoxLayout()
        self.add_item_button = QtWidgets.QPushButton("Re-write item...")
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

        widget = QtWidgets.QWidget()
        widget.setLayout(v_layout)
        self.setCentralWidget(widget)
        widget.setContentsMargins(10, 10, 10, 10)

    def connectButtons(self):
        self.add_item_button.clicked.connect(self.editItemAction)
        self.close_button.clicked.connect(self.closeButtonAction)
        self.dropdown_menu.activated[str].connect(self.dropdownSelectedAction)
        self.dropdownSelectedAction()

    # ===================================
    # GUI actions:
    # ===================================
    def closeButtonAction(self):
        if self.reset_main_dropbox is True:
            main.mainWindow.reagent_selection_dropdown.setCurrentIndex(0)
        main.dialog_busy = False
        self.close()

    def dropdownSelectedAction(self):
        self.reagent_input.setText(self.dropdown_menu.currentText())
        if self.dropdown_menu.currentText() != "":
            self.reagent_MW.setText(str(main.stored_data["Reagents"][self.dropdown_menu.currentText()]))

    def editItemAction(self):
        errorReset(self.reagent_input)
        errorReset(self.reagent_MW)

        if self.reagent_input != "" and self.reagent_MW != "":
            self.reset_main_dropbox = False

            # Delete the old item.
            # main.writeToStorage("Reagents", self.dropdown_menu.currentText(), del_item=True)

            # Write the nw item and write change to the file
            main.writeToStorage("Reagents", {"name": self.reagent_input.text(),
                                             "data": float(self.reagent_MW.text())})
            # Close the dialog
            self.closeButtonAction()

        else:
            if self.reagent_input == "":
                errorHighlight(self.reagent_input)
            if self.reagent_MW == "":
                errorHighlight(self.reagent_MW)


class GenerateMainGUI(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.createGUI()
        self.retranslateUi()

    def createGUI(self):
        self.resize(440, 349)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setMinimumSize(QtCore.QSize(440, 349))
        self.setMaximumSize(QtCore.QSize(440, 349))
        self.tab_object = QtWidgets.QTabWidget(self)
        self.tab_object.setGeometry(QtCore.QRect(10, 10, 420, 300))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tab_object.sizePolicy().hasHeightForWidth())
        self.tab_object.setSizePolicy(sizePolicy)
        self.tab_object.setMinimumSize(QtCore.QSize(420, 300))
        self.tab_object.setMaximumSize(QtCore.QSize(420, 29))
        self.tab_object.setObjectName("tab_object")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.tab)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 411, 271))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(10, 10, 10, 10)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label.setMinimumSize(QtCore.QSize(107, 26))
        self.label.setMaximumSize(QtCore.QSize(107, 26))
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.m_reagent_dropdown = QtWidgets.QComboBox(self.verticalLayoutWidget)
        self.m_reagent_dropdown.setMinimumSize(QtCore.QSize(185, 26))
        self.m_reagent_dropdown.setMaximumSize(QtCore.QSize(129, 26))
        self.m_reagent_dropdown.setObjectName("m_reagent_dropdown")
        self.horizontalLayout.addWidget(self.m_reagent_dropdown)
        self.m_mw_label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.m_mw_label.setMinimumSize(QtCore.QSize(85, 26))
        self.m_mw_label.setMaximumSize(QtCore.QSize(85, 26))
        self.m_mw_label.setObjectName("m_mw_label")
        self.horizontalLayout.addWidget(self.m_mw_label)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_3 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_2.addWidget(self.label_3)
        self.m_conc_textbox = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.m_conc_textbox.setMinimumSize(QtCore.QSize(190, 21))
        self.m_conc_textbox.setMaximumSize(QtCore.QSize(190, 21))
        self.m_conc_textbox.setObjectName("m_conc_textbox")
        self.m_conc_textbox.setValidator(QtGui.QDoubleValidator(0.00, 1000, 1))
        self.horizontalLayout_2.addWidget(self.m_conc_textbox)
        self.m_conc_dropdown = QtWidgets.QComboBox(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.m_conc_dropdown.sizePolicy().hasHeightForWidth())
        self.m_conc_dropdown.setSizePolicy(sizePolicy)
        self.m_conc_dropdown.setMinimumSize(QtCore.QSize(80, 26))
        self.m_conc_dropdown.setMaximumSize(QtCore.QSize(80, 26))
        self.m_conc_dropdown.setObjectName("m_conc_dropdown")
        self.horizontalLayout_2.addWidget(self.m_conc_dropdown)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_4 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_3.addWidget(self.label_4)
        self.m_vol_textbox = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.m_vol_textbox.setMinimumSize(QtCore.QSize(190, 21))
        self.m_vol_textbox.setMaximumSize(QtCore.QSize(190, 21))
        self.m_vol_textbox.setObjectName("m_vol_textbox")
        self.m_vol_textbox.setValidator(QtGui.QDoubleValidator(0.00, 1000, 1))
        self.horizontalLayout_3.addWidget(self.m_vol_textbox)
        self.m_vol_dropdown = QtWidgets.QComboBox(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.m_vol_dropdown.sizePolicy().hasHeightForWidth())
        self.m_vol_dropdown.setSizePolicy(sizePolicy)
        self.m_vol_dropdown.setMinimumSize(QtCore.QSize(80, 26))
        self.m_vol_dropdown.setMaximumSize(QtCore.QSize(8, 26))
        self.m_vol_dropdown.setObjectName("m_vol_dropdown")
        self.horizontalLayout_3.addWidget(self.m_vol_dropdown)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.m_calc_button = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.m_calc_button.setMinimumSize(QtCore.QSize(195, 32))
        self.m_calc_button.setMaximumSize(QtCore.QSize(195, 32))
        self.m_calc_button.setObjectName("m_calc_button")
        self.horizontalLayout_4.addWidget(self.m_calc_button)
        self.m_clear_calc_button = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.m_clear_calc_button.setMinimumSize(QtCore.QSize(194, 32))
        self.m_clear_calc_button.setMaximumSize(QtCore.QSize(194, 32))
        self.m_clear_calc_button.setObjectName("m_clear_calc_button")
        self.horizontalLayout_4.addWidget(self.m_clear_calc_button)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.line = QtWidgets.QFrame(self.verticalLayoutWidget)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.m_output = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.m_output.setMinimumSize(QtCore.QSize(391, 37))
        self.m_output.setMaximumSize(QtCore.QSize(391, 37))
        self.m_output.setText("")
        self.m_output.setAlignment(QtCore.Qt.AlignCenter)
        self.m_output.setObjectName("m_output")
        self.verticalLayout.addWidget(self.m_output)
        self.line_2 = QtWidgets.QFrame(self.verticalLayoutWidget)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.verticalLayout.addWidget(self.line_2)
        self.tab_object.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.tab_2)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(0, 0, 411, 271))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_6.setContentsMargins(10, 10, 10, 10)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.horizontalLayout_21 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_21.setObjectName("horizontalLayout_21")
        self.label_10 = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.label_10.setMinimumSize(QtCore.QSize(107, 26))
        self.label_10.setMaximumSize(QtCore.QSize(107, 26))
        self.label_10.setObjectName("label_10")
        self.horizontalLayout_21.addWidget(self.label_10)
        self.v_reagent_dropdown = QtWidgets.QComboBox(self.verticalLayoutWidget_2)
        self.v_reagent_dropdown.setMinimumSize(QtCore.QSize(185, 26))
        self.v_reagent_dropdown.setMaximumSize(QtCore.QSize(129, 26))
        self.v_reagent_dropdown.setObjectName("v_reagent_dropdown")
        self.horizontalLayout_21.addWidget(self.v_reagent_dropdown)
        self.v_mw_label = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.v_mw_label.setMinimumSize(QtCore.QSize(85, 26))
        self.v_mw_label.setMaximumSize(QtCore.QSize(85, 26))
        self.v_mw_label.setObjectName("v_mw_label")
        self.horizontalLayout_21.addWidget(self.v_mw_label)
        self.verticalLayout_6.addLayout(self.horizontalLayout_21)
        self.horizontalLayout_22 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_22.setObjectName("horizontalLayout_22")
        self.label_21 = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.label_21.setObjectName("label_21")
        self.horizontalLayout_22.addWidget(self.label_21)
        self.v_conc_textbox = QtWidgets.QLineEdit(self.verticalLayoutWidget_2)
        self.v_conc_textbox.setMinimumSize(QtCore.QSize(190, 21))
        self.v_conc_textbox.setMaximumSize(QtCore.QSize(190, 21))
        self.v_conc_textbox.setObjectName("v_conc_textbox")
        self.v_conc_textbox.setValidator(QtGui.QDoubleValidator(0.00, 1000, 1))
        self.horizontalLayout_22.addWidget(self.v_conc_textbox)
        self.v_conc_dropdown = QtWidgets.QComboBox(self.verticalLayoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.v_conc_dropdown.sizePolicy().hasHeightForWidth())
        self.v_conc_dropdown.setSizePolicy(sizePolicy)
        self.v_conc_dropdown.setMinimumSize(QtCore.QSize(80, 26))
        self.v_conc_dropdown.setMaximumSize(QtCore.QSize(80, 26))
        self.v_conc_dropdown.setObjectName("v_conc_dropdown")
        self.horizontalLayout_22.addWidget(self.v_conc_dropdown)
        self.verticalLayout_6.addLayout(self.horizontalLayout_22)
        self.horizontalLayout_23 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_23.setObjectName("horizontalLayout_23")
        self.label_22 = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.label_22.setObjectName("label_22")
        self.horizontalLayout_23.addWidget(self.label_22)
        self.v_mass_textbox = QtWidgets.QLineEdit(self.verticalLayoutWidget_2)
        self.v_mass_textbox.setMinimumSize(QtCore.QSize(190, 21))
        self.v_mass_textbox.setMaximumSize(QtCore.QSize(190, 21))
        self.v_mass_textbox.setObjectName("v_mass_textbox")
        self.v_mass_textbox.setValidator(QtGui.QDoubleValidator(0.00, 1000, 1))
        self.horizontalLayout_23.addWidget(self.v_mass_textbox)
        self.v_mass_dropdown = QtWidgets.QComboBox(self.verticalLayoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.v_mass_dropdown.sizePolicy().hasHeightForWidth())
        self.v_mass_dropdown.setSizePolicy(sizePolicy)
        self.v_mass_dropdown.setMinimumSize(QtCore.QSize(80, 26))
        self.v_mass_dropdown.setMaximumSize(QtCore.QSize(8, 26))
        self.v_mass_dropdown.setObjectName("v_mass_dropdown")
        self.horizontalLayout_23.addWidget(self.v_mass_dropdown)
        self.verticalLayout_6.addLayout(self.horizontalLayout_23)
        self.horizontalLayout_24 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_24.setObjectName("horizontalLayout_24")
        self.v_calc_button = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        self.v_calc_button.setMinimumSize(QtCore.QSize(195, 32))
        self.v_calc_button.setMaximumSize(QtCore.QSize(195, 32))
        self.v_calc_button.setObjectName("v_calc_button")
        self.horizontalLayout_24.addWidget(self.v_calc_button)
        self.v_clear_calc_button = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        self.v_clear_calc_button.setMinimumSize(QtCore.QSize(194, 32))
        self.v_clear_calc_button.setMaximumSize(QtCore.QSize(194, 32))
        self.v_clear_calc_button.setObjectName("v_clear_calc_button")
        self.horizontalLayout_24.addWidget(self.v_clear_calc_button)
        self.verticalLayout_6.addLayout(self.horizontalLayout_24)
        self.line_11 = QtWidgets.QFrame(self.verticalLayoutWidget_2)
        self.line_11.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_11.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_11.setObjectName("line_11")
        self.verticalLayout_6.addWidget(self.line_11)
        self.v_output = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.v_output.setMinimumSize(QtCore.QSize(391, 37))
        self.v_output.setMaximumSize(QtCore.QSize(391, 37))
        self.v_output.setText("")
        self.v_output.setObjectName("v_output")
        self.v_output.setAlignment(QtCore.Qt.AlignCenter)
        self.verticalLayout_6.addWidget(self.v_output)
        self.line_12 = QtWidgets.QFrame(self.verticalLayoutWidget_2)
        self.line_12.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_12.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_12.setObjectName("line_12")
        self.verticalLayout_6.addWidget(self.line_12)
        self.tab_object.addTab(self.tab_2, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.verticalLayoutWidget_3 = QtWidgets.QWidget(self.tab_3)
        self.verticalLayoutWidget_3.setGeometry(QtCore.QRect(0, 0, 411, 271))
        self.verticalLayoutWidget_3.setObjectName("verticalLayoutWidget_3")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_3)
        self.verticalLayout_7.setContentsMargins(10, 10, 10, 10)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.horizontalLayout_25 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_25.setObjectName("horizontalLayout_25")
        self.label_16 = QtWidgets.QLabel(self.verticalLayoutWidget_3)
        self.label_16.setMinimumSize(QtCore.QSize(107, 26))
        self.label_16.setMaximumSize(QtCore.QSize(107, 26))
        self.label_16.setObjectName("label_16")
        self.horizontalLayout_25.addWidget(self.label_16)
        self.c_reagent_dropdown = QtWidgets.QComboBox(self.verticalLayoutWidget_3)
        self.c_reagent_dropdown.setMinimumSize(QtCore.QSize(185, 26))
        self.c_reagent_dropdown.setMaximumSize(QtCore.QSize(129, 26))
        self.c_reagent_dropdown.setObjectName("c_reagent_dropdown")
        self.horizontalLayout_25.addWidget(self.c_reagent_dropdown)
        self.c_mw_label = QtWidgets.QLabel(self.verticalLayoutWidget_3)
        self.c_mw_label.setMinimumSize(QtCore.QSize(85, 26))
        self.c_mw_label.setMaximumSize(QtCore.QSize(85, 26))
        self.c_mw_label.setObjectName("c_mw_label")
        self.horizontalLayout_25.addWidget(self.c_mw_label)
        self.verticalLayout_7.addLayout(self.horizontalLayout_25)
        self.horizontalLayout_26 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_26.setObjectName("horizontalLayout_26")
        self.label_23 = QtWidgets.QLabel(self.verticalLayoutWidget_3)
        self.label_23.setObjectName("label_23")
        self.horizontalLayout_26.addWidget(self.label_23)
        self.c_vol_textbox = QtWidgets.QLineEdit(self.verticalLayoutWidget_3)
        self.c_vol_textbox.setMinimumSize(QtCore.QSize(190, 21))
        self.c_vol_textbox.setMaximumSize(QtCore.QSize(190, 21))
        self.c_vol_textbox.setObjectName("c_vol_textbox")
        self.c_vol_textbox.setValidator(QtGui.QDoubleValidator(0.00, 1000, 1))
        self.horizontalLayout_26.addWidget(self.c_vol_textbox)
        self.c_vol_dropdown = QtWidgets.QComboBox(self.verticalLayoutWidget_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.c_vol_dropdown.sizePolicy().hasHeightForWidth())
        self.c_vol_dropdown.setSizePolicy(sizePolicy)
        self.c_vol_dropdown.setMinimumSize(QtCore.QSize(80, 26))
        self.c_vol_dropdown.setMaximumSize(QtCore.QSize(80, 26))
        self.c_vol_dropdown.setObjectName("c_vol_dropdown")
        self.horizontalLayout_26.addWidget(self.c_vol_dropdown)
        self.verticalLayout_7.addLayout(self.horizontalLayout_26)
        self.horizontalLayout_27 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_27.setObjectName("horizontalLayout_27")
        self.label_24 = QtWidgets.QLabel(self.verticalLayoutWidget_3)
        self.label_24.setObjectName("label_24")
        self.horizontalLayout_27.addWidget(self.label_24)
        self.c_mass_textbox = QtWidgets.QLineEdit(self.verticalLayoutWidget_3)
        self.c_mass_textbox.setMinimumSize(QtCore.QSize(190, 21))
        self.c_mass_textbox.setMaximumSize(QtCore.QSize(190, 21))
        self.c_mass_textbox.setObjectName("c_mass_textbox")
        self.c_mass_textbox.setValidator(QtGui.QDoubleValidator(0.00, 1000, 1))
        self.horizontalLayout_27.addWidget(self.c_mass_textbox)
        self.c_mass_dropdown = QtWidgets.QComboBox(self.verticalLayoutWidget_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.c_mass_dropdown.sizePolicy().hasHeightForWidth())
        self.c_mass_dropdown.setSizePolicy(sizePolicy)
        self.c_mass_dropdown.setMinimumSize(QtCore.QSize(80, 26))
        self.c_mass_dropdown.setMaximumSize(QtCore.QSize(8, 26))
        self.c_mass_dropdown.setObjectName("c_mass_dropdown")
        self.horizontalLayout_27.addWidget(self.c_mass_dropdown)
        self.verticalLayout_7.addLayout(self.horizontalLayout_27)
        self.horizontalLayout_28 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_28.setObjectName("horizontalLayout_28")
        self.c_calc_button = QtWidgets.QPushButton(self.verticalLayoutWidget_3)
        self.c_calc_button.setMinimumSize(QtCore.QSize(195, 32))
        self.c_calc_button.setMaximumSize(QtCore.QSize(195, 32))
        self.c_calc_button.setObjectName("c_calc_button")
        self.horizontalLayout_28.addWidget(self.c_calc_button)
        self.c_clear_calc_button = QtWidgets.QPushButton(self.verticalLayoutWidget_3)
        self.c_clear_calc_button.setMinimumSize(QtCore.QSize(194, 32))
        self.c_clear_calc_button.setMaximumSize(QtCore.QSize(194, 32))
        self.c_clear_calc_button.setObjectName("c_clear_calc_button")
        self.horizontalLayout_28.addWidget(self.c_clear_calc_button)
        self.verticalLayout_7.addLayout(self.horizontalLayout_28)
        self.line_13 = QtWidgets.QFrame(self.verticalLayoutWidget_3)
        self.line_13.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_13.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_13.setObjectName("line_13")
        self.verticalLayout_7.addWidget(self.line_13)
        self.c_output = QtWidgets.QLabel(self.verticalLayoutWidget_3)
        self.c_output.setMinimumSize(QtCore.QSize(391, 37))
        self.c_output.setMaximumSize(QtCore.QSize(391, 37))
        self.c_output.setText("")
        self.c_output.setObjectName("c_output")
        self.c_output.setAlignment(QtCore.Qt.AlignCenter)
        self.verticalLayout_7.addWidget(self.c_output)
        self.line_14 = QtWidgets.QFrame(self.verticalLayoutWidget_3)
        self.line_14.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_14.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_14.setObjectName("line_14")
        self.verticalLayout_7.addWidget(self.line_14)
        self.tab_object.addTab(self.tab_3, "")
        self.close_button = QtWidgets.QPushButton(self)
        self.close_button.setGeometry(QtCore.QRect(160, 314, 113, 32))
        self.close_button.setMinimumSize(QtCore.QSize(113, 32))
        self.close_button.setMaximumSize(QtCore.QSize(113, 32))
        self.close_button.setObjectName("close_button")

        self.retranslateUi()
        self.tab_object.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Form", "Molecular Calculator"))
        self.label.setText(_translate("Form", "Select a reagent: "))
        self.m_mw_label.setText(_translate("Form", "MW:--"))
        self.label_3.setText(_translate("Form", "Concentration: "))
        self.label_4.setText(_translate("Form", "Volume: "))
        self.m_calc_button.setText(_translate("Form", "Calculate"))
        self.m_clear_calc_button.setText(_translate("Form", "Clear Calculation"))
        self.tab_object.setTabText(self.tab_object.indexOf(self.tab), _translate("Form", "Mass"))
        self.label_10.setText(_translate("Form", "Select a reagent: "))
        self.v_mw_label.setText(_translate("Form", "MW:--"))
        self.label_21.setText(_translate("Form", "Concentration: "))
        self.label_22.setText(_translate("Form", "Mass:"))
        self.v_calc_button.setText(_translate("Form", "Calculate"))
        self.v_clear_calc_button.setText(_translate("Form", "Clear Calculation"))
        self.tab_object.setTabText(self.tab_object.indexOf(self.tab_2), _translate("Form", "Volume"))
        self.label_16.setText(_translate("Form", "Select a reagent: "))
        self.c_mw_label.setText(_translate("Form", "MW:--"))
        self.label_23.setText(_translate("Form", "Volume:"))
        self.label_24.setText(_translate("Form", "Mass:"))
        self.c_calc_button.setText(_translate("Form", "Calculate"))
        self.c_clear_calc_button.setText(_translate("Form", "Clear Calculation"))
        self.tab_object.setTabText(self.tab_object.indexOf(self.tab_3), _translate("Form", "Concentration"))
        self.close_button.setText(_translate("Form", "Close"))


app = QtWidgets.QApplication.instance()
if app is None:
    app = QtWidgets.QApplication(sys.argv)
main = MainWindow()
main.Gui.show()
sys.exit(app.exec_())
