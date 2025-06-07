import pandas as pd

def recherche_twitter(mot):
    
    df = pd.read_csv('data/french_tweets.csv') 
    df = df[["text"]]
    df["text"] = df["text"].str.lower()

    
    nbr_tweets = df.shape[0]
    tweets_avec_mot = df[df["text"].str.contains(mot)]
    
    print(tweets_avec_mot)
    frequence_mot = tweets_avec_mot.shape[0]
    
    #print(nbr_tweets, frequence_mot)
    
    #Si le mot choisi apparaissait autant de fois dans les tweets que le nombre de tweets de notre dataset, on considérait qu'il mérite le score maximum et son score de popularité serait 100%.
    score_popularite = ((frequence_mot/nbr_tweets)*100)
    
    #print(f"Popularité du mot '{mot}' : {round(score_popularite, 2)} %")
    #exemple : Popularité du mot 'je' : 25.9 %

    from exportation_csv import exporter_donnees_csv

    exporter_donnees_csv(
        {"mot":[mot],
        "score":[score_popularite]},
        "score_de_popularite.csv"
    )

    tweets_avec_mot.to_csv("data/tweets_avec_mot.csv")

    return score_popularite

recherche_twitter("creativite")