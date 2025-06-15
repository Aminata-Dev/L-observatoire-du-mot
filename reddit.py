import pandas as pd

def posts_reddit_r_france(mot):

    # URL du fichier CSV sur GitHub
    url = "https://raw.githubusercontent.com/umbrae/reddit-top-2.5-million/master/data/france.csv"
    
    # Lire le fichier CSV directement depuis l'URL
    df = pd.read_csv(url)
    
    df["annee"] = pd.to_datetime(df["created_utc"]).dt.year #conversion objet temps puis extraction de l'année
    
    # Afficher les premières lignes du DataFrame
    df.head()
    
    #filtrer les lignes où 'selftext' ou 'title' contenant le mot
    reddit_posts_avec_mot = df[
        df['selftext'].dropna().str.contains(mot.lower(), na=False) |
        df['title'].str.contains(mot.lower(), na=False)
    ] #rq : selftext contient des navalues qui empêchent le calcul si ces lignes ne sont pas exclus de la recherche sur le contenu des posts

    reddit_posts_avec_mot.to_csv(f"data/reddit_posts_avec_mot.csv")
    
    return reddit_posts_avec_mot