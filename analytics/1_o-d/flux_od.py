"""
Lignes de désir (desire lines) : flux origine-destination agrégés entre villes / arrondissements
Sortie : output/desire_lines.html
"""
import sys
from pathlib import Path
import folium
import numpy as np
import pandas as pd
sys.path.insert(0, str(Path(__file__).resolve().parent.parent)) # -> analytics/
from common import load_requetes, OUTPUT_DIR

centre_lyon = [45.75, 4.85]
seuil_volume = 3            # 3 trajets minimum pour afficher un flux
seuil_asymetrie = 0.7       # au-delà de 70% de part en départ/arrivé on trace une flèche


def centroides_villes(df):
    """Coordonnées moyenne de chaque ville"""
    depart = df.groupby("start_city")[["start_lat", "start_lon"]].mean()
    arrivee = df.groupby("end_city")[["end_lat",   "end_lon"]].mean()

    return pd.concat([
        depart.rename(columns={"start_lat": "lat", "start_lon": "lon"}),
        arrivee.rename(columns={"end_lat":   "lat", "end_lon":   "lon"}),
    ]).groupby(level=0).mean()

def volumes_villes(df):
    """Nb de départ/arrivées par ville et ratio départs/(départs+arrivées)"""
    depart = df.groupby("start_city").size().rename("departs")
    arrivee = df.groupby("end_city").size().rename("arrivees")
    vol = pd.concat([depart, arrivee], axis=1).fillna(0)
    vol["ratio"] = vol["departs"] / (vol["departs"] + vol["arrivees"])
    return vol


def flux_od(df, seuil):
    """Flux agrégés entre villes différentes, filtrés au seuil de volume"""
    od = (
        df.groupby(["start_city", "end_city"]).size()
        .reset_index(name="count")
        .query("start_city != end_city")
        .query(f"count >= {seuil}")
        .sort_values("count")
    )

    # Table indexé (départ, arrivée) -> count, pour retrouver le sens inverse en O(1)
    counts = od.set_index(["start_city", "end_city"])["count"]
    
    od["reverse_count"] = [counts.get((d, o), 0) for o, d in zip(od["start_city"], od["end_city"])]
    od["ratio_asymetrie"] = od["count"] / (od["count"] + od["reverse_count"])
    return od


def trace_flux(m, od, coords):
    """Trace les lignes de flux, avec une flèche si l'asymétrie dépasse le seuil"""
    count_max = od["count"].max()
    for _, row in od.iterrows():
        o, d, count = row["start_city"], row["end_city"], row["count"]
        if o not in coords.index or d not in coords.index:
            continue
        lat_o, lon_o = coords.loc[o, "lat"], coords.loc[o, "lon"]
        lat_d, lon_d = coords.loc[d, "lat"], coords.loc[d, "lon"]

        folium.PolyLine(
            locations=[[lat_o, lon_o], [lat_d, lon_d]],
            weight=0.8 + 3 * (count / count_max),
            color="#2c7bb6",
            opacity=0.15 + 0.6 * (count / count_max),
            tooltip=f"{o} → {d} : {count} trajets",
        ).add_to(m)

        if row["ratio_asymetrie"] > seuil_asymetrie:
            angle = -np.degrees(np.arctan2(lat_d - lat_o, lon_d - lon_o))
            folium.Marker(
                location=[(lat_o + lat_d) / 2, (lon_o + lon_d) / 2],
                icon=folium.DivIcon(
                    html=f'<div style="font-size:16px; color:#2c7bb6; transform: rotate({angle}deg);">➤</div>',
                    icon_size=(20, 20), icon_anchor=(10, 10),
                ),
                tooltip=f"{o} -> {d} : {count} trajets",
            ).add_to(m)

def trace_villes(m, coords, vol):
    """Place les villes, colorées selon leur profil"""
    for city, row in coords.iterrows():
        if city not in vol.index:
            continue
        ratio = vol.loc[city, "ratio"]
        departs = int(vol.loc[city, "departs"])
        arrivees = int(vol.loc[city, "arrivees"])

        if ratio > 0.6:
            color = "#f46d43"
            label = "départ"
        elif ratio < 0.4:
            color = "#74add1"
            label = "arrivée"
        else:
            color = "#888888"
            label = "mixte"

        folium.CircleMarker(
            location=[row["lat"], row["lon"]],
            radius=7, color="white", weight=1.5, fill=True,
            fill_color=color, fill_opacity=0.9,
            tooltip=f"{city} — {departs} départs · {arrivees} arrivées ({label})",
        ).add_to(m)
        folium.Marker(
            location=[row["lat"] + 0.003, row["lon"]],
            icon=folium.DivIcon(
                html=f'<div style="font-size:10px; font-weight:600; color:#333; white-space:nowrap;">{city}</div>',
                icon_size=(200, 20), icon_anchor=(0, 0),
            ),
        ).add_to(m)

def ajoute_legende(m):
    """Légende expliquant les couleurs et les seuils"""
    html = f"""
    <div style="position:fixed; bottom:30px; left:30px; z-index:1000;
        background:white; padding:12px 16px; border-radius:8px;
        box-shadow:0 2px 8px rgba(0,0,0,0.2); font-family:sans-serif; font-size:12px;">
    <b>Villes</b><br>
    <span style="color:#f46d43">●</span> Plutôt départ<br>
    <span style="color:#74add1">●</span> Plutôt arrivée<br>
    <span style="color:#888">●</span> Mixte<br><br>
    <b>Flux</b><br>
    <span style="color:#2c7bb6">—</span> Épaisseur = volume<br>
    ➤ Flèche si flux &gt; {seuil_asymetrie * 100}% dans un sens<br>
    Seuil : ≥ {seuil_volume} trajets
    </div>
    """
    m.get_root().html.add_child(folium.Element(html))


def main():
    df = load_requetes()
    coords = centroides_villes(df)
    vol = volumes_villes(df)
    od = flux_od(df, seuil_volume)

    m = folium.Map(location=centre_lyon, zoom_start=12, tiles="CartoDB positron")
    trace_flux(m, od, coords)
    trace_villes(m, coords, vol)
    ajoute_legende(m)

    sortie = OUTPUT_DIR / "desire_lines.html"
    m.save(str(sortie))

if __name__ == "__main__":
    main()