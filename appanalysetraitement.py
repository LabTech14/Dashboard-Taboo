#!/usr/bin/env python
# coding: utf-8

# In[21]:


import os
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import datetime
from decimal import Decimal
from pathlib import Path
import locale
from calendar import month_name
#import pendulum
import plotly.io as pio
pio.renderers.default = "browser"  # Utiliser le rendu dans le navigateur

import warnings
warnings.filterwarnings("ignore")

# Charger le DataFrame INVENTAIRE2
#inventaire2_df = pd.read_excel("consolidated_data.xlsx")

# Chemin du répertoire contenant les fichiers Excel
input_directory = r'input'
#fina = pd.read_csv(r'non.csv')
#fina = pd.read_csv(r'non.csv', encoding='utf-8', errors='replace')


# Essayer de lire le fichier CSV en utilisant utf-8
try:
    fina = pd.read_excel('non.xlsx')
except UnicodeDecodeError:
    # En cas d'erreur d'encodage, essayez en utilisant latin-1
    fina = pd.read_excel('non.xlsx', encoding='latin-1')


############################################## exploration et traitements des données #####################################

# Chemin du répertoire du fichier Analyse TB2023
excel_file = r"Analyse TB2023.xlsx"

# Choisir les feuilles a sélectionnées pour le chiffre d'affaire monthly du fichier Analyse TB2023 que vous souhaitez consolider
sheets_to_consolidate = ['AVRIL 23', 'MAI 23','JUIN 23', 'JUILLET 23','AOUT 23','SEPTEMBRE 23','OCTOBRE 23'] #'AVRIL 23', 'MAI 23', 

# Charger les feuilles spécifiées en un dictionnaire de DataFrames
dfs = pd.read_excel(excel_file, sheet_name=sheets_to_consolidate)

# Concaténer les DataFrames en utilisant les noms d'entête de colonnes
consolidated_sheet = pd.concat(dfs, ignore_index=True, sort=False)

# Convertir la colonne "Date " en format de date avec gestion des erreurs
consolidated_sheet["Date "] = pd.to_datetime(consolidated_sheet["Date "], format="%Y-%m-%d %H:%M:%S", errors='coerce')

# Filtrer les lignes où la colonne "Date " est au format de date valide
consolidated_sheet = consolidated_sheet[consolidated_sheet["Date "].notnull()]

# Sélectionner uniquement les colonnes "Date ", "CA" et "ACHATS"
columns_to_keep = ["Date ", "CA", "ACHATS"]
consolidated_sheet = consolidated_sheet[columns_to_keep]


# Enregistrer la feuille consolidée avec les colonnes spécifiques dans un nouveau fichier Excel
consolidated_excel_file = 'feuille_consolid.xlsx'
consolidated_sheet.to_excel(consolidated_excel_file, index=False)


################################################### 2 #############################################################################

# Ouvrir le fichier Excel "Analyse TB2023.xlsx" et charger la feuille "Détail Dépenses"
excel_file = r"Analyse TB2023.xlsx"
sheet_name =  "Détail Dépenses"

df = pd.read_excel(excel_file, sheet_name)

# Transformer la colonne "Date " en format de date avec gestion des erreurs
df["Date "] = pd.to_datetime(df["Date "], format="%Y-%m-%d %H:%M:%S", errors='coerce')

# Supprimer les lignes où la colonne "Date " n'est pas au format "date"
df = df.dropna(subset=["Date "])

# Supprimer les colonnes "Unnamed: 25" et "JOURS"
columns_to_drop = ["Unnamed: 25", "JOURS","TOTAL DEPENSES "]
df = df.drop(columns=columns_to_drop)

# Enregistrer les données dans un nouveau fichier Excel "Analyse.xlsx"
new_excel_file = "Analyse.xlsx"

df.to_excel(new_excel_file, index=False)

################################################ 3 ###############################################################################
# Fusionner les DataFrames df et consolidated_sheet sur la colonne "Date "
merged_df = df.merge(consolidated_sheet[["Date ", "CA", "ACHATS"]], on="Date ", how="left")



# Remplacer les valeurs NaN par 0 dans tout le DataFrame
merged_df.fillna(0, inplace=True)


# Enregistrer les données dans un nouveau fichier Excel "Analyse.xlsx"
new_excel_file = "Analyse_Globale.xlsx"

merged_df.to_excel(new_excel_file, index=False)

print(f"Données de la feuille '{sheet_name}' traitées et enregistrées dans '{new_excel_file}'.")


###################################################  4  #######################################################################

# Charger les données de la feuille "RH" depuis le fichier Excel Analyse TB2023
excel_file = r"Analyse TB2023.xlsx"
sheet_name = "RH"
df = pd.read_excel(excel_file, sheet_name)

# Ouvrir un nouveau fichier Excel pour sauvegarder le contenu traité
new_excel_file = "ChargePersonnel.xlsx"
with pd.ExcelWriter(new_excel_file, engine="xlsxwriter") as writer:
    # Enregistrer le DataFrame d'origine dans le nouveau fichier Excel
    df.to_excel(writer, sheet_name="RH", index=False)

