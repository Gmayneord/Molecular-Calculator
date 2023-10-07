# -*- coding: utf-8 -*-
"""
Created on Tue Dec 13 08:38:33 2022

@author: g.mayneord
"""
from PyQt5.QtCore import QRect, Qt, QSize, QTimer
from PyQt5.QtWidgets import QWidget, QFrame, QSizePolicy, QVBoxLayout, QMainWindow, QApplication, QHBoxLayout, QComboBox, QLabel, QSpacerItem, QGridLayout, QLineEdit, QPushButton
from PyQt5.QtGui import QDoubleValidator
import sys
from os import path, mkdir
from json import dump, load

# =====================================================================
# Parameters:
# =====================================================================
# Storage location of file:
data_storage_file_loc = path.realpath("C:\\Python Files\\Molecular Calculator\\Stored_data.json")

# ===============================
# Range of units
# ===============================
concentration_scaler_dict = {"M": 1,
                             "mM": 0.001,
                             "uM": 0.000001,
                             "nM": 0.000000001,
                             }

volume_scaler_dict = {"L": 1,
                      "mL": 0.001,
                      "uL": 0.000001,
                      "nL": 0.000000001,
                      }

mass_scaler_dict = {"kg": 1000,
                    "g": 1,
                    "mg": 0.001,
                    "ug": 0.000001,
                    "ng": 0.000000001,
                    }

concentration_scaler_default = "mM"
volume_scaler_default = "mL"

# Text for commands from text boxes
add_new_item_text = "Add new item..."
delete_item_text = "Delete item..."
edit_item_text = "Edit item..."


# =====================================================================
# Processing functions:
# =====================================================================
def updateDropdownBox(dropdown_box_object, list_to_populate, add_del_option=False, sort_list=True):
    dropdown_box_object.clear()
    if sort_list:
        list_to_populate = sorted(list_to_populate, key=str.lower)

    # If we want to add the options to the dropdown box...
    if add_del_option:
        list_to_populate.append(add_new_item_text)
        list_to_populate.append(delete_item_text)
        list_to_populate.append(edit_item_text)

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
    # Run if no data file is detected. Will sort out making the file.
    # Make the file path in C drive first if it is the initial run.
    storage_dir = path.dirname(data_storage_file_loc)
    createDirPath(storage_dir)
    file_data = {"Reagents": {}}
    with open(data_storage_file_loc, "w") as file_obj:
        dump(file_data, file_obj)
    file_obj.close()
    return file_data


# =====================================================================
# GUI elements:
# =====================================================================
# Allow dialog scaling on high resolution displays (e.g. 4K)
QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)


