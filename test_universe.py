from core.data import load_idx_universe
import pandas as pd

print("Testing Universe Functions...")
df = load_idx_universe()
print(f"✅ Universe loaded: {len(df)} stocks")
print(f"✅ Sectors: {df['Sector'].nunique()}")
print(f"✅ Top 5 stocks by Market Cap:")
top5 = df.nlargest(5, 'MarketCap')[['Symbol', 'Name', 'Sector']]
print(top5.to_string(index=False))
