import sqlite3
import pandas as pd
from database import DB_PATH

conn = sqlite3.connect(DB_PATH)
df = pd.read_sql_query("SELECT * FROM articles", conn)
conn.close()

print("Nombre total d'articles dans la base :", len(df))
print("\nRépartition par entreprise :")
print(df["entreprise_cible"].value_counts())
print("\nAperçu :")
print(df[["entreprise_cible", "title", "ticker_sentiment_label"]].head(5))