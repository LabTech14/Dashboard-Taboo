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


# Liste pour stocker les DataFrames de chaque fichier
data_frames = []


# Parcourir tous les fichiers Excel dans le répertoire
for filename in os.listdir(input_directory):
    if filename.endswith('.xlsx') and not filename.startswith('~$'):
        file_path = os.path.join(input_directory, filename)
        try:
            # Lire le fichier Excel dans un DataFrame
            df = pd.read_excel(file_path)
            # Ajouter le DataFrame à la liste
            data_frames.append(df)
        except PermissionError:
            print(f"Ignoré : {filename} (Fichier verrouillé)")

# Concaténer les DataFrames en un seul DataFrame
consolidated_df = pd.concat(data_frames, ignore_index=True)


inventaire2_df = consolidated_df 

# Renommer la colonne "Famille/Produit" en "Item"
inventaire2_df.rename(columns={"Famille/Produit": "Item"}, inplace=True)

# Charger le DataFrame de correspondance
correspondances_df = pd.read_excel(r"correspondances.xlsx")

# Créer les nouvelles colonnes "Catégorie" et "Sous-catégorie"
inventaire2_df["Catégorie"] = ""
inventaire2_df["Sous-catégorie"] = ""

# Remplir les colonnes "Catégorie" et "Sous-catégorie" en utilisant la correspondance
for index, row in inventaire2_df.iterrows():
    item = row["Item"]
    matching_row = correspondances_df[correspondances_df["Item"] == item]
    if not matching_row.empty:
        inventaire2_df.at[index, "Catégorie"] = matching_row["Catégorie"].values[0]
        inventaire2_df.at[index, "Sous-catégorie"] = matching_row["Sous-catégorie"].values[0]

# Remplacer les "NaN" dans la colonne "Total HT" par 0
inventaire2_df["Total HT"].fillna(0, inplace=True)

# Réorganiser les colonnes
column_order = ["Catégorie", "Sous-catégorie", "Item","Qté", "Offert","Offert formule","Total Qté","Total TTC","Coût",
                "Total remise","TTC remisé","Total HT","Mois","Années"]
inventaire2_df = inventaire2_df[column_order]

# Supprimer les lignes commençant par "Total..." ou "TOTAL..."
inventaire2_df = inventaire2_df[~inventaire2_df["Item"].str.startswith("Total", na=False)]
inventaire2_df = inventaire2_df[~inventaire2_df["Item"].str.startswith("TOTAL", na=False)]

# Supprimer les lignes ayant au moins trois NaN
inventaire2_df = inventaire2_df.dropna(thresh=inventaire2_df.shape[1] - 3)

# Supprimer les lignes vides
inventaire2_df = inventaire2_df.dropna(how="all")

# Réinitialiser les index
inventaire2_df.reset_index(drop=True, inplace=True)

# Calculer la somme de Total Qté par Sous-Catégorie
sous_cat_sum = inventaire2_df.groupby('Sous-catégorie')['Total Qté'].transform('sum')

# Calculer la colonne "Quantité Absolue"
inventaire2_df['Quantité Absolue'] = inventaire2_df['Total Qté'] / sous_cat_sum*100

# Calculer la colonne "Quantité Relative"
total_sum = inventaire2_df['Total Qté'].sum()

inventaire2_df['Quantité Relative'] = inventaire2_df['Total Qté'] / sous_cat_sum

# Afficher le DataFrame résultant
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

df = inventaire2_df    #pd.read_excel(file_path)


# Obtenir la liste des mois uniques dans la colonne 'Mois'
#mois_list = df['Mois'].unique()
mois_list = sorted(df['Mois'].unique())
# Créez un dictionnaire de correspondance entre les noms de mois et les numéros de mois
#mois_numeros = {
    #'Janvier': 1, 'Février': 2, 'Mars': 3, 'Avril': 4, 'Mai': 5, 'Juin': 6,
    #'Juillet': 7, 'Août': 8, 'Septembre': 9, 'Octobre': 10, 'Novembre': 11, 'Décembre': 12
#}

# Triez les mois en fonction de leur numéro de mois
#mois_list = sorted(df['Mois'].unique(), key=lambda x: mois_numeros.get(x.lower(), 0))



# Obtenir la liste des années uniques dans la colonne 'Année'
#annee_list = df['Années'].unique()
annee_list = df['Années'].astype(int).unique()


# Obtenir la liste des années uniques dans la colonne 'Année'
categorie_list = df['Catégorie'].unique()

# Obtenir la liste des années uniques dans la colonne 'Année'
sous_categorie_list = df['Sous-catégorie'].unique()


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

print(f"Les calculs ont été effectués avec succès et enregistrés dans {excel_file_path}")



#################################################################################################################################################

########################################### Fonctions pour générer les visualisations des KPIs ##################################################
import plotly.graph_objects as go

def generate_pie_chart_weight_on_revenue(filtered_df):
    df_category_revenue = filtered_df.groupby('Catégorie')['Total HT'].sum().reset_index()
    total_revenue = df_category_revenue['Total HT'].sum()

    df_category_revenue['Poids'] = df_category_revenue['Total HT'] / total_revenue

    df_category_revenue['Valeur Absolue'] = df_category_revenue['Total HT']

    # Trouver l'indice de la part la plus petite
    min_index = df_category_revenue['Poids'].idxmin()
    explode = [0.1 if i == min_index else 0 for i in range(len(df_category_revenue))]

    fig = go.Figure(go.Pie(
        labels=df_category_revenue['Catégorie'],
        values=df_category_revenue['Poids'],
        textinfo='label+percent',
        textfont=dict(color='white'),  # Modifier la couleur des étiquettes en blanc
        hovertemplate='<b>%{label}</b><br>Poids : %{percent:.%}<br>Valeur Absolue : %{customdata} FCFA',
        customdata=df_category_revenue['Valeur Absolue'],
        marker=dict(
            colors=['#FF5733', '#FFC300', '#36D7B7', '#3C40C6', '#27AE60', '#F39C12', '#9B59B6', '#D4AC0D', '#E74C3C', '#3498DB']
        ),
        hole=0.4,
        sort=False,
        pull=explode  # Appliquer la fonction d'explosion
    ))

    fig.update_layout(
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )

    return fig




#########    2    ########
#def generate_treemap_item_subcategory(filtered_df):

import plotly.express as px

def generate_treemap_item_subcategory(filtered_df):
    df = filtered_df.copy()
    total_revenue = df['Total HT'].sum()

    df['Poids'] = df['Total HT'] / total_revenue * 100  # Calcul du poids en pourcentage

    fig = px.treemap(df, path=['Catégorie', 'Sous-catégorie'],
                     values='Poids',  # Utilisation des poids calculés
                     color='Sous-catégorie',
                     custom_data=['Poids']  # Stockage des poids dans les données personnalisées
                     )

    fig.update_layout()

    fig.update_traces(
        hovertemplate='<b>%{label}</b><br>Poids: %{customdata[0]:.0f}%',  # Format sans chiffre après la virgule
        textinfo='label+percent entry',  # Affiche le label de la catégorie et le pourcentage
        textposition='middle center',  # Centre l'affichage du texte
        textfont=dict(color='white')  # Couleur des étiquettes en blanc
    )

    return fig




#########    2 b   ########
#def generate_treemap_item_subcategory(filtered_df):


def generate_treemap_subcategory(filtered_df):
    df = filtered_df.copy()
    total_revenue = df['Total HT'].sum()

    df['Poids'] = df['Total HT'] / total_revenue * 100  # Calcul du poids en pourcentage

    fig = px.treemap(df, path=['Catégorie', 'Sous-catégorie','Item'],
                     values='Poids',  # Utilisation des poids calculés
                     color='Sous-catégorie',
                     custom_data=['Poids']  # Stockage des poids dans les données personnalisées
                     )
    fig.update_layout()

    fig.update_traces(
        hovertemplate='<b>%{label}</b><br>Poids: %{value:.0f}%',  # Format avec 2 décimales
        textinfo='label+percent entry',  # Affiche le label de la catégorie et le pourcentage
        textposition='middle center',  # Centre l'affichage du texte
        textfont=dict(color='white')  # Couleur des étiquettes en blanc
    )

    
    return fig


#########    3    ########

def generate_sunburst_item_category(filtered_df):
    fig = go.Figure()

    # Ajouter une trace de barres pour le CA
    bar_trace = go.Bar(x=fina['Mois'], y=fina['CA'], name='Chiffre d\'affaires'.upper())
    fig.add_trace(bar_trace)

    # Ajouter une trace de ligne pour le taux de marge brute avec un axe y secondaire
    line_trace = go.Scatter(x=fina['Mois'], y=fina['Taux marge brute'], mode='lines', yaxis='y2', name='Taux de marge brute'.upper())
    fig.add_trace(line_trace)

    # Ajouter des étiquettes de données pour les barres du chiffre d'affaires
    for i, value in enumerate(fina['CA']):
        fig.add_annotation(
            x=fina['Mois'][i],
            y=value,
            text=f"{value:.0f}",  # Format avec deux décimales
            showarrow=False,
            font=dict(size=12, color="red"),
            yshift=10  # Ajustement vertical
        )

    # Ajouter des étiquettes de données pour la ligne de taux de marge brute
    for i, value in enumerate(fina['Taux marge brute']):
        fig.add_annotation(
            x=fina['Mois'][i],
            y=value,
            text=f"{value:.0%}",  # Format en pourcentage
            showarrow=False,
            font=dict(size=12, color="white"),  # Couleur différente pour se distinguer
            yshift=10  # Ajustement vertical
        )

    # Personnalisation de l'axe y2 (axe de droite)
    fig.update_layout(yaxis2=dict(anchor='x', overlaying='y', side='right'))

    # Personnalisation du titre et des axes
    fig.update_layout(
        title_text='',
        title_x=0.5,
        xaxis_title='Mois'.upper(),
        yaxis_title='Chiffre d\'affaires'.upper(),
        yaxis2_title='Taux de marge brute'.upper()
    )

    # Placer la légende en dessous du graphique
    fig.update_layout(
        legend=dict(
            orientation="h",  # Orientation horizontale pour la légende
            yanchor="bottom",  # Ancre la légende en bas
            y=1.02,  # Ajuste la position verticale pour placer en dessous
            xanchor="right",  # Ancre la légende à droite
            x=1#,  # Centre la légende horizontalement
            #textfont=dict(color='white')
        )
    )

    return fig

