import os
import json
from enum import Enum

Key_JsonFile = "Database.json"
Key_JsonArray = "Assets"
Key_TempFolder = "Temp"

Key_ColumnName      = "Name"
Key_ColumnLocation  = "Location"
Key_ColumnType      = "Type"
Key_ColumnURL       = "URL"

class SupportedTypes(Enum):
    Mega = 0

class ETools:

    root_folder = None
    config_folder = None

    @staticmethod
    def save_json(array_data):
        json_data = { Key_JsonArray: array_data }

        os.makedirs(ETools.config_folder, exist_ok=True)

        file_path = os.path.join(ETools.config_folder, Key_JsonFile)

        with open(file_path, 'w') as json_file:
            json.dump(json_data, json_file, indent=4)
    
    @staticmethod
    def load_json():
        try:
            with open(ETools.config_folder + "/" + Key_JsonFile, 'r') as file:
                data = json.load(file)
                return data.get(Key_JsonArray, None)
            
        except FileNotFoundError:
            return None
    
    @staticmethod
    def get_temp_folder():
        return os.path.join(ETools.config_folder)
