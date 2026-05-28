"""
Quick verification script for Market-Wide Screener implementation
Run this to verify all components are working
"""

import sys
from pathlib import Path

print("=" * 60)
print("Market-Wide Screener - Verification Script")
print("=" * 60)

# Check files
print("\n📁 Checking Files...")
files_to_check = [
    "idx_universe.csv",
    "pages/0_🌍_Universe_Filter.py",
    "UNIVERSE_UPDATE_GUIDE.md",
    "MARKET_WIDE_SCREENER_SUMMARY.md"
]

all_good = True
for file in files_to_check:
    file_path = Path(file)
    if file_path.exists():
        print(f"✅ {file}")
    else:
        print(f"❌ {file} - NOT FOUND!")
        all_good = False

# Check universe data
print("\n📊 Checking Universe Data...")
try:
    import pandas as pd
    df = pd.read_csv("idx_universe.csv")
    print(f"✅ Universe loaded: {len(df)} stocks")
    print(f"   Sectors: {df['Sector'].nunique()}")
    print(f"   Columns: {', '.join(df.columns.tolist())}")
    
    # Check required columns
    required_cols = ['Symbol', 'Name', 'Sector', 'MarketCap', 'AvgVolume', 'LastPrice']
    missing = [col for col in required_cols if col not in df.columns]
    if missing:
        print(f"❌ Missing columns: {missing}")
        all_good = False
    else:
        print("✅ All required columns present")
        
except Exception as e:
    print(f"❌ Error loading universe: {e}")
    all_good = False

# Check core functions
print("\n🔧 Checking Core Functions...")
try:
    from core.data import load_idx_universe, get_universe_symbols, merge_watchlist_and_universe
    print("✅ Universe utility functions imported")
    
    # Test load
    df = load_idx_universe()
    if not df.empty:
        print(f"✅ load_idx_universe() works: {len(df)} stocks")
    else:
        print("❌ load_idx_universe() returned empty")
        all_good = False
        
    # Test get symbols
    symbols = get_universe_symbols(df)
    if symbols:
        print(f"✅ get_universe_symbols() works: {len(symbols)} symbols")
    else:
        print("❌ get_universe_symbols() returned empty")
        all_good = False
        
except Exception as e:
    print(f"❌ Error testing functions: {e}")
    all_good = False

# Check page files
print("\n📄 Checking Page Files...")
try:
    # Check Universe Filter page
    with open("pages/0_🌍_Universe_Filter.py", "r", encoding="utf-8") as f:
        content = f.read()
        if "Universe Filter" in content and "filtered_universe" in content:
            print("✅ Universe Filter page looks good")
        else:
            print("❌ Universe Filter page may have issues")
            all_good = False
    
    # Check Scan Harian integration
    with open("pages/1_📊_Scan_Harian.py", "r", encoding="utf-8") as f:
        content = f.read()
        if "merge_watchlist_and_universe" in content and "use_universe" in content:
            print("✅ Scan Harian integration looks good")
        else:
            print("❌ Scan Harian may not be integrated properly")
            all_good = False
            
except Exception as e:
    print(f"❌ Error checking pages: {e}")
    all_good = False

# Final summary
print("\n" + "=" * 60)
if all_good:
    print("✅ ALL CHECKS PASSED!")
    print("\n🚀 Ready to use Market-Wide Screener!")
    print("\nNext steps:")
    print("1. Run: streamlit run Home.py")
    print("2. Open Universe Filter page")
    print("3. Apply filters and see results")
    print("4. Go to Scan Harian and enable 'Gunakan Filtered Universe'")
else:
    print("❌ SOME CHECKS FAILED!")
    print("\nPlease review the errors above and fix them.")

print("=" * 60)
