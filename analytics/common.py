"""
Socle partagé permettant de nettoyer et d'extraire les informations pertinentes des requêtes.
"""

import json
from pathlib import Path
import pandas as pd

# Chemins relatifs à ce fichier
ANALYTICS_DIR = Path(__file__).resolve().parent
REPO_ROOT = ANALYTICS_DIR.parent
DATA_DIR = ANALYTICS_DIR / "data"
OUTPUT_DIR = ANALYTICS_DIR / "output"
GRAPH_DIR = REPO_ROOT / "backend/score_calculation_it/output_data/network/graph"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


LYON_ARRONDISSEMENTS = {
    "69001": "Lyon 1er Arrondissement",
    "69002": "Lyon 2ème Arrondissement",
    "69003": "Lyon 3ème Arrondissement",
    "69004": "Lyon 4ème Arrondissement",
    "69005": "Lyon 5ème Arrondissement",
    "69006": "Lyon 6ème Arrondissement",
    "69007": "Lyon 7ème Arrondissement",
    "69008": "Lyon 8ème Arrondissement",
    "69009": "Lyon 9ème Arrondissement",
}


def normalize_city(city, postcode):
    """
    Pour régler le pb quand il y a écrit "Lyon" alors que le postcode donne bien l'arrondissement
    Cas aussi traité de la fusion de Oullins et Pierre-Bénite (qui sont fusionnées dans OSM)
    """
    city = str(city).strip()
    postcode = str(postcode).strip()

    if postcode in LYON_ARRONDISSEMENTS:
        return LYON_ARRONDISSEMENTS[postcode]

    if city == "Oullins":
        return "Oullins-Pierre-Bénite"

    return city




def parse_requete(requete_matomo):
    """
    Retourne un dict JSON si c'est une requête valide avec start+end, None sinon.
    """
    if not requete_matomo.strip().startswith("{"): # si autre requete
        return None
    
    data = json.loads(requete_matomo.strip())

    start = data.get("startAddress")
    end = data.get("endAddress")

    if start is None or end is None: # on ne considère pas si pas de O-D précis
        return None

    return data




def flatten_address(addr, prefix):
    """
    Retourne un dict avec les colonnes aplaties pour l'adresse donnée (start ou end)
    """
    props = addr.get("properties", {})
    coords = addr.get("geometry", {}).get("coordinates", [None, None])
    city = normalize_city(props.get("city", ""), props.get("postcode", ""))
    return {
        f"{prefix}_lon":            coords[0],
        f"{prefix}_lat":            coords[1],
        f"{prefix}_name":           props.get("name", ""),
        f"{prefix}_street":         props.get("street", ""),
        f"{prefix}_housenumber":    props.get("housenumber", ""),
        f"{prefix}_postcode":       props.get("postcode", ""),
        f"{prefix}_city":           city,
        f"{prefix}_countrycode":    props.get("countrycode", ""),
        f"{prefix}_osm_id":         props.get("osm_id"),
        f"{prefix}_insee":          props.get("extra", {}).get("insee", ""),
        f"{prefix}_metropole":      props.get("extra", {}).get("metropole", ""),
        f"{prefix}_espacepublic":   props.get("extra", {}).get("espace_public", "")
    }



def load_requetes(save_clean=False):
    """
    Charge data/requetes.csv, nettoie et aplatit les adresses, et retourne un DataFrame.

    Le False permet de ne pas réécrire le fichier à chaque fois, seul le lancement de ce fichier génère le fichier nettoyé.
    """
    df_raw = pd.read_csv(DATA_DIR/"requetes.csv", encoding="utf-16")

    # Aplatissement
    rows = []
    for _, row in df_raw.iterrows():
        parsed = parse_requete(row.get("Nom", "")) # Nom est la colonne du csv contenant le JSON de la requête
        if parsed is None:
            continue
        rows.append({
            **flatten_address(parsed["startAddress"], "start"),
            **flatten_address(parsed["endAddress"],   "end"),
            "criteria": json.dumps(parsed.get("criteria", []), ensure_ascii=False),
            **{k: v for k, v in row.items() if k != "Nom"}
        })

    df = pd.DataFrame(rows)

    if save_clean:
        df.to_csv(OUTPUT_DIR/"requetes_clean.csv", index=False, encoding="utf-8")

    return df

if __name__ == "__main__":
    df = load_requetes(save_clean=True)