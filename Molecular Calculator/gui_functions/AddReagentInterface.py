from guis.AddReagentGUI import AddReagentGUI
from gui_functions.CommonFunctions import batch_error_reset, error_highlight


class AddWindow:
    def __init__(self, main_window):
        super().__init__()
        self.GUI = AddReagentGUI()
        self.Main_Window = main_window
        self.Storage = main_window.Storage
        self.reset_main_dropbox = True
        self.Main_Window.dialog_busy = True
        self.connect_buttons()

    def connect_buttons(self) -> None:
        self.GUI.add_item_button.clicked.connect(self.add_item_action)
        self.GUI.close_button.clicked.connect(self.close_button_action)

    def close_button_action(self) -> None:
        if self.reset_main_dropbox:
            self.Main_Window.populate_reagent_dropdowns()
        self.Main_Window.dialog_busy = False
        self.GUI.close()

    def add_item_action(self):
        batch_error_reset([self.GUI.reagent_input,
                           self.GUI.mw_input,
                           self.GUI.product_code_input,
                           self.GUI.supplier_input,
                           self.GUI.h_code_input])

        if self.GUI.reagent_input.text() != "" and self.GUI.mw_input.text() != "":
            reagent_text = self.GUI.reagent_input.text()
            mw_text = self.GUI.mw_input.text()
            product_text = self.GUI.product_code_input.text()
            supplier_text = self.GUI.supplier_input.text()
            h_code_text = self.GUI.h_code_input.text()

            self.Storage.add_reagent(name=reagent_text,
                                      molecular_weight=float(mw_text),
                                      product_code=product_text,
                                      supplier=supplier_text,
                                      h_codes=h_code_text,
                                      )
            # Set the index on the dropdown box to be the new item...
            self.Main_Window.populate_reagent_dropdowns(default_value=reagent_text)

            # Set this variable so the first element in the dropbox list isn't selected when we return to the main interface.
            self.reset_main_dropbox = False

            # Close the dialog
            self.close_button_action()

        else:
            if self.GUI.reagent_input.text() == "":
                error_highlight(self.GUI.reagent_input)
            if self.GUI.mw_input.text() == "":
                error_highlight(self.GUI.mw_input)
