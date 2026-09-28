# CODE.KAISEN — Component Anomaly Detection MVP

SIH PS 26170: AI Driven Anomaly Detection in Component Burn-In and Screening.

This Streamlit prototype analyzes burn-in readings using temperature, current, voltage, and time-trend features. It flags unusual behavior for engineer review; a flag is not a confirmation of component failure.

## Run locally

```powershell
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

## CSV format

Required columns:

`component_id,time_min,temperature_c,current_a,voltage_v`

## Prototype method

Robust statistical deviation (median/MAD) plus time-trend features across multiple parameters. The MVP intentionally avoids SciPy and scikit-learn dependencies.

## Deployment

This repository is intended to be deployed with Streamlit Community Cloud using `app.py` as the main file.
