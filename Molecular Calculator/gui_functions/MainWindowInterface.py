from os import path

from guis.MainWindowGUI import MainGUI
from data.datatypes import ReagentDatabase
from data.constants import (DATA_STORAGE_FILE_LOC,
                            CONC_SCALER_DICT, CONC_SCALER_DEFAULT,
                            VOL_SCALER_DICT, VOL_SCALER_DEFAULT,
                            MASS_SCALER_DICT, MASS_SCALER_DEFAULT,
                            ADD_NEW_ITEM_TEXT, DELETE_ITEM_TEXT, EDIT_ITEM_TEXT)
from gui_functions.AddReagentInterface import AddWindow
from gui_functions.DeleteReagentInterface import DeleteWindow
from gui_functions.EditReagentInterface import EditWindow
from gui_functions.InspectReagentInterface import InspectionWindow
from gui_functions.common_functions import populate_dropdown_box, update_mw_label, error_reset, error_highlight

class MainWindow():
    def __init__(self):
        # Initially set this as busy for the creation of the dialog
        self.dialog_busy = True
        self.GUI = MainGUI()
        self.Database = ReagentDatabase()
        self.all_dropdown_boxes = [self.GUI.m_reagent_dropdown, self.GUI.c_reagent_dropdown,
                                   self.GUI.v_reagent_dropdown, self.GUI.i_reagent_dropdown]

        # Check if the database file exists, if it doesn't (Assume it's the initial run) and make a new one.
        if path.isfile(DATA_STORAGE_FILE_LOC):
            self.Database.load_database()

        else:
            self.Database.initial_run()
            self.GUI.m_output.setText('First runtime detected... A new data storage file has been created!')
            self.GUI.v_output.setText('First runtime detected... A new data storage file has been created!')
            self.GUI.c_output.setText('First runtime detected... A new data storage file has been created!')
        self.connect_actions()
        self.dialog_busy = False

    def connect_actions(self):
        GUI = self.GUI
        def connect_mass_tab(self, GUI):
            GUI.m_calc_button.clicked.connect(self.m_calculate_button_action)
            GUI.m_clear_calc_button.clicked.connect(
                lambda: self.clear_calculation_action(GUI.m_output, GUI.m_calc_button, GUI.m_clear_calc_button))

        def connect_vol_tab(self, GUI):
            GUI.v_calc_button.clicked.connect(self.v_calculate_button_action)
            GUI.v_clear_calc_button.clicked.connect(
                lambda: self.clear_calculation_action(GUI.v_output, GUI.v_calc_button, GUI.v_clear_calc_button))

        def connect_conc_tab(self, GUI):
            GUI.c_calc_button.clicked.connect(self.c_calculate_button_action)
            GUI.c_clear_calc_button.clicked.connect(
                lambda: self.clear_calculation_action(GUI.c_output, GUI.c_calc_button, GUI.c_clear_calc_button))

        def connect_inspection_tab(self, GUI):
            GUI.inspect_reagent_button.clicked.connect(self.inspect_reagent_button_action)

        connect_mass_tab(self, GUI)
        connect_vol_tab(self, GUI)
        connect_conc_tab(self, GUI)
        connect_inspection_tab(self, GUI)
        self.populate_scaler_dropdowns()
        self.populate_reagent_dropdowns(connect_mw_responses=True)
        GUI.close_button.clicked.connect(self.close_button_action)

    def populate_scaler_dropdowns(self):
        # ======================================================================
        # Populate scalers for mass tab
        populate_dropdown_box(dropdown_box_object=self.GUI.m_conc_dropdown,
                              list_to_populate=list(CONC_SCALER_DICT),
                              sort_list=False,
                              default_value=CONC_SCALER_DEFAULT
                              )
        populate_dropdown_box(dropdown_box_object=self.GUI.m_vol_dropdown,
                              list_to_populate=list(VOL_SCALER_DICT),
                              sort_list=False,
                              default_value=VOL_SCALER_DEFAULT
                              )

        # ======================================================================
        # Populate scalers for volume tab
        populate_dropdown_box(dropdown_box_object=self.GUI.v_conc_dropdown,
                              list_to_populate=list(CONC_SCALER_DICT),
                              sort_list=False,
                              default_value=CONC_SCALER_DEFAULT
                              )
        populate_dropdown_box(dropdown_box_object=self.GUI.v_mass_dropdown,
                              list_to_populate=list(MASS_SCALER_DICT),
                              sort_list=False,
                              default_value=MASS_SCALER_DEFAULT
                              )

        # ======================================================================
        # Populate scalers for conc tab
        populate_dropdown_box(dropdown_box_object=self.GUI.c_vol_dropdown,
                              list_to_populate=list(VOL_SCALER_DICT),
                              sort_list=False,
                              default_value=VOL_SCALER_DEFAULT
                              )
        populate_dropdown_box(dropdown_box_object=self.GUI.c_mass_dropdown,
                              list_to_populate=list(MASS_SCALER_DICT),
                              sort_list=False,
                              default_value=MASS_SCALER_DEFAULT
                              )
        # ======================================================================

    def populate_reagent_dropdowns(self, default_value: str="", connect_mw_responses=False):
        reagent_list = self.Database.create_database_list()
        # ======================================================================
        # Populate dropdowns for mass tab
        populate_dropdown_box(dropdown_box_object=self.GUI.m_reagent_dropdown,
                              list_to_populate=reagent_list,
                              additional_opt=True,
                              default_value=default_value
                              )

        self.reagent_selected_action(self.GUI.m_reagent_dropdown, self.GUI.m_mw_label)
        if connect_mw_responses:
            self.GUI.m_reagent_dropdown.activated[str].connect(lambda: self.reagent_selected_action(self.GUI.m_reagent_dropdown, self.GUI.m_mw_label))

        # ======================================================================
        # Populate dropdowns for volume tab
        populate_dropdown_box(dropdown_box_object=self.GUI.v_reagent_dropdown,
                              list_to_populate=reagent_list,
                              additional_opt=True,
                              default_value=default_value
                              )

        self.reagent_selected_action(self.GUI.v_reagent_dropdown, self.GUI.v_mw_label)
        if connect_mw_responses:
            self.GUI.v_reagent_dropdown.activated[str].connect(lambda: self.reagent_selected_action(self.GUI.v_reagent_dropdown, self.GUI.v_mw_label))

        # ======================================================================
        # Populate dropdowns for concentration tab
        populate_dropdown_box(dropdown_box_object=self.GUI.c_reagent_dropdown,
                              list_to_populate=reagent_list,
                              additional_opt=True,
                              default_value=default_value
                              )

        self.reagent_selected_action(self.GUI.c_reagent_dropdown, self.GUI.c_mw_label)
        if connect_mw_responses:
            self.GUI.c_reagent_dropdown.activated[str].connect(lambda: self.reagent_selected_action(self.GUI.c_reagent_dropdown, self.GUI.c_mw_label))

        # ======================================================================
        # Populate dropdowns for inspection tab
        # Now also issue an additional one for the inspection tab.
        populate_dropdown_box(dropdown_box_object=self.GUI.i_reagent_dropdown,
                              list_to_populate=reagent_list,
                              default_value=default_value
                              )

        self.reagent_selected_action(self.GUI.i_reagent_dropdown, self.GUI.i_mw_label)
        if connect_mw_responses:
            self.GUI.i_reagent_dropdown.activated[str].connect(lambda: self.reagent_selected_action(self.GUI.i_reagent_dropdown, self.GUI.i_mw_label))
        # ======================================================================

    def reagent_selected_action(self, dropdown_obj, mw_label_obj):
        # Only look at whether it's one of these options if the interface is not busy
        update_mw = True
        current_dropdown_text = dropdown_obj.currentText()
        if self.dialog_busy is False:
            if current_dropdown_text == ADD_NEW_ITEM_TEXT:
                update_mw = False
                self.add_item_window = AddWindow(self)
                self.add_item_window.GUI.show()

            elif current_dropdown_text == DELETE_ITEM_TEXT:
                update_mw = False
                self.delete_new_window = DeleteWindow(self)
                self.delete_new_window.GUI.show()

            elif current_dropdown_text == EDIT_ITEM_TEXT:
                update_mw = False
                self.edit_window = EditWindow(self)
                self.edit_window.GUI.show()

        if update_mw:
            if len(self.Database.reagent_database) > 0:
                # Update the molecular weight label with the current selected item
                reagent_choice = self.Database.return_reagent(current_dropdown_text)
                mol_weight = str(reagent_choice.molecular_weight)
                update_mw_label(mw_label_obj,
                                mol_weight)
            else:
                update_mw_label(mw_label_obj,
                                " --")


    def clear_calculation_action(self, text_to_reset, calc_button, clear_button):
        text_to_reset.setText(" ")
        calc_button.setDisabled(False)
        clear_button.setDisabled(True)

    def m_calculate_button_action(self):
        GUI = self.GUI
        error_reset(GUI.m_conc_textbox)
        error_reset(GUI.m_vol_textbox)
        reagent_selection_box = GUI.m_reagent_dropdown

        conc_textbox = GUI.m_conc_textbox
        conc_scaler = GUI.m_conc_dropdown
        vol_textbox = GUI.m_vol_textbox
        vol_scaler = GUI.m_vol_dropdown

        # Check for blank fields
        if conc_textbox.text() == "":
            error_highlight(conc_textbox)

        if vol_textbox.text() == "":
            error_highlight(vol_textbox)

        if reagent_selection_box.currentText() == ADD_NEW_ITEM_TEXT:
            error_highlight(reagent_selection_box)

        if conc_textbox.text() != "" and vol_textbox.text() != "" and reagent_selection_box.currentText() != ADD_NEW_ITEM_TEXT:
            concentration = float(conc_textbox.text())
            volume = float(vol_textbox.text())
            selected_reagent = self.Database.return_reagent(reagent_selection_box.currentText())
            self.mass_calc_and_display(input_conc=concentration,
                                       input_vol=volume,
                                       inputMW=selected_reagent.molecular_weight,
                                       vol_scaler=vol_scaler.currentText(),
                                       conc_scaler=conc_scaler.currentText(),
                                       reagent_name=reagent_selection_box.currentText())

    def v_calculate_button_action(self):
        GUI = self.GUI
        error_reset(GUI.v_conc_textbox)
        error_reset(GUI.v_mass_textbox)
        reagent_selection_box = GUI.v_reagent_dropdown

        conc_textbox = GUI.v_conc_textbox
        conc_scaler = GUI.v_conc_dropdown
        mass_textbox = GUI.v_mass_textbox
        mass_scaler = GUI.v_mass_dropdown

        # Check for blank fields
        if conc_textbox.text() == "":
            error_highlight(conc_textbox)

        if mass_textbox.text() == "":
            error_highlight(mass_textbox)

        if reagent_selection_box.currentText() == ADD_NEW_ITEM_TEXT:
            error_highlight(reagent_selection_box)

        if conc_textbox.text() != "" and mass_textbox.text() != "" and reagent_selection_box.currentText() != ADD_NEW_ITEM_TEXT:
            concentration = float(conc_textbox.text())
            mass = float(mass_textbox.text())
            selected_reagent = self.Database.return_reagent(reagent_selection_box.currentText())

            self.vol_calc_and_display(input_conc=concentration,
                                      conc_scaler=conc_scaler.currentText(),
                                      input_mass=mass,
                                      mass_scaler=mass_scaler.currentText(),
                                      inputMW=selected_reagent.molecular_weight,
                                      reagent_name=reagent_selection_box.currentText())

    def c_calculate_button_action(self):
        GUI = self.GUI
        mass_textbox = GUI.c_mass_textbox
        vol_textbox = GUI.c_vol_textbox

        error_reset(vol_textbox)
        error_reset(mass_textbox)
        reagent_selection_box = GUI.c_reagent_dropdown

        vol_scaler = GUI.c_vol_dropdown
        mass_scaler = GUI.c_mass_dropdown

        # Check for blank fields
        if vol_textbox.text() == "":
            error_highlight(vol_textbox)

        if mass_textbox.text() == "":
            error_highlight(mass_textbox)

        if reagent_selection_box.currentText() == ADD_NEW_ITEM_TEXT:
            error_highlight(reagent_selection_box)

        if vol_textbox.text() != "" and mass_textbox.text() != "" and reagent_selection_box.currentText() != ADD_NEW_ITEM_TEXT:
            vol = float(vol_textbox.text())
            mass = float(mass_textbox.text())
            selected_reagent = self.Database.return_reagent(reagent_selection_box.currentText())

            self.conc_calc_and_display(input_mass=mass,
                                       mass_scaler=mass_scaler.currentText(),
                                       input_vol=vol,
                                       vol_scaler=vol_scaler.currentText(),
                                       inputMW=selected_reagent.molecular_weight,
                                       reagent_name=reagent_selection_box.currentText())

    def inspect_reagent_button_action(self):
        # If there isn't anything in the database, do nothing for now
        if len(self.Database.reagent_database) > 0:
            # Get the item which is currently selected for inspection
            selected_item = self.GUI.i_reagent_dropdown.currentText()
            Reagent_obj = self.Database.return_reagent(selected_item)
            self.inpection_window = InspectionWindow(Reagent_obj)
            self.inpection_window.GUI.show()

    def close_button_action(self) -> None:
        """
        Function for closing the interface down.
        :return: None
        """
        if self.dialog_busy is False:
            # Stop the button being active if the dialog is busy.
            self.GUI.close()

    def mass_calc_and_display(self, input_conc, conc_scaler, input_vol, vol_scaler, inputMW, reagent_name):
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
            self.GUI.m_output.setText("The current calculation is out of bounds of the pre-defined scaling parameters. Please consider increasing scaling parameters to fix this")
        else:
            self.GUI.m_output.setText(f"For {input_vol}{vol_scaler} of {input_conc}{conc_scaler} use {adj_calc_mass}{mass_mag} of {reagent_name}")
            self.GUI.m_calc_button.setDisabled(True)
            self.GUI.m_clear_calc_button.setDisabled(False)

    def vol_calc_and_display(self, input_conc, conc_scaler, input_mass, mass_scaler, inputMW, reagent_name):
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
            self.GUI.v_output.setText("The current calculation is out of bounds of the pre-defined scaling parameters. Please consider increasing scaling parameters to fix this")
        else:
            self.GUI.v_output.setText(f"For {input_conc}{conc_scaler} using {input_mass}{mass_scaler} of {reagent_name}, use a total volume of {adj_calc_vol}{vol_mag}")
            self.GUI.v_calc_button.setDisabled(True)
            self.GUI.v_clear_calc_button.setDisabled(False)

    def conc_calc_and_display(self, input_mass, mass_scaler, input_vol, vol_scaler, inputMW, reagent_name):
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
            self.GUI.c_output.setText("The current calculation is out of bounds of the pre-defined scaling parameters. Please consider increasing scaling parameters to fix this")
        else:
            self.GUI.c_output.setText(f"With {input_mass}{mass_scaler} of {reagent_name} in {input_vol}{vol_scaler} you will have {adj_calc_conc}{conc_mag}")
            self.GUI.c_calc_button.setDisabled(True)
            self.GUI.c_clear_calc_button.setDisabled(False)

    def update_reagent_dropdown(self, reagent_selected):
        dropdown_list = [self.GUI.m_reagent_dropdown,
                         self.GUI.v_reagent_dropdown,
                         self.GUI.c_reagent_dropdown,
                         self.GUI.i_reagent_dropdown]

        mw_label_list = [self.GUI.m_mw_label,
                         self.GUI.v_mw_label,
                         self.GUI.c_mw_label,
                         self.GUI.i_mw_label]

        reagent_list = self.Database.create_database_list()
        for obj_no in range(len(dropdown_list)):
            dropdown_obj = dropdown_list[obj_no]
            populate_dropdown_box(dropdown_obj, reagent_list, additional_opt=True)

            if reagent_selected is None:
                dropdown_index = 0
            else:
                dropdown_index = dropdown_obj.findText(reagent_selected)
            dropdown_obj.setCurrentIndex(dropdown_index)


            if len(reagent_list) > 0:
                selected_reagent = self.Database.return_reagent(dropdown_obj.currentText())
                mol_weight = str(selected_reagent.molecular_weight)
                update_mw_label(mw_label_list[obj_no],
                                mol_weight)
            else:
                update_mw_label(mw_label_list[obj_no],
                                "--")