# Lire le nouveau fichier Excel pour le traitement ultérieur
df_new = pd.read_excel(new_excel_file, sheet_name="RH")

# Sélectionner uniquement la colonne "Date" et la colonne "ChargePersonnel"
df_filtered = df_new[['Date ', "RH"]]

# Supprimer les lignes vides ou égales à 0
df_filtered = df_filtered.dropna(subset=['Date ', "RH"])
df_filtered = df_filtered[(df_filtered != 0).all(axis=1)]

# Transformer la colonne "Date" au format de date
#df_filtered['Date '] = pd.to_datetime(df_filtered['Date '], format="%Y-%m-%d %H:%M:%S")  # Adapter le format au format réel dans votre fichier
df_filtered["Date "] = pd.to_datetime(df_filtered["Date "], format="%Y-%m-%d %H:%M:%S", errors='coerce')

# Enregistrer le DataFrame filtré dans un autre fichier Excel
new_filtered_excel_file = "ChargePersonnel.xlsx"
df_filtered.to_excel(new_filtered_excel_file, index=False)

print(f"Données filtrées enregistrées dans '{new_filtered_excel_file}'.")
#df_filtered

merged = merged_df.merge(df_filtered[["Date ", "RH"]], on="Date ", how="left")

merged.fillna(0, inplace=True)

merged


# Enregistrer le DataFrame filtré dans un autre fichier Excel
new_filtered_excel_file = "DétailsDépenses.xlsx"
merged.to_excel(new_filtered_excel_file, index=False)

print(f"Données consolidées et enregistrées dans '{new_filtered_excel_file}'.")
#df_filtered

#merged


########################################### calcul financier #################################################################


merged_copy = merged.copy()
df0 = merged_copy

########Calculer le total par colonne :#########

# Somme de chaque colonne
#total_par_colonne = df0.sum()
# Sélectionner uniquement les colonnes numériques (excluant la colonne "Date")
numeric_columns = df0.select_dtypes(include=["number"])

# Calculer la somme des colonnes numériques
sum_by_column = numeric_columns.sum()

# Sélectionner uniquement les colonnes numériques (excluant la colonne "Date")
numeric_columns = df0.select_dtypes(include=["number"])

# Calculer la somme des colonnes numériques par ligne (axis=1)
sum_by_row = numeric_columns.sum(axis=1)



######Coûts des produits vendus##########

# Liste des colonnes à inclure dans le calcul
colonnes_ = [  "DRINK", "MIAMI 228 ", "PICASSO", "GLACONS"]

# Ajouter une colonne "Coûts des produits vendus"
df0["DRINKS"] = df0[colonnes_].sum(axis=1)


# Création de la colonne eats qui regroupe la colonne eta et gaz 
df0["EATS"] = df0["EAT"] + df0["GAZ"]

# Les colonnes a inclures dans le calcul du coûts des produits vendus
colonnes_a_inclure = ["SMOKE", "EATS", "DRINKS"]

# Ajouter une colonne "Coûts des produits vendus"
df0["Coûts des produits vendus"] = df0[colonnes_a_inclure].sum(axis=1)



###############################################################################################################################

##################################################### Marge brute##############################################################

# Créer la nouvelle colonne "Marge brute"
df0["Marge brute"] = df0["CA"] - df0["Coûts des produits vendus"]

##################################################### Charge operationnel ####################################################

# Liste des colonnes à inclure dans le calcul
colonnesinclure = ['CACHETS',  'CASH POWER',
         'MARKETING','ADMINISTRATIF',
        'MONNAIE', 
       'CREDIT TEL', 'INTERNET / TV', 'LOYERS',
       'CONSOMMABLES', 'ENTRETIEN ', 'TRANSPORT', 'AUTRE',  'RH']

# Ajouter une colonne "OPEX"
df0["OPEX"] = df0[colonnesinclure].sum(axis=1)

################################################### Resultat d'exploitation #################################################

df0["Resultat d'exploitation"] = df0["Marge brute"] - df0["OPEX"]

################################################### Resultat avant Impôts ####################################################

ChargesInterets = 0
df0["Resultat avant Impôts"] = df0["Resultat d'exploitation"] - ChargesInterets

################################################### Resultat net comptable ###################################################

Taxes = 0
df0["Resultat net comptable"] = df0["Resultat avant Impôts"] - Taxes

 ################################################## Tresorerie net d'exploitation ###########################################


df0["Tresorerie net d'exploitation"] = df0["Resultat net comptable"]

################################################### Travaux et equipements ###################################################

# Liste des colonnes à inclure dans le calcul
colonnescal = ['EQUIPEMENTS','TRAVAUX']

# Ajouter une colonne "Coûts des produits vendus"
df0["Travaux et equipements"] = -df0[colonnescal].sum(axis=1)

########## Tresorerie net d'investissement ##########

df0["Tresorerie net d'investissement"] = df0["Travaux et equipements"]

########## Resultat net ##########

