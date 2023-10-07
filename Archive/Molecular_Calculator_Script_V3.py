#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 26 17:19:23 2022

@author: guymayneord
"""
#==============================================================================
# Imports:
#==============================================================================
from os import path
from PyQt5 import QtWidgets, uic, QtCore
from sys import exit as exit_prog, argv
from json import dump, load
#==============================================================================
# Parameters
#==============================================================================
#===============================
# Storage locations of files storing the reagents
#===============================
data_storage_file_loc = path.join(path.dirname(path.realpath(__file__)), "Stored_data.json")
#===============================
# Range of units
#===============================
concentration_scaler_dict={'M' : 1,
                           'mM': 0.001, 
                           'uM': 0.000001,
                           'nM': 0.000000001
                           }
volume_scaler_dict={'L': 1,
                    'mL': 0.001,
                    'uL': 0.000001,
                    'nL': 0.000000001
                    }
mass_magnitude_dict={'kg' : 1000,
                     'g' : 1,
                     'mg' : 0.001,
                     'ug' : 0.000001,
                     'ng' : 0.000000001
                     }

concentration_scaler_default='mM'
volume_scaler_default='mL'
#===============================
# Text for commands from text boxes
#===============================
adding_new_item_text='Add new item...'
delete_item_from_list='Delete item...'
#==============================================================================
# Processing functions
#==============================================================================
def update_dropdown_box(dropdown_box_object, list_to_populate, add_del_option=False, sort_list=False):
    dropdown_box_object.clear()
    if sort_list:
        list_to_populate = sorted(list_to_populate, key=str.lower)
    # If we want to add and remove items from this list then add in the option.
    if add_del_option:
        list_to_populate.append(adding_new_item_text)
        list_to_populate.append(delete_item_from_list)

    for each_item in list_to_populate:
        dropdown_box_object.addItem(each_item)

def textbox_error_highlight(textbox_to_change):
    textbox_to_change.setStyleSheet("background: red;")

def textbox_error_reset(textbox_to_change):
    textbox_to_change.setStyleSheet("background: None;")

def initial_run():
    file_data = {"Reagents" : {}, "Stock Solutions" : {}}
    with open(data_storage_file_loc, 'w') as file_obj:
        dump(file_data, file_obj)
    file_obj.close()

#==============================================================================
# GUI Elements
#==============================================================================
#===================================================
# Main Window
#===================================================
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.Main_window=uic.loadUi(path.join(path.dirname(path.realpath(__file__)), 'User_interface_file.ui'), self)
        # Check if the data storage file exists, if not make a new one.
        if path.isfile(data_storage_file_loc) ==  False:
            initial_run()
            self.Main_window.ouput_text_box.setText("First runtime detected... A new data storage file has been created!")
        self.Stored_data=self.read_from_storage(data_storage_file_loc)
        self.Dialogue_busy=False

        #===============================
        # Link molecular calculator tab.
        #===============================
        # Need to add the items in the list we're reading from
        update_dropdown_box(self.Main_window.reagent_selection_box, list(self.Stored_data["Reagents"].keys()), add_del_option=True, sort_list=True)
        # The first time this runs, also want to update the MW box to see the first mw
        if len(self.Stored_data["Reagents"]) != 0:
            # Stops a blank list automaticaly spawning the add reagent box.
            self.reagent_selected_action()

        # Populate the concentration and volume magnitude scaler lists.
        update_dropdown_box(self.Main_window.concentration_scaler, concentration_scaler_dict)
        update_dropdown_box(self.Main_window.volume_scaler, volume_scaler_dict)

        # Sort out the list so that the standard defaults for each parameter come up
        self.Main_window.concentration_scaler.setCurrentIndex(self.Main_window.concentration_scaler.findText(concentration_scaler_default))
        self.Main_window.volume_scaler.setCurrentIndex(self.Main_window.volume_scaler.findText(volume_scaler_default))

        # Assign buttons to their actions
        self.Main_window.close_button.clicked.connect(self.close_button_action)
        self.Main_window.calculate_button.clicked.connect(self.calculate_button_action)
        self.Main_window.reset_button.clicked.connect(self.reset_button_action)

        self.Main_window.reagent_selection_box.activated[str].connect(self.reagent_selected_action)
        #===============================
        # Link stock solutions tab
        #===============================
        update_dropdown_box(self.Main_window.stock_solutions_dropbox, list(self.Stored_data["Stock Solutions"].keys()), add_del_option=True)
        update_dropdown_box(self.Main_window.concentration_scaler_dil, list(concentration_scaler_dict))
        update_dropdown_box(self.Main_window.volume_scaler_panel_dil, list(volume_scaler_dict))
        
        self.Main_window.concentration_scaler_dil.setCurrentIndex(self.Main_window.concentration_scaler_dil.findText(concentration_scaler_default))
        self.Main_window.volume_scaler_panel_dil.setCurrentIndex(self.Main_window.volume_scaler_panel_dil.findText(volume_scaler_default))
        
        
    #===============================
    # Operating functions
    #===============================
    def conc_calculation_and_display(self, input_concentration, input_volume, input_MW):
        calculated_mass=input_concentration * input_volume * input_MW
        adjusted_calculated_mass = None
        # Work out the magnitude for the output number.
        for each_magnitude in mass_magnitude_dict:
            if calculated_mass / mass_magnitude_dict[each_magnitude] > 1:
                #Only need 5 significant values, beyond this it's not really helpful.
                adjusted_calculated_mass=str.format('{0:.2f}', calculated_mass / mass_magnitude_dict[each_magnitude])
                break
        if adjusted_calculated_mass == None:
            self.Main_window.ouput_text_box.setText("The current calculation is out of bounds of the pre-defined scaling parameters. Please consider increasing scaling parameters to fix this")
        else:
            self.Main_window.ouput_text_box.setText('For ' + str(self.Main_window.volume_input.text()) + self.Main_window.volume_scaler.currentText() +
                                                    ' of ' + str(self.Main_window.concentration_input.text()) + self.Main_window.concentration_scaler.currentText() +
                                                    ' use ' + adjusted_calculated_mass + each_magnitude +
                                                    ' of ' + self.Main_window.reagent_selection_box.currentText())
            self.Main_window.calculate_button.setDisabled(True)
            self.Main_window.reset_button.setDisabled(False)

    def read_from_storage(self, file_to_read, Specific_section = None):
        with open(file_to_read, 'r') as file_obj:
            stored_data = load(file_obj)
        file_obj.close()
        # By default return the whole dictionary
        if Specific_section == None:
            return stored_data
        else:
            return stored_data[Specific_section]

    def write_to_storage(self, Section_to_update, Selected_element, add_item=True, Dropbox_to_update=None, Label_to_update=None):
        if add_item:
            self.Stored_data[Section_to_update][Selected_element["Name"]] = Selected_element["Data"]
        else:
            del self.Stored_data[Section_to_update][Selected_element]
        with open(data_storage_file_loc, 'w') as file_obj:
            dump(self.Stored_data, file_obj)
        file_obj.close()

        if Dropbox_to_update != None:
            update_dropdown_box(Dropbox_to_update, self.Stored_data[Section_to_update].keys())

        if Label_to_update != None:
            Label_to_update.setText("MW: " + str(Selected_element["Data"]))
        
    def update_MW_label(self, molecular_weight):
        self.Main_window.molecular_weight_label.setText("MW: " + str(molecular_weight))
    #===============================
    # Linking button actions
    #===============================
    # When something is selected from the dropdown menu.
    def reagent_selected_action(self):
        if self.Dialogue_busy == False:
            current_selected_reagent=self.Main_window.reagent_selection_box.currentText()
            # If we have selected we want a new item...
            if current_selected_reagent == adding_new_item_text:
                new_input_window_obj=new_item_window(self.Main_window.reagent_selection_box)
                new_input_window_obj.show()
            # If we have selected we want to delete an item...
            elif current_selected_reagent == delete_item_from_list:
                # Also need to reset main window with new changes.
                delete_reagent_obj=delete_reagent_window(self.Main_window.reagent_selection_box)
                delete_reagent_obj.show()
            else:
                self.update_MW_label(self.Stored_data["Reagents"][current_selected_reagent])



    def calculate_button_action(self):
        # Just set them back in case error got triggered.
        textbox_error_reset(self.Main_window.concentration_input)
        textbox_error_reset(self.Main_window.volume_input)

        # Check if these are blank and inform user if so.
        if self.Main_window.concentration_input.text() == '':
            textbox_error_highlight(self.Main_window.concentration_input)
        if self.Main_window.volume_input.text() == '':
            textbox_error_highlight(self.Main_window.volume_input)
        if self.Main_window.concentration_input.text() != '' and self.Main_window.volume_input.text() != '':
            self.conc_calculation_and_display(input_concentration = float(self.Main_window.concentration_input.text())*concentration_scaler_dict[self.Main_window.concentration_scaler.currentText()],
                                              input_volume = float(self.Main_window.volume_input.text())*volume_scaler_dict[self.Main_window.volume_scaler.currentText()],
                                              input_MW = float(self.Stored_data["Reagents"][self.Main_window.reagent_selection_box.currentText()]))

    def reset_button_action(self):
        self.Main_window.ouput_text_box.setText(' ')
        self.Main_window.calculate_button.setDisabled(False)
        self.Main_window.reset_button.setDisabled(True)

    def close_button_action(self):
        self.Main_window.close()

#===================================================
# New Window
#===================================================
class new_item_window(QtWidgets.QWidget):
    def __init__(self, dropbox_object_to_update):
        super().__init__()
        self.dropbox_object_to_update = dropbox_object_to_update
        self.new_reagent_window=uic.loadUi(path.join(path.dirname(path.realpath(__file__)), 'new_reagent.ui'), self)

        # Assign buttons to their actions
        self.new_submit_button.clicked.connect(self.submit_button_action)
        self.cancel_button.clicked.connect(self.cancel_button_action)
        main.Dialogue_busy = True

    def submit_button_action(self):
        textbox_error_reset(self.new_reagent_window.reagent_name_input)
        textbox_error_reset(self.new_reagent_window.molecular_weight_input)

        #Need to get the text in the box
        new_reagent_name=self.new_reagent_window.reagent_name_input.text()
        new_reagent_mw=self.new_reagent_window.molecular_weight_input.text()
        
        
        if new_reagent_name != '' and new_reagent_mw != '':
            if new_reagent_name not in list(main.Stored_data["Reagents"].keys()):
                # Also update the label next to it.
                main.update_MW_label(new_reagent_mw)
                # Write the new dictionary to the list
                main.write_to_storage("Reagents", {"Name" : new_reagent_name, "Data" : new_reagent_mw}, add_item=True, Dropbox_to_update=self.dropbox_object_to_update)
    
                update_dropdown_box(self.dropbox_object_to_update, list(main.Stored_data["Reagents"].keys()), add_del_option=True, sort_list=True)
    
                # Set the current item to be the one we just endered.
                self.dropbox_object_to_update.setCurrentIndex(self.dropbox_object_to_update.findText(new_reagent_name))
                #Need to have code here to also save if it's not one use.
                # Close the window.
                main.Dialogue_busy=False
                self.new_reagent_window.close()
            else:
                textbox_error_highlight(self.new_reagent_window.reagent_name_input)
                self.new_reagent_window.reagent_name_input.setText("Reagent name: " + new_reagent_name + " already taken")

        else:
            if new_reagent_name == '':
                textbox_error_highlight(self.new_reagent_window.reagent_name_input)
            if new_reagent_mw == '':
                textbox_error_highlight(self.new_reagent_window.molecular_weight_input)

    def cancel_button_action(self):
        self.dropbox_object_to_update.setCurrentIndex(0)
        main.Dialogue_busy = False
        self.new_reagent_window.close()

#===================================================
# Delete Window
#===================================================
class delete_reagent_window(QtWidgets.QMainWindow):
    def __init__(self, reagent_selection_box):
        # Initiate the UI window.
        super().__init__()
        self.reagent_selection_box = reagent_selection_box
        # Load in the UI from the file
        self.delete_window=uic.loadUi(path.join(path.dirname(path.realpath(__file__)), 'delete_reagent_box.ui'), self)
        main.Dialogue_busy = True
        # Populate with our current list of reagents
        update_dropdown_box(self.delete_window.delete_selection_box, list(main.Stored_data["Reagents"].keys()), sort_list=True)

        # Connect the buttons
        self.delete_window.delete_button.clicked.connect(self.delete_button_action)
        self.delete_window.close_button.clicked.connect(self.close_button_action)

    def delete_button_action(self):
        #Quickly turn off the button for a few seconds to avoid accidental multiple deletions.
        self.delete_window.delete_button.setEnabled(False)

        # And now update the file so that the storage also reflects the deletion
        main.write_to_storage("Reagents", self.delete_window.delete_selection_box.currentText(), add_item = False, Dropbox_to_update=self.delete_window.delete_selection_box)

        # and update the main window to reflect the deletion (Could do it via close, but then may not always trigger if X in corner is pressed)
        update_dropdown_box(self.reagent_selection_box, list(main.Stored_data["Reagents"].keys()), add_del_option=True, sort_list=True)
        main.reagent_selected_action()
        # Turn the button back on after 1 second.
        QtCore.QTimer.singleShot(1000, lambda: self.delete_window.delete_button.setEnabled(True))

    def close_button_action(self):
        main.Dialogue_busy = False
        self.delete_window.close()

#===================================================
# Running code
#===================================================
app = QtWidgets.QApplication.instance()
if app is None:
    app = QtWidgets.QApplication(argv)
main= MainWindow()
main.show()
exit_prog(app.exec_())
