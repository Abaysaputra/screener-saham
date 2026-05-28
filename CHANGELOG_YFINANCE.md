# Changelog - Migrasi ke Yahoo Finance

## [2.0.0] - 2026-01-17

### 🎯 Major Changes - 100% Yahoo Finance Migration

#### ✨ Added

**Data Module (`core/data.py`)**
- ✅ `get_realtime_price()` - Real-time price menggunakan yfinance (cache 1 menit)
- ✅ `get_intraday_data()` - Intraday data dengan interval 1m, 5m, 15m, 30m, 1h
- ✅ `get_stock_info()` - Stock information dari Yahoo Finance
- ✅ Backward compatibility: `get_realtime_goapi()` sebagai alias

**Configuration (`core/config.py`)**
- ✅ `DATA_SOURCE = "yfinance"` - Primary data source
- ✅ `YF_SUFFIX = ".JK"` - Auto suffix untuk IDX stocks
- ❌ Removed: `API_GOAPI_KEY`, `GOAPI_BASE_URL` (tidak diperlukan)

**Documentation**
- ✅ `YFINANCE_MIGRATION.md` - Dokumentasi lengkap migrasi yfinance
- ✅ `CHANGELOG_YFINANCE.md` - Changelog perubahan (file ini)
- ✅ Updated `README.md` - Mencerminkan penggunaan yfinance

**UI/UX (`pages/1_📊_Scan_Harian.py`)**
- ✅ Modal per saham dapat diatur di sidebar sebagai default
- ✅ Modal dapat diedit manual per saham di tabel hasil
- ✅ Perhitungan dinamis: Size, Potential Profit/Loss berdasarkan modal user
- ✅ Dua tabel: Input modal & Detail perhitungan

**Homepage (`Home.py`)**
- ✅ Badge "100% Gratis - No API Key Required"
- ✅ Penjelasan keunggulan yfinance untuk swing trading
- ✅ Tips optimal waktu scan dan strategi modal
- ✅ Link ke dokumentasi yfinance

**Settings (`pages/4_⚙️_Settings.py`)**
- ✅ "Test Data Connection" menggunakan yfinance
- ❌ Removed: "Test API Connection" untuk GOAPI

#### 🔧 Modified

**Data Fetching**
- 🔄 Semua fungsi data menggunakan yfinance
- 🔄 Cache strategy dioptimalkan:
  - Historical: 1 jam
  - Daily scan: 10 menit  
  - Real-time: 1 menit
  - Intraday: 5 menit
- 🔄 Error handling ditingkatkan
- 🔄 Logging lebih detail

**Symbol Handling**
- 🔄 `normalize_symbol()` otomatis menambahkan `.JK` suffix
- 🔄 User input tetap tanpa suffix (BBCA, TLKM)
- 🔄 Internal: semua symbol dengan suffix (BBCA.JK, TLKM.JK)

#### ❌ Removed

**Dependencies**
- ❌ `requests` library (tidak diperlukan)
- ❌ API key management untuk GOAPI
- ❌ Real-time API berbayar

**Configuration**
- ❌ `API_GOAPI_KEY` environment variable
- ❌ `GOAPI_BASE_URL` environment variable
- ❌ API validation di `Config.validate()`

### 📊 Impact

#### Positive
- ✅ **Cost**: Rp 0/bulan (dari yang tadinya Rp 100rb-1jt/bulan)
- ✅ **Setup**: 30 detik (dari 5-10 menit dengan API key)
- ✅ **Data Quality**: Sama reliable untuk swing trading
- ✅ **Historical**: Data sampai puluhan tahun
- ✅ **Maintenance**: Minimal, tidak perlu manage API keys

#### Trade-offs
- ⚠️ **Real-time Delay**: ~15-20 menit (acceptable untuk swing)
- ⚠️ **Intraday Limit**: 1m data max 7 hari (cukup untuk analisis)

### 🎯 Use Cases

