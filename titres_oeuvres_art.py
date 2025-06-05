import requests

def rechercher_oeuvres_wikidata(mot, langue="fr"):
    """
    Recherche les titres d'œuvres contenant un mot via Wikidata (SPARQL).
    Retourne une liste de titres.
    """
    url = "https://query.wikidata.org/sparql"
    
    # Requête SPARQL : cherche des titres d'œuvres contenant le mot
    #Nous rendons notre requête la plus modulable possible grâce à l'ajout de f-string
    query = f"""SELECT DISTINCT ?oeuvre ?oeuvreLabel ?typeLabel
        WHERE
        {{
            VALUES ?type_oeuvres_art_interet {{ wd:Q7725634 wd:Q2431196 wd:Q2188189}}.
  ?oeuvre wdt:P31/wdt:P279 ?type_oeuvres_art_interet. # instance de n'importe quelle sous-classe d'une œuvre d'art
          ?oeuvre wdt:P31 ?type.
          ?oeuvre rdfs:label ?oeuvreLabel. #Nous obtenons les libellés avec le triplet ?oeuvre rdfs:label ?oeuvreLabel,
          #FILTER(LANG(?oeuvreLabel) = "{langue}"). #nous restreignons les libellés aux libéllés français
          FILTER(CONTAINS(LCASE(?oeuvreLabel), "{mot.lower()}")). #...puis nous vérifions que les libéllés contiennent le mot-test "nuit".
          SERVICE wikibase:label {{ bd:serviceParam wikibase:language "{langue}". }}
        }}"""


    #expliquer succintement ce qu'est un f-string (1 phrase max)

    headers = {"Accept": "application/sparql-results+json"}
    response = requests.get(url, params={"query": query}, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"Erreur lors de la requête SPARQL : {response.status_code}")

    return response.json()

donnees = rechercher_oeuvres_wikidata("nuit")
table_requete = donnees["results"]["bindings"]

#voici à quoi ressemble une observation de notre table résultat :
print(table_requete[0])

noms_oeuvres = []
#Observons la répartition du type d'oeuvre
repartition = {}
for item in table_requete:
    type_oeuvre = item["typeLabel"]["value"]
    repartition[type_oeuvre] = repartition.get(type_oeuvre, 0) + 1
    noms_oeuvres.append(item['oeuvreLabel']['value'])

print(repartition)
print("Voyage au bout de la nuit" in noms_oeuvres)
print("La Nuit étoilée" in noms_oeuvres)
print("Le Songe d'une nuit d'été" in noms_oeuvres)