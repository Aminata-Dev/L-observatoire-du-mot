import feedparser
import pandas as pd

def recup_articles(mot):

    #Les flux RSS possèdent tous la même structure
    #Il est donc simple de récupérer les informations souhaitées provenant de plusieurs sources différentes sans ne créer d'exception
    def filtrer_articles_rss(url_flux, mot):
        # Lecture du flux
        flux = feedparser.parse(url_flux)
        
        # Liste pour stocker les articles filtrés
        articles = []
    
        # Parcours des articles
        
        
        for entree in flux.entries:
            #documentation W3C > The get() method returns the value of the item with the specified key + Optional : a value to return if the specified key does not exist.
            titre = entree.get("title", "")
            description = entree.get("description", "")
            if (mot.lower() in titre.lower()) or (mot.lower() in description.lower()):
                articles.append({
                    "titre": titre,
                    "date": entree.get("published", ""),
                    "description": description,
                    "lien": entree.get("link", "")
                })
    
        return pd.DataFrame(articles)

    flux_list = [    
        #depuis la liste initiale
        "https://www.lemonde.fr/actualite-medias/rss_full.xml", #Le Monde #validé "france"
        "https://www.lemonde.fr/culture/rss_full.xml", #Le Monde 
        "https://www.liberation.fr/arc/outboundfeeds/rss/category/economie/medias/?outputType=xml", #Libération #validé "france"
        "https://www.lefigaro.fr/rss/figaro_medias.xml", #Le Figaro #validé "france"
        "https://bsky.app/profile/did:plc:2egpzsea27fru2vkrjgdw2ob/rss", #MediaPart
        #Le monde diplomatique
        "https://www.courrierinternational.com/feed/rubrique/ecrans/rss.xml", #Courrier international #validé "france"
        #Huffington Post
        #Canard Enchaîné
        "https://www.humanite.fr/sections/medias/feed", #L'humanité #validé "france"
        "https://www.nouvelobs.com/rss.xml",  #L'obs #validé "ukraine"
    
        #Autres
        "https://www.afp.com/fr/rss.xml", #AFP #validé "le"
    
        #Nous demandons ensuite à un LLM d'en générer le maximum sans ne regarder un par un la validité des liens
        # Culture, musique, littérature
        "https://actualitte.com/feed",                          # ActuaLitté (littérature)
        "https://www.lesinrocks.com/musique/feed/",             # Les Inrocks Musique
        "https://www.rollingstone.fr/feed/",                    # Rolling Stone France
        "https://www.telerama.fr/rss.xml",                      # Télérama
        "https://www.franceculture.fr/rss.xml",                 # France Culture
    
        # Sciences humaines et philo
        "https://www.philomag.com/rss.xml",                     # Philosophie Magazine
        "https://www.scienceshumaines.com/rss.xml",             # Sciences Humaines
    
        # Autres journaux généralistes
        "https://www.francetvinfo.fr/titres.rss",               # France Info
        "https://www.radiofrance.fr/podcasts",                  # Radio France
        "https://www.ouest-france.fr/rss-en-continu.xml",       # Ouest-France
        "https://www.sudouest.fr/rss.xml",                      # Sud-Ouest
        "https://www.ladepeche.fr/rss.xml",                     # La Dépêche
        "https://www.midilibre.fr/rss.xml",                     # Midi Libre
        "https://www.lavoixdunord.fr/rss.xml",                  # La Voix du Nord
        "https://www.nicematin.com/rss",                        # Nice Matin
        "https://www.20minutes.fr/rss/actu-france.xml",         # 20 Minutes
        "https://www.france24.com/fr/rss",                      # France 24
    
        # Médias alternatifs et indépendants
        "https://www.bastamag.net/spip.php?page=backend",       # Basta!
        "https://www.arretsurimages.net/rss/articles",          # Arrêt sur Images
        "https://www.acrimed.org/spip.php?page=backend",        # Acrimed
    
        # Médias francophones internationaux
        "https://ici.radio-canada.ca/rss/4159",                 # Radio-Canada
        "https://www.rfi.fr/fr/rss",                            # RFI
        "https://www.tv5monde.com/rss/actualites",              # TV5Monde
    
        # Humour et satire
        "https://www.legorafi.fr/feed/",                        # Le Gorafi
    
        # Podcasts (audio)
        "https://feeds.acast.com/public/shows/61e6d2548e88e00012e13d0d",  # Programme B (Binge)
        "https://rss.art19.com/le-code-a-change"              # Le code a changé (Slate)
        
    ]
    
    df_total = pd.DataFrame()
    
    for flux in flux_list:
        df_flux = filtrer_articles_rss(flux, mot)
    
        #fusion du df obtenu avec le df total (concaténation ligne par ligne)
        df_total = pd.concat([df_total, df_flux], ignore_index=True)

    if not df_total.empty: #pour éviter les indexages de colonnes qui n'existent pas
        #conversion objet temps puis extraction de l'année
        df_total["annee"] = pd.to_datetime(df_total["date"], errors='coerce', utc=True).dt.year
        
        #suppression formattage balises html : nous souhaitons supprimer le formattage html grâce à bs4 pour la lisibilité et l'intégration au verbatim
        from bs4 import BeautifulSoup
    
        textes_propres = []
        for description_html in df_total["description"].values:
            soup = BeautifulSoup(description_html, "html.parser")
            texte_propre = soup.text.strip()
            textes_propres.append(texte_propre)
        
        df_total["description"] = textes_propres

    #exportation
    df_total.to_csv("data/actualite_avec_mot.csv")
    
    return df_total