df0["Resultat net"] = df0["Tresorerie net d'exploitation"] + df0["Tresorerie net d'investissement"]

########## Working Capital ##########

df0["Working Capital"] = df0["ACHATS"]

########## Trésorerie Fin de Mois ##########

df0["Trésorerie Fin de Mois"] = df0["Working Capital"]

########## Taux marge brute ##########

#df0["Taux marge brute"] = df0["Marge brute"]/df0["CA"]
#df0["TMB"] = df0["Marge brute"]/df0["CA"]


# Liste des colonnes à inclure dans le calcul
col = ['MONNAIE', 
       'CREDIT TEL', 'INTERNET / TV', 'LOYERS',
        'ENTRETIEN ', 'TRANSPORT', 'AUTRE']

# Ajouter une colonne "Autres"
df0["Autres"] = df0[col].sum(axis=1)


# Liste des colonnes à inclure dans le calcul
col1 = [ 'MARKETING', 'ADMINISTRATIF']

# Ajouter une colonne "MARKETINGADMINISTRATIF"
df0["MARKETING_ADMIN"] = df0[col1].sum(axis=1)


# Liste des colonnes à afficher
#columns_to_display = ['Date ', "Coûts des produits vendus", "Marge brute", "OPEX", "Resultat d'exploitation","Resultat avant Impôts",
#                     "Resultat net comptable","Tresorerie net d'exploitation","Travaux et equipements","Tresorerie net d'investissement",
#                     "Resultat net","Working Capital","Trésorerie Fin de Mois","Taux marge brute"]

# Créer un nouveau DataFrame avec uniquement les colonnes à afficher
#df_subset = df0[columns_to_display]

# Afficher le DataFrame résultat
#df_subset

############################################ TCD #############################################################

# Convertir la colonne 'Date' en type datetime
df0['Date '] = pd.to_datetime(df0['Date '])

# Extraire le mois et l'année à partir de la colonne 'Date'
df0['Mois'] = df0['Date '].dt.to_period('M')

# Liste des colonnes pour le TCD
columns_for_tcd = ['Mois', "CA",'Coûts des produits vendus', 'Marge brute','CACHETS', 'CASH POWER',
                   "MARKETING_ADMIN",'RH',"Autres",'OPEX', 'Resultat d\'exploitation',
                   'Resultat avant Impôts', 'Resultat net comptable', 'Tresorerie net d\'exploitation',
                   'Travaux et equipements', 'Tresorerie net d\'investissement', 'Resultat net',
                   'Working Capital', 'Trésorerie Fin de Mois','CONSOMMABLES',"DRINKS","EATS","SMOKE"]

# Créer le TCD en groupant par mois
tcd = df0[columns_for_tcd].groupby('Mois').sum()

#calcul du Taux de Marge brute après le groupeby
#tcd = df0[columns_for_tcd].groupby('Mois').sum()
tcd["Taux marge brute"] = (tcd["Marge brute"])/(tcd["CA"])
tcd["Taux EATS"] = round((tcd["EATS"])/(tcd["CA"]),2)
tcd["Taux DRINKS"] =round( (tcd["DRINKS"])/(tcd["CA"]),2)
tcd["Taux SMOKE"] = round((tcd["SMOKE"])/(tcd["CA"]),2)
tcd["Profitabilité"] = round((tcd["Resultat net"])/(tcd["CA"]),2)

# Afficher le tableau croisé dynamique
#tcd
# Enregistrer le DataFrame filtré dans un autre fichier Excel
new_filtered_excel_file = r"non.xlsx"
tcd.to_excel(new_filtered_excel_file, index=True)

print(f"Données consolidées et enregistrées dans '{new_filtered_excel_file}'.")


input_directory = r'input'

# Créer une liste pour stocker les DataFrames
data_frames = []

# Lire le premier fichier Excel dans le répertoire
filename = os.listdir(input_directory)[0]
if filename.endswith('.xlsx') and not filename.startswith('~$'):
    file_path = os.path.join(input_directory, filename)
    try:
        # Lire le fichier Excel dans un DataFrame
        df = pd.read_excel(file_path)
        # Ajouter le DataFrame à la liste
        data_frames.append(df)
    except PermissionError:
        print(f"Ignoré : {filename} (Fichier verrouillé)")
else:
    print("Aucun fichier valide trouvé dans le répertoire.")



            
# Concaténer les DataFrames en un seul DataFrame
consolidated_df = pd.concat(data_frames, ignore_index=True)

# Vous pouvez continuer à utiliser consolidated_df comme vous le souhaitez
print(consolidated_df.head())


# Définition du dictionnaire de correspondance des mois anglais et français
month_translation = {
    "January": "Janvier",
    "February": "Février",
    "March": "Mars",
    "April": "Avril",
    "May": "Mai",
    "June": "Juin",
    "July": "Juillet",
    "August": "Août",
    "September": "Septembre",
    "October": "Octobre",
    "November": "Novembre",
    "December": "Décembre"
}