class MainWindow():
    # ===================================
    # GUI setup:
    # ===================================
    def __init__(self):
        self.mainWindow = BuildMainDialog()
        if path.isfile(data_storage_file_loc) is False:
            self.stored_data = initialRun()
            self.mainWindow.output_label.setText("First runtime detected... A new data storage file has been created!")
        else:
            self.stored_data = self.readFromStorage(data_storage_file_loc)

        self.dialog_busy = False
        self.fillDropdownMenus()
        self.connectButtons()

    def fillDropdownMenus(self):
        # Populate lists and set selected item to the default
        updateDropdownBox(self.mainWindow.concentration_scaler, list(concentration_scaler_dict), sort_list=False)
        self.mainWindow.concentration_scaler.setCurrentIndex(self.mainWindow.concentration_scaler.findText(concentration_scaler_default))
        updateDropdownBox(self.mainWindow.volume_scaler, list(volume_scaler_dict), sort_list=False)
        self.mainWindow.volume_scaler.setCurrentIndex(self.mainWindow.volume_scaler.findText(volume_scaler_default))

        updateDropdownBox(self.mainWindow.reagent_selection_dropdown, list(self.stored_data["Reagents"].keys()), add_del_option=True)
        if len(list(self.stored_data["Reagents"].keys())) != 0:
            self.reagentSelectedAction()
        # Also set up action for when dropdown menu item is selected
        self.mainWindow.reagent_selection_dropdown.activated[str].connect(self.reagentSelectedAction)

    def connectButtons(self):
        self.mainWindow.calculate_button.clicked.connect(self.calculateButtonAction)
        self.mainWindow.clear_calculation_button.clicked.connect(self.clearCalculationAction)
        self.mainWindow.close_button.clicked.connect(self.closeButtonAction)

    # ===================================
    # GUI actions:
    # ===================================
    def reagentSelectedAction(self):
        if self.dialog_busy is False:
            if self.mainWindow.reagent_selection_dropdown.currentText() == add_new_item_text:
                self.add_item_window = AddWindow()
                self.add_item_window.show()
                # Need to write add new item class
            elif self.mainWindow.reagent_selection_dropdown.currentText() == delete_item_text:
                self.delete_new_window = DeleteWindow()
                self.delete_new_window.show()
            # Also need to write this
            elif self.mainWindow.reagent_selection_dropdown.currentText() == edit_item_text:
                self.edit_window = EditWindow()
                self.edit_window.show()
            else:
                # Update the molecular weight label with the current selected item
                self.updateMWLabel(self.stored_data["Reagents"][self.mainWindow.reagent_selection_dropdown.currentText()])

    def calculateButtonAction(self):
        errorReset(self.mainWindow.concentration_input)
        errorReset(self.mainWindow.volume_input)
        reagent_selection_box = self.mainWindow.reagent_selection_dropdown

        concentration_textbox = self.mainWindow.concentration_input
        volume_textbox = self.mainWindow.volume_input

        # Check for blank fields
        if concentration_textbox.text() == "":
            errorHighlight(concentration_textbox)

        if volume_textbox.text() == "":
            errorHighlight(volume_textbox)

        if reagent_selection_box.currentText() == add_new_item_text:
            errorHighlight(reagent_selection_box)

        if concentration_textbox.text() != "" and volume_textbox.text() != "" and reagent_selection_box.currentText() != add_new_item_text:
            concentration = float(concentration_textbox.text())
            concentration_scaler = concentration_scaler_dict[self.mainWindow.concentration_scaler.currentText()]
            volume = float(self.mainWindow.volume_input.text())
            volume_scaler = volume_scaler_dict[self.mainWindow.volume_scaler.currentText()]
            molecular_weight = float(self.stored_data["Reagents"][reagent_selection_box.currentText()])
            self.concCalculationAndDisplay(input_concentration=concentration * concentration_scaler,
                                           input_volume=volume * volume_scaler,
                                           inputMW=molecular_weight)

    def clearCalculationAction(self):
        self.mainWindow.output_label.setText(" ")
        self.mainWindow.calculate_button.setDisabled(False)
        self.mainWindow.clear_calculation_button.setDisabled(True)

    def updateMWLabel(self, molecular_weight):
        self.mainWindow.molecular_weight_label.setText("MW: " + str(molecular_weight))

    def closeButtonAction(self):
        self.mainWindow.close()

    # ===================================
    # Operating functions:
    # ===================================
    def concCalculationAndDisplay(self, input_concentration, input_volume, inputMW):
        calculated_mass = input_concentration * input_volume * inputMW
        adjusted_calculated_mass = None

        # Work out magnitude for output number
        for each_mag in mass_scaler_dict:
            # Calculated value starts off small, and increases with each iteration. When it is above 1 we know we're on the right scale (e.g. mg)
            if calculated_mass / mass_scaler_dict[each_mag] > 1:
                adjusted_calculated_mass = str.format('{0:.2f}', calculated_mass / mass_scaler_dict[each_mag])
                break
        if adjusted_calculated_mass is None:
            self.mainWindow.output_label.setText("The current caculation is out of bounds of the pre-defined scaling parameters. Please consider increasing scaling parameters to fix this")
        else:
            self.mainWindow.output_label.setText(f"For {str(self.mainWindow.volume_input.text())}{self.mainWindow.volume_scaler.currentText()} of {str(self.mainWindow.concentration_input.text())}{self.mainWindow.concentration_scaler.currentText()} use {adjusted_calculated_mass}{each_mag} of {self.mainWindow.reagent_selection_dropdown.currentText()}")
            self.mainWindow.calculate_button.setDisabled(True)
            self.mainWindow.clear_calculation_button.setDisabled(False)

    def readFromStorage(self, file_to_read, specific_section=None):
        with open(file_to_read, "r") as file_obj:
            stored_data = load(file_obj)
        file_obj.close()

        if specific_section is None:
            return stored_data
        else:
            return stored_data[specific_section]

    def writeToStorage(self, section_to_update, selected_element, del_item=False, dropbox_to_update=None, update_MW_label=True):
        if del_item:
            del self.stored_data[section_to_update][selected_element]
        else:
            self.stored_data[section_to_update][selected_element["name"]] = selected_element["data"]
        # Write this new edited data into the file.
        with open(data_storage_file_loc, "w") as file_obj:
            dump(self.stored_data, file_obj)
        file_obj.close()

        if dropbox_to_update is not None:
            updateDropdownBox(dropbox_to_update, list(self.stored_data[section_to_update]), add_del_option=True)

        if update_MW_label:
            if del_item:
                if self.mainWindow.reagent_selection_dropdown.currentText() != add_new_item_text:
                    self.updateMWLabel(self.stored_data["Reagents"][self.mainWindow.reagent_selection_dropdown.currentText()])
            else:
                self.updateMWLabel(selected_element["data"])


