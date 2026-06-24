# Hypertension Project

This repository is structured as a larger project with three separate but connected parts. The split follows the project plan in [docs/projektidee.odt].

## Educational Project Context

This repository documents an educational final project in Data Science. The goal is to combine data preparation, exploratory analysis, machine learning, and dashboard development in one coherent end-to-end project.

The project topic was chosen because hypertension is an important public health issue and a major risk factor for cardiovascular disease. At the same time, it is often not noticed for a long time because it may develop without clear symptoms. This makes the topic suitable for analysis from two perspectives:

- a public health perspective using WHO data for Germany
- an individual risk perspective using NHANES data and machine learning

More background on the project motivation and presentation can be found in [docs/presentation-power-point.pptx](docs/presentation-power-point.pptx).

## Project Goals

The project pursues four connected goals:

- analyze how hypertension prevalence in Germany changed between 2000 and 2019
- examine mortality trends related to hypertensive heart disease
- identify differences between men and women in hypertension prevalence
- build a machine learning model that estimates hypertension risk from individual health characteristics

## Questions This Project Answers

Across its analytical parts, the project is designed to answer the following questions:

- How did hypertension prevalence in Germany develop from 2000 to 2019?
- How did mortality from hypertensive heart disease change over the same period?
- What differences can be observed between men and women?
- Can a machine learning model predict whether a person has hypertension based on individual data?
- Which individual features contribute most strongly to hypertension prediction?

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

## Run the Streamlit App

Use the launcher script from the project root:

```bash
python run_dashboard.py
```

The script is cross-platform and uses the current Python interpreter to start Streamlit with the correct app path.
