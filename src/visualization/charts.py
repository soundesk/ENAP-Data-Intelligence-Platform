# ============================================================
#  src/visualization/charts.py  — Reusable Chart Functions
# ============================================================

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os

# ── Global style ─────────────────────────────────────────────
sns.set_theme(style="darkgrid", palette="muted")
FIGURES_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "rapport", "figures")


def save_fig(name: str, dpi: int = 150):
    """Save current figure to rapport/figures/."""
    os.makedirs(FIGURES_DIR, exist_ok=True)
    path = os.path.join(FIGURES_DIR, f"{name}.png")
    plt.savefig(path, dpi=dpi, bbox_inches="tight")
    print(f"📊 Figure saved: rapport/figures/{name}.png")


def plot_time_series(df: pd.DataFrame, x: str, y: str, title: str = "", save: bool = False):
    """Line plot for time series data."""
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(df[x], df[y], linewidth=2, color="#4A90D9")
    ax.set_title(title or f"{y} over time", fontsize=14, fontweight="bold")
    ax.set_xlabel(x)
    ax.set_ylabel(y)
    plt.tight_layout()
    if save:
        save_fig(title.replace(" ", "_").lower())
    plt.show()


def plot_bar(df: pd.DataFrame, x: str, y: str, title: str = "", top_n: int = None, save: bool = False):
    """Horizontal bar chart."""
    data = df.sort_values(y, ascending=False)
    if top_n:
        data = data.head(top_n)
    fig, ax = plt.subplots(figsize=(10, max(4, len(data) * 0.4)))
    sns.barplot(data=data, x=y, y=x, palette="Blues_d", ax=ax)
    ax.set_title(title or f"{y} by {x}", fontsize=14, fontweight="bold")
    plt.tight_layout()
    if save:
        save_fig(title.replace(" ", "_").lower())
    plt.show()


def plot_distribution(df: pd.DataFrame, col: str, title: str = "", save: bool = False):
    """Histogram + KDE distribution plot."""
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.histplot(df[col].dropna(), kde=True, color="#4A90D9", ax=ax)
    ax.set_title(title or f"Distribution of {col}", fontsize=14, fontweight="bold")
    plt.tight_layout()
    if save:
        save_fig(title.replace(" ", "_").lower())
    plt.show()


def plot_correlation_matrix(df: pd.DataFrame, title: str = "Correlation Matrix", save: bool = False):
    """Heatmap of correlations between numeric columns."""
    corr = df.select_dtypes(include="number").corr()
    fig, ax = plt.subplots(figsize=(12, 8))
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", ax=ax, linewidths=0.5)
    ax.set_title(title, fontsize=14, fontweight="bold")
    plt.tight_layout()
    if save:
        save_fig(title.replace(" ", "_").lower())
    plt.show()


def plot_missing_values(df: pd.DataFrame, save: bool = False):
    """Bar chart of missing values per column."""
    missing = df.isnull().sum()
    missing = missing[missing > 0].sort_values(ascending=False)
    if missing.empty:
        print("✅ No missing values found!")
        return
    fig, ax = plt.subplots(figsize=(10, 4))
    missing.plot(kind="bar", color="#E74C3C", ax=ax)
    ax.set_title("Missing Values per Column", fontsize=14, fontweight="bold")
    ax.set_ylabel("Count")
    plt.tight_layout()
    if save:
        save_fig("missing_values")
    plt.show()