# Lire le fichier CSV en spécifiant le délimiteur et le format de date
#consolidated_df = pd.read_csv(path_to_file, delimiter=';', parse_dates=['Date'], dayfirst=True)

# Charger le fichier consolidé
#iconsolidated_df = df.copy()

# Renommer les colonnes existantes
consolidated_df.rename(columns={"Type": "Catégorie", "Categorie": "Sous-catégorie", "Produits": "Item", "TTC": "Total TTC"}, inplace=True)

# Diviser la colonne "Date" en "Mois" et "Année"
consolidated_df["Date"] = pd.to_datetime(consolidated_df["Date"])
consolidated_df["Mois"] = consolidated_df["Date"].dt.strftime("%B").map(month_translation)

# Ajouter la colonne Année
consolidated_df["Années"] = consolidated_df["Date"].dt.year



# Réorganiser les colonnes selon votre préférence
column_order = ["Date", "Mois", "Années", "Catégorie", "Sous-catégorie", "Item", "Qté", "offert", "Offert formule", "Total Qté", "Total TTC", "Cout", "Total Remise", "Total remisé", "Total HT"]
consolidated_df = consolidated_df[column_order]

inventaire2_df = consolidated_df

# Calculer la somme de Total Qté par Sous-Catégorie
sous_cat_sum = inventaire2_df.groupby('Sous-catégorie')['Total Qté'].transform('sum')

# Calculer la colonne "Quantité Absolue"
inventaire2_df['Quantité Absolue'] = inventaire2_df['Total Qté'] / sous_cat_sum*100

# Calculer la colonne "Quantité Relative"
total_sum = inventaire2_df['Total Qté'].sum()

inventaire2_df['Quantité Relative'] = inventaire2_df['Total Qté'] / sous_cat_sum

# Supprimer les lignes où la colonne 'Date' est vide
inventaire2_df.dropna(subset=['Date'], inplace=True)
# Afficher le DataFrame consolidé

#inventaire2_df




# Chemin du répertoire où vous voulez enregistrer le fichier Excel
output_directory = 'inputcons'

# Vérifier si le répertoire existe, sinon le créer
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Chemin complet du fichier de sortie
output_path = os.path.join(output_directory, 'BD.xlsx')

# Enregistrer le DataFrame en fichier Excel
inventaire2_df.to_excel(output_path, index=False)



#####################################################SECONDE PARTIE#############################################################

# Chargement des données à partir du fichier Excel
#file_path =  r"C:\Users\Administrateur\Desktop\Dashboardv001\inputcons\BD.xlsx"

#######df = pd.read_excel(output_path) #inventaire2_df.copy()    #pd.read_excel(file_path)
#print(df)

# Obtenir la liste des mois uniques dans la colonne 'Mois'
#mois_list = df['Mois'].unique()
######df['Mois'] = df['Mois'].astype(str)

######mois_list = sorted(df['Mois'].unique())



# Créez un dictionnaire de correspondance entre les noms de mois et les numéros de mois
#mois_numeros = {
    #'Janvier': 1, 'Février': 2, 'Mars': 3, 'Avril': 4, 'Mai': 5, 'Juin': 6,
    #'Juillet': 7, 'Août': 8, 'Septembre': 9, 'Octobre': 10, 'Novembre': 11, 'Décembre': 12
#}

# Triez les mois en fonction de leur numéro de mois
#mois_list = sorted(df['Mois'].unique(), key=lambda x: mois_numeros.get(x.lower(), 0))



# Obtenir la liste des années uniques dans la colonne 'Année'
#######annee_list = df['Années'].unique()
#annee_list = df['Années'].astype(int).unique()


# Obtenir la liste des années uniques dans la colonne 'Année'
######categorie_list = df['Catégorie'].unique()

# Obtenir la liste des années uniques dans la colonne 'Année'
#######sous_categorie_list = df['Sous-catégorie'].unique()


#################################################################################################################################################

####################################################### Flux horaire ###################################################################################


"""
# Chemin du dossier contenant les fichiers à consolider
folder_path1 = "C:\\Workdir\\dashbord\\Flux horaire"


def consolidate_files(folder_path1, output_folder1, output_file_name1):
    # Créer le dossier de sortie si nécessaire
    output_path1 = os.path.join(folder_path1, output_folder1)
    if not os.path.exists(output_path1):
        os.makedirs(output_path1)

    # Parcourir tous les fichiers dans le dossier
    all_data1 = []
    for file in os.listdir(folder_path1):
        if file.endswith('.xlsx') or file.endswith('.csv'):
            file_path1 = os.path.join(folder_path1, file)
            if file.endswith('.xlsx'):
                dff = pd.read_excel(file_path1)
            else:  # Pour les fichiers CSV
                dfF = pd.read_csv(file_path1)
            
            # Supprimer les lignes avec des valeurs manquantes
            dff.dropna(inplace=True)

            all_data1.append(dff)

    # Consolider tous les DataFrames en un seul
    consolidated_data1 = pd.concat(all_data1, ignore_index=True)

    # Enregistrer le DataFrame consolidé dans un nouveau fichier Excel
    output_file_path1 = os.path.join(output_path1, f"{output_file_name1}.xlsx")
    consolidated_data1.to_excel(output_file_path1, index=False)
    print(f"Consolidated data written to {output_file_path1}")


# Appeler la fonction
consolidate_files(folder_path1, "consolidate", "Flux horaire")
"""
###########################################################################################################################################
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# Exemple d'utilisation de la fonction
U = Path("Flux horaire/consolidate/Flux horaire.xlsx")
dfl = pd.read_excel(U)

