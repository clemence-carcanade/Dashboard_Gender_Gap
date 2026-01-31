# User Guide

Before running the dashboard, you need to create a Python virtual environment.

### Creating the virtual environment (VS Code)

1. Open the Command Palette `(Ctrl + Shift + P)`

2. Select Python: Select Interpreter

3. Choose Create Virtual Environment

4. Select Venv

5. Choose a Python version

6. Check `requirements.txt` to install the required dependencies

Once the virtual environment is created, run the dashboard from the project root directory:

```python
python main.py
```
After running the command, a link appears in the terminal.
Use `Ctrl + Click` on the link to open the dashboard in your default web browser.

### Using the dashboard

- The navigation bar allows you to move between the different dashboard pages and the About page.

- The first two charts at the international level (Global Gender Inequality Index and Women in STEM worldwide) are interactive.
You can choose the data visualization format (map or histogram).

- Two additional charts focus on France:
    - education gap between women and men
    - wage gap between women and men
    These are also available as maps or histograms.

- Finally, two histograms show the distribution of women across fields of study in France, at Bachelor’s and PhD levels.

No programming knowledge is required to explore the dashboard.

# Data

## Data description and processing

### International data

The data for the **Gender Inequality Index (GII)** at the global level comes from *kaggle.com*.
It covers the period from 1999 to 2018 and is stored in CSV files.

To build the visualizations, we used:

- ISO3 country codes

- country names

- continents

- yearly GII values

The GII values were originally spread across multiple columns, one per year.
To make the data usable for analysis and visualization, the dataset was reshaped into a long format by extracting the year from each column and associating it with the corresponding GII value.

The resulting dataset spans 20 years, allowing us to observe long-term global trends.

For women in **STEM (Science, Technology, Engineering, and Mathematics) worldwide**, the data was sourced from *ourworldindata.org*.

The dataset is provided in CSV format and includes:

- ISO3 country codes

- country names

- years

- percentage of women in STEM fields

The data covers the period from **1999 to 2018**, enabling a nearly 20-year global comparison.

### French data

The two charts related to **education and wage gaps in France** use data from *insee.f*.
The original data was provided in XLSX format. Since standard online converters did not work properly, we used *claude.ai* to generate a custom converter to transform the files into CSV format.

- Education gap data: 2021

- Wage gap data: 2022

Similarly, the **two histograms showing women’s fields of study in France** also come from *insee.fr*.
These datasets were originally in XLSX format and were converted to CSV using an online converter.

The data corresponds to the academic years:

- 2010–2011

- 2020–2021

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
├── src/                           # Dashboard source code
│   ├── assets/                    # Static resources (fonts, images, CSS)
│   │   ├── fonts/
│   │   ├── images/
│   │   └── style.css
│   │
│   ├── charts/                    # Chart generation logic
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
│   ├── components/                # Reusable UI components
│   │   ├── header.py
│   │   ├── footer.py
│   │   ├── navbar.py
│   │   └── card.py
│   │
│   ├── pages/                     # Dashboard pages
│   │   ├── about.py
│   │   ├── home.py
│   │   └── world_analysis.py
│   │
│   ├── graphics/                  # Original graph scripts
│   │
│   └── utils/                     # Utility functions
│       ├── get_data.py             # Data loading
│       └── clean_data.py           # Data cleaning
│
├── config.py                      # Configuration settings
├── main.py                        # Dashboard entry point
├── requirements.txt               # Project dependencies
├── README.md                      # Documentation
└── .gitignore
``` 
## Adding a new chart

1. Create a new Python file in `DASHBOARD_GENDER_GAP/src/charts`

2. Define a `layout` function

3. Import this function into the `home.py` page

Ex :
```python
from src.charts.gii_histogram import layout as gii_bar_layout
```
4. Add the chart to the layout function in `home.py`

## Adding a new page



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

- Lines 8–17 of gii_board.py and lines 16–25 of `gii_world_map.py`
 
    Source: ChatGPT
 
    Explanation: These lines extract the year from column names and convert it to the appropriate data type.

  ```python
  gii_columns = [c for c in df.columns if c.startswith("Gender Inequality Index")]

    df_long = df.melt(
        id_vars=["ISO3", "Country", "Continent"],
        value_vars=gii_columns,
        var_name="Year",
        value_name="GII"
    )

    df_long["Year"] = df_long["Year"].str.extract(r"(\d{4})").astype(int)
    ```
- Lines 42–45 of `gii_world_map.py`
    
    Source: ChatGPT
    
    Explanation: These lines replace missing values with a very small sentinel value in order to display them in grey on the map.

    ```python
    real_min = df_long["GII"].min(skipna=True)
    sentinel = real_min - (abs(real_min) * 0.1 + 0.01)

    merged_df["GII_plot"] = merged_df["GII"].fillna(sentinel)
    ```
- Lines 75–76 of `gii_world_map.py`

    Source: ChatGPT

    Explanation: These lines adjust the border thickness of countries on the map.

    ```python
    fig.update_traces(marker_line_color="#DDDDDD", marker_line_width=0.9)
    fig.update_geos(fitbounds="locations", visible=False)
    ```


