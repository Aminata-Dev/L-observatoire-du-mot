from bs4 import BeautifulSoup
import requests
import csv

#NP
# Ajouter un assert pour vérifier que la longueur de synonymes trouvées est = au nombre affiché dans la page  et mettre à jour le notebook

#####Récupération des synonymes

#Choix du mot
mot_entree = "alambiqué"
#mot_entree = input("\nEntre un mot de ton choix\n@> ")

url = 'https://crisco4.unicaen.fr/des/synonymes/' + mot_entree
page = requests.get(url)

#bs4 permet de parser le contenu html d'une page 
soupe = BeautifulSoup(page.text, features="html.parser")

# print(soupe.prettify())


#####Récupération des synonymes

synonymes = []

#modèle : <a href="/des/synonymes/balle">balle</a>

#Nous ciblons la balise <table> car une simple recherche des balises a href va chercher des synonymes ailleurs dans le tableau identifié et la somme des synonmymes sera supérieure à au nombre de lignes du tableau

for balise_a in soupe.find('table').find_all('a', href=True):
    if "/des/synonymes/" in balise_a['href']:
        synonyme = (balise_a.text).replace('\xa0', '')
        #print(synonyme)
        synonymes.append(synonyme)
#print(synonymes)


#####Score de proximité

#modèle : <hr style="height:6px;width:14px;color:#4040C0;background-color:#4040C0;text-align:left;margin-left:0">

import re
tailles_barre = []

for hr in soupe.find_all('hr', style=True):
    #print(hr["style"])
    
    #extraction du nombre après "width:"
    match = re.search(r'width:(\d+)px', hr["style"])

    if match:
        width = int(match.group(1))
        #print(width)
    
    tailles_barre.append(width)
    
#####Vérifications
assert len(tailles_barre) == len(synonymes)

#modèle : <i class='titre'>18 synonymes</i>
for i in soupe.find_all('i', class_='titre'):

    #match_antonymes = re.search(r'(\d+) antonymes', i.contents[0])
    match_synonymes = re.search(r'(\d+) synonymes', i.text)

    #if match_antonymes:
    #    nbr_antonymes = int(match_antonymes.group(1))
    #    print(nbr_antonymes)
    if match_synonymes:
        nbr_synonymes = int(match_synonymes.group(1))
        #print(nbr_synonymes)

assert nbr_synonymes == len(synonymes)

#####Exportation csv

from exportation_csv import exporter_donnees_csv

synonymes_csv = {
    "mot": [mot_entree] *len(synonymes),
    "synonyme": synonymes,
    "score_proximite_mot": tailles_barre
}

exporter_donnees_csv(synonymes_csv, "synonymes.csv")