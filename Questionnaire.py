import streamlit as st
import pandas as pd

logo = "https://raw.githubusercontent.com/PikaChou82/LeafLab/refs/heads/main/Images/BigFoot.png"

# J'indique que je veux prendre la totalité de l'écran
st.set_page_config(layout="wide")

# Création des différentes listes
liste_to_take = pd.read_csv("https://raw.githubusercontent.com/PikaChou82/LeafLab/refs/heads/main/Datasets_from_ETL/dataset_generator.csv")
alim_to_take = pd.read_csv("https://raw.githubusercontent.com/PikaChou82/LeafLab/refs/heads/main/Datasets_from_ETL/dataset_alimentation.csv")

option_appareil_numerique = list(liste_to_take[liste_to_take['Name_Category'] == 'Numérique']['Name_SubCategory'].unique())

option_usage_numerique = list(liste_to_take[liste_to_take['Name_Category'] == 'Usage numérique']['Name_SubCategory'].unique())

option_usage_chauffage = list(liste_to_take[liste_to_take['Name_Category'] == 'Chauffage']['Name_SubCategory'].unique())

option_usage_electromenager = list(liste_to_take[liste_to_take['Name_Category'] == 'Électroménager']['Name_SubCategory'].unique())
option_appareils_electromenager = option_usage_electromenager

option_transport_quotidien = list(liste_to_take[liste_to_take['Name_Category'] == 'Transport']['Name_SubCategory'].unique())
option_transport_voyage = option_transport_quotidien

option_achat_mobilier = list(liste_to_take[liste_to_take['Name_Category'] == 'Mobilier']['Name_SubCategory'].unique())

option_achat_habillement = list(liste_to_take[liste_to_take['Name_Category'] == 'Habillement']['Name_SubCategory'].unique())

option_consommation_protéine = list(alim_to_take[alim_to_take['name'].isin(['Viandes', 'Poissons et fruits de mer'])]['slug'].unique())
option_consommation_produits_laitiers = list(alim_to_take[alim_to_take['name'] == 'Oeufs et produits laitiers']['slug'].unique())
option_consommation_céréales =list(alim_to_take[alim_to_take['name'] == "Céréales et légumineuses"]['slug'].unique())
option_consommation_plats = list(alim_to_take[alim_to_take['name'].isin(['En-cas', 'Plats préparés'])]['slug'].unique())
option_consommation_alimentation = list(alim_to_take['name'].unique())
option_consommation_alimentation.remove("Fruits et légumes")
option_consommation_fruits_legumes = list(liste_to_take[liste_to_take['Name_Category'] == 'Fruits et légumes']['Name_SubCategory'].unique())
option_consommation_boisson = list(liste_to_take[liste_to_take['Name_Category'] == 'Boisson']['Name_SubCategory'].unique())

# Questionnaire sur 2eme colonne, qui prend les 2/3 de la page (avec l'option [1, 2])
col1, col2 = st.columns([1, 2])
with col1:
    st.image(logo)

