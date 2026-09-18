import json
import sys
from PySide6.QtWidgets import QApplication, QMessageBox, QTableWidget, QTableWidgetItem

#fonction pour charger le fichier json, exception et fermeture du fichier après lecture. 
def load_json_file(file_path):

    try: 
        file = open(file_path, 'r', encoding="utf-8")
        data = json.load(file)

    except FileNotFoundError as e:
        QMessageBox.critical(None, "Error", f"File not found: {e}", buttons=QMessageBox.Ok)

    except json.JSONDecodeError as e:
        QMessageBox.critical(None, "Error", f"Invalid JSON format in file: {e}", buttons=QMessageBox.Ok)

    else:
        file.close()
        return data

#Fait en sorte que la box ouvre
box = QApplication(sys.argv)

#Met le contenu du fichier json dans la variable
data = load_json_file(input())

#Crée la table pour afficher les données du fichier json
table = QTableWidget()

#Fonction pour mettre les données du fichier json dans la table, fait la gestion du tri et de la recherche
def open_window(data):

    #Set les row et colums de la table en fonction du nombre de row et colums du fichier json
    table.setRowCount(len(data))
    table.setColumnCount(len(data[0])) #0 pour les colonnes car sinon on manque une colonne si on met pas le 0

    #Set les headers de la table en fonction des keys du fichier json
    table.setHorizontalHeaderLabels(data[0].keys())

    #Itère sur les données du fichier json pour remplir la table avec les bonnes valeurs
    #for loop, enumerate pour avoir l'index de la row et de la colums, items pour avoir les keys et values du fichier json
    for row_index, row_data in enumerate(data): #Row
        for col_index, (key, value) in enumerate(row_data.items()): #Colonne 
            table.setItem(row_index, col_index, QTableWidgetItem(str(value))) #Value

            #QTableWigetItem prend en paramètre un string, donc convertir la value en string pour éviter les erreurs


#Appel la fonction pour ouvrir la fenêtre avec les données du fichier json
open_window(data)

#Affiche la table
table.show()

#Ferme la box et quitte le programme
sys.exit(box.exec())

    

