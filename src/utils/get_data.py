import json
import csv
import pandas as pd
import geopandas as gpd

REGION_NAMES_FR = [
    'Île-de-France', 'Centre-Val de Loire', 'Bourgogne-Franche-Comté', 
    'Normandie', 'Hauts-de-France', 'Grand Est', 'Pays de la Loire', 
    'Bretagne', 'Nouvelle-Aquitaine', 'Occitanie', 'Auvergne-Rhône-Alpes',
    'Provence-Alpes-Côte d\'Azur', 'Corse', 'France métropolitaine hors Ile-de-France',
    'France métropolitaine', 'Guadeloupe', 'Martinique', 'Guyane', 'La Réunion',
    'DROM hors Mayotte', 'France hors Mayotte'
]

DISCIPLINE_TRANSLATION_PHD = {
    "Sciences exactes et leurs applications": "Exact fields",
    "Mathématiques et leurs interactions": "Mathematics",
    "Physique": "Physics",
    "Sciences de la Terre et de l'Univers, espace": "Earth & space",
    "Chimie et sciences des matériaux": "Chemistry & materials",
    "Sciences pour l'ingénieur": "Engineering",
    "Sciences et technologies de l'information et de la communication": "Computer science & ICT",
    "Sciences du vivant": "Life",
    "Biologie, médecine et santé": "Biology & health",
    "Sciences agronomiques et écologiques": "Agriculture & environment",
    "Sciences humaines et sociales": "Social",
    "Sciences humaines et humanités": "Humanities",
    "Sciences de la société": "Society",
    "Ensemble des doctorants": "All PhD"
}

DISCIPLINE_TRANSLATION_UNIVERSITY = {
    "Universités - Formations scientifiques y compris ingénieurs": "Engineering",
    "Sciences fondamentales et applications": "Fundamental",
    "Sciences de la Vie, de la santé, de la Terre et de l'Univers": "Life, Health & Earth",
    "Plurisciences1": "Multidisciplinary",
    "Universités - Santé": "Health",
    "Médecine et odontologie": "Medicine & Dentistry",
    "Pharmacie": "Pharmacy",
    "Plurisanté (Paces et Pass2)": "Multidisciplinary Health",
    "DUT - Spécialités de la production et de l'informatique": "DUT - Production & IT",
    "Ensemble": "All Bachelor"
}

def get_gii_data():
    df = pd.read_csv("data/raw/world_GII.csv")
    return df

def get_gii_long_format():
    df = get_gii_data()
    gii_columns = [col for col in df.columns if col.startswith("Gender Inequality Index")]
    
    df_long = df.melt(
        id_vars=["ISO3", "Country", "Continent"],
        value_vars=gii_columns,
        var_name="Year",
        value_name="GII"
    )
    
    df_long['Year'] = df_long['Year'].str.extract(r'(\d{4})').astype(int)
    df_long = df_long.dropna(subset=['GII'])
    
    return df_long

def get_stem_data():
    df = pd.read_csv("data/raw/world_women_in_stem.csv")
    
    VALUE_COL = (
        "Female share of graduates from Science, Technology, Engineering and Mathematics "
        "(STEM) programmes, tertiary (%)"
    )
    
    df = df.dropna(subset=[VALUE_COL])
    df["Year"] = df["Year"].astype(int)
    
    return df

def get_stem_filtered_years():
    df = get_stem_data()
    years = sorted(y for y in df["Year"].unique() if y not in (1998, 2019))
    return years

def get_world_boundaries():
    world = gpd.read_file("data/cleaned/world_boundaries_simplified.geojson")
    return world

def get_world_geojson():
    with open("data/cleaned/world_boundaries_simplified.geojson") as f:
        return json.load(f)


def get_iso3_to_name_mapping():
    geojson = get_world_geojson()
    return {
        feature["properties"]["iso3"]: feature["properties"]["name"]
        for feature in geojson["features"]
    }

def prepare_world_choropleth_data(df, value_col, years, iso_col='Code', entity_col='Entity'):
    world = get_world_boundaries()

    all_countries = world[['iso3']].copy()
    all_years = pd.DataFrame({'Year': years})
    all_combinations = all_countries.merge(all_years, how='cross')

    merged_df = all_combinations.merge(
        df,
        left_on=['iso3', 'Year'],
        right_on=[iso_col, 'Year'],
        how='left'
    )

    merged_df[iso_col] = merged_df[iso_col].fillna(merged_df['iso3'])
    merged_df['plot_iso'] = merged_df[iso_col]

    real_min = df[value_col].min()
    sentinel = real_min - (abs(real_min) * 0.1 + 0.01)

    merged_df[f"{value_col}_plot"] = merged_df[value_col].fillna(sentinel)
    merged_df[f"{value_col}_hover"] = merged_df[value_col].where(
        merged_df[value_col].notna(),
        "Unknown"
    )

    merged_df["Country_hover"] = merged_df[entity_col]
    iso3_to_name = get_iso3_to_name_mapping()
    
    merged_df["Country_hover"] = merged_df.apply(
        lambda row: iso3_to_name.get(row["plot_iso"])
        if pd.isna(row["Country_hover"])
        else row["Country_hover"],
        axis=1
    )
    
    return merged_df, sentinel

def add_bins_to_dataframe(df, column, bins, labels):
    df[f'{column}_Range'] = pd.cut(
        df[column],
        bins=bins,
        labels=labels,
        include_lowest=True
    )
    return df

def get_fr_regions_data():
    df = pd.read_csv("data/cleaned/fr_regions_gender_inequality_cleaned.csv")
    return df

def get_fr_departments_data():
    df = get_fr_regions_data()
    df_departments = df[~df['Region'].isin(REGION_NAMES_FR)].copy()
    df_departments['Salary_Gap_2022_abs'] = df_departments['Salary_Gap_2022'].abs()
    return df_departments

def get_fr_geojson():
    with open("data/raw/fr_departments.geojson") as f:
        return json.load(f)

def _parse_french_research_csv(filepath, discipline_translation):
    with open(filepath, newline="", encoding="utf-8") as fichier:
        lecteur = csv.reader(fichier)
        lignes = list(lecteur)
    
    index_header = None
    for i, ligne in enumerate(lignes):
        if "2010-2011" in ligne and "2020-2021" in ligne:
            index_header = i
            break
    
    if index_header is None:
        raise ValueError(f"Header not found in {filepath}")
    
    col_discipline = 0
    col_2010 = lignes[index_header].index("2010-2011")
    col_2020 = lignes[index_header].index("2020-2021")
    
    data = []
    for ligne in lignes[index_header + 1:]:
        try:
            if ligne[col_2010] and ligne[col_2020]:
                data.append({
                    "discipline": ligne[col_discipline],
                    "2010-2011": float(ligne[col_2010]),
                    "2020-2021": float(ligne[col_2020]),
                })
        except (ValueError, IndexError):
            continue
    
    df = pd.DataFrame(data)
    df["discipline"] = df["discipline"].str.strip().replace(discipline_translation)
    
    return df

def get_fr_phd_data():
    return _parse_french_research_csv(
        "data/raw/fr_research_women_feuille2.csv",
        DISCIPLINE_TRANSLATION_PHD
    )

def get_fr_university_data():
    return _parse_french_research_csv(
        "data/raw/fr_research_women_feuille1.csv",
        DISCIPLINE_TRANSLATION_UNIVERSITY
    )