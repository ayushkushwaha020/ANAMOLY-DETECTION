# CODE.KAISEN — Component Anomaly Detection MVP

AI-assisted component anomaly detection for burn-in and screening analysis.

## Working Links

- **Live Demo:** https://anomaly-detection-xxmd.onrender.com
- **GitHub Repository:** https://github.com/ayushkushwaha020/ANOMALY-DETECTION

## SIH Ideas Details

- **SIH Problem Statement:** SIH26170
- **Problem Statement:** AI Driven Anomaly Detection in Component Burn-In and Screening
- **Submission:** Smart India Hackathon (SIH) Ideas
- **Selection Pool:** 500 ideas

This project was submitted independently under SIH Ideas. The **DX TECHIES** team credits are **not** attributed to this project.

## What It Does

This Streamlit prototype analyzes burn-in readings using:

- Temperature
- Current
- Voltage
- Time-trend features

It flags unusual behavior for engineer review. A flag is **not** a confirmation of component failure, and final screening decisions remain with the engineer.

## Prototype Method

The MVP uses a lightweight, explainable approach:

- Robust statistical deviation using median/MAD
- Time-trend features across multiple parameters
- Combined anomaly scoring
- Automatic screening threshold based on the 90th percentile of prototype scores

The MVP intentionally avoids SciPy and scikit-learn dependencies.

## Architecture

```text
CSV / Demo Data
      │
      ▼
Data Validation & Cleaning
      │
      ▼
Per-Component Feature Extraction
      │
      ├── Temperature change / rate
      ├── Current change / rate
      └── Voltage variation / rate
      │
      ▼
Robust Multi-Parameter Scoring
      │
      ▼
90th-Percentile Screening Threshold
      │
      ├── Normal
      └── Potential anomaly → Engineer review
      │
      ▼
Interactive Streamlit Dashboard
      │
      └── CSV reports / analyzed readings
```

## CSV Format

Required columns:

`component_id,time_min,temperature_c,current_a,voltage_v`

A sample dataset is included in `sample_burnin_data.csv`.

## Features

- Demo burn-in dataset for immediate exploration
- CSV upload for custom burn-in readings
- Screening overview
- Potential anomaly list
- Per-component analysis
- Temperature/current/voltage trend visualization
- Engineer-review indicators
- Downloadable flagged-component report
- Downloadable screening report
- Downloadable analyzed readings

## Run Locally

```powershell
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

## Deployment

Deployed as a Streamlit application on Render.

The Render service is configured for automatic deployment from the `main` branch.

## Validation Note

The repository contains a deterministic demo dataset and an interactive upload path. The live deployment should be treated as a prototype demonstration rather than a production component-screening system.

## Disclaimer

This is a **prototype/MVP for screening and decision support**. An anomaly flag does not establish that a component is defective. Engineering validation and review are required before any production decision.
