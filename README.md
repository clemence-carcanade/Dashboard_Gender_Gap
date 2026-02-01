# User Guide

### Creating the virtual environment (VS Code)

Before running the dashboard, you need to create a Python virtual environment.

In VS Code:
1. Open the Command Palette (`Ctrl + Shift + P`)
2. Select **Python: Select Interpreter**
3. Choose **Create Virtual Environment**
4. Select **Venv**
5. Choose a Python version
6. Check `requirements.txt`

Once the virtual environment is created, run the dashboard from the project root:

```bash
#optionnal: download all datasets from web
cd src/utils
python get_data.py
python clean_data.py

#from the project root:
python main.py
```

Use `Ctrl + Click` on the link int the terminal to open the dashboard in your default web browser.

### Using the dashboard

- The navigation bar allows you to move between the different dashboard pages.
- Two charts at the international level (Global Gender Inequality Index and Women in STEM worldwide) are interactive.
- Two additional charts focus on France (education gap and wage gap between women and men).
- You can choose the data visualization format for all charts (map or histogram).
- Two histograms show the distribution of women across fields of study in France, at Bachelor’s and PhD levels.

# Data

## Data description and processing

### International data

The data for the **Gender Inequality Index (GII)** at the global level comes from *kaggle.com* : https://www.kaggle.com/code/anoopjohny/gender-inequality-study
<br>For women in **STEM (Science, Technology, Engineering, and Mathematics) worldwide**, the data was sourced from *ourworldindata.org* : https://ourworldindata.org/grapher/share-graduates-stem-female

Both covers the period from 1999 to 2018 and are stored in CSV files.
To build the visualizations, we used ISO3 country codes.

The GII values were originally spread across multiple columns, one per year. To make the data usable for analysis and visualization, the dataset was reshaped into a long format by extracting the year from each column and associating it with the corresponding GII value.

Those datasets allowed us to observe long-term global trends.

### French data

The two charts related to **education gap (2021) and wage gap (2022) in France** use data from *insee.fr* : https://www.insee.fr/fr/statistiques/2513786#consulter
<br>Similarly, the **two histograms showing women’s fields of study in France** also come from *insee.fr* : https://www.insee.fr/fr/statistiques/6047727?sommaire=6047805#

### GeoJSON

All geolocalized data requires boundary GeoJSON files:
- World boundaries (countries): https://public.opendatasoft.com/explore/assets/world-administrative-boundaries/export/
- France boundaries (departments): https://france-geojson.gregoiredavid.fr/

# Developer Guide

## Project architecture

The project follows a modular structure.
The main program calls different functions, each responsible for a specific task.
These functions are organized into dedicated Python files and folders to ensure clarity, maintainability, and scalability.

## Project structure

```text
DASHBOARD_GENDER_GAP
│
├── data/                          # Project datasets
│   ├── cleaned/                   # Cleaned and processed data
│   │   ├── fr_regions_gender_inequality_cleaned.csv
│   │   └── world_boundaries_simplified.geojson
│   │
│   └── raw/                       # Raw (unprocessed) data
│       ├── fr_departments.geojson
│       ├── fr_regions_gender_inequality.xls
│       ├── fr_research_women_feuille1.csv
│       ├── fr_research_women_feuille2.csv
│       ├── world_boundaries.geojson
│       ├── world_GII.csv
│       └── world_women_in_stem.csv
│
├── src/                           # Dashboard source code
│   ├── assets/                    # Static resources (fonts, images, CSS)
│   │   ├── fonts/
│   │   ├── images/
│   │   ├── favicon.ico
|   |   └── style.css
│   │
│   ├── charts/                    # Chart generation logic
│   │   ├── board.py
│   │   ├── fr_board.py
│   │   ├── fr_histogram.py
│   │   ├── fr_map.py
│   │   ├── fr_phd.py
│   │   ├── fr_university.py
│   │   ├── gii_histogram.py
│   │   ├── gii_world_map.py
│   │   ├── slider.py
│   │   ├── stem_histogram.py
│   │   └── stem_world_map.py
│   │
│   ├── components/                # Reusable UI components
│   │   ├── card.py
│   │   ├── footer.py
│   │   ├── navbar.py
│   │   └── segmented_control.py
│   │
│   ├── pages/                     # Dashboard pages
│   │   ├── about.py
│   │   ├── france_analysis.py
│   │   ├── home.py
│   │   ├── study_analysis.py
│   │   └── world_analysis.py
│   │
│   ├── graphics/                  # Original chart scripts
│   │
│   └── utils/                     # Utility functions
│       ├── chart.py               # Chart templates
│       ├── clean_data.py          # Data cleaning
│       ├── get_data.py            # Data loading
│       └── prepare_data.py        # Data functions redundant
│
├── config.py                      # Environment variables
├── Gender_Gap_Demo.mp4            # Video demonstration of the dashboard
├── main.py                        # Dashboard entry point
├── requirements.txt               # Project dependencies
├── README.md                      # Documentation
└── .gitignore
``` 
## Adding a new chart

