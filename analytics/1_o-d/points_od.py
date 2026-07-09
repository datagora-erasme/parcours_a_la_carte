"""
Cartes des points origine-destination avec transparence
Sortie : output/points_OD.html
"""
import sys
from pathlib import Path
import folium
sys.path.insert(0, str(Path(__file__).resolve().parent.parent)) # -> analytics/
from common import load_requetes, OUTPUT_DIR

centre_lyon = [45.75, 4.85] # coordonnées pour centrer la carte sur Lyon
couleur_depart = "#f46d43"  # orange
couleur_arrivee = "#2c7bb6"  # bleu

def ajoute_legende(m, entrees):
    """Ajout de la légende HTML"""
    items = "<br>".join(f'<span style="color:{c}">●</span> {label}' for c, label in entrees)
    
    html = f"""
    <div style="position:fixed; bottom:30px; left:30px; z-index:1000;
        background:white; padding:12px 16px; border-radius:8px;
        box-shadow:0 2px 8px rgba(0,0,0,0.2); font-family:sans-serif; font-size:12px;">
        <b>Légende</b><br>
    {items}
    </div>
    """

    m.get_root().html.add_child(folium.Element(html))


def carte_points(df):
    """
    Construit la carte des points de départ et d'arrivée avec transparence.
    """
    m = folium.Map(location=centre_lyon, zoom_start=11, tiles="CartoDB positron")

    for _, row in df.iterrows():
        # Cercle des départs
        folium.CircleMarker(
            location=[row["start_lat"], row["start_lon"]],
            radius=4, color=couleur_depart, fill=True, fill_color=couleur_depart,
            fill_opacity=0.5, weight=0, tooltip=row["start_city"],
        ).add_to(m)

        # Cercle des arrivées
        folium.CircleMarker(
            location=[row["end_lat"], row["end_lon"]],
            radius=4, color=couleur_arrivee, fill=True, fill_color=couleur_arrivee,
            fill_opacity=0.5, weight=0, tooltip=row["end_city"],
        ).add_to(m)
    ajoute_legende(m, [(couleur_depart, "Départ"), (couleur_arrivee, "Arrivée")])
    return m


def main():
    df = load_requetes()
    sortie = OUTPUT_DIR / "points_OD.html"
    carte_points(df).save(str(sortie))

if __name__ == "__main__":
    main()