def create_sales_dashboard(dfl):
    # Création des subplots
    fig = make_subplots(rows=2, cols=2, 
        subplot_titles=("Chiffre d'Affaires par Heure", "Nombre de Ventes par Heure",
                        ))#"Nombre de Vendeurs par Heure", "Panier Moyen par Heure"

    # Ajout des tracés pour chaque métrique et pour chaque mois
    for mois in dfl['Mois'].unique():
        df_mois = dfl[dfl['Mois'] == mois]
        fig.add_trace(go.Bar(x=df_mois["Heure"], y=df_mois["CA"], name=f"CA - {mois}"), row=1, col=1)
        #fig.add_trace(go.Scatter(x=df_mois["Heure"], y=df_mois["ventes"], mode="lines+markers", name=f"Ventes - {mois}"), row=1, col=2)
        #fig.add_trace(go.Scatter(x=df_mois["Heure"], y=df_mois["Vendeurs"], mode="lines+markers", name=f"Vendeurs - {mois}"), row=2, col=1)
        fig.add_trace(go.Scatter(x=df_mois["Heure"], y=df_mois["Panier Moyen"], mode="lines+markers", name=f"Panier Moyen - {mois}"), row=1, col=2)

    # Création des boutons pour filtrer par mois et par année
    mois_buttons = [
        dict(label="Tous les mois",
             method="update",
             args=[{"visible": [True] * (4 * len(dfl['Mois'].unique()))}, {"title": "Toutes les données"}])
    ]

    for mois in dfl['Mois'].unique():
        visible = [trace.name.endswith(mois) for trace in fig.data]
        mois_buttons.append(
            dict(label=mois,
                 method="update",
                 args=[{"visible": visible}, {"title": f"Données de {mois}"}])
        )

    annee_buttons = [
        dict(label=str(annee),
             method="update",
             args=[{"visible": [trace.name.endswith(str(annee)) for trace in fig.data]}, {"title": f"Données de {annee}"}])
        for annee in dfl['Année'].unique()
    ]

    fig.update_layout(
        updatemenus=[
            dict(buttons=mois_buttons, direction="down", x=0.1, xanchor="left", y=1.15, yanchor="top"),
            dict(buttons=annee_buttons, direction="down", x=0.3, xanchor="left", y=1.15, yanchor="top")
        ],
        title="",#Analyse des Performances de Vente par Heure, Mois et Année
        height=700
    )

    return fig



#fig.show()


################################################## Analyse Catégorielle ##################################################################
#from pathlib import Path

# Chemin complet vers le fichier source
file_path = Path("inputcons/BD.xlsx")#r"BD.xlsx"

# Lire les données du fichier Excel dans un DataFrame pandas
dif = pd.read_excel(file_path)

# Grouper les données par 'Mois', 'Années', et 'Catégorie', et calculer la somme du 'Total HT' pour chaque groupe
grouped_d = dif.groupby(['Mois', 'Années', 'Catégorie'])['Total HT'].sum().reset_index()

# Renommer la colonne 'Total HT' en 'CA'
grouped_d = grouped_d.rename(columns={'Total HT': 'CA'})

# Filtrer les données pour obtenir les chiffres d'affaires pour les catégories 'EAT', 'SMOKE', et 'DRINK'
filtered_dif = grouped_d[grouped_d['Catégorie'].isin(['EAT', 'SMOKE', 'DRINK'])]

# Chemin du répertoire de sortie
output_directory = r"inputcons"

# Vérifiez si le répertoire existe, sinon créez-le
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Nom du fichier de sortie Excel
output_file = 'categoriel.xlsx'

# Chemin complet du fichier de sortie
output_path = os.path.join(output_directory, output_file)

# Enregistrer le DataFrame filtré dans un fichier Excel
filtered_dif.to_excel(output_path, index=False)

print(f"Le fichier a été enregistré avec succès sous : {output_path}")



#################################################""""""""""""""############################################################

# Chemin du fichier original (remplacez par votre chemin réel)
chemin_original = Path("Analyse_Globale.xlsx")

# Faire une copie du fichier pour travailler dessus (remplacez par votre chemin réel)
chemin_copie = chemin_original.with_name("Analyse_Globale.xlsx")

# Lire les données depuis la copie
dif = pd.read_excel(chemin_copie)

