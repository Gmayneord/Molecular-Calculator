#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 26 10:31:22 2021

@author: guymayneord
"""
from os import path

#========================================================
# Setting up parameters
current_directory=path.dirname(path.realpath(__file__))
reagent_storage_file=path.join(current_directory, "Reagent_storage_file.txt")
stock_solutions_file=path.join(current_directory, "stock_sol_file.txt")
storage_seperator="---"
adding_new_item_text='Add new item...'
delete_item_from_list='Delete item...'
concentration_scaler_dict={'M': 1, 'mM': 0.001, 'uM': 0.000001,'nM': 0.000000001}
concentration_scaler_default='mM'
volume_scaler_dict={'L': 1, 'mL': 0.001, 'uL': 0.000001,'nL': 0.000000001}
volume_scaler_default='mL'
mass_magnitude_list={1:'g' , 1000:'mg', 1000000 : 'ug', 1000000000: 'ng'}


#========================================================
# File processing section
def open_storage_file(file_to_read):
    reagent_dict={}
    textfile=open(file_to_read)
    for line in textfile:
        line_list=line.split(storage_seperator)
        reagent_dict[line_list[0]]=float(line_list[1])
    textfile.close()
    return reagent_dict

def write_reagent_storage_file(dictionary_to_write, file_to_update):
    from os import remove as remove_file
    # Section for writing new dictionary to the storage file.
    remove_file(file_to_update)
    #Write a new one
    storage_file= open(file_to_update, 'w')
    for each_reagent in dictionary_to_write:
        storage_file.write(each_reagent + storage_seperator + str(dictionary_to_write[each_reagent]) + '\n')
    storage_file.close()

#========================================================
# Useful code:
def write_list_to_dropdown_box(dropdown_box_object, input_list_to_write):
    for each_item in input_list_to_write:
        dropdown_box_object.addItem(each_item)

def update_MW_label(label_object, molecular_weight):
    label_object.setText("MW: " + str(molecular_weight))

def textbox_error_highlight(textbox_to_change):
    textbox_to_change.setStyleSheet("background: red;")

def textbox_error_reset(textbox_to_change):
    textbox_to_change.setStyleSheet("background: white;")

def update_reagents_box(reagent_box_object, current_reagent_dictionary, add_del_option=True):
    reagent_box_object.clear()
    Reagents_list=sorted(list(current_reagent_dictionary.keys()), key=str.lower)
    # If we want to add and remove items from this list add them in, if not dont bother.
    if add_del_option:
        Reagents_list.append(adding_new_item_text)
        Reagents_list.append(delete_item_from_list)
    write_list_to_dropdown_box(reagent_box_object, Reagents_list)


#========================================================
# Now stuff with the GUI

from PyQt5 import QtWidgets, uic, QtCore, QtGui
import sys

# Section for the input of a new reagent:
class new_item_window(QtWidgets.QWidget):
    def __init__(self, dropbox_object_to_update, label_to_update):
        super().__init__()
        new_reagent_window=uic.loadUi(path.join(current_directory, 'new_reagent.ui'), self)

        def submit_button_action():
            textbox_error_reset(new_reagent_window.reagent_name_input)
            textbox_error_reset(new_reagent_window.molecular_weight_input)

            #Need to get the text in the box
            new_reagent_name=new_reagent_window.reagent_name_input.text()
            new_reagent_mw=new_reagent_window.molecular_weight_input.text()
            if new_reagent_name != '' and new_reagent_mw != '':
                # Re-read the storage file, so that when any change is made, it is both written and read (not an issue at this scale)
                Reagents_dictionary=open_storage_file(reagent_storage_file)
                # And add it to the dropdown
                Reagents_dictionary[new_reagent_name]=new_reagent_mw

                # Now clear the dropdown box and re-write it wih the new list.
                update_reagents_box(dropbox_object_to_update, Reagents_dictionary)
                # Also update the label next to it.
                update_MW_label(label_to_update, new_reagent_mw)
                # Write the new dictionary to the list
                write_reagent_storage_file(Reagents_dictionary, reagent_storage_file)

                # Set the current item to be the one we just endered.
                dropbox_object_to_update.setCurrentIndex(dropbox_object_to_update.findText(new_reagent_name))
                #Need to have code here to also save if it's not one use.
                # Close the window.
                new_reagent_window.close()

            else:
                textbox_error_reset(new_reagent_window.reagent_name_input)
                textbox_error_reset(new_reagent_window.molecular_weight_input)
                if new_reagent_name == '':
                    textbox_error_highlight(new_reagent_window.reagent_name_input)
                if new_reagent_mw == '':
                    textbox_error_highlight(new_reagent_window.molecular_weight_input)

        def cancel_button_action():
            dropbox_object_to_update.setCurrentIndex(0)
            new_reagent_window.close()

        # Assign buttons to their actions
        self.new_submit_button.clicked.connect(submit_button_action)
        self.cancel_button.clicked.connect(cancel_button_action)

# Section for deleting a reagent:
class delete_window(QtWidgets.QMainWindow):
    def __init__(self, Reagents_dictionary, reagent_selection_box):
        # Initiate the UI window.
        super().__init__()
        # Load in the UI from the file
        delete_window=uic.loadUi(path.join(current_directory, 'delete_reagent_box.ui'), self)

        # Populate with our current list of reagents
        write_list_to_dropdown_box(delete_window.delete_selection_box, sorted(list(Reagents_dictionary.keys()), key=str.lower))

        def delete_button_action():
            #Quickly turn off the button for a few seconds to avoid accidental multiple deletions.
            delete_window.delete_button.setEnabled(False)

            # Grab the item currently selected in the list and delete it form the dictionary.
            del Reagents_dictionary[delete_window.delete_selection_box.currentText()]

            # And now update the file so that the storage also reflects the deletion
            write_reagent_storage_file(Reagents_dictionary, reagent_storage_file)

            # Update the local box to reflec the change.
            update_reagents_box(delete_window.delete_selection_box, Reagents_dictionary,  add_del_option=False)

            # and update the main window to reflect the deletion (Could do it via close, but then may not always trigger if X in corner is pressed)
            update_reagents_box(reagent_selection_box, Reagents_dictionary)

            # Turn the button back on after 1 second.
            QtCore.QTimer.singleShot(1000, lambda: delete_window.delete_button.setEnabled(True))

        def close_button_action():
            delete_window.close()

        delete_window.delete_button.clicked.connect(delete_button_action)
        delete_window.close_button.clicked.connect(close_button_action)


# Section for the main window of the program.
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        # Initiate the UI window.
        super(MainWindow, self).__init__(*args, **kwargs)

        # Load in the UI from the file
        main_window_1=uic.loadUi(path.join(current_directory, 'User_interface_file.ui'), self)

        # Set up button actions here
        def reagent_selected_action():
            Reagents_dictionary=open_storage_file(reagent_storage_file)
            current_selected_reagent=main_window_1.reagent_selection_box.currentText()
            # If we have selected we want a new item...
            if current_selected_reagent == adding_new_item_text:
                new_input_window=new_item_window(main_window_1.reagent_selection_box, main_window_1.molecular_weight_label)
                new_input_window.show()
            # If we have selected we want to delete an item...
            elif current_selected_reagent == delete_item_from_list:
                # Also need to reset main window with new changes.
                delete_reagent_window=delete_window(Reagents_dictionary, main_window_1.reagent_selection_box)
                delete_reagent_window.show()
            # If we've selected any of the reagents themselves.
            else:
                reagent_mw=Reagents_dictionary[current_selected_reagent]
                update_MW_label(main_window_1.molecular_weight_label, reagent_mw)

        def calculate_button_action():
            # Just set them back in case error got triggered.
            textbox_error_reset(main_window_1.concentration_input)
            textbox_error_reset(main_window_1.volume_input)

            # Re-check to ensure no changes have occured since program started running.
            Reagents_dictionary=open_storage_file(reagent_storage_file)

            # Check if these are blank and inform user if so.
            if main_window_1.concentration_input.text() == '':
                textbox_error_highlight(main_window_1.concentration_input)
            if main_window_1.volume_input.text() == '':
                textbox_error_highlight(main_window_1.volume_input)
            if main_window_1.concentration_input.text() != '' and main_window_1.volume_input.text() != '':

                concentration_input=float(main_window_1.concentration_input.text())*concentration_scaler_dict[main_window_1.concentration_scaler.currentText()]
                volume_input=float(main_window_1.volume_input.text())*volume_scaler_dict[main_window_1.volume_scaler.currentText()]
                calculated_moles=concentration_input * volume_input
                calculated_mass=calculated_moles * float(Reagents_dictionary[main_window_1.reagent_selection_box.currentText()])

                # Work out the magnitude for the output number.
                for each_magnitude in mass_magnitude_list:
                    if calculated_mass*each_magnitude > 1:
                        mass_magnitude=mass_magnitude_list[each_magnitude]
                        #Only need 5 significant values, beyond this it's not really helpful.
                        adjusted_calculated_mass=str.format('{0:.2f}', calculated_mass*each_magnitude)
                        break

                main_window_1.ouput_text_box.setText('For ' + str(main_window_1.volume_input.text()) + main_window_1.volume_scaler.currentText() + ' of ' + str(main_window_1.concentration_input.text()) + main_window_1.concentration_scaler.currentText() + ' use ' + adjusted_calculated_mass + mass_magnitude + ' of ' +' ' + main_window_1.reagent_selection_box.currentText())

                main_window_1.calculate_button.setDisabled(True)
                main_window_1.reset_button.setDisabled(False)

        def reset_button_action():
            main_window_1.ouput_text_box.setText(' ')
            main_window_1.calculate_button.setDisabled(False)
            main_window_1.reset_button.setDisabled(True)

        def close_button_action():
            main_window_1.close()

        Reagents_dictionary=open_storage_file(reagent_storage_file)
        # Need to add the items in the list we're reading from
        update_reagents_box(main_window_1.reagent_selection_box, Reagents_dictionary)
        # The first time this runs, also want to update the MW box to see the first mw
        reagent_selected_action()

        # Populate the concentration and volume magnitude scaler lists.
        write_list_to_dropdown_box(main_window_1.concentration_scaler, list(concentration_scaler_dict.keys()))
        write_list_to_dropdown_box(main_window_1.concentration_scaler_dil, list(concentration_scaler_dict.keys()))
        write_list_to_dropdown_box(main_window_1.volume_scaler, list(volume_scaler_dict.keys()))
        write_list_to_dropdown_box(main_window_1.volume_scaler_panel_dil, list(volume_scaler_dict.keys()))

        # Sort out the list so that the standard defaults for each parameter come up
        main_window_1.concentration_scaler.setCurrentIndex(main_window_1.concentration_scaler.findText(concentration_scaler_default))
        main_window_1.volume_scaler.setCurrentIndex(main_window_1.volume_scaler.findText(volume_scaler_default))

        main_window_1.concentration_scaler_dil.setCurrentIndex(main_window_1.concentration_scaler_dil.findText(concentration_scaler_default))
        main_window_1.volume_scaler_panel_dil.setCurrentIndex(main_window_1.volume_scaler_panel_dil.findText(volume_scaler_default))

        # Assign buttons to their actions
        main_window_1.close_button.clicked.connect(close_button_action)
        main_window_1.calculate_button.clicked.connect(calculate_button_action)
        main_window_1.reset_button.clicked.connect(reset_button_action)

        main_window_1.reagent_selection_box.activated[str].connect(reagent_selected_action)

app = QtWidgets.QApplication.instance()
if app is None:
    app = QtWidgets.QApplication(sys.argv)
main= MainWindow()
main.show()
sys.exit(app.exec_())

