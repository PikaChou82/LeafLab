# Librairies
import streamlit as st
import pandas as pd
import random
import numpy as np

# J'indique que je veux prendre la totalité de l'écran
st.set_page_config(layout="wide")

page_element="""<style>[data-testid="stAppViewContainer"]{background-image: url("https://raw.githubusercontent.com/PikaChou82/LeafLab/refs/heads/main/Images/fond.png");
  background-size: cover;}</style>"""
st.markdown(page_element, unsafe_allow_html=True)

logo = "https://raw.githubusercontent.com/PikaChou82/LeafLab/refs/heads/main/Images/BigFoot.png"

# Récupération des DataFrame
liste_to_take = pd.read_csv("https://raw.githubusercontent.com/PikaChou82/LeafLab/refs/heads/main/Datasets_from_ETL/dataset_generator.csv")
alim_to_take = pd.read_csv("https://raw.githubusercontent.com/PikaChou82/LeafLab/refs/heads/main/Datasets_from_ETL/dataset_alimentation.csv")
proteine_to_take = pd.read_csv("https://raw.githubusercontent.com/PikaChou82/LeafLab/refs/heads/main/Datasets_from_ETL/df_prot_cat.csv")
encas_to_take = pd.read_csv("https://raw.githubusercontent.com/PikaChou82/LeafLab/refs/heads/main/Datasets_from_ETL/df_encas_cat.csv")
cereales_to_take = pd.read_csv("https://raw.githubusercontent.com/PikaChou82/LeafLab/refs/heads/main/Datasets_from_ETL/df_cereales_cat.csv")
boissons_to_take = pd.read_csv("https://raw.githubusercontent.com/PikaChou82/LeafLab/refs/heads/main/Datasets_from_ETL/df_boissons_cat.csv")
laitier_to_take = pd.read_csv("https://raw.githubusercontent.com/PikaChou82/LeafLab/refs/heads/main/Datasets_from_ETL/df_laitier_cat.csv")
electro = pd.read_csv("https://raw.githubusercontent.com/PikaChou82/LeafLab/refs/heads/main/Datasets_from_ETL/dataset_electro.csv")
usage_num = pd.read_csv("https://raw.githubusercontent.com/PikaChou82/LeafLab/refs/heads/main/Datasets_from_ETL/df_usagenum_cat.csv")

# Création des différentes listes
option_appareil_numerique = list(liste_to_take[liste_to_take['Name_Category'] == 'Numérique']['Name_SubCategory'].unique())
option_usage_numerique = list(usage_num['Libellé'].unique())
option_usage_chauffage = list(liste_to_take[liste_to_take['Name_Category'] == 'Chauffage']['Name_SubCategory'].unique())
option_usage_electromenager = list(liste_to_take[liste_to_take['Name_Category'] == 'Électroménager']['Name_SubCategory'].unique())
option_appareils_electromenager = option_usage_electromenager
option_transport_quotidien = list(liste_to_take[liste_to_take['Name_Category'] == 'Transport']['Name_SubCategory'].unique())
option_transport_voyage = option_transport_quotidien
option_achat_mobilier = list(liste_to_take[liste_to_take['Name_Category'] == 'Mobilier']['Name_SubCategory'].unique())
option_achat_habillement = list(liste_to_take[liste_to_take['Name_Category'] == 'Habillement']['Name_SubCategory'].unique())
option_consommation_protéine = list(proteine_to_take['Libellé'].unique())
option_consommation_produits_laitiers = list(laitier_to_take['Libellé'].unique())
option_consommation_céréales = list(cereales_to_take['Libellé'].unique())
option_consommation_plats = list(encas_to_take['Libellé'].unique())
option_consommation_alimentation = list(alim_to_take['name'].unique())
option_consommation_alimentation.remove("Fruits et légumes")
option_consommation_fruits_legumes = list(liste_to_take[liste_to_take['Name_Category'] == 'Fruits et légumes']['Name_SubCategory'].unique())
option_consommation_boisson = list(boissons_to_take['Libellé'].unique())

