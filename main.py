import json
import sys
from PySide6.QtWidgets import QApplication, QHBoxLayout, QLabel, QLineEdit, QMessageBox, QTableWidget, QTableWidgetItem, QPushButton, QVBoxLayout, QWidget
from PySide6.QtCore import Qt

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
        global filename
        filename = file_path.split(".")[-2].split("\\")[-1]  # Récupère le nom du fichier sans l'extension et le chemin le . signal de de couper au point et \\ signifier de couper au \\
        return data

#Fait en sorte que la box ouvre
box = QApplication(sys.argv)

#Met le contenu du fichier json dans la variable
data = load_json_file(input())

#Crée la table pour afficher les données du fichier json
table = QTableWidget()

#Crée les boutons pour trier les données du fichier json
sort_ascending = QPushButton("Tri Ascendant")
sort_descending = QPushButton("Tri Descendant")
#Barre de recherche et le texte de base 
search_bar = QLineEdit()
search_bar.setPlaceholderText("Recherche...")

#Affiche un label et je set le texte que je veux dedans
display_box = QLabel()
display_box.setText(f"Affichage du fichier: {filename}\nTaille en mémoire: {sys.getsizeof(data)} bytes\nNombre d'éléments: {len(data)}") 

#Container qui contiens toute le visuelle
container = QWidget()
layout_v = QVBoxLayout(container) #Vertical 
layout_h = QHBoxLayout() #Horizontal
layout_h.addWidget(sort_ascending)  #add sort_ascending au layout_h
layout_h.addWidget(sort_descending) #add sort_descending au layout_h
layout_v.addLayout(layout_h) #add layout_h au layout_v
layout_v.addWidget(search_bar) #add search_bar au layout_v
layout_v.addWidget(table) #add table au layout_v
layout_v.addWidget(display_box) #Ajoute le display box au layout_v
container.setLayout(layout_v) #Set le layout pour le container

#Fonction pour mettre les données du fichier json dans la table, fait la gestion du tri et de la recherche
def create_table(data):

    #Connecte les boutons au def que je veux. 
    #J'ai fais un lambda car je veux que le code s'exécute quand on appuie sur le bouton et pas tout de suite.
    sort_ascending.clicked.connect(lambda: sort_table("Croissant"))
    sort_descending.clicked.connect(lambda: sort_table("Décroissant"))
    search_bar.textChanged.connect(lambda text: search_table(text)) 
    #text parce que lambda a besoin d'un paramètre, sa aurait pu être banane

    #Set les row et colums de la table en fonction du nombre de row et colums du fichier json
    table.setRowCount(len(data))
    table.setColumnCount(len(data[0])) #0 pour les colonnes car sinon on manque une colonne si on met pas le 0

    #Set les headers des colonnes en fonction des keys du fichier json
    table.setHorizontalHeaderLabels(data[0].keys())

    #Itère sur les données du fichier json pour remplir la table avec les bonnes valeurs
    #for loop, enumerate pour avoir l'index de la row et de la colums, items pour avoir les keys et values du fichier json
    for row_index, row_data in enumerate(data): #Row
        for col_index, (key, value) in enumerate(row_data.items()): #Colonne .item() veux dier enumrer les items a cette row la
            table.setItem(row_index, col_index, QTableWidgetItem(str(value))) #Value
            #QTableWigetItem prend en paramètre un string, donc convertir la value en string pour éviter les erreurs


#Fonction de tri
def sort_table(type):
 if type == "Croissant":
   table.sortItems(0, Qt.AscendingOrder) #0 pour la première colonne, Qt.AscendingOrder pour trier en ordre croissant
 elif type == "Décroissant":
     table.sortItems(0, Qt.DescendingOrder) #0 pour la première colonne, Qt.DescendingOrder pour trier en ordre décroissant

#Fonction de recherche
def search_table(search_text):
    matched_rows = set() #Crée un set pour stocker les rows que je dois garder
    items = table.findItems(search_text, Qt.MatchContains) #Qt.MatchContains est pour regarder si le texte est indentique 

    for item in items: #itère dans les items pour trouver les rows qui matchent avec le texte 
      row = item.row() #mettre les row trouver dans row
      matched_rows.add(row) # ajouter les rows trouver dans le set matched_rows

    for row in range(table.rowCount()): #Itère sur toutes les rows et cache celles qui ne matchent pas avec le texte de recherche
       table.setRowHidden(row, row not in matched_rows) 


#Appel la fonction pour ouvrir la fenêtre avec les données du fichier json
create_table(data)
#Resize la fenetre pour ne plus avoir a l'agrandir manuellement
container.resize(container.size())
#Affiche la table
container.show()
 
#Ferme la box et quitte le programme
sys.exit(box.exec())

    

