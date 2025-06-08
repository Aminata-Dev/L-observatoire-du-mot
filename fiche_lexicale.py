import requests
from bs4 import BeautifulSoup
from exportation_csv import exporter_donnees_csv

def recup_fiche_lexicale(mot):
    """
    Définitions et étymologie sur CNRTL
    Prononciation, citations et traduction sur Wikitionary
    """

    #CNRTL
    url = f"https://www.cnrtl.fr/definition/{mot}"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')

    ##### Définitions
    definitions = []
    for span in soup.find_all("span", class_="tlf_cdefinition"):
        definitions.append(span.text)

    exporter_donnees_csv(
        {"mot": [mot] * len(definitions),
        "définition":definitions},
        "definitions.csv"
    )
    
    ##### Étymologie
    etymologies = []
    for span in soup.find_all("span", class_="tlf_ety"):
        etymologies.append(span.text)

    exporter_donnees_csv(
        {"mot": [mot] * len(etymologies),
        "etymologie":etymologies},
        "etymologies.csv"
    )
    
    #Wikitionary
    url = f"https://fr.wiktionary.org/wiki/{mot}"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    
    ##### Citations
    #modèle : <bdi lang="fr" class="lang-fr"><i>Le lendemain, ils ne se voyaient pas. Les couples restaient enfermés chez eux, à la diète, écœurés, abusant de cafés noirs et de cachets <b>effervescents</b>.</i></bdi>
    citations = []
    for bdi in soup.find_all("bdi", lang="fr", class_="lang-fr"):
        if bdi.get("about", "") != "#mwt10": #sinon prends des choses autres que des défintions dans la page
            try:
                citation = bdi.find("i").text
                #print(citation)
                citations.append(citation)
            except:pass #si pas de citations

    # print("\nCitations :")
    # for c in citations:
    #     print("-", c)
    
    exporter_donnees_csv(
        {"mot": [mot] * len(citations),
        "citation":citations},
        "citations.csv"
    )

    ##### Prononciation API
    #modèle prononciation : <span class="API" title="Prononciation API">\e.fɛʁ.ve.sɑ̃\</span></a>
    prononciation = mot
    for span in soup.find("span", class_="API",title="Prononciation API"): #le premier est le français, les autres concernent les traductions
        #print(span)
        prononciation = span.text

    exporter_donnees_csv(
        {"mot": [mot],
        "prononciation":[prononciation]},
        "prononciation.csv"
    )
    

recup_fiche_lexicale("alambiqué")

