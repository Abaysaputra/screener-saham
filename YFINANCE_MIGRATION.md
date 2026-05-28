# Migrasi ke Yahoo Finance (yfinance)

## 🎯 Ringkasan

Sistem swing trader telah **100% menggunakan yfinance (Yahoo Finance)** sebagai sumber data. Tidak ada lagi dependency ke API eksternal berbayar.

## ✅ Keunggulan

### 1. **Gratis & Tanpa API Key**
- Tidak perlu mendaftar atau membayar
- Tidak ada batasan API calls
- Data langsung dari Yahoo Finance

### 2. **Data Lengkap**
- **Historical data**: Sampai puluhan tahun ke belakang
- **Daily data**: Perfect untuk swing trading
- **Intraday data**: 1m, 5m, 15m, 30m, 1h (untuk analisis detail)
- **Real-time price**: Update setiap menit

### 3. **Cocok untuk Swing Trading**
- Data daily cukup untuk entry/exit decision
- Delay beberapa menit tidak berpengaruh signifikan
- Backtest bisa sampai bertahun-tahun
- Scan sinyal di akhir hari / menjelang close

## 📊 Fungsi-Fungsi Tersedia

### 1. Historical Daily Data
```python
from core.data import get_daily_history_for_scan

# Ambil 120 hari terakhir
df = get_daily_history_for_scan("BBCA", days=120)
```

### 2. Historical Data Custom Range
```python
from core.data import get_history_yf

df = get_history_yf("BBCA.JK", start="2023-01-01", end="2024-12-31")
```

### 3. Real-time Price
```python
from core.data import get_realtime_price

price_data = get_realtime_price("BBCA")
# Returns: {price, open, high, low, volume, change, change_percent}
```

### 4. Intraday Data
```python
from core.data import get_intraday_data

# Data 5 menit untuk 7 hari terakhir
df = get_intraday_data("BBCA", interval="5m", days=7)

# Available intervals: "1m", "5m", "15m", "30m", "1h"
```

### 5. Stock Info
```python
from core.data import get_stock_info

info = get_stock_info("BBCA")
# Returns: market cap, sector, industry, dll
```

## 🔧 Konfigurasi

File `core/config.py` sudah dioptimalkan:

```python
class Config:
    DATA_SOURCE = "yfinance"  # Primary data source
    YF_SUFFIX = ".JK"  # Suffix untuk saham IDX
    
    # Trading Parameters
    DEFAULT_EMA_FAST = 20
    DEFAULT_EMA_SLOW = 50
    DEFAULT_RSI_PERIOD = 14
    DEFAULT_RISK_PER_TRADE = 0.015
```

## 📝 Format Symbol

Semua symbol IDX otomatis ditambahkan suffix `.JK`:
- Input: `BBCA` → Yahoo Finance: `BBCA.JK`
- Input: `TLKM` → Yahoo Finance: `TLKM.JK`
- Input: `BBRI.JK` → Yahoo Finance: `BBRI.JK` (tetap)

## ⚡ Caching Strategy

Untuk performa optimal, semua fungsi menggunakan Streamlit cache:

| Fungsi | Cache TTL | Alasan |
|--------|-----------|--------|
| `get_history_yf` | 1 jam | Historical data jarang berubah |
| `get_daily_history_for_scan` | 10 menit | Scan di market hours |
| `get_realtime_price` | 1 menit | Real-time tapi tidak perlu terlalu sering |
| `get_intraday_data` | 5 menit | Intraday update secukupnya |

## 🚀 Penggunaan

### Scan Harian
1. Masukkan modal per saham di sidebar
2. Set periode scan (hari)
3. Klik "Mulai Scan"
4. Edit modal per saham sesuai keinginan
5. Sistem hitung potential profit otomatis

### Backtest
1. Pilih saham dari watchlist
2. Set periode backtest
3. Atur parameter strategi (EMA, RSI)
4. Jalankan backtest
5. Review hasil dan metrics

### Journal Trading
1. Catat setiap trade (manual atau import)
2. Review performance
3. Analisis win rate, R/R ratio, dll

## 🔍 Testing

Test koneksi yfinance:
1. Buka halaman "Settings"
2. Klik "🧪 Test Data Connection"
3. Jika sukses, akan muncul data BBCA

## 📌 Tips Penggunaan

### 1. Waktu Optimal Scan
- **15:30-16:00 WIB**: Menjelang close untuk sinyal H+1
- **16:00-17:00 WIB**: Setelah close untuk persiapan esok hari

### 2. Data Quality
- Hari libur: Data kosong (normal)
- Suspend saham: Data tidak update
- Corporate action: Cek manual jika ada gap besar

### 3. Backtest
- Gunakan minimal 1-2 tahun data
- Perhatikan periode bearish/bullish
- Test di berbagai kondisi market

### 4. Real-time Price
- Update setiap 1 menit (cached)
- Cukup untuk swing trading
- Untuk intraday aktif, gunakan `get_intraday_data`

## ⚠️ Limitations

1. **Delay**: 
   - Real-time ada delay ~15-20 menit
   - Untuk swing trading, ini tidak masalah
   
2. **Intraday Historical**: 
   - Interval 1m: Max 7 hari
   - Interval lain: Max 60 hari
   - Daily: Unlimited (puluhan tahun)

3. **Market Hours**:
   - Data update saat market buka
   - Weekend/holiday tidak ada update

## 🆚 Perbandingan dengan API Berbayar

| Aspek | yfinance | API Berbayar |
|-------|----------|--------------|
| **Biaya** | ✅ Gratis | ❌ Rp 100rb-1jt/bulan |
| **Setup** | ✅ Install library | ❌ Register, API key |
| **Historical** | ✅ Puluhan tahun | ✅ Tergantung paket |
| **Real-time** | ⚠️ Delay ~15 menit | ✅ True real-time |
| **Intraday** | ✅ 1m, 5m, 15m, 30m, 1h | ✅ Tick by tick |
| **Reliability** | ✅ Sangat baik | ✅ Excellent |
| **Cocok Swing** | ✅ Perfect | ⚠️ Overkill |

## 💡 Kesimpulan

**yfinance adalah pilihan perfect untuk swing trading karena:**

1. ✅ Gratis dan mudah digunakan
2. ✅ Data historical lengkap untuk backtest
3. ✅ Daily data cukup untuk decision making
4. ✅ Delay tidak berpengaruh untuk swing (hold 3-7 hari)
5. ✅ Tidak perlu API key atau registrasi
6. ✅ Reliable dan digunakan banyak trader

**Untuk day trading aktif atau scalping**, baru pertimbangkan API real-time berbayar.

## 📚 Resources

- **yfinance Documentation**: https://github.com/ranaroussi/yfinance
- **Yahoo Finance**: https://finance.yahoo.com
- **IDX Stocks Format**: `SYMBOL.JK` (e.g., BBCA.JK, TLKM.JK)

## 🔄 Backward Compatibility

Fungsi lama `get_realtime_goapi()` masih tersedia sebagai alias ke `get_realtime_price()` untuk backward compatibility. Namun disarankan menggunakan nama baru.

---

**Update terakhir**: 17 Januari 2026
**Status**: ✅ Production Ready
