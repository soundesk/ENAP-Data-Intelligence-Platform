# ============================================================
#  src/data/extract.py  — Pull tables from SQL Server
# ============================================================

import pandas as pd
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))
from config.db_config import query_to_df, list_tables

RAW_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data", "raw")


def extract_table(table_name: str, schema: str = "dbo", save: bool = True) -> pd.DataFrame:
    """
    Extract a full table from SQL Server and optionally save to data/raw/.

    Args:
        table_name: Name of the SQL table
        schema: Schema name (default: dbo)
        save: If True, saves result as CSV in data/raw/

    Returns:
        DataFrame with table contents
    """
    print(f"📥 Extracting [{schema}].[{table_name}]...")
    sql = f"SELECT * FROM [{schema}].[{table_name}]"
    df = query_to_df(sql)
    print(f"   ✅ {len(df):,} rows × {len(df.columns)} columns")

    if save:
        os.makedirs(RAW_DIR, exist_ok=True)
        path = os.path.join(RAW_DIR, f"{table_name}.csv")
        df.to_csv(path, index=False, encoding="utf-8-sig")
        print(f"   💾 Saved to data/raw/{table_name}.csv")

    return df


def extract_all_tables(save: bool = True) -> dict:
    """
    Extract ALL tables in the database and save them as CSVs.

    Returns:
        dict of {table_name: DataFrame}
    """
    tables_df = list_tables()
    results = {}
    print(f"🗄️  Found {len(tables_df)} tables to extract\n")

    for _, row in tables_df.iterrows():
        name = row["TABLE_NAME"]
        schema = row["TABLE_SCHEMA"]
        try:
            results[name] = extract_table(name, schema, save=save)
        except Exception as e:
            print(f"   ❌ Failed to extract {name}: {e}")

    print(f"\n✅ Done. Extracted {len(results)} tables.")
    return results


def extract_custom(sql: str, label: str = "custom", save: bool = False) -> pd.DataFrame:
    """Run a custom SQL query and return as DataFrame."""
    print(f"🔍 Running custom query: {label}")
    df = query_to_df(sql)
    print(f"   ✅ {len(df):,} rows × {len(df.columns)} columns")

    if save:
        path = os.path.join(RAW_DIR, f"{label}.csv")
        df.to_csv(path, index=False, encoding="utf-8-sig")
        print(f"   💾 Saved to data/raw/{label}.csv")
    return df


# ── Run this file directly to test the extraction ────────────
if __name__ == "__main__":
    print("=" * 50)
    print("  Data Extraction Script")
    print("=" * 50)
    
    print("\nTesting extraction with two core tables: CLIENT and ARTICLE")
    try:
        extract_all_tables()
        print("\n✅ Extraction complete. Check the 'data/raw/' directory!")
        
        print("\n💡 NOTE: To extract ALL 263 tables, run this in a notebook instead:")
        print("   from src.data.extract import extract_all_tables")
        print("   extract_all_tables()")
    except Exception as e:
        print(f"\n❌ Extraction failed: {e}")
