from unidecode import unidecode
import pandas as pd

def recherche_twitter(mot):
    
    df = pd.read_csv('data/french_tweets_mini.csv') #le fichier csv a été réduit à 50000 observations pour permettre le stockage sur Github
    mot_normalise = unidecode(mot.lower()) #Les tweets du fichier csv ont subit les mêmes opérations (unicode + lower)

    nbr_tweets = df.shape[0]
    tweets_avec_mot = df[df["tweets"].str.contains(mot_normalise)] 

    tweets_avec_mot.to_csv("data/tweets_avec_mot.csv")

    return tweets_avec_mot, nbr_tweets

#print(recherche_twitter("je"))
#assert recherche_twitter("cree").equals(recherche_twitter("créé"))
#test : recherche_twitter("creativite")