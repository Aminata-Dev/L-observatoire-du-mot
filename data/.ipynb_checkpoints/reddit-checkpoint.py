import requests

def recup_reddit(mot):
    url = f"https://api.pushshift.io/reddit/search/comment/?q={word}&size=0&aggs=created_utc&frequency=month"
    r = requests.get(url)
    print(r.json())

recup_reddit("nuit")