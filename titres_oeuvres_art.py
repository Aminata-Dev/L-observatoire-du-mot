import requests
import pandas as pd

def recherche_wikidata_oeuvres_art(mot):
    # Types d'œuvres : peinture, œuvre littéraire, film, album musical
    types_oeuvres = {
        "peinture": "wd:Q3305213",
        "oeuvre_litteraire": "wd:Q7725634",
        "film": "wd:Q11424",
        "album_musical": "wd:Q482994"
    }
    
    def requete_sparql_par_type(type_wikidata):
        """
        Recherche les titres d'œuvres contenant un mot via Wikidata (SPARQL).
        Retourne une liste de titres.
        """
        
        # Requête SPARQL : cherche des titres d'œuvres contenant le mot
        #Nous rendons notre requête la plus modulable possible grâce à l'ajout de f-string
        query = f"""
        SELECT ?typeLabel (COUNT(?oeuvre) AS ?nbr)
        WHERE {{
          VALUES ?type {{ {type_wikidata} }} #peinture, oeuvres littéraires, film, album musical /// wd:Q3305213 wd:Q7725634 wd:Q11424 wd:Q482994
    
          ?oeuvre wdt:P31 ?type. #instance de l'ensemble de classe selectionné ci-dessus
          
          ?oeuvre rdfs:label ?oeuvreLabel. #Nous obtenons l'ensemble des libellés de nos oeuvres dans ?oeuvreLabel,
          FILTER(LANG(?oeuvreLabel) = "fr"). #nous restreignons les libellés aux libéllés français
          FILTER(CONTAINS(LCASE(?oeuvreLabel), "{mot.lower()}")). #...puis nous vérifions que les libéllés contiennent le mot en questions
          
          #?oeuvre wdt:P166 ?prix.  #uniquement les œuvres primées pour éviter un trop grand nombre de résultats
    
          SERVICE wikibase:label {{ bd:serviceParam wikibase:language "fr". }} #Nous créons les libéllés des variables
    
        }}
        GROUP BY ?typeLabel
        LIMIT 450
        """
        #Un f-string est une manière simple de créer des chaînes de caractères qui incluent des variables ou des expressions en les plaçant entre accolades dans une chaîne préfixée par f.
    
        #envoie de la requête et récupération du résultat en json
        url = "https://query.wikidata.org/sparql"
        headers = {"Accept": "application/sparql-results+json"}
        response = requests.get(url, params={"query": query}, headers=headers)
        if response.status_code != 200:
            print(f"Erreur lors de la requête SPARQL : {response.status_code}")
            return False #Limit time exceeded
        return response.json()
    
    #lancement de la requête pour chaque type
    resultats = []
    for label, qid in types_oeuvres.items():
        json_data = requete_sparql_par_type(qid)
        if json_data: #False si pas de données trouvées
            bindings = json_data["results"]["bindings"]
            for res in bindings:
                nbr_type = {
                    "type": res["typeLabel"]["value"],
                    "nombre": int(res["nbr"]["value"])
                }
                resultats.append(nbr_type)
    
    #et fusion des résultats dans un DataFrame
    df_resultats = pd.DataFrame(resultats)
    
    df_resultats.to_csv("data/repartition_types_oeuvres_art.csv")
    return df_resultats