
# Storage location of database file:
DATA_STORAGE_FILE_LOC = "Reagent_Storage.json"

# Version number for the reagent, to be updated when modifications are made to the reagent type.
REAGENT_VERSION_NO = 1.0

# ==========================================
# Parameters for the input for the calculation (e.g. in mass tab, the concentration and volume fields)
# Minimum value
REAGENT_FIELD_MIN_VAL = 0

# Maximum value
REAGENT_FIELD_MAX_VAL = 1000

# Number of decimal places
REAGENT_FIELD_DECIMALS_NO = 1
# ==========================================
# Field parameters for the input of molecular weight when adding / editing a reagent.
# Minimum value
MW_FIELD_MIN_VAL = 0

# Maximum value
MW_FIELD_MAX_VAL = 1000000

# Number of decimal places
MW_FIELD_DECIMAL_NO = 2
# ==========================================

# ==========================================
# Range of units for dropdown menus
CONC_SCALER_DICT = {"M": 1,
                    "mM": 0.001,
                    "uM": 0.000001,
                    "nM": 0.000000001,
                    "pM": 0.000000000001,
                    }

VOL_SCALER_DICT = {"L": 1,
                   "mL": 0.001,
                   "uL": 0.000001,
                   "nL": 0.000000001,
                   "pL": 0.000000000001,
                   }

MASS_SCALER_DICT = {"kg": 1000,
                    "g": 1,
                    "mg": 0.001,
                    "ug": 0.000001,
                    "ng": 0.000000001,
                    "pg": 0.000000000001,
                    }
# ==========================================

# ==========================================
# Default values for the scaling dropdown menus
CONC_SCALER_DEFAULT = "mM"
VOL_SCALER_DEFAULT = "mL"
MASS_SCALER_DEFAULT = "g"
# ==========================================

# ==========================================
# Text for commands from text boxes
ADD_NEW_ITEM_TEXT = "Add new item..."
DELETE_ITEM_TEXT = "Delete item..."
EDIT_ITEM_TEXT = "Edit item..."
# ==========================================
