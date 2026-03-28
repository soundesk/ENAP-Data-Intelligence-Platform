# ============================================================
#  config/db_config.example.py
#  Copy this file to db_config.py and fill in your settings
# ============================================================

SERVER   = r"YOUR_PC_NAME\SQLEXPRESS"
DATABASE = "YOUR_DATABASE_NAME"

CONNECTION_STRING = (
    f"DRIVER={{ODBC Driver 18 for SQL Server}};"
    f"SERVER={SERVER};"
    f"DATABASE={DATABASE};"
    f"Trusted_Connection=yes;"
    f"TrustServerCertificate=yes;"
)
