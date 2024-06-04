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