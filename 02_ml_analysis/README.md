# Hypertension Risk Prediction with NHANES Data

## Project Overview

This project analyzes hypertension risk factors using data from the National Health and Nutrition Examination Survey (NHANES) 2021–2023. The goal is to develop a machine-learning-based risk assessment model for hypertension and implement the final model in a Streamlit application.

The project combines public health, exploratory data analysis and machine learning to demonstrate how health survey data can be used for preventive risk assessment.

## Data Source

The analysis is based on publicly available NHANES data from the cycle August 2021–August 2023.

The following NHANES files were used:

| File      | Content                                    | Role in the Project                      |
| --------- | ------------------------------------------ | ---------------------------------------- |
| `BPQ_L`   | Blood Pressure & Cholesterol Questionnaire | Target variable: hypertension            |
| `DEMO_L`  | Demographic Variables                      | Age and gender                           |
| `BMX_L`   | Body Measures                              | BMI, height, weight, waist circumference |
| `SMQ_L`   | Smoking Questionnaire                      | Smoking behavior                         |
| `ALQ_L`   | Alcohol Use Questionnaire                  | Alcohol consumption                      |
| `PAQ_L`   | Physical Activity Questionnaire            | Physical activity and sitting time       |
| `DIQ_L`   | Diabetes Questionnaire                     | Diabetes status                          |
| `KIQ_U_L` | Kidney Conditions Questionnaire            | Kidney disease status                    |

The datasets were merged using the participant identifier `SEQN`.

## Target Variable

The target variable is based on `BPQ020`, which asks whether a person has ever been told by a doctor or health professional that they had high blood pressure.

The variable was recoded into a binary target:

| Original Value | Meaning                        | Model Coding       |
| -------------- | ------------------------------ | ------------------ |
| 1              | Yes                            | 1                  |
| 2              | No                             | 0                  |
| 7, 9, missing  | Refused / Don’t know / Missing | treated as missing |

The final target variable is called `hypertension`.

## Selected Features

The selected features include demographic, anthropometric, behavioral and medical risk factors:

* Age
* Gender
* BMI
* Waist circumference
* Smoking status
* Alcohol use
* Physical activity
* Sitting time
* Diabetes
* Kidney disease
* High cholesterol

These variables were selected because they are clinically and epidemiologically relevant, available in NHANES and suitable for a simple risk assessment application.

## Methodology

The project includes the following steps:

1. Data loading and variable selection
2. Data merging using `SEQN`
3. Data cleaning and handling of missing values
4. Feature engineering
5. Exploratory data analysis
6. Model training and model comparison
7. Model evaluation
8. Feature importance analysis
9. Development of a Streamlit application

## Machine Learning Models

Several classification models were tested:

* Logistic Regression
* Random Forest
* Decision Tree

The logistic regression model was selected as the main model because it provided a good balance between performance and interpretability.

## Model Evaluation

The models were evaluated using:

* Accuracy
* Precision
* Recall
* F1-score
* ROC-AUC
* Confusion Matrix

Because this project focuses on preventive risk assessment, recall was considered especially important. A lower decision threshold was also tested to improve the detection of hypertension cases.

## Streamlit Application

The final model is implemented in a Streamlit app. Users can enter selected risk factors and receive a model-based hypertension risk assessment.

The app is intended as a data science demonstration and does not replace medical diagnosis.

## Limitations

The analysis is based on observational survey data. Therefore, the results cannot be interpreted as causal effects.

The target variable is based on self-reported information about whether hypertension was ever diagnosed by a health professional. This may lead to misclassification.

The model should be understood as an exploratory risk assessment tool, not as a clinical diagnostic system.

## Project Goal

This project demonstrates an end-to-end data science workflow in the public health context: from data preparation and exploratory analysis to machine learning and deployment in a simple web application.
