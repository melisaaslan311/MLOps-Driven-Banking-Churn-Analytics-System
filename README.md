# MLOps-Driven-Banking-Churn-Analytics-System

An end-to-end, production-oriented analytics and machine learning system designed to predict and monitor customer churn in banking operations.

Built as a full data pipeline covering ingestion, transformation, storage, model training, real-time inference, and business intelligence visualization.

---

## What This Project Does

Transforms raw banking customer data into actionable churn predictions using an automated ML pipeline:

* Detects high-risk customers (churn probability)
* Automates ETL workflows with Airflow
* Serves real-time predictions via API
* Provides interactive BI dashboards for decision-making

---

## System Flow

```text id="p9x2ka"
Raw Data → ETL Pipeline → MySQL → ML Models → FastAPI → Streamlit Dashboard
```

---

## Tech Stack

* **Data Engineering:** Pandas, SQLAlchemy, MySQL
* **Machine Learning:** XGBoost, LightGBM, Random Forest, Scikit-learn
* **Orchestration:** Apache Airflow
* **API Layer:** FastAPI, Uvicorn
* **Visualization:** Streamlit, Plotly

---

## Pipeline (ETL)

Automated 3-stage pipeline:

* **Extract:** Load raw CSV data
* **Transform:** Cleaning + One-hot encoding
* **Load:** Persist into MySQL (`customers` table)

Airflow orchestration:

```text id="9v8m2c"
extract >> transform >> load
```

---

## Machine Learning Layer

Models evaluated under cross-validation:

* XGBoost (primary model)
* LightGBM
* Random Forest

Evaluation metrics:

* ROC-AUC Score
* K-Fold Validation

---

## API Service

Real-time inference engine built with FastAPI:

```http id="z1kq9m"
POST /predict
```

Returns:

* Churn probability
* Risk classification (Risky / Safe)
<img width="1600" height="509" alt="image" src="https://github.com/user-attachments/assets/5ff1b801-9be2-4d6d-844d-32b8be47d9d2" />
<img width="1600" height="324" alt="image" src="https://github.com/user-attachments/assets/57f0b420-7fae-4786-b0d5-ec97a4d85219" />

---

## Dashboard

Interactive Streamlit interface for business insights:

* Customer churn KPIs
* Risk segmentation
* Credit score & balance analysis
* Geography-based churn patterns
* Dynamic filtering system

---

## Key Value

This system enables:

* Early churn detection
* Data-driven retention strategies
* Automated ML workflow execution
* Real-time decision support

---