# =====================================================================
# Delete window
# =====================================================================
class DeleteWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        main.dialog_busy = True
        self.createGUI()
        self.connectButtons()
        self.reset_main_dropbox = True

    def createGUI(self):
        self.setWindowTitle("Delete items")
        self.resize(300, 100)
        v_layout = QVBoxLayout()
        h_layout = QHBoxLayout()
        label = QLabel("Delete item:")
        h_layout.addWidget(label)
        self.dropdown_menu = QComboBox()
        self.dropdown_menu.setMinimumSize(QSize(150, 20))
        self.dropdown_menu.setMaximumSize(QSize(150, 20))
        # Populate the list with items stored from the main data storage
        updateDropdownBox(self.dropdown_menu, list(main.stored_data["Reagents"]))

        h_layout.addWidget(self.dropdown_menu)
        self.delete_button = QPushButton("Delete...")
        h_layout.addWidget(self.delete_button)

        v_layout.addLayout(h_layout)

        h_layout = QHBoxLayout()
        self.close_button = QPushButton("Close")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.close_button.sizePolicy().hasHeightForWidth())
        self.close_button.setSizePolicy(sizePolicy)

        h_layout.addWidget(self.close_button)
        v_layout.addLayout(h_layout)

        widget = QWidget()
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
            main.mainWindow.reagent_selection_dropdown.setCurrentIndex(0)
        main.dialog_busy = False
        self.close()

    def deleteButtonAction(self):
        errorReset(self.dropdown_menu)
        if self.dropdown_menu.currentText() != "":
            self.reset_main_dropbox = False
            # Turn off button to avoid accidental multiple activations
            self.delete_button.setEnabled(False)
            # Remove it and write the change to the file
            main.writeToStorage("Reagents", self.dropdown_menu.currentText(), del_item=True, dropbox_to_update=main.mainWindow.reagent_selection_dropdown)
            # Also update the dropdown box in the main window
            updateDropdownBox(self.dropdown_menu, list(main.stored_data["Reagents"]), add_del_option=False)
            main.reagentSelectedAction()
            QTimer.singleShot(1000, lambda: self.delete_button.setEnabled(True))
        else:
            errorHighlight(self.dropdown_menu)


# =====================================================================
# Add window
# =====================================================================
class AddWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        main.dialog_busy = True
        self.createGUI()
        self.connectButtons()
        self.reset_main_dropbox = True

    def createGUI(self):
        self.setWindowTitle("Add items")
        self.resize(300, 100)
        v_layout = QVBoxLayout()
        h_layout = QHBoxLayout()
        label = QLabel("Reagent name:")
        h_layout.addWidget(label)
        self.reagent_input = QLineEdit()
        self.reagent_input.setMinimumSize(QSize(150, 20))
        self.reagent_input.setMaximumSize(QSize(150, 20))
        h_layout.addWidget(self.reagent_input)
        v_layout.addLayout(h_layout)

        h_layout = QHBoxLayout()
        label = QLabel("Reagent MW:")
        h_layout.addWidget(label)
        self.reagent_MW = QLineEdit()
        self.reagent_MW.setMinimumSize(QSize(150, 20))
        self.reagent_MW.setMaximumSize(QSize(150, 20))
        h_layout.addWidget(self.reagent_MW)
        v_layout.addLayout(h_layout)

        h_layout = QHBoxLayout()
        self.add_item_button = QPushButton("Add item...")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.add_item_button.sizePolicy().hasHeightForWidth())
        self.add_item_button.setSizePolicy(sizePolicy)
        h_layout.addWidget(self.add_item_button)

        self.close_button = QPushButton("Close")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.close_button.sizePolicy().hasHeightForWidth())
        self.close_button.setSizePolicy(sizePolicy)
        h_layout.addWidget(self.close_button)

        v_layout.addLayout(h_layout)

        widget = QWidget()
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
            main.mainWindow.reagent_selection_dropdown.setCurrentIndex(0)
        main.dialog_busy = False
        self.close()

    def add_item_action(self):
        errorReset(self.reagent_input)
        errorReset(self.reagent_MW)
        errorReset(main.mainWindow.reagent_selection_dropdown)

        if self.reagent_input != "" and self.reagent_MW != "":
            self.reset_main_dropbox = False
            # Remove it and write the change to the file
            main.writeToStorage("Reagents", {"name": self.reagent_input.text(),
                                             "data": float(self.reagent_MW.text())},
                                dropbox_to_update=main.mainWindow.reagent_selection_dropdown)
            # Set the index on the dropdown box to be the new item...
            main.mainWindow.reagent_selection_dropdown.setCurrentIndex(main.mainWindow.reagent_selection_dropdown.findText(self.reagent_input.text()))
            # Process it so that the MW is displayed is correct
            main.reagentSelectedAction()
            # Close the dialog
            self.closeButtonAction()
        else:
            if self.reagent_input == "":
                errorHighlight(self.reagent_input)
            if self.reagent_MW == "":
                errorHighlight(self.reagent_MW)


