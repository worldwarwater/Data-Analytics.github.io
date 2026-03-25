#!/usr/bin/env python3
"""
Execute SQL queries and display results in a formatted output file
Results saved to: data/processed/query_results.txt
"""

import sqlite3
import pandas as pd
import re

# Connect to database
conn = sqlite3.connect('data/processed/marketing.db')

# Read SQL file
with open('sql/analysis_queries.sql', 'r') as f:
    sql_content = f.read()

# Parse queries (split by -- before each query description)
query_blocks = re.split(r'(?=-- ────)', sql_content)

output_file = 'data/processed/query_results.txt'

with open(output_file, 'w') as out:
    out.write("="*80 + "\n")
    out.write("MARKETING CAMPAIGN ANALYSIS — SQL QUERY RESULTS\n")
    out.write("="*80 + "\n\n")
    
    query_num = 0
    
    for block in query_blocks:
        block = block.strip()
        if not block:
            continue
        
        # Extract query description and SQL
        lines = block.split('\n')
        description = []
        sql_query = []
        in_sql = False
        
        for line in lines:
            if line.startswith('SELECT') or line.startswith('WITH'):
                in_sql = True
            
            if in_sql:
                sql_query.append(line)
            elif line.startswith('--'):
                description.append(line.replace('--', '').strip())
        
        sql_str = '\n'.join(sql_query).strip()
        
        if not sql_str:
            continue
        
        query_num += 1
        
        # Write to output file
        out.write(f"\n{'='*80}\n")
        out.write(f"QUERY {query_num}: {' '.join(description[:2])}\n")
        out.write(f"{'='*80}\n\n")
        
        try:
            # Execute query
            df = pd.read_sql(sql_str, conn)
            
            # Write results
            out.write(df.to_string(index=False))
            out.write(f"\n\n[{len(df)} rows returned]\n")
            
            # Also print to console
            print(f"✓ Query {query_num}: {' '.join(description[:2])}")
        
        except Exception as e:
            out.write(f"ERROR: {str(e)}\n")
            print(f"✗ Query {query_num} failed: {str(e)}")

conn.close()

print(f"\n✅ Results saved to: {output_file}")
print(f"   Open with: cat data/processed/query_results.txt")