# Initialisation des variables d'état
if 'afficher_bloc' not in st.session_state:
    st.session_state.afficher_bloc = 'questionnaire'  
if 'results_df' not in st.session_state:  
    st.session_state.results_df = None

# Fonctions de navigation
def afficher_questionnaire():
    st.session_state.afficher_bloc = 'questionnaire'

def afficher_résultats(results):
    st.session_state.afficher_bloc = 'résultats'
    st.session_state.results_df = results

# Bloc 1 : Affichage du Questionnaire
if st.session_state.afficher_bloc == 'questionnaire':

    # Questionnaire sur 2eme colonne, qui prend les 2/3 de la page (avec l'option [1, 2])
    col1, col2 = st.columns([2, 5])
    with col1:
        st.image(logo)

    with col2:

        # Fonction d'affichage des questions sous forme de liste
        def afficher_section_liste(theme, sous_themes, questions,options, keys, emoji):
            theme = f"### **{theme}**"
            with st.expander(theme, icon= emoji):  
                for i, sous_theme in enumerate(sous_themes):
                    st.subheader(sous_theme)
                    st.write(questions[i])
                    reponse = st.multiselect("Sélectionnez une ou plusieurs options :", options[i], key=keys[i]) 
                    yield reponse  # Générateur pour retourner une réponse sans sortir de la fonction

        # Fonction d'affichage des questions sous forme d'entrée en 1 puis liste en 2 
        def afficher_section_num_liste(theme, sous_themes, questions, options, keys, emoji):
            theme = f"### **{theme}**"
            with st.expander(theme, icon= emoji):
                for i, sous_theme in enumerate(sous_themes):
                    st.subheader(sous_theme)
                    st.write(questions[i])
                    if i == 0:
                        reponse = st.text_input("Votre réponse ici:", key=keys[i])
                    else:
                        reponse = st.selectbox("Sélectionnez une ou plusieurs options :", options[i], key=keys[i]) 
                    yield reponse  # Générateur pour retourner une réponse sans sortir de la fonction

        # Fonction d'affichage des questions sous forme de tableau pour saisie
        def afficher_section_tableau(theme, sous_themes, questions, options, keys, boolean, emoji):
            theme = f"### **{theme}**"
            with st.expander(theme, expanded= boolean, icon= emoji):
                for i, sous_theme in enumerate(sous_themes):
                    st.subheader(sous_theme)
                    st.write(questions[i])
                    dataset = pd.DataFrame({"Libellé": options[i], "Quantité": [0.0] * len(options[i])})
                    edited_dataset = st.data_editor(dataset,width=1300, key=keys[i]) # dataset_editor sert à autoriser la saisie
                    yield edited_dataset  # Générateur pour retourner une réponse sans sortir de la fonction


        # Fonction d'affichage des questions sous forme de liste puis chiffre (*2)
        def afficher_section_liste_chiffre_tableau(theme, sous_themes, questions, options, keys, emoji):
            theme = f"### **{theme}**"
            with st.expander(theme, icon= emoji):
                for i, sous_theme in enumerate(sous_themes):
                    st.subheader(sous_theme)
                    st.write(questions[i])
                    if i == 4 or i ==5 or i ==6  :
                        reponse = st.text_input("Votre réponse ici:", key=keys[i])
                    else:
                        dataset = pd.DataFrame({"Libellé": options[i], "Quantité": [0.0] * len(options[i])})
                        reponse = st.data_editor(dataset,width=1300, key=keys[i]) # dataset_editor sert à autoriser la saisie
                    yield reponse  # Générateur pour retourner une réponse sans sortir de la fonction

        st.title("J'évalue ma conso")

        # Questions Numérique
        sous_themes_numerique = ["Appareils", "Usage"]
        questions_numerique = [
            "Quels appareils numériques avez-vous acheté neuf ces 12 derniers mois ?",
            "Quantifiez vos usages du numérique ? (en moyenne par semaine, en nombre ou en heures)"
        ]
        options_numerique = [option_appareil_numerique,
            option_usage_numerique
        ]
        keys_numerique = ["numerique_appareils", "numerique_usage"]

        reponses_numerique = afficher_section_tableau("Numérique", sous_themes_numerique, questions_numerique, options_numerique, keys_numerique, True, "💻")
        reponses_numerique_appareil, reponses_numerique_usage = tuple(reponses_numerique)

        # Questions Alimentation
        sous_themes_alimentation = ["Viandes & Poissons","Produits Laitiers","Céréales & Légumineuses","Plats Préparés & Snacks", "Légumes", "Fruits", "Fruits Exotiques", "Boissons"]
        questions_alimentation = [
            "Quel(s) aliment(s) et plat(s) avez-vous consommé cette semaine ? (en portions)",
            "Quel(s) aliment(s) et plat(s) avez-vous consommé cette semaine ? (en portions)",
            "Quel(s) aliment(s) et plat(s) avez-vous consommé cette semaine ? (en portions)",
            "Quel(s) aliment(s) et plat(s) avez-vous consommé cette semaine ? (en portions)",
            "Combien de légumes consommez-vous par jour ? (en moyenne)",
            "Combien de fruits consommez-vous par jour ? (en moyenne)",
            "Combien avez-vous consommé de mangues cette année ? (en moyenne)", 
            "Combien de litres de boissons consommez-vous par semaine ?"
        ]
        options_alimentation = [option_consommation_protéine, option_consommation_produits_laitiers, option_consommation_céréales, option_consommation_plats, None, None,None, option_consommation_boisson]
        
        keys_alimentation = ["consommation_protéines","consommation_produits_laitiers","consommation_céréales","consommation_plats", "nb_legumes","nb_fruits","nb_mangues","consommation_boisson"]

        reponses_alimentation = afficher_section_liste_chiffre_tableau("Alimentation", sous_themes_alimentation, questions_alimentation, options_alimentation, keys_alimentation, "🍏")
        reponses_alimentation_proteines, reponses_alimentation_produits_laitiers, reponses_alimentation_cereales, reponses_alimentation_plats ,reponses_alimentation_legumes,reponses_alimentation_fruits, reponses_alimentaiton_mangue, reponses_alimentation_boisson  = tuple(reponses_alimentation)

        # Questions Transport
        sous_themes_transport = ["Au quotidien", "Mes voyages"]
        questions_transport = [
            "Quel(s) moyen(s) de transport utilisez-vous au quotidien (et quelle distance en km) ?",
            "Avez-vous voyagé au cours des 12 derniers mois (et quelle distance en km) ?"
        ]
        options_transport = [option_transport_quotidien, option_transport_voyage]
        
        keys_transport = ["transport_quotidien", "transport_voyage"]

        responses_transport = afficher_section_tableau("Transport", sous_themes_transport, questions_transport, options_transport, keys_transport, False, "🚗")
        responses_transport_quotidien,responses_transport_voyage = tuple(responses_transport)

        # Questions Habillement
        sous_themes_habillement = ["Achat"]
        questions_habillement = [
            "Quel(s) type(s) de vêtements avez-vous acheté au cours des 12 derniers mois ?"
        ]
        options_habillement = [option_achat_habillement
        ]
        keys_habillement = ["habillement_achat"]

        reponses_habillement = afficher_section_tableau("Habillement", sous_themes_habillement, questions_habillement, options_habillement, keys_habillement, False, "👕")
        reponses_habillement_achat = tuple(reponses_habillement)

        # Questions Electroménager
        sous_themes_electromenager = ["Usage", "Appareil"]
        questions_electromenager = [
            "Quel(s) électroménager(s) avez-vous utilisé cette année ?",
            "Quel(s) appareil(s) d'électroménager avez-vous acheté au cours des 12 derniers mois ?"
        ]

        options_electromenager = [ option_usage_electromenager,
            option_appareils_electromenager
        ]
        keys_electromenager = ["electromenager_usage", "electromenager_appareil"]

        reponses_electromenager = afficher_section_liste("Electroménager", sous_themes_electromenager, questions_electromenager, options_electromenager, keys_electromenager, "🔌")
        reponses_electromenager_usage, reponses_electromenager_appareils = tuple(reponses_electromenager)

        # Questions Mobilier
        sous_themes_mobilier = ["Achat"]
        questions_mobilier = [
            "Quel(s) type(s) de mobilier acheté au cours des 12 derniers mois ?"
        ]

        options_mobilier = [option_achat_mobilier]
        keys_mobilier = ["mobilier_achat"]

        reponses_mobilier = afficher_section_liste("Mobilier", sous_themes_mobilier, questions_mobilier, options_mobilier, keys_mobilier, "🛏️")
        reponses_mobilier_achat = tuple(reponses_mobilier)

        # Questions Chauffage
        sous_themes_chauffage = ["Logement", "Type de Chauffage"]
        questions_chauffage = [
            "Quelle est la taille de votre logement ? (en m²)",
            "Quel mode de chauffage est présent dans votre logement ?"
        ]

        options_chauffage = [ None,
            option_usage_chauffage
        ]
        keys_chauffage = ["chauffage_taille", "chauffage_type"]

        reponses_chauffage = afficher_section_num_liste("Chauffage", sous_themes_chauffage, questions_chauffage, options_chauffage, keys_chauffage,"🔥")
        reponses_chauffage_superficie, reponses_chauffage_type = tuple(reponses_chauffage)

    # Mise en Forme des DataFrames Spécifiques
    results = pd.DataFrame(liste_to_take)
    results = results.iloc[:,1:]
    results = results[results['Category'] != 2]
    results = results[results['Category'] != 9]
    results = results[results['Category'] != 3]
    results = results[results['Category'] != 10]

    compteur = 0
    liste_compteur = ['Viandes & Poissons','Céréales & Légumineuses', 'Plats Préparés & Encas', 'Oeufs & Produits Laitiers', 'Boissons', 'Usage numérique']
    for dataframe in [proteine_to_take, cereales_to_take, encas_to_take, laitier_to_take, boissons_to_take, usage_num]:
        dataframe = pd.DataFrame(dataframe)
        dataframe = dataframe.iloc[:,1:]
        if compteur == 3:
            dataframe = dataframe.rename(columns={'Libellé': 'Name_SubCategory', 'ecv_par_portion': 'ecv'})
        else:
            dataframe = dataframe.rename(columns={'Libellé': 'Name_SubCategory', 'ecv': 'ecv'})
        if compteur == 4:
            dataframe['Name_Category'] = 'Boissons'
            dataframe['Category'] = 3
        else:        
            dataframe['Name_Category'] = 'Alimentation'
            dataframe['Category'] = 2
        dataframe['slug'] = liste_compteur[compteur] 
        dataframe = dataframe[['Category', 'Name_Category', 'Name_SubCategory', 'slug', 'ecv']]
        results= pd.concat([results,dataframe ])
        compteur += 1

    reponses_alimentation_fruits = pd.to_numeric(reponses_alimentation_fruits, errors="coerce")
    reponses_alimentaiton_mangue = pd.to_numeric(reponses_alimentaiton_mangue, errors="coerce")
    reponses_alimentation_legumes = pd.to_numeric(reponses_alimentation_legumes, errors="coerce")

    results["User"] = 0
    results["Usage"]= 0

    fruits_legumes = {'Category': [9, 9, 9],
                'Name_Category': ['Fruits & Légumes', 'Fruits & Légumes', 'Fruits & Légumes'],
                'Name_SubCategory': ['Fruits', 'Mangues', 'Légumes'],
                'slug': ['Fruits', 'Fruits', 'Légumes'],
                'ecv': [0.99, 11.66, 0.90],
                'User_2': [reponses_alimentation_fruits*.1*365,reponses_alimentaiton_mangue*0.45,reponses_alimentation_legumes*.2*365],
                'Usage' : [0,0,0]}

    fruits_legumes = pd.DataFrame(fruits_legumes)

    # Concaténer les deux DataFrames
    results = pd.concat([results, fruits_legumes], ignore_index=True)


    results.sort_values('Category', inplace= True)

    # Création du DataFrame personnalisé
    reponses_numerique_appareil = reponses_numerique_appareil.rename(columns={'Libellé': 'Libellé_Num_Appareil', 'Quantité': 'Quantité_Num_Appareil'})
    reponses_numerique_usage = reponses_numerique_usage.rename(columns={'Libellé': 'Libellé_Num_Usage', 'Quantité': 'Quantité_Num_Usage'})
    reponses_alimentation_boisson = reponses_alimentation_boisson.rename(columns={'Libellé': 'Libellé_Alim_Boisson', 'Quantité': 'Quantité_Alim_Boisson'})
    reponses_habillement_achat = reponses_habillement_achat[0].rename(columns={'Libellé': 'Libellé_Habillement', 'Quantité': 'Quantité_Habillement'})
    reponses_alimentation_proteines = reponses_alimentation_proteines.rename(columns={'Libellé': 'Libellé_Proteines', 'Quantité': 'Quantité_Proteines'})
    reponses_alimentation_cereales = reponses_alimentation_cereales.rename(columns={'Libellé': 'Libellé_Cereales', 'Quantité': 'Quantité_Cereales'})
    reponses_alimentation_plats = reponses_alimentation_plats.rename(columns={'Libellé': 'Libellé_Plats', 'Quantité': 'Quantité_Plats'})
    reponses_alimentation_produits_laitiers = reponses_alimentation_produits_laitiers.rename(columns={'Libellé': 'Libellé_Produits_Laitiers', 'Quantité': 'Quantité_Produits_Laitiers'})
    responses_transport_quotidien = responses_transport_quotidien .rename(columns={'Libellé': 'Libellé_Transport_Quotidien', 'Quantité': 'Quantité_Transport_Quotidien'})
    responses_transport_voyage = responses_transport_voyage .rename(columns={'Libellé': 'Libellé_Transport_Voyage', 'Quantité': 'Quantité_Transport_Voyage'})
    reponses_chauffage_superficie = pd.to_numeric(reponses_chauffage_superficie, errors='coerce')
    results = pd.merge(results, reponses_numerique_appareil, how = "left", left_on = "Name_SubCategory", right_on= "Libellé_Num_Appareil")
    results =pd.merge(results, reponses_numerique_usage, how = "left", left_on = "Name_SubCategory", right_on= "Libellé_Num_Usage")
    results =pd.merge(results, reponses_alimentation_boisson, how = "left", left_on = "Name_SubCategory", right_on= "Libellé_Alim_Boisson")
    results =pd.merge(results, reponses_habillement_achat, how = "left", left_on = "Name_SubCategory", right_on= "Libellé_Habillement")
    results =pd.merge(results, reponses_alimentation_proteines, how = "left", left_on = "Name_SubCategory", right_on= "Libellé_Proteines")
    results =pd.merge(results, reponses_alimentation_cereales, how = "left", left_on = "Name_SubCategory", right_on= "Libellé_Cereales")
    results =pd.merge(results, reponses_alimentation_plats, how = "left", left_on = "Name_SubCategory", right_on= "Libellé_Plats")
    results =pd.merge(results, responses_transport_voyage, how = "left", left_on = "Name_SubCategory", right_on= "Libellé_Transport_Voyage")
    results =pd.merge(results, responses_transport_quotidien, how = "left", left_on = "Name_SubCategory", right_on= "Libellé_Transport_Quotidien")
    results =pd.merge(results, reponses_alimentation_produits_laitiers, how = "left", left_on = "Name_SubCategory", right_on= "Libellé_Produits_Laitiers")

    results["User"] = (results["Quantité_Num_Appareil"].fillna(0) + results["Quantité_Num_Usage"].fillna(0)*52 + results["Quantité_Alim_Boisson"].fillna(0)*52 +
    results["Quantité_Habillement"].fillna(0) + results["Quantité_Proteines"].fillna(0) * 0.15 * 52 + results["Quantité_Cereales"].fillna(0) * 0.15 * 52 + 
    results["Quantité_Plats"].fillna(0) * 0.45 * 52 + results['Quantité_Produits_Laitiers'].fillna(0) * 52 + results['Quantité_Transport_Quotidien'].fillna(0) *365
    + results['Quantité_Transport_Voyage'].fillna(0) + results['User_2'].fillna(0))
    results.loc[results['Name_SubCategory'] == reponses_chauffage_type, 'User'] = ((reponses_chauffage_superficie)/65)
    results['User'] = np.where(results['Name_SubCategory'].isin(reponses_mobilier_achat[0]), 1, results['User'])
    for usage in range(len(reponses_electromenager_usage)):
        results['Usage'] = np.where(results['Name_SubCategory']==reponses_electromenager_usage[usage], 1, results['Usage'])
    for usage in range(len(reponses_electromenager_appareils)):
        results['User'] = np.where(results['Name_SubCategory']==reponses_electromenager_appareils[usage], 1, results['User'])
    results = results.iloc[:,:7]

    def update_usage(row):
        if row['Name_SubCategory'] in electro['name'].values:
            peryear = electro.loc[electro['name'] == row['Name_SubCategory'], 'peryear'].iloc[0]
            return row['Usage'] * peryear
        else:
            return row['Usage']

    results['Usage'] = results.apply(update_usage, axis=1)
    results['Use_Total'] = results['User'] * results['ecv'] + results['Usage']
    Conso_Totale_Tonnes = results['Use_Total'].sum()/1000

    st.title(f"Ma conso moyenne est de {round(Conso_Totale_Tonnes,2)} Tonnes / An !")

    # Indication des Unités 
    def unite(x):
        if 'streaming' in x:
            return "Heures"
        elif x == "Alimentation" or x =="Fruits et légumes":
            return "Kg"
        elif x == "Transport":
            return "Km"
        else :
            return ""

    # Indication des Emojis
    map = { "Alimentation" : "🥗", "Cas pratiques" : "🕑", "Chauffage" : "🔥", "Fruits & Légumes" : "🍏", "Boissons" : "🥛","Mobilier" : "🛏️", "Transport" : "🚗", "Électroménager" : "🔌", "Numérique" : "💻", "Usage numérique" : "💻", "Habillement" : "👕"}

    # Application de la Colonne 
    results["Unité"] = results['Name_Category'].apply(unite)
    results["Emoji"] = results['Name_Category'].map(map)

    
    if st.button("Analyser mes résultats"): 
        st.session_state.results_df = results  
        afficher_résultats(results)
        
