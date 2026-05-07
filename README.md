# Follow the Money — NYC Taxi Tip Geography 2023

Website: https://marijn-118.github.io/


This repository contains the final project for DTU Social Data Analysis and Visualisation. The project investigates how yellow taxi tipping in New York City varies by pickup neighborhood, and whether the geography of tips reflects the geography of neighborhood income.

The main finding is that taxi tip percentages are strongly associated with neighborhood median household income. High-income Manhattan taxi zones consistently produce much higher average tip percentages than lower-income outer-borough zones.

## Project Deliverables

- `index.html` — the public-facing data story website.
- `explainer_notebook.ipynb` — the technical explainer notebook with methodology, EDA, analysis, narrative design choices, discussion, contributions, and references.
- `visualizations/` — exported interactive Plotly HTML visualizations embedded in the website.
- `analysis/` — optional development materials if retained; the final methodology is documented in the explainer notebook.
- `style.css` — website styling.

## Website

Open `index.html` in a browser, or serve the repository through GitHub Pages.

The website is written for a non-technical audience and follows a guided data-story structure:

1. Introduction and motivation
2. Tip percentage map
3. Income map and income-tip correlation
4. Zone rankings
5. Day/night tipping pattern
6. Limitations
7. Conclusion

## Data Sources

- NYC TLC Yellow Taxi Trip Records 2023: https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page
- US Census Bureau ACS 2023, table B19013, Median Household Income: https://data.census.gov/table/ACSDT5Y2023.B19013
- NYC TLC Taxi Zone Shapefile: https://d37ci6vzurychx.cloudfront.net/misc/taxi_zones.zip
- US Census TIGER/Line 2023 census tract boundaries: https://www.census.gov/geographies/mapping-files/time-series/geo/tiger-line-file.html

Raw taxi parquet files are not committed to this repository because of their size. The explainer notebook expects them under `analysis/data/taxi/` if the full pipeline is rerun locally.

## Main Analysis File

- `explainer_notebook.ipynb` documents the final taxi cleaning, zone-level aggregation, ACS income collection, area-weighted spatial join, income-tip correlations, income quintile analysis, visualization choices, discussion, and references.

## Reproducibility Notes

The interactive website can be viewed directly from the committed files. To rerun the full analysis, install the Python geospatial/data stack used by the notebook, including:

- `pandas`
- `geopandas`
- `numpy`
- `scipy`
- `plotly`
- `requests`
- `matplotlib`

Then place the 2023 yellow taxi parquet files in:

```text
analysis/data/taxi/
```

Then open `explainer_notebook.ipynb` and enable the documented full pipeline cells where noted.

## Limitations

- Cash tips are not recorded in the TLC data, so the analysis uses credit-card trips only.
- Neighborhood income is assigned from ACS tract-level medians to taxi zones; it does not represent the individual passenger's income.
- The results are associative, not causal.
- Yellow taxis are not equally common in all boroughs, so low-trip zones are filtered out of the main income analysis.

## Authors

Group project for DTU Social Data Analysis and Visualisation, 2026.
