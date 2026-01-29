# User Guide

To launch the dashboard, run the following command at the root of the project :

```python
python main.py
```
Une fois la commande exécutée, un lien s'affiche dans le terminal.
Faire : CTRL+CLIC et cela s'ouvre dans votre naviagteur par défaut.
La navbar permet de naviguer dans le dashboard ou sur la page about.
Les 2 premiers graphiques, à l'international (GII dans le monde et femme dans les STEM), sont dynamiques vous pouvez sélectionner le format d'affichage des données (carte ou histogramme). Ensuite vous avez accès à 2 autres graphiques sur la France (écart des études, et écart de salaire entre femmes et hommes + disponible sous forme de carte ou d'histogramme également). Enfin vous avez 2 histogrammes sur les secteurs d'études des femmes en Frances (niveau bachelor ou doctorat).

# Data

### Description des données et traitements 

Les données viennent de *kaggle.com* pour **l'indicateur GII (Gender Inequality Index) à l'internationale**. Les données s'étalent de 1999 à 2018. Et nos données sont dans des fichiers csv. Pour faire notre graphique, nous avons utilisé les code ISO3 de chaque pays, les continents, et le GII de chaque année avec l'année. Nous avons d'ailleurs dû séparer les 2 :

```python
gii_columns = []    
for col in df.columns :
    if col.startswith("Gender Inequality Index") :
        gii_columns.append(col)

df_long = df.melt(
    id_vars=['ISO3', 'Country', 'Continent'],  
    value_vars=gii_columns,                                  
    var_name='Year',                                         
    value_name='GII'                                         
)
df_long['Year'] = df_long['Year'].str.extract(r'(\d{4})').astype(int)
```
La plage des années s'étalent de 1998 à 2018, ce qui nous permet d'avoir une évolution dans le monde sur 20 ans.

Pour **les femmes dans les STEM (Science, Technology, Engineering, Math) à l'internationale**, nous avons empreinté nos données sur *ourworldindata.org*. Le fichier est sous format csv et nous avons utilisé le code pays (code ISO3), pays, années et le pourcentage de femmes dans les STEM. La plage des années s'étalent de 1999 à 2018, ce qui nous permet d'avoir une évolution dans le monde sur presque 20 ans.

Ensuite pour nos 2 graphiques d'après portant sur **les écart d'études et salariales france**, viennent de *insee. fr*. Le format à l'origine est xlsx, étant donné que les convertisseurs en ligne ne fonctionnait pas, nous avons solliciter claude.ai pour nous générer un convertisseur spécifiquement pour notre fichier et le mettre au format csv. Les données datent respectivement de 2021 et 2022.

De même pour les **2 histogrammes portant sur les secteurs d'études des femmes en France** viennent de *insee.fr*. Le format à l'origine est xlsx, nous avons donc dû utiliser un convertisseur en ligne pour le mettre au format csv. Les données datent des années scolaires 2010-2011 et 2020-2021 pour les 2 histogrammes.

# Developer Guide

### Architecture du projet

Le programme principal appelle différentes fonctions responsables de tâches spécifiques qui sont chacune regroupée dans des fichiers python bien spécifique, au sein de dossiers, de manière à ce que notre projet soit bien structuré :

### Organisation du projet

```text
DASHBOARD_GENDER_GAP
│
├── data/                          # Données utilisées dans le projet
│   ├── cleaned/                   # Données nettoyées et prêtes à l’analyse
│   │   ├── fr_regions_gender_inequality_cleaned.csv
│   │   └── world_boundaries_simplified.geojson
│   │
│   └── raw/                       # Données brutes (non modifiées)
│       ├── countries.geojson
│       ├── fr_departments.geojson
│       ├── fr_gender_distribution.xlsx
│       ├── fr_regions_gender_inequality.csv
│       ├── fr_regions_gender_inequality.xls
│       ├── fr_research_women_feuille1.csv
│       ├── fr_research_women_feuille2.csv
│       ├── share-graduates-stem-female.csv
│       ├── share-graduates-stem-female_metadata.json
│       ├── world_boundaries.geojson
│       ├── world_GII.csv
│       └── world_women_in_stem.csv
│
├── src/                           # Code source du dashboard
│   ├── assets/                    # Ressources (font, images, css)
│   │   ├── fonts/                 # Polices utilisées
│   │   ├── images/                # Images utilisées dans le dashboard
│   │   └── style.css              # Feuille de style
│   │
│   ├── charts/                    # Code de création des graphiques
│   │   ├── fr_board.py
│   │   ├── fr_histogram.py
│   │   ├── fr_map.py
│   │   ├── fr_phd.py
│   │   ├── fr_university.py
│   │   ├── gii_board.py
│   │   ├── gii_histogram.py
│   │   ├── gii_world_map.py
│   │   ├── slider.py
│   │   ├── stem_histogram.py
│   │   └── stem_world_map.py
│   │
│   ├── components/                # Composants réutilisables de l’interface
│   │   ├── header.py
│   │   ├── footer.py
│   │   ├── navbar.py
│   │   └── card.py
│   │
│   ├── pages/                     Pages du dashboard
│   │   ├── about.py               # Page about
│   │   ├── home.py                # Page d’accueil
│   │   └── world_analysis.py      # Analyse à l’échelle mondiale
│   │
│   ├── graphics/                  # Graphiques d'origines
│   │
│   └── utils/                      # Fonctions utilitaires
│       ├── get_data.py             # Chargement des données
│       └── clean_data.py           # Nettoyage des données
│
├── config.py                      # Paramètres de configuration
├── main.py                        # Point d’entrée du dashboard
├── requirements.txt               # Dépendances du projet
├── README.md                      # Documentation
└── .gitignore
``` 
### Ajouter un nouveau graphique

1. Créer un nouveau fichier dans DASHBOARD_GENDER_GAP/src/charts 
2. Créer une fonction layout 
3. Faire l'import de cette fonction dans la page *home.py*

Ex :
```python
from src.charts.gii_histogram import layout as gii_bar_layout
```
4. L'ajouter dans la fonction layout de la page *home.py*

### Ajouter une nouvelle page



# Analysis Report

L'analyse des données met en évidence plusieurs aspects de l'égalité entre les hommes et les femmes dans le monde et en France.

### Dans le monde 

- Les données sur le GII révèlent que les pays les plus "riches" montrent un taux d'inégalité faible, contrairement aux pays les plus "pauvres". 
- Les pays les plus "pauvres" sont moins touchés par un faible taux de femmes dans les STEM, contrairement aux pays "riches"

# Copyright