# =====================================================================
# Edit window
# =====================================================================
class EditWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        main.dialog_busy = True
        self.create_GUI()
        self.connectButtons()
        self.reset_main_dropbox = True

    def create_GUI(self):
        self.setWindowTitle("Edit items")
        self.resize(300, 100)
        v_layout = QVBoxLayout()

        h_layout = QHBoxLayout()
        label = QLabel("Select a reagent:")
        h_layout.addWidget(label)
        self.dropdown_menu = QComboBox()
        h_layout.addWidget(self.dropdown_menu)
        # Populate the list with items stored from the main data storage
        updateDropdownBox(self.dropdown_menu, list(main.stored_data["Reagents"]))
        v_layout.addLayout(h_layout)

        h_layout = QHBoxLayout()
        label = QLabel("Reagent name:")
        h_layout.addWidget(label)
        self.reagent_input = QLineEdit()
        self.reagent_input.setMinimumSize(QSize(150, 20))
        self.reagent_input.setMaximumSize(QSize(150, 20))
        h_layout.addWidget(self.reagent_input)
        v_layout.addLayout(h_layout)

        h_layout = QHBoxLayout()
        label = QLabel("Reagent MW:")
        h_layout.addWidget(label)
        self.reagent_MW = QLineEdit()
        self.reagent_MW.setMinimumSize(QSize(150, 20))
        self.reagent_MW.setMaximumSize(QSize(150, 20))
        h_layout.addWidget(self.reagent_MW)
        v_layout.addLayout(h_layout)

        h_layout = QHBoxLayout()
        self.add_item_button = QPushButton("Re-write item...")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.add_item_button.sizePolicy().hasHeightForWidth())
        self.add_item_button.setSizePolicy(sizePolicy)
        h_layout.addWidget(self.add_item_button)

        self.close_button = QPushButton("Close")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.close_button.sizePolicy().hasHeightForWidth())
        self.close_button.setSizePolicy(sizePolicy)
        h_layout.addWidget(self.close_button)

        v_layout.addLayout(h_layout)

        widget = QWidget()
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
            main.writeToStorage("Reagents", self.dropdown_menu.currentText(), del_item=True, update_MW_label=False)

            # Write the nw item and write change to the file
            main.writeToStorage("Reagents", {"name": self.reagent_input.text(),
                                             "data": float(self.reagent_MW.text())},
                                dropbox_to_update=main.mainWindow.reagent_selection_dropdown)

            # Set the index on the dropdown box to be the new item...
            main.mainWindow.reagent_selection_dropdown.setCurrentIndex(main.mainWindow.reagent_selection_dropdown.findText(self.reagent_input.text()))
            # Process it so that the MW is displayed is correct
            main.reagentSelectedAction()
            # Close the dialog
            self.closeButtonAction()
        else:
            if self.reagent_input == "":
                errorHighlight(self.reagent_input)
            if self.reagent_MW == "":
                errorHighlight(self.reagent_MW)


