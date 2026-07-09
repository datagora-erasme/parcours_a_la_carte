"""
Cartes choroplèthes du nombre de points o-d par commune / arrondissements.
Sorties : output_choropleth_{critere}.html (un fichier par critère)
"""
import re
import sys
from pathlib import Path
import geopandas as gpd
import folium
sys.path.insert(0, str(Path(__file__).resolve().parent.parent)) # -> analytics/
from common import load_requetes, DATA_DIR, OUTPUT_DIR

centre_lyon = [45.75, 4.85]
criteres = ["pollen", "frais", "bruit", "tourisme"]
palettes = {"pollen":"YlGn", "frais":"Blues", "bruit":"Oranges", "tourisme":"Reds"}

def normalize_commune(nom):
    """Uniformise le geojson sur ceux du df"""
    match = re.match(r"Lyon (\d+)(?:er|e)\s+Arrondissement", nom, re.IGNORECASE)
    if match:
        n = int(match.group(1))
        suffix = "er" if n == 1 else "ème"
        return f"Lyon {n}{suffix} Arrondissement"
    if nom == "Oullins":
        return "Oullins-Pierre-Bénite"
    return nom

def short_name(nom):
    """Pour la lisbilité de la carte abrège 'Lyon 3ème Arrondisseent' en 'Lyon 3'"""
    match = re.match(r"Lyon (\d+)(?:er|ème) Arrondissement", nom)
    return f"Lyon {match.group(1)}" if match else nom

def charge_communes():
    """Charge le fond de carte"""
    communes = gpd.read_file(DATA_DIR/"communes.geojson").to_crs(epsg=4326)
    communes["nom_norm"] = communes["nom"].apply(normalize_commune)
    return communes

def compte_od_par_commune(df, critere):
    """Nombre de points O-D par commune"""
    df_c = df[df["criteria"].str.contains(critere)]
    total = (df_c.groupby("start_city").size()
             .add(df_c.groupby("end_city").size(), fill_value=0)
             .reset_index())
    total.columns = ["nom_norm", "count"]
    return total


def genere_carte_critere(df, communes, critere):
    """Consrtuit et renvoie la carte choroplèthe d'un critère"""
    total = compte_od_par_commune(df, critere)
    communes_count = communes.merge(total, on="nom_norm", how="left")
    communes_count["count"] = communes_count["count"].fillna(0)

    m = folium.Map(location=centre_lyon, zoom_start=11, tiles="CartoDB positron")
    folium.Choropleth(
        geo_data=communes_count.__geo_interface__,
        data=communes_count,
        columns=["nom_norm", "count"],
        key_on="feature.properties.nom_norm",
        fill_color=palettes[critere],
        fill_opacity=0.7,
        line_opacity=0.3,
        legend_name=f"Nombre de points O-D '{critere}'",
        nan_fill_color="white",
    ).add_to(m)

    # seule les 10 communes majoritaires auront leur étiquette car trop de chevauchement sinon
    top10 = set(communes_count.nlargest(10, "count")["nom_norm"])
    for _, row in communes_count.iterrows():
        if row["count"] > 0:
            centroid = row["geometry"].centroid
            if row["nom_norm"] in top10:
                html = f'<div style="font-size:9px; font-weight:bold; color:#333; white-space:nowrap;">{short_name(row["nom_norm"])}<br>{int(row["count"])}</div>'
            else:
                html = f'<div style="font-size:9px; color:#333;">{int(row["count"])}</div>'
            
            folium.Marker(
                location=[centroid.y, centroid.x],
                icon=folium.DivIcon(html=html, icon_size=(150, 30), icon_anchor=(20, 5),),
            ).add_to(m)

    return m

def main():
    df = load_requetes()
    communes = charge_communes()
    for critere in criteres:
        sortie = OUTPUT_DIR / f"choropleth_{critere}.html"
        genere_carte_critere(df, communes, critere).save(str(sortie))

if __name__ == "__main__":
    main()