import pandas as pd
import os

base = r'C:\Users\dell\Desktop\ENAP - projet pluridisciplinaire\data\raw'
files = ['FACTURE.csv', 'LIGFAC.csv', 'CLIENT.csv', 'ARTICLE.csv', 'STOCK.csv', 'MOUVEMENTS.csv', 'ECRITURE.csv']

print("--- CORE TABLE ANALYSIS ---")
for f in files:
    try:
        path = os.path.join(base, f)
        if not os.path.exists(path):
            continue
            
        # Read just the first row to get columns quickly
        df = pd.read_csv(path, nrows=0)
        size_mb = os.path.getsize(path) / (1024*1024)
        
        print(f"\n📌 {f} ({size_mb:.2f} MB)")
        print(f"   Columns ({len(df.columns)}): {', '.join(list(df.columns)[:8])} ...")
    except Exception as e:
        print(f"Error on {f}: {e}")
