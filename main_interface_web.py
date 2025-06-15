import streamlit as st #https://www.youtube.com/watch?v=D0D4Pa22iG0
import pandas as pd

st.title("L'Observatoire du mot")

st.write("Bienvenue dans l'_Observatoire du mot_ !")

#mot en entrée
import requests
import random
url = 'https://raw.githubusercontent.com/drogbadvc/wiktionaire-fr/refs/heads/main/dict.txt'
response = requests.get(url)

if response.status_code == 200:
    content = response.text
    mot = random.choice(content.splitlines())
else:
    mot = "sable"

mot_entree = st.text_input("Quel mot souhaites-tu observer ?", "sable") #on capture la valeur de l'entrée dans la variable mot_entree
#valeur par défaut = sable pour test

#is_clicked = st.button("Click Me")


st.write("Voici les données générées concernant le mot en entrée. Le tableau de bord Excel sera prêt à la fin du chargement indiqué en haut à gauche (Running)")

#Dimension sémantique
from synonymes import exportation_synonymes #synonymes et score de proximité
if exportation_synonymes(mot_entree): #la fonction retourne false en cas d'erreur
    st.bar_chart(pd.read_csv("data/synonymes.csv"),
             x="synonyme",
             y="score_proximite_mot",
            horizontal=True) #graphique : https://docs.streamlit.io/develop/api-reference/charts

from fiche_lexicale import recup_fiche_lexicale
recup_fiche_lexicale(mot_entree)
st.write(pd.read_csv("data/definitions.csv"))
st.write(pd.read_csv("data/prononciation.csv"))
st.write(pd.read_csv("data/etymologies.csv"))
st.write(pd.read_csv("data/citations.csv"))

#Dimension culturelle
from titres_oeuvres_art import recherche_wikidata_oeuvres_art
recherche_wikidata_oeuvres_art(mot_entree)
st.write(pd.read_csv("data/repartition_types_oeuvres_art.csv"))

#Dimension sociale
from score_de_popularite import calcul_score_de_popularite #cette fonction appelle twitter.py et reddit.py et crée les fichiers csv correspondant aux posts contenant le mot d'entrée
calcul_score_de_popularite(mot_entree)
st.write(pd.read_csv("data/tweets_avec_mot.csv"))
st.write(pd.read_csv("data/reddit_posts_avec_mot.csv"))
st.write(pd.read_csv("data/score_de_popularite.csv"))
#st.line_chart() #graphique : https://docs.streamlit.io/develop/api-reference/charts

#Dimension médiatique
from flux_rss import recup_articles
if recup_articles(mot_entree): #la fonction retourne false en cas d'erreur
    st.write(pd.read_csv("data/actualite_avec_mot.csv"))

#execution génération fichier excel
with open("main_excel.py", 'r', encoding='utf-8') as f:
    code = f.read()
    exec(code)

#références
st.link_button("Lien GitHub", url="https://github.com/Aminata-Dev/L-observatoire-du-mot")

# 🌙 Fond noir (mode sombre custom)
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
        color: white;
    }
    input, textarea {
        background-color: #262730;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)