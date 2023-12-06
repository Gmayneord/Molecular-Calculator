from dataclasses import dataclass
from data.constants import DATA_STORAGE_FILE_LOC, REAGENT_VERSION_NO
from json import dump, load


@dataclass
class Reagent:
    """
    Class for storing each individual reagent item.
    """
    name: str
    molecular_weight: float
    product_code: str = ""
    supplier: str = ""
    h_codes: str = ""
    version_no: float = REAGENT_VERSION_NO


class ReagentDatabase:
    def create_database_list(self, sort: bool = True) -> list:
        """
        Function to give a list of items in the database.
        :param sort: boolean to determine whether the list should be sorted alphanumerically prior to return.
        :return: list of items in the reagent database
        """
        output_list = [item.name for item in self.reagent_database]
        if sort:
            output_list = sorted(output_list, key=str.lower)
        return output_list

    def save_database(self) -> None:
        """
        Function to save the current database state to the storage file.
        :return: None
        """
        storage_list = []
        for each_item in self.reagent_database:
            dict_item = vars(each_item)
            storage_list.append(dict_item)

        with open(DATA_STORAGE_FILE_LOC, "w") as json_file:
            dump(storage_list, json_file, indent=4)
        json_file.close()

    def load_database(self) -> None:
        """
        Function to load the current database state from the storage file.
        It will load the items into the self.reagent_database list.
        :return: None
        """
        self.reagent_database = []
        with open(DATA_STORAGE_FILE_LOC, "r") as json_file:
            stored_data = load(json_file)
        json_file.close()

        for each_item in stored_data:
            self.reagent_database.append(Reagent(name=each_item["name"],
                                                 molecular_weight=each_item["molecular_weight"],
                                                 product_code=each_item["product_code"],
                                                 supplier=each_item["supplier"],
                                                 h_codes=each_item["h_codes"],
                                                 version_no=each_item["version_no"],
                                                 )
                                         )

    def initial_run(self) -> None:
        """
        Function to be run when there is no reagent database found (i.e. the initial run). It will
        :return: list
        """
        self.reagent_database = []
        self.save_database()

    def return_reagent(self, reagent_name: str) -> Reagent:
        """
        Function to return the reagent object when given its name.
        :param reagent_name: string containing the name of the reagent.
        :return: Reagent dataclass object for the reagent.
        """
        output_reagent = [x for x in self.reagent_database if x.name == reagent_name][0]
        return output_reagent

    def add_reagent(self,
                    name: str,
                    molecular_weight: float,
                    product_code: str = "",
                    supplier: str = "",
                    h_codes: str = "") -> bool:
        """
        Function for adding an item to the reagent database. This involves a check of the names
        currently in the database to ensure there is no overlap.
        :return: bool, showing whether the item has been added to the database or not.
        """
        # Convert it to lowercase for easier comparison. Differentiating between upper and lowercase for items will just lead to confusion
        new_reagent_name = name.lower()
        overlap_list = [x for x in self.reagent_database if x.name.lower() == new_reagent_name]
        if len(overlap_list) > 0:
            return False
        else:
            new_item = Reagent(name, molecular_weight, product_code, supplier, h_codes)
            self.reagent_database.append(new_item)
            self.save_database()
            return True

    def delete_reagent(self, reagent_name: str) -> bool:
        """
        Function for deleting an item from the reagent database.
        :return: bool, showing whether the item has been deleted from the database or not.
        """
        deletion_item_name = reagent_name.lower()
        deletion_index = [index for (index, item) in enumerate(self.reagent_database) if item.name.lower() == deletion_item_name][0]
        del self.reagent_database[deletion_index]
        self.save_database()
        return True

    def edit_reagent(self,
                     old_reagent_name: str,
                     name: str,
                     molecular_weight: float,
                     product_code: str = "",
                     supplier: str = "",
                     h_codes: str = "") -> bool:
        """
        Function for editing an existing reagent item in the database. It will be passed the new Reagent object,
        and an old reagent object, and will replace the old one with the new one in the database.
        :return: bool, indicating whether changes were successful or not.
        """
        old_reagent_name = old_reagent_name.lower()
        replacement_index = [index for (index, item) in enumerate(self.reagent_database) if item.name.lower() == old_reagent_name][0]
        new_reagent_obj = Reagent(name,
                                  molecular_weight,
                                  product_code,
                                  supplier,
                                  h_codes)
        self.reagent_database[replacement_index] = new_reagent_obj
        self.save_database()
        return True
