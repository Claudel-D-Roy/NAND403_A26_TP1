import json
import sys
from PySide6.QtWidgets import QApplication, QHBoxLayout, QLabel, QLineEdit, QMessageBox, QTableWidget, QTableWidgetItem, QPushButton, QVBoxLayout, QWidget
from PySide6.QtCore import Qt

#Variable globale
#------------------------------------------------------
#Fait en sorte que la box ouvre
box = QApplication(sys.argv)
#Crée la table pour afficher les données du fichier json
table = QTableWidget()
#Container qui contiens toute le visuelle
container = QWidget()
#-------------------------------------------------------

#-------------------json--------------------------------
#fonction pour charger le fichier json, exception et fermeture du fichier après lecture. 
def load_json(file_path):

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

#-------------------------------------------------------


#-------------------variable----------------------------
print("Veuillez écrire le chemin pour un fichier json : ")
filename = input()
data = load_json(filename)
file_split = filename.split(".")[-2].split("\\")[-1]  
# Récupère le nom du fichier sans l'extension et le chemin le . signal de de couper au point et \\ signifier de couper au \\
#-------------------------------------------------------


#---------------------Window----------------------------
# #Crée la fenetre 
def create_window():
   
    #Barre de recherche et le texte de base 
    search_bar = QLineEdit()
    search_bar.setPlaceholderText("Recherche...")

    #Affiche un label et je set le texte que je veux dedans
    display_box = QLabel()
    display_box.setText(f"Nom du fichier: {file_split}\nTaille en mémoire: {sys.getsizeof(data)} bytes\nNombre d'éléments: {len(data)}") 

    #Layout du container
    layout_v = QVBoxLayout(container) #Vertical 
    layout_h = QHBoxLayout() #Horizontal   
    layout_v.addLayout(layout_h) #add layout_h au layout_v
    layout_v.addWidget(search_bar) #add search_bar au layout_v
    layout_v.addWidget(table) #add table au layout_v
    layout_v.addWidget(display_box) #Ajoute le display box au layout_v
    container.setLayout(layout_v) #Set le layout pour le container

    #Appel la fonction pour ouvrir la fenêtre avec les données du fichier json
    create_table(data, search_bar)  
#-------------------------------------------------------
 

#---------------------Tableau---------------------------
#Fonction pour mettre les données du fichier json dans la table, fait la gestion du tri et de la recherche
def create_table(data, search_bar):

    #Connecte les boutons au def que je veux. Lambda = methode anonyme 
    #J'ai fais un lambda car je veux que le code s'exécute quand on appuie sur le bouton et pas tout de suite.
    search_bar.textChanged.connect(lambda text: search_table(text)) 
    #text parce que lambda a besoin d'un paramètre, sa aurait pu être banane

    #Va chercher les headers unique car c'est possible que les headers soit différent
    unique_headers = {} #dictionnaire, va faire ( key, " ") une fois le nested loop va être fini
    for row in data: 
        for key in row.keys():
            unique_headers[key] = None #Viens créer la place vide pour les headers
    headers_list = list(unique_headers.keys()) #Viens faire une liste avec les headers

    #Set les row et colums de la table en fonction du nombre de row et colums du fichier json
    table.setRowCount(len(data))
    table.setColumnCount(len(headers_list)) #La longueur de la lste de header est le nombre de colonne

    #Set les headers des colonnes en fonction de la liste de headers
    table.setHorizontalHeaderLabels(headers_list) 

    #Itère sur les données du fichier json pour remplir la table avec les bonnes valeurs
    #for loop, enumerate pour avoir l'index de la row et de la colums, items pour avoir les keys et values du fichier json
    for row_index, row_data in enumerate(data): #Row row_index est le num ex row 0 et row_data est tous se qui a dans cette object la, donc le id, le nom ect.. en plus des données
        for col_index, header in enumerate(headers_list): #Viens énuméré en fonction des headers
            
            value = row_data.get(header, "") #viens voir si une donnée est associée au header, sinon met ""

            if isinstance(value, int): #Regarde si la value est in int
                item = QTableWidgetItem(value) #ajoute l'item
                item.setData(Qt.ItemDataRole.DisplayRole, value) #DisplayRole fait en sort que sa soit display en text, setData(role, valeur)
            else:
                item = QTableWidgetItem(str(value)) #QTableWigetItem prend en paramètre un string, donc convertir la value en string pour éviter les erreurs
           
            table.setItem(row_index, col_index, item) #item trouver ex NAND403-001

    table.setSortingEnabled(True) #tri ma table en fonction de la colonne que le user a choisi
#-------------------------------------------------------

#----------------------Recherche------------------------
#Fonction de recherche
def search_table(search_text):
    matched_rows = set() #Crée un set pour stocker les rows que je dois garder
    items = table.findItems(search_text, Qt.MatchContains) #Qt.MatchContains est pour regarder si le texte est indentique 

    for item in items: #itère dans les items pour trouver les rows qui matchent avec le texte 
      row = item.row() #mettre les row trouver dans row
      matched_rows.add(row) # ajouter les rows trouver dans le set matched_rows

    for row in range(table.rowCount()): #Itère sur toutes les rows et cache celles qui ne matchent pas avec le texte de recherche
       table.setRowHidden(row, row not in matched_rows) 
#-------------------------------------------------------


#---------------------Appel-----------------------------
create_window()
#-------------------------------------------------------

#----------------------Show-----------------------------
#Resize la fenetre pour ne plus avoir a l'agrandir manuellement
container.resize(container.size())
#Affiche la table
container.show()
#-------------------------------------------------------

#----------------------Exit-----------------------------
#Ferme la box et quitte le programme
sys.exit(box.exec()) 
#-------------------------------------------------------
