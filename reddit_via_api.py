import praw
import pandas as pd


import os
from dotenv import load_dotenv

load_dotenv()  # Charge les variables depuis .env

#https://www.reddit.com/prefs/apps/
reddit = praw.Reddit(
    client_id=os.getenv("CLIENT_ID"),
    client_secret=os.getenv("CLIENT_SECRET"),
    user_agent=os.getenv("USER_AGENT")
)

#documentation : https://praw.readthedocs.io/en/stable/code_overview/models/subreddit.html

#rechercher des posts Reddit contenant le mot
mot = "créativité"
submissions = reddit.subreddit("all").search(mot, sort="hot", limit=100) #voir image documentation

#...et récupération des données dans un dataframe pandas
donnees = []
for post in submissions:
    donnees.append({
        "titre": post.title,
        "texte": post.selftext,
        "subreddit": post.subreddit.display_name,
        "score": post.score,
        "date": pd.to_datetime(post.created_utc, unit="s")
    })

df = pd.DataFrame(donnees)
df.to_csv(f"data/reddit_top_posts_avec_mot.csv")