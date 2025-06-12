from unidecode import unidecode
import pandas as pd

def recherche_twitter(mot):
    
    df = pd.read_csv('data/french_tweets_mini.csv') #le fichier csv a été réduit à 50000 observations pour permettre le stockage sur Github
    mot_normalise = unidecode(mot.lower()) #Les tweets du fichier csv ont subit les mêmes opérations (unicode + lower)

    nbr_tweets = df.shape[0]
    tweets_avec_mot = df[df["tweets"].str.contains(mot_normalise)] 

    
    #print(tweets_avec_mot)
    frequence_mot = tweets_avec_mot.shape[0]
    
    #print(nbr_tweets, frequence_mot)
    
    #Si le mot choisi apparaît autant de fois dans les tweets que la moitié du nombre de tweets de notre dataset, on considère qu'il mérite le score maximum et son score de popularité est de 100%.
    score_popularite = (
        (frequence_mot/ (nbr_tweets/2) )
        *100
    )
    
    #print(f"Popularité du mot '{mot}' : {round(score_popularite, 2)} %")
    #exemple : Popularité du mot 'je' : 25.9 %

    from exportation_csv import exporter_donnees_csv

    exporter_donnees_csv(
        {"mot":[mot],
        "score_de_popularite":[score_popularite]},
        "score_de_popularite.csv"
    )

    tweets_avec_mot.to_csv("data/tweets_avec_mot.csv")

    return score_popularite

#print(recherche_twitter("je"))
assert recherche_twitter("cree") == recherche_twitter("créé")
#test : recherche_twitter("creativite")