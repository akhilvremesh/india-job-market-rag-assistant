# Salary Prediction Results

## Dataset and target

- Source: historical Naukri job-posting sample from 2019.
- Clean postings: 29,425.
- Postings with a usable parsed salary midpoint: 7,739.
- Target: `salary_mid_lpa`, the midpoint of a listed salary range converted to lakhs per annum (LPA).
- Inputs: job title, key skills, functional area, role, location, role category, industry, and numeric experience midpoint.

## Model evaluation

The data was split into training and test sets using an 80/20 random split (`random_state=42`). Five-fold shuffled cross-validation was performed on the training set.

| Model | Test MAE (LPA) | Test R² | CV MAE (LPA) | CV R² |
|---|---:|---:|---:|---:|
| Median baseline | 3.94 | -0.123 | — | — |
| Ridge regression | 2.93 | 0.430 | 2.58 | 0.557 |
| XGBoost | 2.44 | 0.493 | 2.16 | 0.590 |

The selected model is XGBoost. Its mean training MAE was 1.50 LPA and mean validation MAE was 2.16 LPA, a 0.66 LPA gap that suggests some overfitting.

## SHAP explanations

The global SHAP chart was calculated on 30 held-back test postings with a 50-posting training background sample. Numeric experience midpoint had the largest average influence in this sample. The local explanation for the example Merchandiser posting showed a predicted salary of 3.321 LPA versus a listed midpoint of 2.38 LPA.

SHAP describes how the model uses features; it does not show that a feature causes a salary change.

## Limitations

- The source data is from 2019 and does not represent currently available jobs or current salaries.
- The model covers many occupations, including non-technical roles; results may not represent data science or software roles specifically.
- Only postings with parseable, disclosed salaries were used.
- Salary-range midpoints are approximations.
- The random split and cross-validation measure performance within this historical sample, not on future job postings.
- The SHAP global chart uses a sample of 30 test postings.