#Chiffre d\'affaires et Taux de Marge Brute par mois
    
#########    4 devient 6  ########
def generate_sunburst_subcategory_within_category(filtered_df): 
    # Calcul du total pour chaque mois et normalisation des données
    fina_grouped = fina.groupby('Mois').sum().reset_index()
    total_par_mois = fina_grouped[['CACHETS', 'CASH POWER', 'MARKETING_ADMIN', 'RH', 'CONSOMMABLES', 'Autres']].sum(axis=1)
    for column in ['CACHETS', 'CASH POWER', 'MARKETING_ADMIN', 'RH', 'CONSOMMABLES', 'Autres']:
        fina_grouped[column] = fina_grouped[column] / total_par_mois * 100

    fig = px.bar(fina_grouped, x='Mois', y=['CACHETS', 'CASH POWER', 'MARKETING_ADMIN', 'RH', 'CONSOMMABLES', 'Autres'],
                 title='')

    fig.update_layout(title_text='',
                      title_x=0.5, xaxis_title='Mois'.upper(), yaxis_title='Pourcentage (%)'.upper())

    # Mise à jour de la légende
    for legend_item in fig.data:
        legend_item.name = legend_item.name.upper()

    fig.update_layout(
        legend=dict(
            title_text='',
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        yaxis=dict(range=[0, 100])  # Assurer que l'axe des y va de 0 à 100
    )

    # Calculer et ajouter des annotations pour les pourcentages
    for i, (x_val, y_vals) in enumerate(zip(fina_grouped['Mois'], fina_grouped[['CACHETS', 'CASH POWER', 'MARKETING_ADMIN', 'RH', 'CONSOMMABLES', 'Autres']].values)):
        cumul_y = 0
        for y_val, cat_name in zip(y_vals, ['CACHETS', 'CASH POWER', 'MARKETING_ADMIN', 'RH', 'CONSOMMABLES', 'Autres']):
            cumul_y += y_val / 2
            fig.add_annotation(x=x_val, y=cumul_y,
                               text=f"{y_val:.0f}%",
                               showarrow=False,
                               yshift=10,
                               font=dict(color='white'))  # Définition de la couleur du texte en blanc
            cumul_y += y_val / 2

    return fig

#########    5    ########
def generate_bar_weight_on_revenue(filtered_df):
    fina['Profitabilité'] = fina['Resultat net'] / fina['CA']

    colors = px.colors.qualitative.Set1  # Changer Set1 à une autre palette de couleurs si désiré

    fig = go.Figure()

    # Ajouter une trace de barres pour la Profitabilité
    bar_trace = go.Bar(x=fina['Mois'], y=fina['Profitabilité'], name='Rentabilité'.upper(), marker_color=colors[0])
    fig.add_trace(bar_trace)

    # Ajouter une trace de ligne pour le Taux marge brute avec un axe y secondaire
    line_trace = go.Scatter(x=fina['Mois'], y=fina['Taux marge brute'], mode='lines', yaxis='y2', name='Taux marge brute'.upper(), line=dict(color=colors[1]))
    fig.add_trace(line_trace)

    # Ajouter des étiquettes de données sur les barres
    for i, value in enumerate(fina['Profitabilité']):
        fig.add_annotation(
            x=fina['Mois'][i],
            y=value,
            text=f"{value:.0%}",  # Format en pourcentage
            showarrow=False,
            font=dict(size=12, color="black"),
            yshift=10  # Ajustement vertical pour éviter que le texte ne soit sur la barre
        )

    # Personnalisation de l'axe y2 (axe de droite)
    fig.update_layout(yaxis2=dict(anchor='x', overlaying='y', side='right'))

    # Personnalisation du titre et des axes
    fig.update_layout(
        title_text='',
        title_x=0.5,
        xaxis_title='Mois'.upper(),
        yaxis_title='Rentabilité'.upper(),
        yaxis2_title='Taux marge brute'.upper()
    )

    # Placer la légende en dessous du graphique
    fig.update_layout(
        legend=dict(
            orientation="h",  # Orientation horizontale pour la légende
            yanchor="bottom",  # Ancre la légende en bas
            y=1.02,  # Ajuste la position verticale pour placer en dessous
            xanchor="right",  # Ancre la légende à droite
            x=1  # Centre la légende horizontalement
        )
    )

    return fig



 #########   6   ########

def generate_box(filtered_df):
    fig = go.Figure()

    categories = ['Coûts des produits vendus', 'Marge brute']

    # Calcul de la somme pour chaque mois et normalisation des valeurs
    total_par_mois = fina[categories].sum(axis=1)
    for category in categories:
        fina[category] = fina[category] / total_par_mois * 100  # Normalisation
        bar_trace = go.Bar(x=fina['Mois'], y=fina[category], name=f'{category}'.upper())
        fig.add_trace(bar_trace)

    # Ajout des étiquettes de pourcentage sur les barres en couleur blanche
    for i, mois in enumerate(fina['Mois']):
        cumul_y = 0  # Cumul des valeurs précédentes pour positionner l'étiquette
        for category in categories:
            value = fina.at[i, category]
            y_position = cumul_y + value / 2  # Position centrale de la barre actuelle
            if value > 10:  # Si la valeur est assez grande, mettre l'étiquette à l'intérieur
                text_position = 'inside'
            else:  # Sinon, mettre l'étiquette à l'extérieur
                text_position = 'outside'
                y_position = cumul_y + value  # Ajustement de la position y pour l'étiquette externe

            if value != 0:  # Afficher l'étiquette seulement si la valeur n'est pas nulle
                fig.add_annotation(
                    x=mois,
                    y=y_position,
                    text=f"{value:.1f}%",
                    showarrow=False,
                    font=dict(size=12, color="white"),
                    textangle=0,
                    xshift=0,
                    yshift=0 if text_position == 'inside' else 10,  # Décaler légèrement vers le haut si à l'extérieur
                    align='center',
                    valign='middle'
                )

            cumul_y += value

    # Personnalisation du titre et des axes
    fig.update_layout(
        title_text='',  # Coûts des produits vendus et Marge brute
        title_x=0.5,
        xaxis_title='Mois'.upper(),
        yaxis_title='Pourcentage (%)'.upper(),
        barmode='stack',  # Mode de barres empilées
        yaxis=dict(range=[0, 100])  # Assurer que l'axe des y va de 0 à 100
    )

    # Placer la légende en dessous du graphique
    fig.update_layout(
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )

    return fig


#########    7    ########
def generate(filtered_df):
#def generate_clustered_bar_chart(filtered_df):
    fig = go.Figure()

    # Ajouter une trace de barres groupées pour le chiffre d'affaires et le coût des produits vendus
    #trace1 = go.Bar(x=fina['Mois'], y=fina['Coûts des produits vendus'], name='Coûts des produits vendus'.upper())
    trace2 = go.Bar(x=fina['Mois'], y=fina['CA'], name='Chiffre d\'affaires'.upper())
    fig.add_traces([trace2])#trace1, 

    # Personnalisation du titre et des axes
    fig.update_layout(title_text='',  # Titre du graphique
                      title_x=0.5,  # Position du titre
                      xaxis_title='Mois'.upper(),  # Titre de l'axe des x
                      yaxis_title='Montant'.upper())  # Titre de l'axe des y

    # Utiliser le mode "group" au lieu de "stack"
    fig.update_layout(barmode='group')

    # Ajout des étiquettes de pourcentage
    for trace in fig.data:
        y_values = trace.y
        for index, value in enumerate(y_values):
            # Calcul du pourcentage pour chaque segment de la barre
            total =  trace2.y[index]#trace1.y[index] +
            percentage = (value / total * 100) if total != 0 else 0
            fig.add_annotation(
                x=trace.x[index],
                y=value,
                text=f"{percentage:.1f}%",
                showarrow=False,
                font=dict(size=12, color="black")
            )

    # Placer la légende en dessous du graphique
    fig.update_layout(
        legend=dict(
            orientation="h",  # Orientation horizontale pour la légende
            yanchor="bottom",  # Ancre la légende en bas
            y=1.02,  # Ajuste la position verticale pour placer en dessous
            xanchor="right",  # Ancre la légende à droite
            x=1  # Centre la légende horizontalement
        )
    )

    return fig


#########    8   ########
#def generate_(filtered_df):
#    fina_grouped = fina.groupby('Mois').sum().reset_index()
#    fig = px.box(fina_grouped, x='Mois', y=['Tresorerie net d\'exploitation', 'Tresorerie net d\'investissement'],
#                 title='Évolution des Flux de Trésorerie')

#    fig.update_layout(
#        xaxis=dict(title='Mois'),
#        yaxis=dict(title='Montant'),
#        legend_title='Catégorie'
#    )

#    return fig

def generate_(filtered_df):
    fig = go.Figure()

    categories = ['DRINKS', 'EATS', 'SMOKE']

    for category in categories:
        relative_values = fina[category] / fina[categories].sum(axis=1) * 100
        fig.add_trace(go.Scatter(x=fina['Mois'], y=fina[category], name=category.upper()))
        bar_trace = go.Bar(x=fina['Mois'], y=fina[category], name=f'{category}'.upper())
        fig.add_trace(bar_trace)

        for i, value in enumerate(relative_values):
            bar_trace.hoverinfo = 'y+text'
            fig.add_trace(go.Scatter(
                x=[fina['Mois'][i]],
                y=[fina[category][i]],
                mode='markers',
                marker=dict(size=1),
                text=[f"{value:.2f}%"],
                hoverinfo='text',
                showlegend=False
            ))


    # Personnalisation du titre et des axes
    fig.update_layout(title_text='', title_x=0.5, xaxis_title='Mois'.upper(), yaxis_title='Montant / Pourcentage')

    # Placer la légende en dessous du graphique
    fig.update_layout(
        legend=dict(
            orientation="h",  # Orientation horizontale pour la légende
            yanchor="bottom",  # Ancre la légende en bas
            y=1.02,  # Ajuste la position verticale pour placer en dessous
            xanchor="right",  # Ancre la légende à droite
            x=1  # Centre la légende horizontalement
        )
    )

    return fig







################################################ 9 #################################################################

def total_revenue(filtered_df):
    fina_grouped = fina.groupby('Mois').sum().reset_index()
    fig = px.bar(fina_grouped, x='Mois', y=['Tresorerie net d\'exploitation', 'Tresorerie net d\'investissement'],
                 title='')  # Évolution des Flux de Trésorerie

    fig.update_layout(
        barmode='relative',  # Afficher les barres relatives aux valeurs positives et négatives
        bargap=0.1,  # Espacement entre les groupes de barres
        xaxis=dict(title='Mois'.upper()),
        yaxis=dict(title='Montant'.upper()),
        legend=dict(orientation="h"),  # Placer la légende en dessous
        legend_title=''.upper()
    )

    # Placer la légende en dessous du graphique sans titre
    fig.update_layout(
        legend=dict(
            title_text='',  # Enlever le titre de la légende
            orientation="h",  # Orientation horizontale pour la légende
            yanchor="bottom",  # Ancre la légende en bas
            y=1.02,  # Ajuste la position verticale pour placer en dessous
            xanchor="right",  # Ancre la légende à droite
            x=1  # Centre la légende horizontalement
        )
    )

    # Mettre la légende en majuscules
    for legend_item in fig.data:
        legend_item.name = legend_item.name.upper()

    # Ajout des étiquettes de pourcentage
    for i, bar in enumerate(fig.data):
        for index, value in enumerate(bar.y):
            percentage = value / sum(bar.y) * 100 if sum(bar.y) != 0 else 0
            fig.add_annotation(
                x=bar.x[index],
                y=value / 2,
                text=f"{percentage:.1f}%",
                showarrow=False,
                font=dict(size=12, color="white"),
            )

    return fig


################################################ 10 #################################################################

def create_stacked_bar_chart(filtered_df):
    # Calcul des pourcentages
    fina['Taux DRINKS'] = fina['DRINKS'] / fina['CA'].replace(0, 1)
    fina['Taux EATS'] = fina['EATS'] / fina['CA'].replace(0, 1)
    fina['Taux SMOKE'] = fina['SMOKE'] / fina['CA'].replace(0, 1)
    fina['Profitabilité'] = fina['Resultat net'] / fina['CA'].replace(0, 1)

    # Normaliser les pourcentages pour qu'ils totalisent 100%
    total = fina[['Taux DRINKS', 'Taux EATS', 'Taux SMOKE']].sum(axis=1)
    fina['Taux DRINKS'] /= total
    fina['Taux EATS'] /= total
    fina['Taux SMOKE'] /= total

    # Création du graphique
    fig = px.bar(fina, x="Mois", y=["Taux DRINKS", "Taux EATS", "Taux SMOKE"],
                 title="",  # Taux DRINKS, EATS, SMOKE
                 labels={"value": "Taux", "variable": ""},
                 color_discrete_map={"Taux DRINKS": "blue", "Taux EATS": "green", "Taux SMOKE": "red"},
                 barmode="relative")  # Utilisation de barmode "relative" pour empiler les taux

    # Mise à jour de la mise en page
    fig.update_layout(legend=dict(orientation="h"),
                      xaxis_title="Mois".upper(),
                      yaxis_title="Taux")

    # Ajout des annotations pour chaque barre
    for i, (x_val, y_vals) in enumerate(zip(fina['Mois'], fina[["Taux DRINKS", "Taux EATS", "Taux SMOKE"]].values)):
        cumul_y = 0  # Cumul des valeurs précédentes pour positionner correctement l'étiquette
        for y_val, cat_name in zip(y_vals, ["DRINKS", "EATS", "SMOKE"]):
            percentage = y_val * 100  # Convertir en pourcentage
            y_position = cumul_y + y_val / 2  # Position à mi-hauteur de la barre actuelle
            if percentage < 10:  # Si la valeur est petite, positionner l'étiquette à l'extérieur
                y_position = cumul_y + y_val
                y_shift = 10
            else:
                y_shift = 0

            fig.add_annotation(x=x_val, y=y_position,
                               text=f"{percentage:.0f}%",  # Format sans décimale
                               showarrow=False,
                               font=dict(size=12, color="white"),  # Couleur du texte en blanc
                               yshift=y_shift)
            cumul_y += y_val  # Ajouter la valeur de la barre actuelle

    # Ajout de la profitabilité comme une ligne séparée
    fig.add_trace(go.Scatter(x=fina['Mois'], y=fina['Profitabilité'], mode='lines+markers',
                             name='Profitabilité', yaxis='y2'))

    # Mise à jour du layout pour la profitabilité
    fig.update_layout(yaxis2=dict(title='Profitabilité', overlaying='y', side='right'))

    return fig




################################################## Autre ##############################################################
def generate_bar_chart_revenue_by_month(df):
    # Calculer le chiffre d'affaires mensuel par catégorie
    df_monthly_revenue = df.groupby(['Mois', 'Catégorie'])['Total HT'].sum().reset_index()

    # Calculer le pourcentage par catégorie
    df_monthly_revenue['Poids'] = df_monthly_revenue.groupby('Mois')['Total HT'].transform(lambda x: x / x.sum() * 100)

    # Définir l'ordre des mois
    ordered_months = ['Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin', 'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre']

    # Initialiser la figure
    fig = go.Figure()

    # Obtenir les catégories uniques et les couleurs
    catégories = df_monthly_revenue['Catégorie'].unique()
    couleurs = ['#FF5733', '#FFC300', '#36D7B7', '#3C40C6', '#27AE60', '#F39C12', '#9B59B6', '#D4AC0D', '#E74C3C', '#3498DB']

    for catégorie, couleur in zip(catégories, couleurs):
        # Filtrer les données pour la catégorie actuelle
        category_data = df_monthly_revenue[df_monthly_revenue['Catégorie'] == catégorie]

        # Utiliser l'ordre des mois
        category_data['Mois'] = pd.Categorical(category_data['Mois'], categories=ordered_months, ordered=True)
        category_data = category_data.sort_values('Mois')

        # Normaliser les valeurs pour représenter des pourcentages
        category_data['Normalized'] = category_data['Poids'] / 100

        # Ajouter la trace de la barre à la figure
        fig.add_trace(go.Bar(
            x=category_data['Mois'],
            y=category_data['Normalized'],
            name=catégorie,
            marker=dict(color=couleur),
            text=category_data['Poids'].astype(int).astype(str) + '%',
            textposition='auto',
            hoverinfo='text+y',
            showlegend=True,
            textfont=dict(color='white')
        ))

    # Mettre à jour la mise en page de la figure
    fig.update_layout(
        barmode='stack',
        xaxis=dict(title='Mois'),
        yaxis=dict(title='Pourcentage'),
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=1.02,
            xanchor='right',
            x=1
        ),
        # title='Chiffre d\'affaires mensuelles par catégorie',
    )

    # Retourner la figure
    return fig




