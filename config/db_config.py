# ============================================================
#  config/db_config.py  — SQL Server Connection Settings
# ============================================================

import pyodbc
import pandas as pd
import warnings

# Suppress pandas warning about SQLAlchemy since pyodbc is sufficient here
warnings.filterwarnings('ignore', category=UserWarning, module='pandas')

# ── 🔧 Fill in your settings here ───────────────────────────
SERVER   = r"Soundes\SQLEXPRESS"     # raw string avoids \S escape warning
DATABASE = "Asysenap"
# ────────────────────────────────────────────────────────────

# Windows Authentication
CONNECTION_STRING = (
    f"DRIVER={{ODBC Driver 18 for SQL Server}};"
    f"SERVER={SERVER};"
    f"DATABASE={DATABASE};"
    f"Trusted_Connection=yes;"
    f"TrustServerCertificate=yes;"
)


def get_connection():
    """Returns an active pyodbc connection."""
    try:
        conn = pyodbc.connect(CONNECTION_STRING)
        print(f"✅ Connected to [{DATABASE}] on [{SERVER}]")
        return conn
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        raise


def query_to_df(sql: str) -> pd.DataFrame:
    """Execute a SQL query and return a pandas DataFrame."""
    conn = get_connection()
    try:
        df = pd.read_sql(sql, conn)
        return df
    finally:
        conn.close()


def list_tables() -> pd.DataFrame:
    """List all user tables in the database."""
    sql = """
        SELECT TABLE_SCHEMA, TABLE_NAME
        FROM INFORMATION_SCHEMA.TABLES
        WHERE TABLE_TYPE = 'BASE TABLE'
        ORDER BY TABLE_SCHEMA, TABLE_NAME
    """
    return query_to_df(sql)


# ── Run this file directly to test the connection ────────────
if __name__ == "__main__":
    print("=" * 50)
    print(f"  Server  : {SERVER}")
    print(f"  Database: {DATABASE}")
    print("=" * 50)

    print("\n🔌 Testing connection...")
    try:
        conn = get_connection()
        conn.close()

        print("\n📋 Tables found in the database:")
        tables = list_tables()
        if tables.empty:
            print("   ⚠️  No tables found.")
        else:
            for _, row in tables.iterrows():
                print(f"   • [{row['TABLE_SCHEMA']}].[{row['TABLE_NAME']}]")
            print(f"\n✅ Total: {len(tables)} tables")
    except Exception as e:
        print(f"\n❌ Could not connect: {e}")