# Création des nouvelles colonnes pour les catégories combinées
dif['DRINKS'] = dif[['DRINK', 'MIAMI 228 ', 'PICASSO', 'GLACONS']].sum(axis=1)
dif['EATS'] = dif['EAT'] + dif['GAZ']
dif['SMOKE'] = dif['SMOKE']
dif['CACHETS_EAT'] = dif['CACHETS']*(40/100)
dif['CACHETS_DRINK'] = dif['CACHETS']*(40/100)
dif['CACHETS_SMOKE'] = dif['CACHETS']**(20/100) 


# Extraction du mois et de l'année à partir de la colonne 'Date '
dif['Mois'] = pd.to_datetime(dif['Date ']).dt.strftime('%B')
dif['Années'] = pd.to_datetime(dif['Date ']).dt.year
dif = dif
# Traduire les mois en français
months_translation = {
    'January': 'Janvier', 'February': 'Février', 'March': 'Mars',
    'April': 'Avril', 'May': 'Mai', 'June': 'Juin',
    'July': 'Juillet', 'August': 'Août', 'September': 'Septembre',
    'October': 'Octobre', 'November': 'Novembre', 'December': 'Décembre'
}
dif['Mois'] = dif['Mois'].map(months_translation)

# Grouper par 'Mois' et 'Années' et sommer pour chaque catégorie
df_group = dif.groupby(['Mois', 'Années']).agg({
    'DRINKS': 'sum',
    'EATS': 'sum',
    'SMOKE': 'sum',
    #'CACHETS_SMOKE': 'sum',
    #'CACHETS_DRINK': 'sum',
   # 'CACHETS_EAT': 'sum'
    
}).reset_index()

# Renommage des colonnes pour correspondre à l'aperçu fourni
df_group.rename(columns={
    'DRINKS': 'Coûts par catégories DRINKS',
    'EATS': 'Coûts par catégories EATS',
    'SMOKE': 'Coûts par catégories SMOKE'
}, inplace=True)

# Fusionner les lignes pour chaque mois en une seule ligne par mois
df_final = df_group.melt(id_vars=['Mois', 'Années'], var_name='Catégories_Coûts', value_name='Coût des produits vendus')

# Ajouter une colonne 'Catégorie' en fonction de 'Catégories_Coûts'
category_mapping = {
    'Coûts par catégories DRINKS': 'DRINK',
    'Coûts par catégories EATS': 'EAT',
    'Coûts par catégories SMOKE': 'SMOKE'
}
df_final['Catégorie'] = df_final['Catégories_Coûts'].map(category_mapping)

# Supprimer la colonne 'Catégories_Coûts'
df_final.drop('Catégories_Coûts', axis=1, inplace=True)

# Triez par mois et années pour l'ordre chronologique
df_final.sort_values(by=['Années', 'Mois'], inplace=True)

# Préparation du chemin de sortie
output_directory = Path("inputcons")
output_directory.mkdir(exist_ok=True)
output_file_name = 'Recap_Categories.xlsx'
output_file_path = output_directory / output_file_name

# Sauvegarder le résultat dans un nouveau fichier Excel
df_final.to_excel(output_file_path, index=False)

print(f"Le récapitulatif a été sauvegardé à {output_file_path}")

#################################################""""""""""""""############################################################
# Remplacer par les chemins réels de vos fichiers
chemin_recap = "inputcons/Recap_Categories.xlsx"
chemin_categoriel = "inputcons/categoriel.xlsx"

# Charger les fichiers dans des DataFrames
df_recap = pd.read_excel(chemin_recap)
df_categoriel = pd.read_excel(chemin_categoriel)

# Fusionner les DataFrames sur les colonnes 'Mois', 'Années' et 'Catégorie'
df_merged12 = pd.merge(df_recap, df_categoriel, on=['Mois', 'Années', 'Catégorie'])

# Sauvegarder le résultat de la fusion dans un nouveau fichier Excel
chemin_resultat = "inputcons/Resultat_Fusion.xlsx"
df_merged12.to_excel(chemin_resultat, index=False)

#################################################""""""""""""""############################################################


# Définir la locale en français pour les noms des mois
#locale.setlocale(locale.LC_TIME, 'fr_FR')
#locale.setlocale(locale.LC_TIME, 'fr_FR.utf8')
#formatted_date = pendulum.now().locale('fr_FR').format('MMMM')


# Chemin vers le fichier original et le répertoire de destination
original_file_path = Path("DétailsDépenses.xlsx")
destination_directory = Path("inputcons")

# Faire une copie du fichier
copied_file_path = destination_directory / original_file_path.name
if not destination_directory.exists():
    destination_directory.mkdir(parents=True)
atch = pd.read_excel(original_file_path)
atch.to_excel(copied_file_path, index=False)

# Lire les données du fichier copié
atch = pd.read_excel(copied_file_path)

# Création des nouvelles colonnes basées sur les pourcentages fournis
categories = ['EAT', 'DRINK', 'SMOKE']
allocations = {'CACHETS': [0.4, 0.4, 0.2], 'CASH POWER': [0.4, 0.4, 0.2], 'RH': [0.4, 0.4, 0.2]}
other_columns = ['MONNAIE', 'CREDIT TEL', 'INTERNET / TV', 'LOYERS', 'ENTRETIEN ', 'TRANSPORT', 'AUTRE']
marketing_admin_columns = ['MARKETING', 'ADMINISTRATIF']

