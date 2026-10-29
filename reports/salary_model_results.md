# Salary Prediction Model Results

## Goal

Predict the listed salary midpoint for a job posting, measured in lakhs per annum (LPA).

## Data

- Source: PromptCloud Naukri job postings dataset.
- Time period: July–August 2019.
- Cleaned postings: 29,425.
- Postings with a parsed salary target: 7,739.
- Target: `salary_mid_lpa`, the midpoint of the parsed listed salary range.
- Rows without a usable salary target were excluded from model training.

Salary-like amounts were removed from the job title, skills, and functional-area text to reduce target leakage. The model uses job text, role, location, experience, role category, and industry.

## Modeling

- Train/test split: 80% training and 20% held-back test data.
- Split seed: 42.
- Model: XGBoost regressor with TF-IDF text features and one-hot encoded categories.
- Missing experience values were filled using the training-set median.
- Cross-validation: five shuffled folds on the training set.

## Results

| Metric | Result |
|---|---:|
| Test MAE | 2.43 LPA |
| Test R² | 0.495 |
| Mean cross-validation MAE | 2.16 LPA |
| Cross-validation MAE standard deviation | 0.04 LPA |
| Mean cross-validation R² | 0.600 |
| Training MAE | 1.54 LPA |

MAE is the average absolute difference between predicted and listed salary midpoints. For example, a test MAE of 2.43 LPA means predictions were off by 2.43 LPA on average in the held-back test set.

R² describes how much salary variation the model explains relative to a simple average-based prediction. It is not a measure of prediction accuracy in LPA.

## SHAP interpretation

SHAP was used to explain overall feature influence and one individual prediction. In the example posting, the model predicted 3.37 LPA and the listed midpoint was 2.38 LPA. Experience midpoint was the largest downward contribution in that example.

SHAP describes how the model used its inputs. These associations do not show that a feature causes a salary to change.

## Limitations

- The dataset contains historical postings from 2019 and does not represent current job availability or current salary levels.
- Salaries are listed ranges parsed from job descriptions; parsing errors and unusual values may remain.
- The model was trained only on postings with usable salary information, which may differ from postings that omit salary.
- The model estimates historical listed salary midpoints, not an individual's guaranteed offer or take-home pay.
- The training MAE is lower than the test MAE, so some overfitting may remain.
- The model should not be used as a substitute for checking current job listings and compensation sources.
