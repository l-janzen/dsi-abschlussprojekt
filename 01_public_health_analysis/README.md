# Hypertension and Public Health in Germany

This project explores hypertension prevalence and hypertensive heart disease mortality in Germany between 2000 and 2019. It combines public health indicators, sex-specific prevalence data, and mortality trends to create a compact analytical dataset for exploratory analysis and visualization.

## Research Goal

The main goal of this project is to examine how hypertension prevalence in Germany changed over time and how these changes relate to mortality from hypertensive heart disease.

The analysis focuses on three questions:

- How did hypertension prevalence in Germany change between 2000 and 2019?
- How did prevalence differ between men and women?
- How did mortality from hypertensive heart disease change in Germany over the same period?

## Data Sources

The project uses CSV datasets collected from public health sources (WHO GHO) and prepared in the notebooks.

Main input files:

- `data/raw/hypertension-adults-30-79.csv`
- `data/raw/women-high-blood-pressure.csv`
- `data/raw/men-high-blood-pressure.csv`
- `data/raw/death-rate-from-hypertensive-heart-disease-who-ghe-age-standardized.csv`

Processed datasets created during the project:

- `data/processed/germany_hypertension_by_sex_2000_2019.csv`
- `data/processed/germany_hypertension_prevalence_and_mortality_2000_2019.csv`
- `data/processed/germany_hypertension_public_health_2000_2019.csv`
- `data/processed/germany_hypertensive_heart_disease_mortality_2000_2019.csv`

## Project Structure

- `data/raw` - raw source data in CSV format
- `data/processed` - cleaned and merged datasets used for analysis
- `notebooks` - Jupyter notebooks for data preparation and analysis
- `docs` - supporting materials for this project part, including the presentation
- `dashboards/tableau` - Tableau workbook for visualization

## Tools / Technologies

- `Python` for data preparation and analysis
- `Pandas` for data cleaning, filtering, and merging
- `Jupyter Notebook` for the analytical workflow
- `Matplotlib` for visualizations in the analysis notebook
- `Tableau` for dashboarding and presentation-ready visualizations
- `CSV` files as the main data exchange format

## Workflow

- `notebooks/data_collection.ipynb` prepares, filters, and combines the source datasets for Germany
- `notebooks/analysis.ipynb` performs exploratory analysis and creates visualizations
- `dashboards/tableau/visualisation.twbx` contains the Tableau-based visual presentation

## Summary of Results

The analysis shows that hypertension prevalence in Germany declined steadily from 2000 to 2019.

- Prevalence decreased for both men and women over the observed period.
- Men consistently showed higher hypertension prevalence than women.
- The gender gap narrowed slightly over time.
- Hypertensive heart disease mortality increased over much of the same period.
- A negative correlation appears between prevalence and mortality in the final dataset, but this should not be interpreted as a causal relationship because both measures are strongly influenced by time trends.
