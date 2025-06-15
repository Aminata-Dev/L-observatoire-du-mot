import streamlit as st #https://www.youtube.com/watch?v=D0D4Pa22iG0
import pandas as pd

st.title("L'Observatoire du mot")

#columns gestion

st.write("Bienvenue dans l'_Observatoire du mot_ !")

mot_entree = st.text_input("Quel mot souhaites-tu observer ?", "sensible") #on capture la valeur de l'entrée dans la variable mot_entree
#Valeur par défaut = ???

#is_clicked = st.button("Click Me")


st.write("Voir les fichiers csv créés pendant que le Excel se génère : ")

#Dimension sémantique

from synonymes import exportation_synonymes #synonymes et score de proximité
if exportation_synonymes(mot_entree): #la fonction retourne false en cas d'erreur
    st.bar_chart(pd.read_csv("data/synonymes.csv"),
             x="synonyme",
             y="score_proximite_mot",
            horizontal=True)

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
st.write(pd.read_csv("data/tweets_avec_mot.csv").head())
st.write(pd.read_csv("data/reddit_posts_avec_mot.csv").head())
st.write(pd.read_csv("data/score_de_popularite.csv"))

#Dimension médiatique
from flux_rss import recup_articles
recup_articles(mot_entree)
st.write(pd.read_csv("data/actualite_avec_mot.csv"))

#graphique ! https://docs.streamlit.io/develop/api-reference/charts
st.bar_chart()
st.line_chart()

#multi pages

#
st.link_button("Profile", url="https://github.com/Aminata-Dev")