# 🎨 ENAP Data Intelligence Platform

> End-to-end data science project built on a real ERP database from **ENAP** (Entreprise Nationale des Peintures — Algeria's leading paint and varnish manufacturer), covering business intelligence, predictive analytics, and anomaly detection.

---

## 📌 Context

This project was developed as part of the **Projet Pluridisciplinaire** module in the 4th year of a Data Science degree. It uses real operational data from ENAP Souk Ahras, extracted from their SQL Server ERP system (Asysnap).

> ⚠️ The dataset is not included in this repository for confidentiality reasons.

---

## 🏗️ Project Structure

```
ENAP_Projet_Pluridisciplinaire/
│
├── config/
│   └── db_config.py                  # SQL Server connection settings
│
├── data/
│   ├── raw/                          # Data extracted from SQL (not tracked)
│   ├── processed/                    # Cleaned and transformed data (not tracked)
│   └── features/                     # ML-ready features (not tracked)
│
├── notebooks/
│   ├── 01_data_exploration.ipynb
│   ├── 02_eda_sales.ipynb
│   ├── 03_eda_stock.ipynb
│   ├── 04_eda_clients.ipynb
│   ├── 05_forecasting_experiments.ipynb
│   ├── 06_churn_experiments.ipynb
│   └── 07_anomaly_experiments.ipynb
│
├── src/
│   ├── data/
│   │   ├── extract.py                # SQL extraction functions
│   │   └── clean.py                  # Data cleaning functions
│   ├── features/
│   │   ├── sales_features.py
│   │   ├── churn_features.py
│   │   └── anomaly_features.py
│   ├── models/
│   │   ├── forecasting.py            # LSTM / Prophet
│   │   ├── churn.py                  # Churn prediction
│   │   └── anomaly.py                # Autoencoder / Isolation Forest
│   └── visualization/
│       └── charts.py
│
├── models_saved/                     # Trained model files (not tracked)
│
├── dashboard/
│   ├── app.py                        # Streamlit main entry point
│   └── pages/
│       ├── 1_accueil.py
│       ├── 2_ventes.py
│       ├── 3_stock.py
│       ├── 4_clients.py
│       ├── 5_previsions.py
│       ├── 6_churn.py
│       └── 7_anomalies.py
│
├── rapport/
│   └── rapport_stage.docx
│
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 🚀 Modules

### Module 1 — Business Intelligence Dashboard
> Status: 🔄 In Progress

- Sales analysis vs objectives
- ABC classification of products and clients
- Stock level monitoring
- Regional and temporal performance
- Built with **Python**, **Plotly**, and **Streamlit**

### Module 2 — Predictive Analytics
> Status: ⏳ Planned

- **Demand Forecasting** — Prophet + LSTM for sales prediction by product family
- **Churn Prediction** — Classification model with entity embeddings to identify at-risk clients

### Module 3 — Anomaly Detection
> Status: ⏳ Planned

- **Autoencoder** on invoice data to flag unusual transactions
- **Isolation Forest** as cross-validation method
- Alert system integrated into the dashboard

---

## 🛠️ Tech Stack

| Category | Tools |
|----------|-------|
| Language | Python 3.10+ |
| Database | SQL Server 2022 (local), pyodbc |
| Dashboard | Streamlit, Plotly |
| ML / DL | Scikit-learn, TensorFlow/Keras, Prophet |
| Data | Pandas, NumPy |
| Visualization | Matplotlib, Seaborn, Plotly |
| Environment | VS Code, Jupyter Notebook |
| Version Control | Git, GitHub |

---

## ⚙️ Setup

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/ENAP-Data-Intelligence-Platform.git
cd ENAP-Data-Intelligence-Platform
```

### 2. Create a virtual environment
```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # Mac/Linux
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure the database connection
Edit `config/db_config.py` with your local SQL Server credentials.

### 5. Run the dashboard
```bash
python -m streamlit run dashboard/app.py
```

---

## 📊 Data Source

Data extracted from the **Asysnap ERP system** used by ENAP, containing tables related to:
- Sales and invoicing (`FACTURE`, `LIGFAC`, `CLIENT`)
- Inventory and stock (`STOCK`, `MOUVEMENTS`, `ARTICLE`)
- Production (`FICFAB`, `ATELIER`, `GAMME`)
- Finance (`BILAN`, `BALANCE`, `ECRITURE`)
- Commercial objectives (`OBJECTIF`, `OBJECTIFCLIENT`)

---

## 👨‍💻 Author

Soundes Kohil
4th Year Data Science Student
University of Badji Mokhtar Annaba - 2026

---

## 📄 License

This project is for academic purposes only. The data belongs to ENAP and is not redistributed.
```