# Calcul des allocations pour les colonnes 'Autres' et 'MARKETING_ADMIN'
atch['Autres'] = atch[other_columns].sum(axis=1)
atch['MARKETING_ADMIN'] = atch[marketing_admin_columns].sum(axis=1)
allocations['Autres'] = [0.4, 0.4, 0.2]
allocations['MARKETING_ADMIN'] = [0.4, 0.4, 0.2]

# Calcul des colonnes par catégorie
for alloc in allocations:
    for i, cat in enumerate(categories):
        atch[f'{alloc}_{cat}'] = atch[alloc] * allocations[alloc][i]

# Convertir les dates en mois et années séparés
atch['Mois'] = pd.to_datetime(atch['Date ']).dt.month.apply(lambda x: month_name[x].capitalize())
atch['Année'] = pd.to_datetime(atch['Date ']).dt.year

# Traduire les mois en français
months_translation = {
    'January': 'Janvier', 'February': 'Février', 'March': 'Mars',
    'April': 'Avril', 'May': 'Mai', 'June': 'Juin',
    'July': 'Juillet', 'August': 'Août', 'September': 'Septembre',
    'October': 'Octobre', 'November': 'Novembre', 'December': 'Décembre'
}
atch['Mois'] = atch['Mois'].map(months_translation)

# Maintenant, créons le DataFrame final avec les lignes pour chaque catégorie
final_rows = []
for i, row in atch.iterrows():
    for cat in categories:
        new_row = {
            'Année': row['Année'],
            'Mois': row['Mois'],
            'MARKETING_ADMIN': row[f'MARKETING_ADMIN_{cat}'],
            'CACHETS': row[f'CACHETS_{cat}'],
            'CASH POWER': row[f'CASH POWER_{cat}'],
            'Autres': row[f'Autres_{cat}'],
            'RH': row[f'RH_{cat}'],
            'Opex': row[f'MARKETING_ADMIN_{cat}'] + row[f'CACHETS_{cat}'] + row[f'CASH POWER_{cat}'] + row[f'Autres_{cat}'] + row[f'RH_{cat}'],
            'Catégorie': cat
        }
        final_rows.append(new_row)

# Transformer en DataFrame
final_dfu = pd.DataFrame(final_rows)

# Effectuer un groupby sur 'Année', 'Mois' et 'Catégorie'
grouped_dfu = final_dfu.groupby(['Année', 'Mois', 'Catégorie']).sum().reset_index()

# Trier le DataFrame groupé par Année et Mois
grouped_dfu.sort_values(by=['Année', 'Mois'], inplace=True)

# Enregistrer le DataFrame groupé
final_file_path = destination_directory / 'Grouped_Final_Details.xlsx'
grouped_dfu.to_excel(final_file_path, index=False)

print(f"Le fichier groupé a été enregistré avec succès sous : {final_file_path}")



#################################################""""""""""""""############################################################

# Chemins vers les fichiers Excel
grouped_details_path = Path("inputcons/Grouped_Final_Details.xlsx")
result_fusion_path = Path("inputcons/Resultat_Fusion.xlsx")

# Chargement des DataFrames
grouped_df = pd.read_excel(grouped_details_path)
result_fusion_df = pd.read_excel(result_fusion_path)

# Renommer les colonnes pour uniformiser les noms
result_fusion_df.rename(columns={'Années': 'Année'}, inplace=True)

# Assurez-vous que le format des mois est le même dans les deux DataFrames
# Si nécessaire, mappez les noms des mois en français pour 'result_fusion_df'

# Fusionner les DataFrames sur les colonnes 'Année', 'Mois', et 'Catégorie'
combined_df = pd.merge(grouped_df, result_fusion_df, on=['Année', 'Mois', 'Catégorie'], how='outer')

# Enregistrer le DataFrame combiné dans un nouveau fichier Excel
combined_file_path = Path("inputcons/Combined_Details.xlsx")
combined_df.to_excel(combined_file_path, index=False)

print(f"Le fichier combiné a été enregistré avec succès sous : {combined_file_path}")


#################################################""""""""""""""############################################################

# Chemin vers le fichier Excel
excel_file_path = Path("inputcons/Combined_Details.xlsx")

# Lire les données du fichier Excel
walla = pd.read_excel(excel_file_path)

# Calcul de la Marge brute
walla['Marge brute'] = walla['CA'] - walla['Coût des produits vendus']

# Calcul du Résultat d'exploitation
walla['Resultat d\'exploitation'] = walla['Marge brute'] - walla['Opex']

# Calcul de la Rentabilité
walla['Rentabilite'] = round((walla['Resultat d\'exploitation'] / walla['CA'])*100, 1)
#walla['Rentabilite'] = (walla['Resultat d\'exploitation'] / walla['CA']) * 100
walla['Rentabilite'] = walla['Rentabilite'].apply(lambda x: "{:.1f}%".format(x))


