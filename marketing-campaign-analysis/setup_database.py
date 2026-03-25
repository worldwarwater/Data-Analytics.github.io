#!/usr/bin/env python3
"""
Setup script to create SQLite database from marketing_segmented.csv
Run once before executing SQL queries
"""

import sqlite3
import pandas as pd

# Load the segmented data
print("📁 Loading data from marketing_segmented.csv...")
df = pd.read_csv('data/processed/marketing_segmented.csv')
print(f"   ✓ Loaded {len(df)} rows, {len(df.columns)} columns")

# Create/connect to database
print("🗄️  Creating SQLite database...")
conn = sqlite3.connect('data/processed/marketing.db')

# Load into database
df.to_sql('customers', conn, if_exists='replace', index=False)
print("   ✓ Loaded data into 'customers' table")

conn.close()
print("\n✅ Database ready! Run SQL queries with:")
print("   sqlite3 data/processed/marketing.db < sql/analysis_queries.sql")
