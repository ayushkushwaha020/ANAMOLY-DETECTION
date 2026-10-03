# CODE.KAISEN — Component Anomaly Detection MVP

SIH PS 26170: AI Driven Anomaly Detection in Component Burn-In and Screening.

## Working Links

- **Live Demo:** https://anomaly-detection-xxmd.onrender.com
- **GitHub Repository:** https://github.com/ayushkushwaha020/ANOMALY-DETECTION

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

Deployed as a Streamlit application on Render. The service is configured for automatic deployment from the `main` branch.
