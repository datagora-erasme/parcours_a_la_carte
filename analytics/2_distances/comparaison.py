"""
Comparaison des distances de trajet entre intra-Lyon et le reste de la Métropole
Sortie : output/distribution_distances_comparaison.png
"""
import sys
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
sys.path.insert(0, str(Path(__file__).resolve().parent.parent)) # -> analytics/
from common import load_requetes, OUTPUT_DIR, LYON_ARRONDISSEMENTS

ARRONDISSEMENTS_LYON = set(LYON_ARRONDISSEMENTS.values())

def charge_df_avec_distances():
    """Charge les requêtes et y rattache les distances calculées par distribution.py"""
    df = load_requetes()
    distances = pd.read_csv(OUTPUT_DIR/"distances.csv")
    # distances.csv est aligné par ordre avec load_requetes
    df["distance_km"] = distances["distance_km"].values
    return df

def separe_intra_lyon(df):
    """Sépare les trajets entièrement intra-lyon des autres"""
    intra_lyon = df["start_city"].isin(ARRONDISSEMENTS_LYON) & df["end_city"].isin(ARRONDISSEMENTS_LYON)
    return df[intra_lyon], df[~intra_lyon]

def trace_comparaison(intra_lyon, peripheries):
    """Deux histogrammes côte à côte : intra_lyon et le reste de la métropole"""
    fig, axes = plt.subplots(1, 2, figsize=(14, 5), sharey=True)
    axes[0].hist(intra_lyon["distance_km"].dropna(), bins=20, color="#2c7bb6", edgecolor="white")
    axes[0].set_title(f"Intra-Lyon ({len(intra_lyon)} trajets)")
    axes[0].set_xlabel("Distance (km)")
    axes[0].set_ylabel("Nombre de trajets")
    axes[1].hist(peripheries["distance_km"].dropna(), bins=20, color="#f46d43", edgecolor="white")
    axes[1].set_title(f"Autres Métropole ({len(peripheries)} trajets)")
    axes[1].set_xlabel("Distance (km)")
    plt.suptitle("Distribution des distances selon le type de trajet", fontsize=13)
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/distribution_distances_comparaison.png", dpi=150)

def main():
    df = charge_df_avec_distances()
    intra_lyon, peripherie = separe_intra_lyon(df)
    trace_comparaison(intra_lyon, peripherie)

    for categorie, groupe in [("Intra-Lyon", intra_lyon), ("Autres", peripherie)]:
        print(f"{categorie} :")
        print(f"  Médiane : {groupe['distance_km'].median():.2f} km")
        print(f"  Moyenne : {groupe['distance_km'].mean():.2f} km")

if __name__ == "__main__":
    main()