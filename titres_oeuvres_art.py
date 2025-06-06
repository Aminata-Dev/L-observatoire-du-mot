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
          VALUES ?type {{ wd:Q3305213 wd:Q7725634 wd:Q11424 wd:Q482994}}. #peinture, oeuvres littéraires, film, album musical
          #wd:Q7725634 wd:Q11424 wd:Q482994
          ?oeuvre wdt:P31 ?type. #instance de l'ensemble de classe selectionné ci-dessus
          
          ?oeuvre rdfs:label ?oeuvreLabel. #Nous obtenons l'ensemble des libellés de nos oeuvres dans ?oeuvreLabel,
          FILTER(LANG(?oeuvreLabel) = "{langue}"). #nous restreignons les libellés aux libéllés français
          FILTER(CONTAINS(LCASE(?oeuvreLabel), "{mot.lower()}")). #...puis nous vérifions que les libéllés contiennent le mot en questions
          
          SERVICE wikibase:label {{ bd:serviceParam wikibase:language "{langue}". }} #Nous créons les libéllés des variables
        }}"""
    #Un f-string est une manière simple de créer des chaînes de caractères qui incluent des variables ou des expressions en les plaçant entre accolades dans une chaîne préfixée par f.

    #envoie de la requête et récupération du résultat en json
    headers = {"Accept": "application/sparql-results+json"}
    response = requests.get(url, params={"query": query}, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Erreur lors de la requête SPARQL : {response.status_code}")
    return response.json()

donnees = rechercher_oeuvres_wikidata("nuit") #mot-test choisi = nuit

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
    if 'http://www.wikidata.org/entity/' + item["oeuvre"]["value"] == "http://www.wikidata.org/entity/Q45585":
        print(item['oeuvreLabel']['value'])

print(repartition)
#print(repartition.items())
top_5 = dict(sorted(repartition.items(), key=lambda x: x[1], reverse=True)[0:5])
print(top_5)
#print(sorted(repartition.items(), key=lambda x: x[1], reverse=True))
print("Voyage au bout de la nuit" in noms_oeuvres)
print("La Nuit étoilée" in noms_oeuvres)
print("Le Songe d'une nuit d'été" in noms_oeuvres)