##################################################################### new graph #######################################################
# Charger les données depuis le fichier Excel
file_path = "inputcons/Combined_Details.xlsx"
graph = pd.read_excel(file_path)

categories = ['DRINK', 'EAT', 'SMOKE']
def generate_combined_bar_chart(file_path, categories):
    # Charger les données depuis le fichier Excel
    graph = pd.read_excel(file_path)

    # Filtrer les données pour les catégories spécifiées
    filtered_data = graph[graph['Catégorie'].isin(categories)]

    # Définir l'ordre des mois de manière appropriée
    ordered_months = ['Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin', 'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre']
    filtered_data['Mois'] = pd.Categorical(filtered_data['Mois'], categories=ordered_months, ordered=True)

    # Trier le DataFrame par la colonne 'Mois'
    filtered_data.sort_values('Mois', inplace=True)

    # Créer un graphique en barres combinées avec l'étiquette de données
    fig = px.bar(filtered_data, x='Mois', y='Taux Opex', color='Catégorie', text='Taux Opex',
                 title='Taux Opex par Catégorie',
                 labels={'Taux Opex': 'Taux Opex', 'Catégorie': 'Catégorie'})

    # Personnalisation du style du titre
    fig.update_layout(title_text='',
                      title_x=0.5, xaxis_title='Mois', yaxis_title='Taux Opex')

    # Placer l'étiquette de données à l'intérieur des barres
    fig.update_traces(textposition='inside')

    # Placer la légende en dessous du graphique sans titre
    fig.update_layout(
        legend=dict(
            title_text='',  # Enlever le titre de la légende
            orientation="h",  # Orientation horizontale pour la légende
            yanchor="bottom",  # Ancre la légende en bas
            y=1.02,  # Ajuste la position verticale pour placer en dessous
            xanchor="right",  # Ancre la légende à droite
            x=1  # Centre la légende horizontalement
        )
    )

    return fig

