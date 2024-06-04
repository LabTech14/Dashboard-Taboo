
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
    
    filtered_df = ddff[ddff['Catégorie'].isin(selected_categories)]
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