with col2:
    
    # Fonction d'affichage des questions sous forme de liste
    def afficher_section_liste(theme, sous_themes, questions,options, keys, emoji):
        theme = f"**{theme}**"
        with st.expander(theme, icon= emoji):  
            for i, sous_theme in enumerate(sous_themes):
                st.subheader(sous_theme)
                st.write(questions[i])
                reponse = st.multiselect("Sélectionnez une ou plusieurs options :", options[i], key=keys[i]) 
                yield reponse  # Générateur pour retourner une réponse sans sortir de la fonction

    # Fonction d'affichage des questions sous forme d'entrée en 1 puis liste en 2 
    def afficher_section_num_liste(theme, sous_themes, questions, options, keys, emoji):
        theme = f"**{theme}**"
        with st.expander(theme, icon= emoji):
            for i, sous_theme in enumerate(sous_themes):
                st.subheader(sous_theme)
                st.write(questions[i])
                if i == 0:
                    reponse = st.text_input("Votre réponse ici:", key=keys[i])
                else:
                    reponse = st.multiselect("Sélectionnez une ou plusieurs options :", options[i], key=keys[i]) 
                yield reponse  # Générateur pour retourner une réponse sans sortir de la fonction

    # Fonction d'affichage des questions sous forme de tableau pour saisie
    def afficher_section_tableau(theme, sous_themes, questions, options, keys, boolean, emoji):
        theme = f"**{theme}**"
        with st.expander(theme, expanded= boolean, icon= emoji):
            for i, sous_theme in enumerate(sous_themes):
                st.subheader(sous_theme)
                st.write(questions[i])
                dataset = pd.DataFrame({"Libellé": options[i], "Quantité": [0.0] * len(options[i])})
                edited_dataset = st.data_editor(dataset,width=800, key=keys[i]) # dataset_editor sert à autoriser la saisie
                yield edited_dataset  # Générateur pour retourner une réponse sans sortir de la fonction


    # Fonction d'affichage des questions sous forme de liste puis chiffre (*2)
    def afficher_section_liste_chiffre_tableau(theme, sous_themes, questions, options, keys, emoji):
        theme = f"**{theme}**"
        with st.expander(theme, icon= emoji):
            for i, sous_theme in enumerate(sous_themes):
                st.subheader(sous_theme)
                st.write(questions[i])
                if i == 0 or i ==1 or i ==2 or i ==3 or i==5:
                    reponse = st.multiselect("Sélectionnez une ou plusieurs options :", options[i], key=keys[i]) 
                elif i ==4 :
                    reponse = st.text_input("Votre réponse ici:", key=keys[i])
                else:
                    dataset = pd.DataFrame({"Libellé": options[i], "Quantité": [0.0] * len(options[i])})
                    reponse = st.data_editor(dataset,width=800, key=keys[i]) # dataset_editor sert à autoriser la saisie
                yield reponse  # Générateur pour retourner une réponse sans sortir de la fonction

    st.title("J'évalue ma conso")

    # Questions Numérique
    sous_themes_numerique = ["Appareils", "Usage"]
    questions_numerique = [
        "Quels appareils numériques avez-vous acheté neuf ces 12 derniers mois ?",
        "Quantifiez vos usages du numérique ? (nombre / heures)"
    ]
    options_numerique = [option_appareil_numerique,
        option_usage_numerique
    ]
    keys_numerique = ["numerique_appareils", "numerique_usage"]

    reponses_numerique = afficher_section_tableau("Numérique", sous_themes_numerique, questions_numerique, options_numerique, keys_numerique, True, "💻")
    reponses_numerique_appareil, reponses_numerique_usage = tuple(reponses_numerique)

    # Questions Alimentation
    sous_themes_alimentation = ["Viandes & Poissons","Produits Laitiers","Céréales & Légumineuses","Plats Préparés & Snacks", "Fruits & Légumes", "Fruits & Légumes (Type)", "Boissons"]
    questions_alimentation = [
        "Quel(s) aliment(s) et plat(s) avez-vous consommé cette semaine ? (Viandes & Poissons)",
        "Quel(s) aliment(s) et plat(s) avez-vous consommé cette semaine ? (Produits Laitiers)",
        "Quel(s) aliment(s) et plat(s) avez-vous consommé cette semaine ? (Céréales & Légumineuses)",
        "Quel(s) aliment(s) et plat(s) avez-vous consommé cette semaine ? (Plats Préparés & Snacks)",
        "Combien de fruits et légumes consommez-vous par jour ?",
        "Quels fruits et légumes avez-vous consommé cette année ?",
        "Combien de litres de boissons consommez-vous par semaine ?"
    ]
    options_alimentation = [option_consommation_protéine, option_consommation_produits_laitiers, option_consommation_céréales, option_consommation_plats, None,option_consommation_fruits_legumes, option_consommation_boisson]
    
    keys_alimentation = ["consommation_protéines","consommation_produits_laitiers","consommation_céréales","consommation_plats", "kg_fruits_legumes","consommation_fruits_legumes","consommation_boisson"]

    reponses_alimentation = afficher_section_liste_chiffre_tableau("Alimentation", sous_themes_alimentation, questions_alimentation, options_alimentation, keys_alimentation, "🍏")
    reponses_alimentation_proteines, reponses_alimentation_produits_laitiers, reponses_alimentation_cereales, reponses_alimentation_plats ,reponses_alimentation_kg,reponses_alimentation_fruits_legumes, reponses_alimentation_boisson  = tuple(reponses_alimentation)

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