#### Perfect For ✅
- Swing trading (hold 3-7 hari)
- Daily signal scanning
- Historical backtesting
- End-of-day analysis
- Educational purpose

#### Not Ideal For ⚠️
- Day trading aktif (butuh tick-by-tick)
- Scalping (<1 menit)
- High-frequency trading
- True real-time arbitrage

### 📚 Documentation Updates

**New Files**
- `YFINANCE_MIGRATION.md` - Comprehensive guide
- `CHANGELOG_YFINANCE.md` - This file

**Updated Files**
- `README.md` - Added yfinance info, updated setup, tips
- `Home.py` - New UI, yfinance badge, tips
- `ARCHITECTURE.md` - Updated data layer

### 🚀 Migration Guide

#### For New Users
1. Clone repo
2. `pip install -r requirements.txt`
3. Edit `watchlist.txt`
4. `streamlit run Home.py`
5. Done! ✅

#### For Existing Users
1. Pull latest changes
2. No need to update `.env` (API keys optional)
3. Test connection in Settings
4. Previous watchlist still works
5. Previous journal data preserved

### 🧪 Testing

**Tested Features**
- ✅ Daily data fetching (BBCA, TLKM, BBRI)
- ✅ Historical data (1 year, 5 years, 10 years)
- ✅ Real-time price (all IDX stocks)
- ✅ Intraday data (1m, 5m, 15m, 30m, 1h)
- ✅ Scan harian with manual modal
- ✅ Backtest dengan data historical
- ✅ Symbol normalization (.JK suffix)
- ✅ Error handling & logging
- ✅ Cache performance

**Test Environment**
- Python 3.8+
- Windows 10/11
- Internet connection required
- No proxy tested yet

### 💡 Best Practices

**Modal Management**
1. Set default modal per saham di sidebar (misal Rp 10jt)
2. Edit manual di tabel untuk fine-tuning
3. Prioritas R/R > 2 dapat alokasi lebih
4. Reserve 10-20% untuk averaging down

**Scanning Strategy**
1. Scan 15:30-16:00 WIB (menjelang close)
2. Review hasil, edit modal
3. Prepare order untuk H+1
4. Re-scan 08:55-09:00 WIB (pre-market check)

**Data Usage**
1. Daily data untuk swing entry/exit
2. Intraday 15m/30m untuk confirmation
3. Historical untuk backtest dan learning
4. Real-time untuk quick price check

### 🐛 Known Issues

1. **Weekend/Holiday**: Data tidak update (normal)
2. **Suspended Stocks**: Data akan kosong atau tidak update
3. **Corporate Action**: Manual check jika ada gap besar
4. **Connection**: Perlu internet stabil

### 🔮 Future Enhancements

**Planned**
- [ ] Multi-timeframe analysis (D, W, M)
- [ ] Volume analysis
- [ ] Support/Resistance detection
- [ ] Multiple strategy comparison
- [ ] Export dengan chart ke PDF

**Under Consideration**
- [ ] Intraday signal scanning
- [ ] Alert system (Telegram/Email)
- [ ] Portfolio tracker
- [ ] Paper trading simulator

### 📞 Support

**Issues**
- yfinance not working? Check internet connection
- Symbol not found? Verify ticker di Yahoo Finance
- Slow performance? Clear Streamlit cache

**Resources**
- yfinance docs: https://github.com/ranaroussi/yfinance
- Yahoo Finance: https://finance.yahoo.com
- IDX tickers: https://www.idx.co.id

### 🙏 Credits

- **yfinance** by Ran Aroussi - Amazing free library
- **Yahoo Finance** - Reliable data source
- **Streamlit** - Beautiful framework
- **Indonesian Trading Community** - Feedback & support

---

**Version**: 2.0.0  
**Release Date**: 17 Januari 2026  
**Status**: ✅ Production Ready  
**Breaking Changes**: None (backward compatible)
