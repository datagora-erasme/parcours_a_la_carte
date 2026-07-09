# Analyse géographique des usages

Regroupement des scripts d'analyse des trajets demandés par les utilisateurs de l'application. À partir des requêtes réelles (exportées de Matomo), ils permettent de voir d'où partent et où vont les gens, et de comparer les itinéraires proposés selon chaque critère (pollen, fraîcheur, bruit, tourisme) au trajet le plus court.

## Avant de lancer

- Python 3.11 avec les dépendances : `pip install -r requirements.txt`
- Les graphes du réseau routier (produits par le backend) doivent être présents
  dans `backend/score_calculation_it/output_data/network/graph/`
  (`merged_network.pickle.gz` et `merged_network_multidigraph.pickle.gz`).

## Données utilisées (`data/`)

- `requetes.csv` — les requêtes des utilisateurs exportées de Matomo
- `communes.geojson` — le fond de carte des communes de la Métropole

## Comment lancer

Les scripts se lancent depuis la racine du projet, par exemple :

```bash
venv/bin/python analytics/common.py
venv/bin/python analytics/1_o-d/points_od.py
```

`common.py` est la base commune : il lit et nettoie les requêtes, et tous les
autres scripts s'en servent. `distribution.py` doit être lancé avant
`comparaison.py`, qui réutilise ses résultats.

## Ce que produit chaque script

| Script | Ce qu'il fait | Résultat (dans `output/`) |
|---|---|---|
| `common.py` | Nettoie les requêtes origine-destination | `requetes_clean.csv` |
| `1_o-d/points_od.py` | Points de départ et d'arrivée | `points_OD.html` |
| `1_o-d/flux_od.py` | Flux entre les villes (lignes de désir) | `desire_lines.html` |
| `1_o-d/choropleth.py` | Nombre de points par commune, par critère | `choropleth_<critère>.html` |
| `2_distances/distribution.py` | Distribution des distances de trajet | `distances.csv`, `distribution_distances.png` |
| `2_distances/comparaison.py` | Distances intra-Lyon vs reste de la métropole | `distribution_distances_comparaison.png` |
| `3_comparaison_itineraires/detours.py` | Segments évités ou détournés par un critère | `detours_<critère>.html` |

Pour `detours.py`, on peut préciser le ou les critères à calculer, par exemple
`... detours.py bruit` (sans argument, les 4 sont calculés, ce qui est long).

Le dossier `output/` n'est pas versionné : les résultats se régénèrent en
relançant les scripts.