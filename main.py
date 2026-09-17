import json
import sys
import PySide6.QtWidgets 
#import QApplication, QtableWidget, QTableWidgetItem, QMainWindow





def Load_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data