# Calcul du Taux Coût des produits vendus
walla['Taux Coût des produits vendus'] = round((walla['Coût des produits vendus'] / walla['CA'])*100, 1)
walla['Taux Coût des produits vendus'] = walla['Taux Coût des produits vendus'].apply(lambda x: "{:.1f}%".format(x))
# Calcul du Taux Opex
walla['Taux Opex'] = round((walla['Opex'] / walla['CA'])*100, 1)
walla['Taux Opex'] = walla['Taux Opex'].apply(lambda x: "{:.1f}%".format(x))
# Calcul du Taux Marge brute
walla['Taux Marge brute'] = round((walla['Marge brute'] / walla['CA'])*100, 1)
walla['Taux Marge brute'] =walla['Taux Marge brute'].apply(lambda x: "{:.1f}%".format(x))
# Enregistrer les résultats dans le même fichier Excel
walla.to_excel(excel_file_path, index=False)


# Convertir les noms des mois en une forme ordonnable
months = {
    'Janvier': 1, 'Février': 2, 'Mars': 3, 'Avril': 4, 'Mai': 5, 'Juin': 6, 
    'Juillet': 7, 'Août': 8, 'Septembre': 9, 'Octobre': 10, 'Novembre': 11, 'Décembre': 12
}
walla['Mois'] = walla['Mois'].map(months)

# Trier les données par Année, Mois et Catégorie
walla.sort_values(by=['Année', 'Mois', 'Catégorie'], inplace=True)

# Calculer la variation mensuelle pour chaque catégorie
# Créer un groupe pour chaque catégorie
grouped = walla.groupby('Catégorie')

# Créer un DataFrame vide pour les résultats
result = pd.DataFrame()

for name, group in grouped:
    # Calculer la variation pour le groupe actuel
    group = group.sort_values(by=['Année', 'Mois'])
    for column in group.select_dtypes(include=['number']).columns:
        if 'Année' not in column and 'Mois' not in column:  # Ignorer les colonnes Année et Mois pour le calcul
            # Calculer la variation en pourcentage et remplacer inf par 0
            group[f'var_{column}'] = (group[column].pct_change().replace([float('inf'), -float('inf'), float('nan')], 0) * 100).apply(lambda x: f"{x:.1f}%")
    #group[f'var_{column}'].apply(lambda x: f"{x:.2f}%")
    # Ajouter les résultats du groupe au DataFrame des résultats
    result = pd.concat([result, group])

# Remettre les mois dans le format d'origine
inverse_months = {v: k for k, v in months.items()}
result['Mois'] = result['Mois'].map(inverse_months)

# Définir le chemin de sortie pour le fichier Excel
output_file_path = Path("inputcons/Variations_Combined_Details.xlsx")

# Sauvegarder les résultats dans un fichier Excel au chemin spécifié
result.to_excel(output_file_path, index=False)


print(f"Les calculs ont été effectués avec succès et enregistrés dans {excel_file_path}")

# Chemin complet vers le fichier source
file_path = Path("inputcons/Variations_Combined_Details.xlsx")#r"Variations_Combined_Details.xlsx"

# Lire les données du fichier Excel dans un DataFrame pandas
#df = pd.read_excel(file_path)
#print(df)
#####################################################SECONDE PARTIE#############################################################

# Chargement des données à partir du fichier Excel
#file_path =  r"C:\Users\Administrateur\Desktop\Dashboardv001\inputcons\BD.xlsx"
#chemin_court = "inputcons/BD.xlsx"
filepath = Path("inputcons/BD.xlsx")
df = pd.read_excel(filepath) #inventaire2_df.copy()    #-pd.read_excel(output_path)
#print(df)

# Obtenir la liste des mois uniques dans la colonne 'Mois'
#mois_list = df['Mois'].unique()
df['Mois'] = df['Mois'].astype(str)

mois_list = sorted(df['Mois'].unique())



# Créez un dictionnaire de correspondance entre les noms de mois et les numéros de mois
#mois_numeros = {
    #'Janvier': 1, 'Février': 2, 'Mars': 3, 'Avril': 4, 'Mai': 5, 'Juin': 6,
    #'Juillet': 7, 'Août': 8, 'Septembre': 9, 'Octobre': 10, 'Novembre': 11, 'Décembre': 12
#}

# Triez les mois en fonction de leur numéro de mois
#mois_list = sorted(df['Mois'].unique(), key=lambda x: mois_numeros.get(x.lower(), 0))



# Obtenir la liste des années uniques dans la colonne 'Année'
annee_list = df['Années'].unique()
#annee_list = df['Années'].astype(int).unique()


# Obtenir la liste des années uniques dans la colonne 'Année'
categorie_list = df['Catégorie'].unique()

#df = pd.read_excel(output_path)
print(df.head())
# Obtenir la liste des années uniques dans la colonne 'Année'
sous_categorie_list = df['Sous-catégorie'].unique()


#################################################################################################################################################




# Copie de BD dans dif
dif = inventaire2_df.copy()

#df = ddff.copy() 


