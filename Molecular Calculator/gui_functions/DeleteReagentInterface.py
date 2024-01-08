from PyQt5 import QtCore
from guis.DeleteReagentGUI import DeleteReagentGUI
from gui_functions.CommonFunctions import populate_dropdown_box, error_reset, error_highlight


class DeleteWindow:
    def __init__(self, main_window):
        self.GUI = DeleteReagentGUI()
        self.reset_main_dropbox = True
        self.Main_Window = main_window
        self.Storage = main_window.Storage
        self.Main_Window.dialog_busy = True
        self.connect_buttons()

    def connect_buttons(self):
        self.GUI.close_button.clicked.connect(self.close_button_action)
        self.GUI.delete_button.clicked.connect(self.delete_button_action)
        populate_dropdown_box(self.GUI.dropdown_menu, self.Storage.create_storage_list())

    def close_button_action(self):
        if self.reset_main_dropbox:
            self.Main_Window.populate_reagent_dropdowns()
        self.Main_Window.dialog_busy = False
        self.GUI.close()

    def delete_button_action(self):
        error_reset(self.GUI.dropdown_menu)
        if self.GUI.dropdown_menu.currentText() == "":
            error_highlight(self.GUI.dropdown_menu)

        else:
            self.reset_main_dropbox = False

            # Turn off button to avoid accidental multiple activations
            self.GUI.delete_button.setEnabled(False)

            # Remove it and write the change to the file
            self.Storage.delete_reagent(self.GUI.dropdown_menu.currentText())

            # Update the dropdown boxes for the main GUI.
            self.Main_Window.populate_reagent_dropdowns()

            # Update the dropdown box for the delete interface itself.
            populate_dropdown_box(self.GUI.dropdown_menu, self.Storage.create_storage_list(), additional_opt=False)

            # Wait a moment to avoid multiple clicks
            QtCore.QTimer.singleShot(1000, lambda: self.GUI.delete_button.setEnabled(True))