####################################################################################################################################################
def generate_combined_bar_chart1(file_path, categories):
    # Charger les données depuis le fichier Excel
    graph = pd.read_excel(file_path)

    # Filtrer les données pour les catégories spécifiées
    filtered_data = graph[graph['Catégorie'].isin(categories)]

    # Définir l'ordre des mois de manière appropriée
    ordered_months = ['Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin', 'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre']
    filtered_data['Mois'] = pd.Categorical(filtered_data['Mois'], categories=ordered_months, ordered=True)

    # Trier le DataFrame par la colonne 'Mois'
    filtered_data.sort_values('Mois', inplace=True)

    # Créer un graphique en barres combinées avec l'étiquette de données
    fig = px.bar(filtered_data, x='Mois', y='Rentabilite', color='Catégorie', text='Rentabilite',
                 title='Rentabilité par Catégorie',
                 labels={'Rentabilite': 'Rentabilité', 'Catégorie': 'Catégorie'})

    # Personnalisation du style du titre
    fig.update_layout(title_text='',
                      title_x=0.5, xaxis_title='Mois', yaxis_title='Rentabilité')

    # Placer l'étiquette de données à l'intérieur des barres
    fig.update_traces(textposition='inside')

    # Placer la légende en dessous du graphique sans titre
    fig.update_layout(
        legend=dict(
            title_text='',  # Enlever le titre de la légende
            orientation="h",  # Orientation horizontale pour la légende
            yanchor="bottom",  # Ancre la légende en bas
            y=1.02,  # Ajuste la position verticale pour placer en dessous
            xanchor="right",  # Ancre la légende à droite
            x=1  # Centre la légende horizontalement
        )
    )

    return fig
###############################################################################################################################################
def generate_combined_bar_chart2(file_path, categories):
    # Charger les données depuis le fichier Excel
    graph = pd.read_excel(file_path)

    # Filtrer les données pour les catégories spécifiées
    filtered_data = graph[graph['Catégorie'].isin(categories)]

    # Définir l'ordre des mois de manière appropriée
    ordered_months = ['Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin', 'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre']
    filtered_data['Mois'] = pd.Categorical(filtered_data['Mois'], categories=ordered_months, ordered=True)

    # Trier le DataFrame par la colonne 'Mois'
    filtered_data.sort_values('Mois', inplace=True)

    # Créer un graphique en barres combinées avec l'étiquette de données
    fig = px.bar(filtered_data, x='Mois', y='Taux Coût des produits vendus', color='Catégorie', text='Taux Coût des produits vendus',
                 title='Taux Coût des produits vendus par Catégorie',
                 labels={'Taux Coût des produits vendus': 'Taux Coût des produits vendus', 'Catégorie': 'Catégorie'})

    # Personnalisation du style du titre
    fig.update_layout(title_text='',
                      title_x=0.5, xaxis_title='Mois', yaxis_title='Taux Coût des produits vendus')

    # Placer l'étiquette de données à l'intérieur des barres
    fig.update_traces(textposition='inside')

    # Placer la légende en dessous du graphique sans titre
    fig.update_layout(
        legend=dict(
            title_text='',  # Enlever le titre de la légende
            orientation="h",  # Orientation horizontale pour la légende
            yanchor="bottom",  # Ancre la légende en bas
            y=1.02,  # Ajuste la position verticale pour placer en dessous
            xanchor="right",  # Ancre la légende à droite
            x=1  # Centre la légende horizontalement
        )
    )

    return fig
#################################################################################################################################################
def generate_combined_bar_chart3(file_path, categories):
    # Charger les données depuis le fichier Excel
    graph = pd.read_excel(file_path)

    # Filtrer les données pour les catégories spécifiées
    filtered_data = graph[graph['Catégorie'].isin(categories)]

    # Définir l'ordre des mois de manière appropriée
    ordered_months = ['Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin', 'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre']
    filtered_data['Mois'] = pd.Categorical(filtered_data['Mois'], categories=ordered_months, ordered=True)

    # Trier le DataFrame par la colonne 'Mois'
    filtered_data.sort_values('Mois', inplace=True)

    # Créer un graphique en barres combinées avec l'étiquette de données
    fig = px.bar(filtered_data, x='Mois', y='Taux Marge brute', color='Catégorie', text='Taux Marge brute',
                 title='Taux Marge brute par Catégorie',
                 labels={'Taux Marge brute': 'Taux Marge brute', 'Catégorie': 'Catégorie'})

    # Personnalisation du style du titre
    fig.update_layout(title_text='',
                      title_x=0.5, xaxis_title='Mois', yaxis_title='Taux Marge brute')

    # Placer l'étiquette de données à l'intérieur des barres
    fig.update_traces(textposition='inside')

    # Placer la légende en dessous du graphique sans titre
    fig.update_layout(
        legend=dict(
            title_text='',  # Enlever le titre de la légende
            orientation="h",  # Orientation horizontale pour la légende
            yanchor="bottom",  # Ancre la légende en bas
            y=1.02,  # Ajuste la position verticale pour placer en dessous
            xanchor="right",  # Ancre la légende à droite
            x=1  # Centre la légende horizontalement
        )
    )

    return fig

#################################################################################################################################################

