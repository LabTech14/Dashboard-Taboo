import dash
import pandas as pd
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
from pathlib import Path
new_filtered_excel_file = r"non.xlsx"
#tcd.to_excel(new_filtered_excel_file, index=True)

filepath = Path("inputcons/BD.xlsx")
df = pd.read_excel(filepath)
# Obtenir la liste des années uniques dans la colonne 'Année'
annee_list = df['Années'].unique()
df['Mois'] = df['Mois'].astype(str)

mois_list = sorted(df['Mois'].unique())

# Obtenir la liste des années uniques dans la colonne 'Année'
categorie_list = df['Catégorie'].unique()

#df = pd.read_excel(output_path)
#print(df.head())
# Obtenir la liste des années uniques dans la colonne 'Année'
sous_categorie_list = df['Sous-catégorie'].unique()

# Initialisation de l'application Dash
app = dash.Dash(__name__)

# Définition de la mise en page principale
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

# Définition des différentes pages de l'application
page_1_layout = html.Div([
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
                    html.H1("DASHBOARD  INVENTAIRES", className="m-0",
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
    

    dcc.Link('DASHBOARD ANALYSE TB', href='/page-2') # Lien vers la page 2
])

page_2_layout = html.Div([
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
                    html.H1("DASHBOARD ANALYSE TB", className="m-0",
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
    dcc.Link('DASHBOARD  INVENTAIRES', href='/') # Lien vers la page 1
])

# Callback pour afficher la page correspondante en fonction de l'URL
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
        return page_1_layout
    elif pathname == '/page-2':
        return page_2_layout
    else:
        return 'Page introuvable'

# Exécution de l'application
if __name__ == '__main__':
    app.run_server(debug=True, port = 4050)
