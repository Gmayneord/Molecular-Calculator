from guis.InspectReagentGUI import InspectReagentGUI
from data.datatypes import Reagent

class InspectionWindow():
    def __init__(self, Reagent_obj: Reagent):
        self.Reagent_obj = Reagent_obj
        self.GUI = InspectReagentGUI()
        self.connect_buttons()

    def connect_buttons(self):
        self.GUI.close_button.clicked.connect(self.close_button_action)
        self.GUI.name_label.setText(self.Reagent_obj.name)
        self.GUI.mw_label.setText(str(self.Reagent_obj.molecular_weight))
        self.GUI.product_code_label.setText(self.Reagent_obj.product_code)
        self.GUI.supplier_label.setText(self.Reagent_obj.supplier)
        self.GUI.h_code_label.setText(self.Reagent_obj.h_codes)

    def close_button_action(self):
        self.GUI.close()
