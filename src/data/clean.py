# ============================================================
#  src/data/clean.py  — Data Cleaning Functions
# ============================================================

import pandas as pd
import numpy as np
import os

PROCESSED_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data", "processed")


def save_processed(df: pd.DataFrame, name: str):
    """Save a cleaned DataFrame to data/processed/."""
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    path = os.path.join(PROCESSED_DIR, f"{name}.csv")
    df.to_csv(path, index=False, encoding="utf-8-sig")
    print(f"💾 Saved to data/processed/{name}.csv")


def basic_clean(df: pd.DataFrame, name: str = "table") -> pd.DataFrame:
    """
    Apply basic cleaning to any DataFrame:
    - Drop full duplicates
    - Strip string columns
    - Report missing values
    """
    original_shape = df.shape
    df = df.drop_duplicates()
    str_cols = df.select_dtypes(include="object").columns
    df[str_cols] = df[str_cols].apply(lambda col: col.str.strip())

    print(f"🧹 Cleaned [{name}]: {original_shape} → {df.shape}")
    missing = df.isnull().sum()
    missing = missing[missing > 0]
    if not missing.empty:
        print(f"   ⚠️  Missing values:\n{missing.to_string()}")
    else:
        print("   ✅ No missing values")
    return df


def clean_dates(df: pd.DataFrame, date_cols: list) -> pd.DataFrame:
    """Convert date columns to datetime."""
    for col in date_cols:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")
            print(f"   📅 Converted [{col}] to datetime")
    return df


def clean_numeric(df: pd.DataFrame, num_cols: list, fill_value=0) -> pd.DataFrame:
    """Convert columns to numeric and fill NaN."""
    for col in num_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(fill_value)
    return df


def remove_outliers_iqr(df: pd.DataFrame, col: str, factor: float = 1.5) -> pd.DataFrame:
    """Remove outliers using IQR method."""
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    before = len(df)
    df = df[(df[col] >= Q1 - factor * IQR) & (df[col] <= Q3 + factor * IQR)]
    print(f"   🔍 Outlier removal [{col}]: {before} → {len(df)} rows ({before - len(df)} removed)")
    return df