1. Create a new Python file in `DASHBOARD_GENDER_GAP/src/charts`
2. Define a `layout` function and use `chart.py`to define your figure
3. Import this function into the `home.py` page
```python
from src.charts.your_chart import layout as your_chart_layout
```
4. Add your chart to the layout function in `home.py`

## Adding a new page

1. Create a new Python file in `DASHBOARD_GENDER_GAP/src/charts`
2. Define a `layout`function
3. Import this function into `main.py`
```python
from src.pages.your_page import layout as your_page_layout
```
4. Add your page to `display_page` function:
```python
elif pathname == "/your_page":
    return your_page_layout()
```

# Analysis Report

The data analysis highlights several key aspects of gender equality worldwide and in France.

## International analysis 

- GII data shows that wealthier countries tend to have lower levels of gender inequality, while poorer countries experience higher inequality.
- Surprisingly, countries with higher gender inequality often show a higher proportion of women in STEM fields.
In countries such as Niger or Tunisia, STEM careers appear to be a pathway for women to achieve social mobility.
- In contrast, countries like Switzerland show low gender inequality overall, but also a low proportion of women in STEM fields, suggesting the persistence of cultural stereotypes.

## France analysis 

- Overall, education gap data shows that women tend to pursue higher levels of education than men, yet receive lower salaries.
- Wage gaps are smaller in departments without major metropolitan areas and in regions dominated by public sector employment, where standardized pay scales reduce inequality.
- In large metropolitan areas such as Paris, wage gaps are more pronounced, largely due to private sector practices.
- The histograms reveal another important pattern:
although women pursue higher education in large numbers, they tend to concentrate in fields such as humanities and social sciences.
These sectors are less impacted by technological innovation, which may reduce women’s access to high-level positions and long-term influence.

# Copyright

We hereby declare that the code provided in this project was produced by us, except for the elements listed below.

### Borrowed code 

In `get_data.py` :
 
Source: ChatGPT

Explanation: These lines extract the year from column names and convert it to the appropriate data type.

```python
gii_columns = [col for col in df.columns if col.startswith("Gender Inequality Index")]
    
df_long = df.melt(
    id_vars=["ISO3", "Country", "Continent"],
    value_vars=gii_columns,
    var_name="Year",
    value_name="GII"
)

df_long['Year'] = df_long['Year'].str.extract(r'(\d{4})').astype(int)
```

Source: ChatGPT

Explanation: These lines replace missing values with a very small sentinel value in order to display them in grey on the map.

```python
real_min = df[value_col].min()
sentinel = real_min - (abs(real_min) * 0.1 + 0.01)
```

Source: Claude.ia

Explanation: These lines remove sentinel value by Unknown when no data is available and displays the name of the country when hover.

```python
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
```

In `chart.py` :

Source: ChatGPT

Explanation: These lines adjust the border thickness of countries on the map.

```python
fig.update_traces(
    marker_line_color="#DDDDDD",
    marker_line_width=0.9,
    hovertemplate=hover_template
)
```

Both `clean_data.py`and `get_data.py`where made with Claude.ia