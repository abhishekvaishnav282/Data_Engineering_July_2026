# Home Credit Dashboard

A multi-page Streamlit dashboard exploring the Home Credit Default Risk dataset (applicant demographics, income/credit ratios, employment, housing, external credit bureau scores, and default risk).

## Dataset

`data/application_train.csv` (~160MB) is **not included** in this repo since it exceeds GitHub's 100MB file limit. Download it and place it in `data/` before running the app:

1. Get `application_train.csv` from the [Home Credit Default Risk competition on Kaggle](https://www.kaggle.com/competitions/home-credit-default-risk/data)
2. Place it at `data/application_train.csv` (relative to this folder)

`data/HomeCredit_columns_description (1).csv` (column descriptions) is included in the repo.

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```
