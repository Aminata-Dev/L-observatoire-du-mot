def calcul_score_de_popularite(mot):
    
    from twitter import recherche_twitter
    tweets_avec_mot, nbr_tweets = recherche_twitter(mot)

    frequence_mot_tweets = tweets_avec_mot.shape[0]
    #print(nbr_tweets, frequence_mot)
    
    #Si le mot choisi apparaît autant de fois dans les tweets que la moitié du nombre de tweets de notre dataset, on considère qu'il mérite le score maximum et son score de popularité est de 100%.
    score_popularite_twitter = (
        (frequence_mot_tweets/ (nbr_tweets/2) )
        *100
    )
    
    print(f"Popularité du mot '{mot}' sur Twitter : {round(score_popularite_twitter, 2)} %")
    #exemple : Popularité du mot 'je' : 79.04 %

    #####################################
    
    from reddit import posts_reddit_r_france
    reddit_posts_avec_mot = posts_reddit_r_france(mot)

    ups_sum = reddit_posts_avec_mot["ups"].sum()
    downs_sum = reddit_posts_avec_mot["downs"].sum()

    if downs_sum != 0: score_popularite_reddit = ups_sum / downs_sum
    else: score_popularite_reddit = 0.00

    print(f"Popularité du mot '{mot}' sur Reddit : {round(score_popularite_reddit, 2)} %")

    #######################################
    from exportation_csv import exporter_donnees_csv

    exporter_donnees_csv(
        {
            "mot":[mot],
            "score_de_popularite_twitter":[score_popularite_twitter],
            "score_de_popularite_reddit":[score_popularite_reddit]
        },
        "score_de_popularite.csv"
    )