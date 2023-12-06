from PyQt5 import QtWidgets

from data.constants import ADD_NEW_ITEM_TEXT, DELETE_ITEM_TEXT, EDIT_ITEM_TEXT


def create_line(orientation: str = "h") -> QtWidgets.QFrame:
    """
    Function to create a vertical or horizontal line for the interface.
    :param orientation: String, either "h" for horizontal or "v" for vertical.
    :return:
    """
    line = QtWidgets.QFrame()
    if orientation == "v":
        line.setFrameShape(QtWidgets.QFrame.VLine)
    elif orientation == "h":
        line.setFrameShape(QtWidgets.QFrame.HLine)
    line.setFrameShadow(QtWidgets.QFrame.Sunken)
    return line


def populate_dropdown_box(dropdown_box_object: QtWidgets.QComboBox,
                          list_to_populate: list,
                          additional_opt: bool = False,
                          sort_list: bool = True,
                          default_value: str = "") -> None:
    """
    Function to populate a dropdown box with a list of items.
    :param dropdown_box_object: QComboBox, which is to be populated with the list.
    :param list_to_populate: list, comprised of strings to populate the QComboBox with.
    :param additional_opt: bool, indicating whether the standard additional items should be appended to the end of the dropdown menu
    :param sort_list: bool, indicating whether to sort the items alphanumerically in the list before adding
    :param default_value: string, indicating which option in the list_to_populate will be selected when the list is populated.
    :return: None
    """
    # Clear the dropdown box data is anything was already stored in it.
    dropdown_box_object.clear()

    if sort_list:
        list_to_populate = sorted(list_to_populate, key=str.lower)

    # If we want to add the options to the dropdown box...
    if additional_opt:
        for item in [ADD_NEW_ITEM_TEXT, DELETE_ITEM_TEXT, EDIT_ITEM_TEXT]:
            list_to_populate.append(item)

    for each_item in list_to_populate:
        dropdown_box_object.addItem(each_item)

    if default_value != "":
        dropdown_box_object.setCurrentIndex(dropdown_box_object.findText(default_value))
    else:
        dropdown_box_object.setCurrentIndex(0)


def error_highlight(object_to_highlight) -> None:
    """
    Function to highlight an error in a QtWidget object
    :param object_to_highlight: Can be any of the QtWidget types, e.g. QComboBox, QlineEdit etc.
    :return: None
    """
    object_to_highlight.setStyleSheet("background: red")


def error_reset(object_to_reset) -> None:
    """
    Function to reset the error state of the QtWidget object given.
    :param object_to_reset: Can be any of the QtWidget types, e.g. QComboBox, QlineEdit etc.
    :return:None
    """
    object_to_reset.setStyleSheet("background: None")


def batch_error_reset(objects_to_reset: list) -> None:
    """
    Function to reset a list of QtWidget items.
    :param objects_to_reset: list containing the QtWidget items
    :return: None
    """
    for each_item in objects_to_reset:
        error_reset(each_item)


def update_mw_label(mw_label_obj: QtWidgets.QLabel, mw_to_write: str) -> None:
    """
    Function to write the string to the molecular weight label object.
    :return: None.
    """
    mw_label_obj.setText(f"MW: {mw_to_write}")
