# ============================================================
#  src/data/extract.py
#  Extract core tables from Asysnap SQL Server database
# ============================================================

import pandas as pd
import os
import sys

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from config.db_config import query_to_df

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'raw')
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ============================================================
# SQL QUERIES
# ============================================================

QUERIES = {

    "facture": """
        SELECT 
            FACT1, CDCLIE, DATE1, TYPEF,
            MONTHT, REMISE, MONTHTNET,
            MODEPAY, DEPOT, TRIMESTRE,
            CODED, UTILISATEUR
        FROM FACTURE
        WHERE TYPEF = 'F'
        AND MONTHTNET IS NOT NULL
    """,

    "ligfac": """
        SELECT 
            L.FACT1, L.PROD, L.QTEFAC, L.PRIXFAC,
            L.MONTLIG, L.REMISEP, L.GAMME, L.FAM,
            L.CDCLIE, L.TYPECL, L.CODED,
            F.DESIGNE as NomProduit,
            G.DESGAM as NomGamme,
            FA.DESFAM as NomFamille
        FROM LIGFAC L
        LEFT JOIN FPROD F ON L.PROD = F.PROD
        LEFT JOIN FAMILLE FA ON F.FAM = FA.FAM
        LEFT JOIN GAMME G ON FA.GAMME = G.GAMME
    """,

    "client": """
        SELECT 
            CDCLIE, RAISON, TYPECL,
            MODEPAY, SECTEUR, ACTIVITE,
            ADR, adresse, ADRESSE1,
            DEBIT, CREDIT, ECHEANCE,
            DATE_SAISIE, VIGUEUR
        FROM CLIENT
    """,

    "article": """
        SELECT 
            PROD, DESIGNE, FAM, GAMME
        FROM FPROD
    """,

    "stock": """
        SELECT 
            NFICHE, NATURE, ATEL,
            QTE_INI, QTE_ENT, QTE_SOR,
            CUMP, STR
        FROM STOCK
    """,

    "gamme": """
        SELECT GAMME, DESGAM FROM GAMME
    """,

    "famille": """
        SELECT FAM, DESFAM, GAMME FROM FAMILLE
    """
}

# ============================================================
# EXTRACTION FUNCTION
# ============================================================

def extract_all(save=True):
    """Extract all core tables and optionally save to CSV."""
    dataframes = {}

    for name, sql in QUERIES.items():
        print(f"⏳ Extracting {name.upper()}...")
        try:
            df = query_to_df(sql)
            print(f"   ✅ {len(df)} rows extracted")

            if save:
                path = os.path.join(OUTPUT_DIR, f"{name}.csv")
                df.to_csv(path, index=False, encoding='utf-8-sig')
                print(f"   💾 Saved to data/raw/{name}.csv")

            dataframes[name] = df

        except Exception as e:
            print(f"   ❌ Failed: {e}")

    print(f"\n🎉 Extraction complete! {len(dataframes)} tables extracted.")
    return dataframes


def extract_table(name):
    """Extract a single table by name."""
    if name not in QUERIES:
        raise ValueError(f"Unknown table: {name}. Available: {list(QUERIES.keys())}")
    return query_to_df(QUERIES[name])


if __name__ == "__main__":
    extract_all(save=True)