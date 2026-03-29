# ============================================================
#  src/data/clean.py
#  Clean and prepare extracted tables for analysis
# ============================================================

import pandas as pd
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

RAW_DIR       = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'raw')
PROCESSED_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'processed')
os.makedirs(PROCESSED_DIR, exist_ok=True)

# ============================================================
# INDIVIDUAL CLEANING FUNCTIONS
# ============================================================

def clean_facture():
    df = pd.read_csv(os.path.join(RAW_DIR, 'facture.csv'))

    # Drop 100% empty columns
    df = df.drop(columns=['DEPOT', 'TRIMESTRE', 'CODED', 'UTILISATEUR'])

    # Convert date
    df['DATE1'] = pd.to_datetime(df['DATE1'])

    # Add useful time columns
    df['ANNEE']    = df['DATE1'].dt.year
    df['MOIS']     = df['DATE1'].dt.month
    df['TRIMESTRE'] = df['DATE1'].dt.quarter
    df['SEMAINE']  = df['DATE1'].dt.isocalendar().week.astype(int)
    df['JOUR_SEM'] = df['DATE1'].dt.day_name()

    # Clean amounts
    df['MONTHTNET'] = pd.to_numeric(df['MONTHTNET'], errors='coerce')
    df['MONTHT']    = pd.to_numeric(df['MONTHT'], errors='coerce')
    df['REMISE']    = pd.to_numeric(df['REMISE'], errors='coerce').fillna(0)

    # Strip whitespace from string columns
    df['CDCLIE']  = df['CDCLIE'].astype(str).str.strip()
    df['MODEPAY'] = df['MODEPAY'].astype(str).str.strip()

    print(f"✅ FACTURE cleaned: {len(df)} rows, {len(df.columns)} columns")
    return df


def clean_ligfac():
    df = pd.read_csv(os.path.join(RAW_DIR, 'ligfac.csv'))

    # Drop useless column
    df = df.drop(columns=['CODED'])

    # Fill missing discounts with 0
    df['REMISEP'] = df['REMISEP'].fillna(0)

    # Fill missing category names
    df['NomGamme']   = df['NomGamme'].fillna('Inconnu')
    df['NomFamille'] = df['NomFamille'].fillna('Inconnu')
    df['NomProduit'] = df['NomProduit'].fillna('Inconnu')

    # Clean numeric columns
    df['QTEFAC']  = pd.to_numeric(df['QTEFAC'],  errors='coerce').fillna(0)
    df['PRIXFAC'] = pd.to_numeric(df['PRIXFAC'], errors='coerce').fillna(0)
    df['MONTLIG'] = pd.to_numeric(df['MONTLIG'], errors='coerce').fillna(0)

    # Strip whitespace
    df['CDCLIE'] = df['CDCLIE'].astype(str).str.strip()
    df['PROD']   = df['PROD'].astype(str).str.strip()

    # Add date from FACT1 prefix (F24XXXXX → year 2024)
    if 'DATES' in df.columns:
        df['DATES'] = pd.to_datetime(df['DATES'], errors='coerce')
    print(f"✅ LIGFAC cleaned: {len(df)} rows, {len(df.columns)} columns")
    return df


def clean_client():
    df = pd.read_csv(os.path.join(RAW_DIR, 'client.csv'))

    # Drop mostly empty columns
    df = df.drop(columns=[
        'SECTEUR', 'ACTIVITE', 'ADRESSE1', 
        'ECHEANCE', 'VIGUEUR', 'adresse'
    ])

    # Fill missing values
    df['MODEPAY'] = df['MODEPAY'].fillna('Non renseigné').astype(str).str.strip()
    df['ADR']     = df['ADR'].fillna('Non renseigné').astype(str).str.strip()
    df['RAISON']  = df['RAISON'].fillna('Inconnu').astype(str).str.strip()
    df['TYPECL']  = df['TYPECL'].fillna('Inconnu').astype(str).str.strip()
    df['CDCLIE']  = df['CDCLIE'].astype(str).str.strip()

    # Strip whitespace from ID
    df['CDCLIE'] = df['CDCLIE'].str.strip()

    print(f"✅ CLIENT cleaned: {len(df)} rows, {len(df.columns)} columns")
    return df


def clean_stock():
    df = pd.read_csv(os.path.join(RAW_DIR, 'stock.csv'))

    # Drop mostly empty columns
    df = df.drop(columns=['NATURE', 'ATEL', 'STR'])

    # Clean numeric columns
    for col in ['QTE_INI', 'QTE_ENT', 'QTE_SOR', 'CUMP']:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

    # Calculate current stock
    df['STOCK_ACTUEL'] = df['QTE_INI'] + df['QTE_ENT'] - df['QTE_SOR']

    # Stock value
    df['VALEUR_STOCK'] = df['STOCK_ACTUEL'] * df['CUMP']

    print(f"✅ STOCK cleaned: {len(df)} rows, {len(df.columns)} columns")
    return df


def clean_article():
    df = pd.read_csv(os.path.join(RAW_DIR, 'article.csv'))
    df['PROD']    = df['PROD'].str.strip()
    df['DESIGNE'] = df['DESIGNE'].str.strip()
    print(f"✅ ARTICLE cleaned: {len(df)} rows, {len(df.columns)} columns")
    return df


# ============================================================
# MASTER FUNCTION
# ============================================================

def clean_all(save=True):
    cleaners = {
        'facture' : clean_facture,
        'ligfac'  : clean_ligfac,
        'client'  : clean_client,
        'stock'   : clean_stock,
        'article' : clean_article,
    }

    dataframes = {}
    for name, func in cleaners.items():
        print(f"⏳ Cleaning {name.upper()}...")
        try:
            df = func()
            if save:
                path = os.path.join(PROCESSED_DIR, f"{name}_clean.csv")
                df.to_csv(path, index=False, encoding='utf-8-sig')
                print(f"   💾 Saved to data/processed/{name}_clean.csv")
            dataframes[name] = df
        except Exception as e:
            print(f"   ❌ Failed: {e}")

    print(f"\n🎉 Cleaning complete! {len(dataframes)} tables cleaned.")
    return dataframes


if __name__ == "__main__":
    clean_all(save=True)