def generate_eat_graph(graph):
    # Filtrer les données pour la catégorie EAT
    eat_data = graph[graph['Catégorie'] == 'EAT'].copy()

    # Définir l'ordre des mois
    ordered_months = ['Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin', 'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre']
    eat_data['Mois'] = pd.Categorical(eat_data['Mois'], categories=ordered_months, ordered=True)

    # Ordonner les données par mois
    eat_data.sort_values('Mois', inplace=True)

    # Remodeler les données
    eat_data = pd.melt(eat_data, id_vars=['Mois'], value_vars=['Taux Coût des produits vendus', 'Rentabilite'],
                       var_name='Taux', value_name='Valeur')

    # S'assurer que les valeurs sont des nombres et non des chaînes
    eat_data['Valeur'] = eat_data['Valeur'].replace('%', '', regex=True).astype(float)

    # Créer un graphique en barres groupées
    fig = px.bar(eat_data, x='Mois', y='Valeur', color='Taux', barmode='group',
                 title='Taux Coût des produits vendus et Rentabilité pour la catégorie EAT',
                 text='Valeur', labels={'Valeur': 'Taux'},
                 color_discrete_map={'Taux Coût des produits vendus': 'blue', 'Rentabilite': 'red'})

    # Personnalisation du style du titre
    fig.update_layout(title_text='', title_x=0.5, xaxis_title='Mois', yaxis_title='Taux (%)')

    # Mise à jour de la légende
    for legend_item in fig.data:
        legend_item.name = legend_item.name.upper()

    # Placer la légende en dessous du graphique sans titre
    fig.update_layout(
        legend=dict(
            title_text='',
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )

    # Centrer les étiquettes de données sur les barres
    #fig.update_traces(textposition='inside')
    # Mettre les étiquettes de données en blanc et sans chiffre après la virgule
    fig.update_traces(textposition='inside', textfont=dict(color='white'))

    return fig


#############################################################################################################################""""""
def generate_drink_graph(graph):
    # Filtrer les données pour la catégorie DRINK
    drink_data = graph[graph['Catégorie'] == 'DRINK'].copy()

    # Définir l'ordre des mois
    ordered_months = ['Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin', 'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre']
    drink_data['Mois'] = pd.Categorical(drink_data['Mois'], categories=ordered_months, ordered=True)

    # Ordonner les données par mois
    drink_data.sort_values('Mois', inplace=True)

    # Remodeler les données
    drink_data = pd.melt(drink_data, id_vars=['Mois'], value_vars=['Taux Coût des produits vendus', 'Rentabilite'],
                         var_name='Taux', value_name='Valeur')

    # Convertir les pourcentages en nombres flottants
    drink_data['Valeur'] = drink_data['Valeur'].replace('%', '', regex=True).astype(float)

    # Créer un graphique en barres groupées avec des couleurs personnalisées
    fig = px.bar(drink_data, x='Mois', y='Valeur', color='Taux', barmode='group',
                 title='Taux Coût des produits vendus et Rentabilité pour la catégorie DRINK',
                 text='Valeur', labels={'Valeur': 'Taux'},
                 color_discrete_map={'Taux Coût des produits vendus': 'orange', 'Rentabilite': 'green'})

    # Personnalisation du style du titre
    fig.update_layout(title_text='', title_x=0.5, xaxis_title='Mois', yaxis_title='Taux (%)')

    # Mise à jour de la légende
    for legend_item in fig.data:
        legend_item.name = legend_item.name.upper()

    # Placer la légende en dessous du graphique sans titre
    fig.update_layout(
        legend=dict(
            title_text='',
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )

    # Mettre les étiquettes de données en blanc et sans chiffre après la virgule
    fig.update_traces(textposition='inside', textfont=dict(color='white'))

    return fig


#################################################################################################################################




# Charger les données depuis le fichier Excel

def generate_smoke_graph(graph):
    # Filtrer les données pour la catégorie EAT
    smoke_data = graph[graph['Catégorie'] == 'SMOKE'].copy()  # Utiliser .copy() pour éviter le avertissement

    # Définir l'ordre des mois
    ordered_months = ['Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin', 'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre']
    smoke_data['Mois'] = pd.Categorical(smoke_data['Mois'], categories=ordered_months, ordered=True)

    # Ordonner les données par mois
    smoke_data.sort_values('Mois', inplace=True)

    # Remodeler les données
    smoke_data = pd.melt(smoke_data, id_vars=['Mois'], value_vars=['Taux Coût des produits vendus', 'Rentabilite'],
                         var_name='Taux', value_name='Valeur')

    # Convertir les pourcentages en nombres flottants
    smoke_data['Valeur'] = smoke_data['Valeur'].replace('%', '', regex=True).astype(float)

    # Créer un graphique en barres groupées avec des couleurs personnalisées
    fig = px.bar(smoke_data, x='Mois', y='Valeur', color='Taux', barmode='group',
                 title='Taux Coût des produits vendus et Rentabilité pour la catégorie SMOKE',
                 text='Valeur', labels={'Valeur': 'Taux'},
                 color_discrete_map={'Taux Coût des produits vendus': 'purple', 'Rentabilite': 'gold'})

    # Personnalisation du style du titre
    fig.update_layout(title_text='', title_x=0.5, xaxis_title='Mois', yaxis_title='Taux (%)')

    # Mise à jour de la légende
    for legend_item in fig.data:
        legend_item.name = legend_item.name.upper()

    # Placer la légende en dessous du graphique sans titre
    fig.update_layout(
        legend=dict(
            title_text='',
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )

    # Mettre les étiquettes de données en blanc et sans chiffre après la virgule
    fig.update_traces(textposition='inside', textfont=dict(color='white'))

    return fig

#############################################################################################################################################

def generat_eat_graph(graph):
    # Filtrer les données pour la catégorie EAT ['Taux Marge brute', 'Rentabilite']
    eat_data = graph[graph['Catégorie'] == 'EAT'].copy()  # Utiliser .copy() pour éviter le avertissement

    # Définir l'ordre des mois
    ordered_months = ['Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin', 'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre']
    eat_data['Mois'] = pd.Categorical(eat_data['Mois'], categories=ordered_months, ordered=True)

    # Ordonner les données par mois
    eat_data.sort_values('Mois', inplace=True)

    # Remodeler les données
    eat_data = pd.melt(eat_data, id_vars=['Mois'], value_vars=['Taux Marge brute', 'Rentabilite'],
                       var_name='Taux', value_name='Valeur')

    # S'assurer que les valeurs sont des nombres et non des chaînes
    eat_data['Valeur'] = eat_data['Valeur'].replace('%', '', regex=True).astype(float)

    # Créer un graphique en barres groupées
    fig = px.bar(eat_data, x='Mois', y='Valeur', color='Taux', barmode='group',
                 title='Taux Marge brute et Rentabilité pour la catégorie EAT',
                 text='Valeur', labels={'Valeur': 'Taux'},
                 color_discrete_map={'Taux Marge brute': 'blue', 'Rentabilite': 'red'})

    # Personnalisation du style du titre
    fig.update_layout(title_text='', title_x=0.5, xaxis_title='Mois', yaxis_title='Taux (%)')

    # Mise à jour de la légende
    for legend_item in fig.data:
        legend_item.name = legend_item.name.upper()

    # Placer la légende en dessous du graphique sans titre
    fig.update_layout(
        legend=dict(
            title_text='',
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )

    # Centrer les étiquettes de données sur les barres
    #fig.update_traces(textposition='inside')
    fig.update_traces(textposition='inside', textfont=dict(color='white'))

    return fig
#############################################################################################################################""""""

def generat_drink_graph(graph):
    # Filtrer les données pour la catégorie DRINK
    drink_data = graph[graph['Catégorie'] == 'DRINK'].copy()  # Utiliser .copy() pour éviter le avertissement

    # Définir l'ordre des mois
    ordered_months = ['Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin', 'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre']
    drink_data['Mois'] = pd.Categorical(drink_data['Mois'], categories=ordered_months, ordered=True)

    # Ordonner les données par mois
    drink_data.sort_values('Mois', inplace=True)

    # Remodeler les données
    drink_data = pd.melt(drink_data, id_vars=['Mois'], value_vars=['Taux Marge brute', 'Rentabilite'],
                         var_name='Taux', value_name='Valeur')

    # Convertir les pourcentages en nombres flottants
    drink_data['Valeur'] = drink_data['Valeur'].replace('%', '', regex=True).astype(float)

    # Créer un graphique en barres groupées avec des couleurs personnalisées
    fig = px.bar(drink_data, x='Mois', y='Valeur', color='Taux', barmode='group',
                 title='Taux Marge brute et Rentabilité pour la catégorie DRINK',
                 text='Valeur', labels={'Valeur': 'Taux'},
                 color_discrete_map={'Taux Marge brute': 'orange', 'Rentabilite': 'green'})

    # Personnalisation du style du titre
    fig.update_layout(title_text='', title_x=0.5, xaxis_title='Mois', yaxis_title='Taux (%)')

    # Mise à jour de la légende
    for legend_item in fig.data:
        legend_item.name = legend_item.name.upper()

    # Placer la légende en dessous du graphique sans titre
    fig.update_layout(
        legend=dict(
            title_text='',
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )

    # Mettre les étiquettes de données en blanc et sans chiffre après la virgule
    fig.update_traces(textposition='inside', textfont=dict(color='white'))

    return fig
#################################################################################################################################

def generat_smoke_graph(graph):
    # Filtrer les données pour la catégorie EAT
    smoke_data = graph[graph['Catégorie'] == 'SMOKE'].copy()  # Utiliser .copy() pour éviter le avertissement

    # Définir l'ordre des mois
    ordered_months = ['Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin', 'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre']
    smoke_data['Mois'] = pd.Categorical(smoke_data['Mois'], categories=ordered_months, ordered=True)

    # Ordonner les données par mois
    smoke_data.sort_values('Mois', inplace=True)

    # Remodeler les données
    smoke_data = pd.melt(smoke_data, id_vars=['Mois'], value_vars=['Taux Marge brute', 'Rentabilite'],
                         var_name='Taux', value_name='Valeur')

    # Convertir les pourcentages en nombres flottants
    smoke_data['Valeur'] = smoke_data['Valeur'].replace('%', '', regex=True).astype(float)

    # Créer un graphique en barres groupées avec des couleurs personnalisées
    fig = px.bar(smoke_data, x='Mois', y='Valeur', color='Taux', barmode='group',
                 title='Taux Marge brute et Rentabilité pour la catégorie SMOKE',
                 text='Valeur', labels={'Valeur': 'Taux'},
                 color_discrete_map={'Taux Marge brute': 'purple', 'Rentabilite': 'gold'})

    # Personnalisation du style du titre
    fig.update_layout(title_text='', title_x=0.5, xaxis_title='Mois', yaxis_title='Taux (%)')

    # Mise à jour de la légende
    for legend_item in fig.data:
        legend_item.name = legend_item.name.upper()

    # Placer la légende en dessous du graphique sans titre
    fig.update_layout(
        legend=dict(
            title_text='',
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )

    # Mettre les étiquettes de données en blanc et sans chiffre après la virgule
    fig.update_traces(textposition='inside', textfont=dict(color='white'))

    return fig
#############################################################################################################################################

def genera_eat_graph(graph):
    # Filtrer les données pour la catégorie EAT Taux Opex
    eat_data = graph[graph['Catégorie'] == 'EAT'].copy()  # Utiliser .copy() pour éviter le avertissement

    # Définir l'ordre des mois
    ordered_months = ['Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin', 'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre']
    eat_data['Mois'] = pd.Categorical(eat_data['Mois'], categories=ordered_months, ordered=True)

    # Ordonner les données par mois
    eat_data.sort_values('Mois', inplace=True)

    # Remodeler les données
    eat_data = pd.melt(eat_data, id_vars=['Mois'], value_vars=['Taux Opex', 'Rentabilite'],
                       var_name='Taux', value_name='Valeur')

    # S'assurer que les valeurs sont des nombres et non des chaînes
    eat_data['Valeur'] = eat_data['Valeur'].replace('%', '', regex=True).astype(float)

    # Créer un graphique en barres groupées
    fig = px.bar(eat_data, x='Mois', y='Valeur', color='Taux', barmode='group',
                 title='Taux Opex et Rentabilité pour la catégorie EAT',
                 text='Valeur', labels={'Valeur': 'Taux'},
                 color_discrete_map={'Taux Opex': 'blue', 'Rentabilite': 'red'})

    # Personnalisation du style du titre
    fig.update_layout(title_text='', title_x=0.5, xaxis_title='Mois', yaxis_title='Taux (%)')

    # Mise à jour de la légende
    for legend_item in fig.data:
        legend_item.name = legend_item.name.upper()

    # Placer la légende en dessous du graphique sans titre
    fig.update_layout(
        legend=dict(
            title_text='',
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )

    # Centrer les étiquettes de données sur les barres
    #fig.update_traces(textposition='inside')
    fig.update_traces(textposition='inside', textfont=dict(color='white'))

    return fig
#############################################################################################################################""""""

def genera_drink_graph(graph):
    # Filtrer les données pour la catégorie DRINK
    drink_data = graph[graph['Catégorie'] == 'DRINK'].copy()  # Utiliser .copy() pour éviter le avertissement

    # Définir l'ordre des mois
    ordered_months = ['Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin', 'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre']
    drink_data['Mois'] = pd.Categorical(drink_data['Mois'], categories=ordered_months, ordered=True)

    # Ordonner les données par mois
    drink_data.sort_values('Mois', inplace=True)

    # Remodeler les données
    drink_data = pd.melt(drink_data, id_vars=['Mois'], value_vars=['Taux Opex', 'Rentabilite'],
                         var_name='Taux', value_name='Valeur')

    # Convertir les pourcentages en nombres flottants
    drink_data['Valeur'] = drink_data['Valeur'].replace('%', '', regex=True).astype(float)

    # Créer un graphique en barres groupées avec des couleurs personnalisées
    fig = px.bar(drink_data, x='Mois', y='Valeur', color='Taux', barmode='group',
                 title='Taux Opex et Rentabilité pour la catégorie DRINK',
                 text='Valeur', labels={'Valeur': 'Taux'},
                 color_discrete_map={'Taux Opex': 'orange', 'Rentabilite': 'green'})

    # Personnalisation du style du titre
    fig.update_layout(title_text='', title_x=0.5, xaxis_title='Mois', yaxis_title='Taux (%)')

    # Mise à jour de la légende
    for legend_item in fig.data:
        legend_item.name = legend_item.name.upper()

    # Placer la légende en dessous du graphique sans titre
    fig.update_layout(
        legend=dict(
            title_text='',
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )

    # Mettre les étiquettes de données en blanc et sans chiffre après la virgule
    fig.update_traces(textposition='inside', textfont=dict(color='white'))

    return fig
#################################################################################################################################

def genera_smoke_graph(graph):
    # Filtrer les données pour la catégorie EAT
    smoke_data = graph[graph['Catégorie'] == 'SMOKE'].copy()  # Utiliser .copy() pour éviter le avertissement

    # Définir l'ordre des mois
    ordered_months = ['Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin', 'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre']
    smoke_data['Mois'] = pd.Categorical(smoke_data['Mois'], categories=ordered_months, ordered=True)

    # Ordonner les données par mois
    smoke_data.sort_values('Mois', inplace=True)

    # Remodeler les données
    smoke_data = pd.melt(smoke_data, id_vars=['Mois'], value_vars=['Taux Opex', 'Rentabilite'],
                         var_name='Taux', value_name='Valeur')

    # Convertir les pourcentages en nombres flottants
    smoke_data['Valeur'] = smoke_data['Valeur'].replace('%', '', regex=True).astype(float)

    # Créer un graphique en barres groupées avec des couleurs personnalisées
    fig = px.bar(smoke_data, x='Mois', y='Valeur', color='Taux', barmode='group',
                 title='Taux Opex et Rentabilité pour la catégorie SMOKE',
                 text='Valeur', labels={'Valeur': 'Taux'},
                 color_discrete_map={'Taux Opex': 'purple', 'Rentabilite': 'gold'})

    # Personnalisation du style du titre
    fig.update_layout(title_text='', title_x=0.5, xaxis_title='Mois', yaxis_title='Taux (%)')

    # Mise à jour de la légende
    for legend_item in fig.data:
        legend_item.name = legend_item.name.upper()

    # Placer la légende en dessous du graphique sans titre
    fig.update_layout(
        legend=dict(
            title_text='',
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )

    # Mettre les étiquettes de données en blanc et sans chiffre après la virgule
    fig.update_traces(textposition='inside', textfont=dict(color='white'))

    return fig
#############################################################################################################################################


# Copie de BD dans dif
dif = inventaire2_df.copy()




################################################ end #################################################################


# Création du tableau de bord
app = dash.Dash(__name__)

# Ajustement de la taille des graphiques Sunburst
sunburst_height = 200

app.layout = html.Div([
    html.Link(
        rel='stylesheet',
        href='https://adminlte.io/themes/v3/plugins/fontawesome-free/css/all.min.css'),    
    html.Link(
        rel='stylesheet',
        href='https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css'),
    html.Link(
        rel='stylesheet',
        href='https://adminlte.io/themes/v3/dist/css/adminlte.min.css?v=3.2.0'),

    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    html.H1("DASHBOARD D'ANALYSE DES DONNEES", className="m-0",
                            style={'font-weight': 'bold', 'font-size': '36px'})  # Ajoutez ici le style CSS pour le gras et la taille de police)
                ], className="col-sm-8"),
                html.Div([
                    html.Ol([
                        html.Li(id='current-time', className="breadcrumb-item active")
                    ], className="breadcrumb float-sm-right")
                ], className="col-sm-4")
            ], className="row mb-2"),
            html.Div([
                html.Div([
                    dcc.Dropdown(id='year-dropdown', options=[{'label': str(annee), 'value': annee} for annee in annee_list],
                                value=None, placeholder="Sélectionnez les années", multi=True)
                ], className='col-md-3'),

                html.Div([
                    dcc.Dropdown(id='month-dropdown', options=[{'label': mois, 'value': mois} for mois in mois_list],
                                value=None, placeholder="Sélectionnez les mois", multi=True)
                ], className='col-md-3'),
                    
                html.Div([
                    dcc.Dropdown(id='categorie-dropdown', options=[{'label': str(categorie), 'value': categorie} for categorie in categorie_list],
                                value=None, placeholder="Sélectionnez les catégories", multi=True)
                ], className='col-md-3'),

                html.Div([
                    dcc.Dropdown(id='sous-categorie-dropdown', options=[{'label': str(sous_categorie), 'value': sous_categorie} for sous_categorie in sous_categorie_list],
                                value=None, placeholder="Sélectionnez les sous catégorie", multi=True)
                ], className='col-md-3'),

            ], className='row mb-3'),

            html.Div(id='revenue-summary')

        ], className="container-fluid")
    ], className="content-header mb-4 pb-1", style={'background-color': '#c2c2c3'} ),

    html.Section([
        html.Div([
            html.Div([
                html.Div(id='visualizations-container'),
            ], className="container-fluid")
        ], className="row"),
    ], className="content"),

    dcc.Interval(id='interval-component', interval=1000, n_intervals=0),  # Rafraîchissement toutes les secondes
], className='content-wrapper', style={'margin-left': '0px', 'min-height': '100vh'})

@app.callback(
    Output('sous-categorie-dropdown', 'options'),
    Input('categorie-dropdown', 'value')
)
def update_sous_categorie_dropdown(selected_categories):
    if selected_categories is None:
        return []
    
    filtered_df = df[df['Catégorie'].isin(selected_categories)]
    sous_categorie_options = [{'label': sous_categorie, 'value': sous_categorie} for sous_categorie in filtered_df['Sous-catégorie'].unique()]
    return sous_categorie_options

@app.callback(
    Output('revenue-summary', 'children'),
    Input('month-dropdown', 'value'),
    Input('year-dropdown', 'value'),
    Input('categorie-dropdown', 'value'),
    Input('sous-categorie-dropdown', 'value'),
    Input('interval-component', 'n_intervals')
)
def update_revenue_summary(selected_months, selected_years, selected_categories, selected_sous_categories, n_intervals):
    if selected_months is None or selected_years is None:
        return html.Div()

    filtered_df = df[df['Années'].isin(selected_years)]
    filtered_df = filtered_df[df['Mois'].isin(selected_months)]
    
    if selected_categories:
        filtered_df = filtered_df[filtered_df['Catégorie'].isin(selected_categories)]
    
    if selected_sous_categories:
        filtered_df = filtered_df[filtered_df['Sous-catégorie'].isin(selected_sous_categories)]

    if filtered_df.empty:
        return html.Div("")

    total_revenue = filtered_df['Total HT'].sum()
    formatted_total_revenue = '{:,.2f}'.format(total_revenue).replace(',', ' ').replace('.', ',') + " FCFA"

    selected_month_names = ', '.join(map(str, selected_months))
    selected_year_names = ', '.join(map(str, selected_years))
    
    if selected_categories:
        selected_categorie_names = ', '.join(selected_categories)
        if selected_sous_categories:
            selected_sous_categorie_names = ', '.join(selected_sous_categories)
            formatted_message = f"Le chiffre d'affaires de(s) sous-catégorie(s) {selected_sous_categorie_names} de(s) catégorie(s) {selected_categorie_names} du mois de {selected_month_names} de l'année {selected_year_names}"
        else:
            formatted_message = f"Le chiffre d'affaires de(s) catégorie(s) {selected_categorie_names} du mois de {selected_month_names} de l'année {selected_year_names}"
    else:
        formatted_message = f"Le chiffre d'affaires du mois de {selected_month_names} de l'année {selected_year_names}"

    return html.Div([
        html.Div([
            html.Div([
                html.H3(f"{formatted_total_revenue}"),
                html.P(f"{formatted_message}", className="mb-0"),
            ], className="inner p-2"),
        ], className="small-box bg-info col-md-12 col-12")
    ], className="")


@app.callback(
    Output('current-time', 'children'),
    Input('interval-component', 'n_intervals')
)
def update_current_time(n_intervals):
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f"Heure actuelle : {current_time}"

@app.callback(
    Output('visualizations-container', 'children'),
    Input('month-dropdown', 'value'),
    Input('year-dropdown', 'value'),
    Input('categorie-dropdown', 'value'),
    Input('sous-categorie-dropdown', 'value')
)
def update_visualizations(selected_months, selected_years, selected_categories, selected_sous_categories):
    if selected_months is None or selected_years is None:
        return html.Div()

    filtered_df = df[df['Années'].isin(selected_years)]
    filtered_df = filtered_df[df['Mois'].isin(selected_months)]
    
    if selected_categories:
        filtered_df = filtered_df[filtered_df['Catégorie'].isin(selected_categories)]
    
    if selected_sous_categories:
        filtered_df = filtered_df[filtered_df['Sous-catégorie'].isin(selected_sous_categories)]

    if filtered_df.empty:
        return html.Div([
            html.Div([
                html.Div([
                    html.Div([
                        html.H1("Aucune données disponibles pour les sélections faites."),
                    ], className="inner p-2"),
                ])
            ], className="small-box bg-danger")
        ], className="col-lg-12 col-12")
    
    # Utilisation des différentes fonctions de génération de graphiques
    fig_pie_chart_weight_on_revenue = generate_pie_chart_weight_on_revenue(filtered_df)#1
    fig0 = generate_bar_chart_revenue_by_month(dif)#2
    fig_treemap_item_subcategory = generate_treemap_item_subcategory(filtered_df)#3
    fig_sunburst_item_category = generate_sunburst_item_category(filtered_df)#5
    fig_sunburst_subcategory_within_category = generate_sunburst_subcategory_within_category(filtered_df)#6
    fig_bar_weight_on_revenue = generate_bar_weight_on_revenue(filtered_df)#10
    fig_box_category_revenue = generate_box(filtered_df)#8
    fig_box_total_revenue = generate(filtered_df)#9
    ###########fig_box_total_revenu = generate_(filtered_df)#7
    fig_total_revenu =  total_revenue(filtered_df)#11
    fig_total = generate_treemap_subcategory(filtered_df)#4
    fig = create_stacked_bar_chart(filtered_df)#12
    eat = generate_eat_graph(graph)
    smoke = generate_smoke_graph(graph)
    drink = generate_drink_graph(graph)
    eat1 = generat_eat_graph(graph)
    drink1 = generat_drink_graph(graph)
    smoke1 = generat_smoke_graph(graph)
    eat2 = genera_eat_graph(graph)
    drink2 = genera_drink_graph(graph)
    smoke2 = genera_smoke_graph(graph)
    opex = generate_combined_bar_chart(file_path, categories)
    Rentabilite = generate_combined_bar_chart1(file_path, categories) 
    tcpv = generate_combined_bar_chart2(file_path, categories) 
    tmb = generate_combined_bar_chart3(file_path, categories) 
    figl = create_sales_dashboard(dfl)


    return html.Div([
                html.Div([
                    html.Div([
                        html.Div([
                            html.H3("Poids de chaque catégorie sur le chiffre d'affaires global".upper(), 
                                    className="card-title",
                                    style={'font-weight': 'bold','font-size': '28px'})  # Ajoutez ici le style CSS pour le gras
                        ], className="card-header"),
                        html.Div([
                            html.Div([
                                html.Div(dcc.Graph(figure=fig_pie_chart_weight_on_revenue.update_layout(margin=dict(t=0, b=0, l=0, r=0)))),
                            ], className="card-body pad table-responsive p-0")
                        ], className="card-body")
                    ], className="card card-primary card-outline")
                ], className="col-md-6"),


                
                html.Div([
                    html.Div([
                        html.Div([
                            html.H3("Chiffre d\'affaires mensuel par catégorie".upper(),
                                    className="card-title",style={'font-weight': 'bold','font-size': '28px'})  # Ajoutez ici le style CSS pour le gras)
                        ], className="card-header"),
                        html.Div([
                            html.Div([
                                html.Div(dcc.Graph(figure=fig0.update_layout(margin=dict(t=0, b=0, l=0, r=0)))),
                            ], className="card-body pad table-responsive p-0")
                        ], className="card-body")
                    ], className="card card-primary card-outline")
                ], className="col-md-6"),

                



            html.Div([
                html.Div([
                    html.Div([
                        html.H3("Poids de chaque sous-catégorie dans sa catégorie".upper(), 
                                className="card-title",style={'font-weight': 'bold','font-size': '28px'})  # Ajoutez ici le style CSS pour le gras
                    ], className="card-header"),
                    html.Div([
                        html.Div([
                            html.Div(dcc.Graph(figure=fig_treemap_item_subcategory.update_layout(margin=dict(t=0, b=0, l=0, r=0)))),
                        ], className="card-body pad table-responsive p-0")
                    ], className="card-body")
                ], className="card card-primary card-outline")
            ], className="col-md-6"),

            html.Div([
                html.Div([
                    html.Div([
                        html.H3("Chiffre d\'affaires et Taux de Marge Brute par mois".upper(), 
                                className="card-title",style={'font-weight': 'bold','font-size': '28px'})  # Ajoutez ici le style CSS pour le gras
                    ], className="card-header"),
                    html.Div([
                        html.Div([
                            html.Div(dcc.Graph(figure=fig_sunburst_item_category.update_layout(margin=dict(t=0, b=0, l=0, r=0)))),
                        ], className="card-body pad table-responsive p-0")
                    ], className="card-body")
                ], className="card card-primary card-outline")
            ], className="col-md-6"),

            html.Div([
                html.Div([
                    html.Div([
                        html.H3("Poids de chaque Item dans sa sous-catégorie".upper(), 
                                className="card-title",style={'font-weight': 'bold','font-size': '28px'})  # Ajoutez ici le style CSS pour le gras)
                    ], className="card-header"),
                    html.Div([
                        html.Div([
                            html.Div(dcc.Graph(figure=fig_total.update_layout(margin=dict(t=0, b=0, l=0, r=0)))),
                        ], className="card-body pad table-responsive p-0")
                    ], className="card-body")
                ], className="card card-primary card-outline")
            ], className="col-md-6"),

            html.Div([
                html.Div([
                    html.Div([
                        html.H3("Évolution des Charges Opérationnelles".upper(), 
                                className="card-title",style={'font-weight': 'bold','font-size': '28px'})  # Ajoutez ici le style CSS pour le gras)
                    ], className="card-header"),
                    html.Div([
                        html.Div([
                            html.Div(dcc.Graph(figure=fig_sunburst_subcategory_within_category.update_layout(margin=dict(t=0, b=0, l=0, r=0)))),
                        ], className="card-body pad table-responsive p-0")
                    ], className="card-body")
                ], className="card card-primary card-outline")
            ], className="col-md-6"),

            html.Div([
                html.Div([
                    html.Div([
                        html.H3("Taux Opex par Catégorie".upper(), #Répartition des charges par catégorie
                                className="card-title",style={'font-weight': 'bold','font-size': '28px'})  # Ajoutez ici le style CSS pour le gras)
                    ], className="card-header"),
                    html.Div([
                        html.Div([
                            html.Div(dcc.Graph(figure = opex.update_layout(margin=dict(t=0, b=0, l=0, r=0)))),#figure=fig_box_total_revenu
                        ], className="card-body pad table-responsive p-0")
                    ], className="card-body")
                ], className="card card-primary card-outline")
            ], className="col-md-6"),

            html.Div([
                html.Div([
                    html.Div([
                        html.H3("Coûts des produits vendus et Marge brute".upper(), 
                                className="card-title",style={'font-weight': 'bold','font-size': '28px'})  # Ajoutez ici le style CSS pour le gras)
                    ], className="card-header"),
                    html.Div([
                        html.Div([
                            html.Div(dcc.Graph(figure=fig_box_category_revenue.update_layout(margin=dict(t=0, b=0, l=0, r=0)))),
                        ], className="card-body pad table-responsive p-0")
                    ], className="card-body")
                ], className="card card-primary card-outline")
            ], className="col-md-6"),

            html.Div([
                html.Div([
                    html.Div([
                        html.H3("Chiffre d'affaires et coût des produits vendus".upper(), 
                                className="card-title",style={'font-weight': 'bold','font-size': '28px'})  # Ajoutez ici le style CSS pour le gras)
                    ], className="card-header"),
                    html.Div([
                        html.Div([
                            html.Div(dcc.Graph(figure=fig_box_total_revenue.update_layout(margin=dict(t=0, b=0, l=0, r=0)))),
                        ], className="card-body pad table-responsive p-0")
                    ], className="card-body")
                ], className="card card-primary card-outline")
            ], className="col-md-6"),
        
       html.Div([
            html.Div([
                html.Div([
                    html.H3("Marge brute et Rentabilité".upper(), 
                            className="card-title",style={'font-weight': 'bold','font-size': '28px'})  # Ajoutez ici le style CSS pour le gras)
                ], className="card-header"),
                html.Div([
                    html.Div([
                        html.Div(dcc.Graph(figure=fig_bar_weight_on_revenue.update_layout(margin=dict(t=0, b=0, l=0, r=0)))),
                    ], className="card-body pad table-responsive p-0")
                ], className="card-body")
            ], className="card card-primary card-outline")
        ], className="col-md-6"),

         html.Div([
            html.Div([
                html.Div([
                    html.H3("Évolution des Flux de Trésorerie".upper(),
                             className="card-title",style={'font-weight': 'bold','font-size': '28px'})  # Ajoutez ici le style CSS pour le gras)
                ], className="card-header"),
                html.Div([
                    html.Div([
                        html.Div(dcc.Graph(figure=fig_total_revenu.update_layout(margin=dict(t=0, b=0, l=0, r=0)))),
                    ], className="card-body pad table-responsive p-0")
                ], className="card-body")
            ], className="card card-primary card-outline")
        ], className="col-md-6"),


         
         html.Div([
            html.Div([
                html.Div([
                    html.H3("Coûts des Ventes".upper(),#Répartition des charges par catégorie
                             className="card-title",style={'font-weight': 'bold','font-size': '28px'})  # Ajoutez ici le style CSS pour le gras)
                ], className="card-header"),
                html.Div([
                    html.Div([
                        html.Div(dcc.Graph(figure=fig.update_layout(margin=dict(t=0, b=0, l=0, r=0)))),
                    ], className="card-body pad table-responsive p-0")
                ], className="card-body")
            ], className="card card-primary card-outline")
        ], className="col-md-6"),


        html.Div([
            html.Div([
                html.Div([
                    html.H3("Eat- Taux Coûts des Ventes et la Rentabilité".upper(),
                             className="card-title",style={'font-weight': 'bold','font-size': '28px'})  # Ajoutez ici le style CSS pour le gras)
                ], className="card-header"),
                html.Div([
                    html.Div([
                        html.Div(dcc.Graph(figure=eat.update_layout(margin=dict(t=0, b=0, l=0, r=0)))),
                    ], className="card-body pad table-responsive p-0")
                ], className="card-body")
            ], className="card card-primary card-outline")
        ], className="col-md-4"),


         html.Div([
            html.Div([
                html.Div([
                    html.H3("Drink- Taux Coûts des Ventes et la Rentabilité".upper(),
                             className="card-title",style={'font-weight': 'bold','font-size': '28px'})  # Ajoutez ici le style CSS pour le gras)
                ], className="card-header"),
                html.Div([
                    html.Div([
                        html.Div(dcc.Graph(figure=drink.update_layout(margin=dict(t=0, b=0, l=0, r=0)))),
                    ], className="card-body pad table-responsive p-0")
                ], className="card-body")
            ], className="card card-primary card-outline")
        ], className="col-md-4"),


        html.Div([
            html.Div([
                html.Div([
                    html.H3("Smoke- Taux Coûts des Ventes et la Rentabilité".upper(),
                             className="card-title",style={'font-weight': 'bold','font-size': '28px'})  # Ajoutez ici le style CSS pour le gras)
                ], className="card-header"),
                html.Div([
                    html.Div([
                        html.Div(dcc.Graph(figure=smoke.update_layout(margin=dict(t=0, b=0, l=0, r=0)))),
                    ], className="card-body pad table-responsive p-0")
                ], className="card-body")
            ], className="card card-primary card-outline")
        ], className="col-md-4"),


        html.Div([
            html.Div([
                html.Div([
                    html.H3("Eat- Taux Marge brute et la Rentabilité".upper(),
                             className="card-title",style={'font-weight': 'bold','font-size': '28px'})  # Ajoutez ici le style CSS pour le gras)
                ], className="card-header"),
                html.Div([
                    html.Div([
                        html.Div(dcc.Graph(figure=eat1.update_layout(margin=dict(t=0, b=0, l=0, r=0)))),
                    ], className="card-body pad table-responsive p-0")
                ], className="card-body")
            ], className="card card-primary card-outline")
        ], className="col-md-4"),


        html.Div([
            html.Div([
                html.Div([
                    html.H3("Drink- Taux Marge brute et la Rentabilité".upper(),
                             className="card-title",style={'font-weight': 'bold','font-size': '28px'})  # Ajoutez ici le style CSS pour le gras)
                ], className="card-header"),
                html.Div([
                    html.Div([
                        html.Div(dcc.Graph(figure=drink1.update_layout(margin=dict(t=0, b=0, l=0, r=0)))),
                    ], className="card-body pad table-responsive p-0")
                ], className="card-body")
            ], className="card card-primary card-outline")
        ], className="col-md-4"),



        html.Div([
            html.Div([
                html.Div([
                    html.H3("Smoke- Taux Marge brute et la Rentabilité".upper(),
                             className="card-title",style={'font-weight': 'bold','font-size': '28px'})  # Ajoutez ici le style CSS pour le gras)
                ], className="card-header"),
                html.Div([
                    html.Div([
                        html.Div(dcc.Graph(figure=smoke1.update_layout(margin=dict(t=0, b=0, l=0, r=0)))),
                    ], className="card-body pad table-responsive p-0")
                ], className="card-body")
            ], className="card card-primary card-outline")
        ], className="col-md-4"),



        
        html.Div([
            html.Div([
                html.Div([
                    html.H3("Eat- Taux Opex et la Rentabilité".upper(),
                             className="card-title",style={'font-weight': 'bold','font-size': '28px'})  # Ajoutez ici le style CSS pour le gras)
                ], className="card-header"),
                html.Div([
                    html.Div([
                        html.Div(dcc.Graph(figure=eat2.update_layout(margin=dict(t=0, b=0, l=0, r=0)))),
                    ], className="card-body pad table-responsive p-0")
                ], className="card-body")
            ], className="card card-primary card-outline")
        ], className="col-md-4"),


        html.Div([
            html.Div([
                html.Div([
                    html.H3("Drink- Taux Opex et la Rentabilité".upper(),
                             className="card-title",style={'font-weight': 'bold','font-size': '28px'})  # Ajoutez ici le style CSS pour le gras)
                ], className="card-header"),
                html.Div([
                    html.Div([
                        html.Div(dcc.Graph(figure=drink2.update_layout(margin=dict(t=0, b=0, l=0, r=0)))),
                    ], className="card-body pad table-responsive p-0")
                ], className="card-body")
            ], className="card card-primary card-outline")
        ], className="col-md-4"),



        html.Div([
            html.Div([
                html.Div([
                    html.H3("Smoke- Taux Opex et la Rentabilité".upper(),
                             className="card-title",style={'font-weight': 'bold','font-size': '28px'})  # Ajoutez ici le style CSS pour le gras)
                ], className="card-header"),
                html.Div([
                    html.Div([
                        html.Div(dcc.Graph(figure=smoke2.update_layout(margin=dict(t=0, b=0, l=0, r=0)))),
                    ], className="card-body pad table-responsive p-0")
                ], className="card-body")
            ], className="card card-primary card-outline")
        ], className="col-md-4"),


         html.Div([
            html.Div([
                html.Div([
                    html.H3("Taux des ventes par catégorie".upper(),
                             className="card-title",style={'font-weight': 'bold','font-size': '28px'})  # Ajoutez ici le style CSS pour le gras)
                ], className="card-header"),
                html.Div([
                    html.Div([
                        html.Div(dcc.Graph(figure=tcpv.update_layout(margin=dict(t=0, b=0, l=0, r=0)))),
                    ], className="card-body pad table-responsive p-0")
                ], className="card-body")
            ], className="card card-primary card-outline")
        ], className="col-md-4"),

        html.Div([
            html.Div([
                html.Div([
                    html.H3("Rentabilité par ncatégorie".upper(),
                             className="card-title",style={'font-weight': 'bold','font-size': '28px'})  # Ajoutez ici le style CSS pour le gras)
                ], className="card-header"),
                html.Div([
                    html.Div([
                        html.Div(dcc.Graph(figure=Rentabilite.update_layout(margin=dict(t=0, b=0, l=0, r=0)))),
                    ], className="card-body pad table-responsive p-0")
                ], className="card-body")
            ], className="card card-primary card-outline")
        ], className="col-md-4"),


        html.Div([
            html.Div([
                html.Div([
                    html.H3("Taux de la marge brute par catégorie".upper(),
                             className="card-title",style={'font-weight': 'bold','font-size': '28px'})  # Ajoutez ici le style CSS pour le gras)
                ], className="card-header"),
                html.Div([
                    html.Div([
                        html.Div(dcc.Graph(figure=tmb.update_layout(margin=dict(t=0, b=0, l=0, r=0)))),
                    ], className="card-body pad table-responsive p-0")
                ], className="card-body")
            ], className="card card-primary card-outline")
        ], className="col-md-4"),


        html.Div([
            html.Div([
                html.Div([
                    html.H3("Analyse des Performances de Vente par Heure, Mois et Année".upper(),
                             className="card-title",style={'font-weight': 'bold','font-size': '28px'})  # Ajoutez ici le style CSS pour le gras)
                ], className="card-header"),
                html.Div([
                    html.Div([
                        html.Div(dcc.Graph(figure=figl.update_layout(margin=dict(t=0, b=0, l=0, r=0)))),
                    ], className="card-body pad table-responsive p-0")
                ], className="card-body")
            ], className="card card-primary card-outline")
        ], className="col-md-12"),




       


        ], className="row")


#if __name__ == '__main__':
    #app.run_server(debug=True, port=5519)

# Récupére le port attribué par Heroku depuis la variable d'environnement
port = int(os.environ.get('PORT', 8050))  

# Créer et exécuter votre application Dash en écoutant sur le port attribué
if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=port)

# In[ ]:




