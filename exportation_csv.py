import pandas as pd
import os

def exporter_donnees_csv(donnees: dict[str, list], nom_fichier: str, index=False) -> None:
    """
    Exporte un dictionnaire de données en fichier CSV.
    
    - donnees : dictionnaire {nom_colonne: liste_valeurs}
    - nom_fichier : nom du fichier csv à créer (ex: "synonymes.csv")
    """

    #création du chemin où sont stockés les données...
    chemin_dossier = 'data'
    chemin_complet = os.path.join(chemin_dossier, nom_fichier)
    #... et création du sous-dossier data s'il n'existe pas
    os.makedirs(chemin_dossier, exist_ok=True)

    df = pd.DataFrame(donnees)
    df.to_csv(chemin_complet, index=index)