elif st.session_state.afficher_bloc == 'résultats':
    
# Calcul des équivalents 
    def calcul_comparative(conso, df):
        comparative_dataset = pd.DataFrame(df)
        comparative_dataset['Equivalent'] = comparative_dataset['ecv'].apply(lambda x : round(conso/x,2) if x !=0  else 0)
        return comparative_dataset

    # Générateur d'équivalents 
    def generateur(df, *categories):

        df2 = calcul_comparative(df['Use_Total'].sum(), df)
        if not categories:
            nombres_aleatoires = set()
            while len(nombres_aleatoires) < 5:
                nombre = random.randint(1, 123)
                nombres_aleatoires.add(nombre)

        print(f"Merci ! Voici tes stats :\n")
        print(f"Pour {df['Use_Total'].sum()} Kg de CO2 on a :\n")
        for i in range(5) :
            st.write(f"{df2.iloc[list(nombres_aleatoires)].iloc[i,-2]} - {df2.iloc[list(nombres_aleatoires)].iloc[i,-1]} {df2.iloc[list(nombres_aleatoires)].iloc[i,-3]} {df2.iloc[list(nombres_aleatoires)].iloc[i,-9]}.")

    if st.session_state.results_df is not None:  
        st.subheader("Page Antoine")
        st.subheader(st.session_state.results_df['Use_Total'].sum())
        generateur(st.session_state.results_df)
    else:
        st.error("Aucun résultat à afficher. Veuillez remplir le questionnaire.")
    if st.button("Retour au questionnaire"):
        afficher_questionnaire()
