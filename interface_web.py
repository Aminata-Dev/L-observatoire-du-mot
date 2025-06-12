import streamlit as st #https://www.youtube.com/watch?v=D0D4Pa22iG0
import pandas as pd

st.title("L'Observatoire du mot")

#columns gestion

st.write("Bienvenue dans l'_Observatoire du mot_ !")

mot_entree = st.text_input("Quel mot souhaites-tu observer ?", "sensible") #on capture la valeur de l'entrée dans la variable mot_entree
#Valeur par défaut = ???

#is_clicked = st.button("Click Me")


st.write("Voir les fichiers csv créés pendant que le Excel se génère : ")

#synonymes et score de proximité
from synonymes import exportation_synonymes
exportation_synonymes(mot_entree)
st.write(pd.read_csv("data/synonymes.csv").head())

from fiche_lexicale import recup_fiche_lexicale
recup_fiche_lexicale(mot_entree)
st.write(pd.read_csv("data/definitions.csv").head())
st.write(pd.read_csv("data/prononciation.csv").head())
st.write(pd.read_csv("data/etymologies.csv").head())
st.write(pd.read_csv("data/citations.csv").head())

#from titres_oeuvres_art import rechercher_oeuvres_wikidata
#rechercher_oeuvres_wikidata(mot_entree)
#st.write(pd.read_csv("data/titres_oeuvres_art.csv").head())

from twitter import recherche_twitter
recherche_twitter(mot_entree)
st.write(pd.read_csv("data/tweets_avec_mot.csv").head())
st.write(pd.read_csv("data/score_de_popularite.csv").head())

from flux_rss import recup_articles
recup_articles(mot_entree)
st.write(pd.read_csv("data/actualite_avec_mot.csv").head())

#graphique ! https://docs.streamlit.io/develop/api-reference/charts
st.bar_chart()
st.line_chart()

#multi pages

#
st.link_button("Profile", url="https://github.com/Aminata-Dev")