class BuildMainDialog(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(385, 270)
        self.setWindowTitle("Molecular Calculator")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(sizePolicy.hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.createGUI()

    def createGUI(self):
        verticalLayoutWidget = QWidget(self)
        verticalLayoutWidget.setGeometry(QRect(10, 10, 371, 250))
        verticalLayout = QVBoxLayout(verticalLayoutWidget)
        verticalLayout.setContentsMargins(10, 10, 10, 10)

        horizontalLayout = QHBoxLayout()
        label = QLabel("Select a reagent:", verticalLayoutWidget)
        label.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)
        horizontalLayout.addWidget(label)

        self.reagent_selection_dropdown = QComboBox(verticalLayoutWidget)
        horizontalLayout.addWidget(self.reagent_selection_dropdown)

        self.molecular_weight_label = QLabel("MW:--", verticalLayoutWidget)
        horizontalLayout.addWidget(self.molecular_weight_label)

        verticalLayout.addLayout(horizontalLayout)
        gridLayout_2 = QGridLayout()

        concentration_title = QLabel("Concentration:", verticalLayoutWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(concentration_title.sizePolicy().hasHeightForWidth())
        concentration_title.setSizePolicy(sizePolicy)
        concentration_title.setLayoutDirection(Qt.RightToLeft)
        concentration_title.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)

        gridLayout_2.addWidget(concentration_title, 0, 0, 1, 1)
        self.concentration_input = QLineEdit(verticalLayoutWidget)
        self.concentration_input.setValidator(QDoubleValidator(0.00, 100000, 5))

        gridLayout_2.addWidget(self.concentration_input, 0, 1, 1, 1)
        self.concentration_scaler = QComboBox(verticalLayoutWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.concentration_scaler.sizePolicy().hasHeightForWidth())
        self.concentration_scaler.setSizePolicy(sizePolicy)
        self.concentration_scaler.setMinimumSize(QSize(70, 30))
        self.concentration_scaler.setMaximumSize(QSize(70, 30))

        gridLayout_2.addWidget(self.concentration_scaler, 0, 2, 1, 1)
        verticalLayout.addLayout(gridLayout_2)
        gridLayout_3 = QGridLayout()

        self.Volume_title = QLabel("           Volume:", verticalLayoutWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Volume_title.sizePolicy().hasHeightForWidth())
        self.Volume_title.setSizePolicy(sizePolicy)
        self.Volume_title.setLayoutDirection(Qt.RightToLeft)
        self.Volume_title.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)

        gridLayout_3.addWidget(self.Volume_title, 0, 0, 1, 1)
        self.volume_input = QLineEdit(verticalLayoutWidget)
        self.volume_input.setValidator(QDoubleValidator(0.00, 100000, 5))

        gridLayout_3.addWidget(self.volume_input, 0, 1, 1, 1)
        self.volume_scaler = QComboBox(verticalLayoutWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.volume_scaler.sizePolicy().hasHeightForWidth())
        self.volume_scaler.setSizePolicy(sizePolicy)
        self.volume_scaler.setMinimumSize(QSize(70, 30))
        self.volume_scaler.setMaximumSize(QSize(70, 30))

        gridLayout_3.addWidget(self.volume_scaler, 0, 2, 1, 1)
        verticalLayout.addLayout(gridLayout_3)
        gridLayout = QGridLayout()

        self.clear_calculation_button = QPushButton("Clear Calculation", verticalLayoutWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.clear_calculation_button.sizePolicy().hasHeightForWidth())
        self.clear_calculation_button.setSizePolicy(sizePolicy)
        self.clear_calculation_button.setDisabled(True)

        gridLayout.addWidget(self.clear_calculation_button, 0, 2, 1, 1)
        self.calculate_button = QPushButton("Calculate", verticalLayoutWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.calculate_button.sizePolicy().hasHeightForWidth())
        self.calculate_button.setSizePolicy(sizePolicy)

        gridLayout.addWidget(self.calculate_button, 0, 1, 1, 1)
        spacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        gridLayout.addItem(spacerItem, 0, 0, 1, 1)
        spacerItem1 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        gridLayout.addItem(spacerItem1, 0, 3, 1, 1)
        verticalLayout.addLayout(gridLayout)
        line_2 = QFrame(verticalLayoutWidget)
        line_2.setFrameShape(QFrame.HLine)
        line_2.setFrameShadow(QFrame.Sunken)

        verticalLayout.addWidget(line_2)
        horizontalLayout_6 = QHBoxLayout()

        self.output_label = QLabel(" ", verticalLayoutWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.output_label.sizePolicy().hasHeightForWidth())
        self.output_label.setSizePolicy(sizePolicy)
        self.output_label.setAlignment(Qt.AlignCenter)

        horizontalLayout_6.addWidget(self.output_label)
        verticalLayout.addLayout(horizontalLayout_6)
        line = QFrame(verticalLayoutWidget)
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)

        verticalLayout.addWidget(line)
        horizontalLayout_5 = QHBoxLayout()

        self.close_button = QPushButton("Close", verticalLayoutWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.close_button.sizePolicy().hasHeightForWidth())
        self.close_button.setSizePolicy(sizePolicy)

        horizontalLayout_5.addWidget(self.close_button)
        verticalLayout.addLayout(horizontalLayout_5)


app = QApplication.instance()
if app is None:
    app = QApplication(sys.argv)
main = MainWindow()
main.mainWindow.show()
sys.exit(app.exec_())
