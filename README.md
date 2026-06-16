# Hypertension Project

This repository is structured as a larger project with three separate but connected parts. The split follows the project plan in [docs/Mögliche Projektidee_MG_2.odt].

## Project Parts

- `01_public_health_analysis` - WHO-based public health analysis for Germany, including data preparation, exploratory analysis, and visualization
- `02_ml_analysis` - NHANES-based machine learning analysis for hypertension risk prediction
- `03_dashboard_app` - app layer for presenting results, planned as a Streamlit dashboard

## Repository Structure

- `docs` - shared project documentation and planning materials
- `01_public_health_analysis/data` - raw and processed WHO-based datasets
- `01_public_health_analysis/notebooks` - notebooks for data preparation and analysis
- `01_public_health_analysis/dashboards` - visualization files for the public health part
- `02_ml_analysis` - workspace for the NHANES machine learning part
- `03_dashboard_app` - workspace for the dashboard/app part

## Notes

- The three parts are intentionally separated because they work on different analytical levels:
  - WHO data: country/year level
  - NHANES data: individual/person level
  - App layer: presentation and interaction
