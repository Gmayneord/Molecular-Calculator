from guis.EditReagentGUI import EditReagentGUI
from gui_functions.CommonFunctions import populate_dropdown_box, batch_error_reset, error_highlight


class EditWindow:
    def __init__(self, main_window):
        super().__init__()
        self.GUI = EditReagentGUI()
        self.Storage = main_window.Storage
        self.Main_Window = main_window
        self.reset_main_dropbox = True
        self.Main_Window.dialog_busy = True
        self.connect_buttons()

    def connect_buttons(self):
        self.GUI.add_item_button.clicked.connect(self.edit_item_action)
        self.GUI.close_button.clicked.connect(self.close_button_action)
        self.GUI.dropdown_menu.activated[str].connect(self.dropdown_selected_action)
        populate_dropdown_box(self.GUI.dropdown_menu, self.Storage.create_storage_list())
        self.dropdown_selected_action()

    def close_button_action(self):
        if self.reset_main_dropbox:
            self.Main_Window.populate_reagent_dropdowns()
        self.Main_Window.dialog_busy = False
        self.GUI.close()

    def dropdown_selected_action(self):
        self.GUI.reagent_input.setText(self.GUI.dropdown_menu.currentText())
        if self.GUI.dropdown_menu.currentText() != "":
            selected_item = self.Storage.return_reagent(self.GUI.dropdown_menu.currentText())
            self.GUI.reagent_input.setText(str(selected_item.name))
            self.GUI.mw_input.setText(str(selected_item.molecular_weight))
            self.GUI.product_code_input.setText(str(selected_item.product_code))
            self.GUI.supplier_input.setText(str(selected_item.supplier))
            self.GUI.h_code_input.setText(str(selected_item.h_codes))

    def edit_item_action(self):
        batch_error_reset([self.GUI.reagent_input,
                           self.GUI.mw_input,
                           self.GUI.supplier_input,
                           self.GUI.h_code_input,
                           self.GUI.product_code_input])
        if self.GUI.reagent_input.text() != "" and self.GUI.mw_input.text() != "":
            # Grab the item that was selected (original item)
            original_reagent_text = self.GUI.dropdown_menu.currentText()

            reagent_text = self.GUI.reagent_input.text()
            mw_text = self.GUI.mw_input.text()
            product_text = self.GUI.product_code_input.text()
            supplier_text = self.GUI.supplier_input.text()
            h_code_text = self.GUI.h_code_input.text()

            self.Storage.edit_reagent(old_reagent_name=original_reagent_text,
                                       name=reagent_text,
                                       molecular_weight=float(mw_text),
                                       product_code=product_text,
                                       supplier=supplier_text,
                                       h_codes=h_code_text)

            self.Main_Window.populate_reagent_dropdowns(default_value=reagent_text)
            self.reset_main_dropbox = False

            # Close the dialog
            self.close_button_action()

        else:
            if self.GUI.reagent_input.text() == "":
                error_highlight(self.GUI.reagent_input)
            if self.GUI.mw_input.text() == "":
                error_highlight(self.GUI.mw_input)
