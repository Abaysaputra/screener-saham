# Swing Trader IDX

Aplikasi Swing Trading Assistant untuk saham Indonesia (IDX) dengan analisis teknikal otomatis dan manajemen risiko.

**🎯 100% menggunakan Yahoo Finance (yfinance) - Gratis & No API Key Required!**

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-red.svg)
![yfinance](https://img.shields.io/badge/Data-Yahoo%20Finance-purple.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## 🎯 Fitur Utama

- **📊 Scan Harian**: Deteksi sinyal BUY otomatis dari watchlist dengan modal yang bisa diatur manual
- **📈 Backtest**: Uji strategi pada data historis dengan visualisasi lengkap
- **� Parameter Optimization**: Grid search untuk temukan parameter terbaik dengan sensitivity analysis
- **📊 Fundamental Analysis**: Filter saham berdasarkan kualitas fundamental (EPS, PE, PB, dll)
- **📓 Trading Journal**: Tracking dan analisis performa trading
- **⚙️ Konfigurasi Fleksibel**: Parameter trading yang bisa disesuaikan
- **💰 Risk Management**: Kalkulasi position size berbasis modal yang Anda tentukan
- **📉 Technical Analysis**: EMA crossover dan RSI indicators
- **🔄 Modal Dinamis**: Input modal per saham secara manual untuk kontrol penuh
- **🎯 R/R Ratio**: Dropdown untuk pilih Risk/Reward ratio target (1.0 - 4.0)

## 🌟 Data Source

Aplikasi ini menggunakan **yfinance (Yahoo Finance)** sebagai sumber data:

✅ **Gratis** - Tidak perlu API key atau biaya berlangganan
✅ **Historical Data** - Data sampai puluhan tahun ke belakang untuk backtest
✅ **Daily & Intraday** - Support 1m, 5m, 15m, 30m, 1h, 1d intervals
✅ **Reliable** - Data dari Yahoo Finance yang sudah terpercaya
✅ **Perfect untuk Swing** - Delay beberapa menit tidak berpengaruh untuk swing trading

Lihat [YFINANCE_MIGRATION.md](YFINANCE_MIGRATION.md) untuk detail lengkap.

## 🚀 Quick Start

### Prerequisites

- Python 3.8 atau lebih baru
- pip (Python package manager)

### Instalasi

1. **Clone atau download repository ini**

```bash
git clone https://github.com/yourusername/swing_trader.git
cd swing_trader
```

2. **Install dependencies**

```bash
pip install -r requirements.txt
```

3. **Setup Watchlist**

Edit file `watchlist.txt` dan tambahkan kode saham:

```
BBCA
BBRI
BMRI
TLKM
ASII
```

**Note**: Tidak perlu menambahkan `.JK` suffix, sistem akan otomatis menambahkannya.

4. **Jalankan Aplikasi**

```bash
streamlit run Home.py
```

Aplikasi akan terbuka di browser: `http://localhost:8501`

**Tidak perlu setup API key atau konfigurasi tambahan!** 🎉

## ☁️ Deploy Cepat ke Streamlit Cloud

Opsi ini paling realistis untuk repo saat ini karena aplikasi sudah berbasis Streamlit.

### Syarat minimum

1. Pastikan repo sudah ada di GitHub.
2. Pastikan file [requirements.txt](requirements.txt) ada dan up to date.
3. Commit file [\.streamlit/config.toml](.streamlit/config.toml) ke GitHub.

### Langkah deploy

1. Buka Streamlit Community Cloud.
2. Klik New app.
3. Pilih repository GitHub ini.
4. Set main file path ke `Home.py`.
5. Klik Deploy.

### Catatan penting

- Gunakan `Home.py` sebagai entry point, bukan `run.py`.
- File `watchlist.txt` dan `trades_journal.csv` saat ini masih memakai storage lokal, jadi data bisa reset saat redeploy.
- Untuk pemakaian awal, cukup baca data dari watchlist yang sudah ada di repo dan hindari fitur yang menulis file jika Anda belum pindah ke storage eksternal.
- Kalau `.streamlit/config.toml` belum ikut ke GitHub, tambahkan dulu sebelum deploy.

### Jangan deploy aplikasi Streamlit ini sebagai Vercel Python Function

Aplikasi ini menggunakan server Streamlit yang berjalan terus-menerus, bukan handler HTTP
serverless. Vercel akan mencoba membundel seluruh dependency Python ke Lambda dan memiliki
batas bundle 500 MB. Dependency seperti `pandas`, `numpy`, `pyarrow`, `plotly`, dan
`streamlit` dapat melewati batas tersebut, sehingga build gagal sebelum aplikasi dijalankan.

Gunakan Streamlit Community Cloud untuk deployment seperti pada langkah di atas. Jika Vercel
harus digunakan, aplikasi perlu diubah menjadi API/serverless function terpisah dan frontend
Streamlit tidak dapat dipakai apa adanya.

### Checklist sebelum klik Deploy

- [ ] `requirements.txt` lolos install lokal
- [ ] `Home.py` bisa jalan dengan `streamlit run Home.py`
- [ ] `.streamlit/config.toml` sudah committed
- [ ] `watchlist.txt` berisi daftar saham awal yang valid
- [ ] Tidak ada dependency yang butuh file write persisten untuk alur utama

## 📁 Struktur Project

```
swing_trader/
├── Home.py                      # Main entry point
├── pages/                       # Multi-page app
│   ├── 1_📊_Scan_Harian.py    # Daily scanner
│   ├── 2_📈_Backtest.py        # Backtesting engine
│   ├── 3_📓_Journal.py         # Trading journal
│   └── 4_⚙️_Settings.py       # Settings page
├── core/                        # Core modules
│   ├── config.py               # Configuration management
│   └── data.py                 # Data fetching with caching
├── utils/                       # Utility functions
│   ├── indicators.py           # Technical indicators
│   ├── strategy.py             # Trading strategy
│   ├── risk.py                 # Risk management
│   ├── backtest.py             # Backtesting logic
│   └── journal.py              # Journal management
├── watchlist.txt               # Stock watchlist
├── trades_journal.csv          # Trading journal data
├── requirements.txt            # Python dependencies
├── .env.example               # Environment template
└── README.md                  # This file
```

## 📊 Strategi Trading

### Entry Signal (BUY)
- EMA Fast (20) cross above EMA Slow (50)
- RSI < 70 (tidak overbought)

### Exit Signal
- **Stop Loss**: 2% di bawah entry price
- **Take Profit**: 2R (2x risiko)
- **Sell Signal**: EMA Fast cross below EMA Slow

### Risk Management
- Position sizing berdasarkan modal yang Anda tentukan secara manual
- Stop Loss: 2% di bawah entry price
- Take Profit: 2R (2x risiko)
- Lot size BEI: 100 shares

## 🎓 Cara Penggunaan

### 1. Scan Harian

1. Buka menu "Scan Harian" di sidebar
2. **Atur Modal per Saham (Default)**: Input modal default untuk setiap saham (misal Rp 10 juta)
3. **Atur Total Modal**: Total modal tersedia untuk validasi
4. **[OPSIONAL] Filter Fundamental**: Aktifkan untuk filter saham berkualitas
   - EPS Positif (hindari saham rugi)
   - PE Ratio < 25 (hindari overvalued)
   - PB Ratio < 3 (hindari premium berlebihan)
   - Profit Margin > 5% (perusahaan efisien)
   - Market Cap > 1T (fokus large cap)
5. Atur periode scan dan RSI maksimum
6. Klik "Mulai Scan"
7. **Edit Modal per Saham**: Klik kolom "Modal Dialokasikan" untuk mengubah modal setiap saham
8. **Review Fundamental**: Jika filter aktif, lihat detail fundamental setiap saham
9. Sistem akan otomatis menghitung:
   - Size (jumlah saham yang bisa dibeli)
   - Potential Profit (berdasarkan modal Anda)
   - Potential Loss
   - Risk/Reward Ratio
10. Download hasil jika diperlukan

**Keunggulan Fitur Modal Dinamis + Fundamental:**
- ✅ Anda yang menentukan berapa modal untuk setiap saham
- ✅ Filter saham berkualitas (hindari gorengan)
- ✅ Kombinasi teknikal + fundamental = strategi robust
- ✅ Bisa diversifikasi dengan modal berbeda-beda
- ✅ Perhitungan profit otomatis berdasarkan modal Anda
- ✅ Total modal dialokasikan akan dibandingkan dengan modal tersedia

### 2. Backtest

**Single Backtest:**
1. Buka tab "Single Backtest"
2. Pilih saham dari watchlist
3. **[OPSIONAL]** Aktifkan "Cek Fundamental Saham" untuk review kualitas
4. Atur periode dan parameter
5. Klik "Jalankan Backtest"
6. Analisis hasil dan metrik performa

**Parameter Optimization:**
1. Buka tab "Parameter Optimization"
2. Pilih saham dan periode (minimal 2-3 tahun)
3. **[OPSIONAL]** Aktifkan "Cek Fundamental" untuk confidence
4. Pilih range parameter untuk test (SL%, TP R, RSI)
5. Klik "Run Parameter Optimization"
6. Review:
   - Top 10 kombinasi parameter terbaik
   - Heatmap sensitivity analysis
   - Robustness analysis
   - Consistency score
7. Pilih parameter dari area "hijau" yang luas (robust)

### 3. Trading Journal

1. Buka menu "Journal"
2. Review performa trading Anda
3. Analisis equity curve dan statistik
4. Download journal untuk analisis lebih lanjut

### 4. Settings

1. Buka menu "Settings"
2. Manage watchlist
3. Atur parameter trading default
4. **Test koneksi yfinance**: Klik "🧪 Test Data Connection"

## 📊 Fundamental Analysis

Aplikasi ini mendukung **analisa fundamental ringan** untuk filter saham berkualitas:

### Metrik yang Didukung:
- **EPS (Earnings Per Share)**: Filter saham profitable
- **PE Ratio**: Valuasi harga (undervalued/overvalued)
- **PB Ratio**: Price to Book value
- **Profit Margin**: Efisiensi operasional
- **ROE**: Return on Equity
- **Market Cap**: Ukuran dan likuiditas

### Kapan Menggunakan?
- ✅ Swing Trading (3-7 hari hold)
- ✅ Position Trading (> 1 minggu)
- ❌ Scalping/Intraday (teknikal lebih penting)

### Recommended Settings:
```
EPS Positif: ✅ (hindari saham rugi)
PE Ratio < 25: ✅ (hindari overvalued)
Market Cap > 1T: ✅ (fokus large cap)
```

**Lihat [FUNDAMENTAL_ANALYSIS_GUIDE.md](FUNDAMENTAL_ANALYSIS_GUIDE.md) untuk panduan lengkap.**

## 🔧 Konfigurasi

### Parameter Trading (Opsional)

Buat file `.env` untuk konfigurasi custom:

```env
# Trading Parameters
DEFAULT_EMA_FAST=20
DEFAULT_EMA_SLOW=50
DEFAULT_RSI_PERIOD=14
DEFAULT_RISK_PER_TRADE=0.015
LOT_SIZE=100

# App Configuration
DEFAULT_CAPITAL=100000000
```

**Note**: Tidak perlu setup GOAPI_KEY atau API keys lainnya!

### Watchlist

Edit `watchlist.txt`:
- Satu kode saham per baris
- Tanpa `.JK` suffix (otomatis ditambahkan)
- Contoh: `BBCA`, `BBRI`, `TLKM`

## 📦 Dependencies

- **streamlit**: Web framework
- **pandas**: Data manipulation
- **yfinance**: Stock data dari Yahoo Finance (FREE!)
- **plotly**: Interactive charts
- **ta**: Technical analysis indicators
- **python-dotenv**: Environment management (optional)

Lihat `requirements.txt` untuk daftar lengkap.

## 💡 Tips Penggunaan

### Waktu Optimal untuk Scan
- **15:30-16:00 WIB**: Menjelang close untuk sinyal H+1
- **16:00-17:00 WIB**: Setelah close untuk persiapan esok hari
- **Pagi hari**: Review sinyal kemarin dan prepare entry

### Strategi Modal
1. **Diversifikasi**: Alokasikan modal berbeda untuk setiap saham
2. **Prioritas**: Saham dengan R/R > 2 dapat alokasi lebih besar
3. **Validasi**: Pastikan total modal tidak melebihi yang tersedia
4. **Reserve**: Sisakan 10-20% modal untuk averaging down jika perlu

## ⚠️ Disclaimer

Aplikasi ini dibuat untuk tujuan **edukasi dan research** saja.

- Trading saham mengandung risiko tinggi
- Tidak ada jaminan profit
- Selalu lakukan riset sendiri (DYOR)
- Gunakan modal yang siap Anda rugikan
- Past performance tidak menjamin hasil masa depan

**Penulis tidak bertanggung jawab atas kerugian trading Anda!**

## 🤝 Contributing

Kontribusi sangat diterima! Jika Anda ingin berkontribusi:

1. Fork repository ini
2. Buat branch baru (`git checkout -b feature/AmazingFeature`)
3. Commit perubahan (`git commit -m 'Add some AmazingFeature'`)
4. Push ke branch (`git push origin feature/AmazingFeature`)
5. Buat Pull Request

## 📝 TODO

- [ ] Multiple timeframe analysis
- [ ] Multiple strategy support
- [ ] Advanced technical indicators (MACD, Bollinger Bands)
- [ ] Portfolio management
- [ ] Export to Excel/PDF with charts
- [ ] Telegram/Email notifications
- [ ] Dark mode UI
- [ ] Multi-language support

## 📚 Documentation

- [YFINANCE_MIGRATION.md](YFINANCE_MIGRATION.md) - Detail tentang penggunaan yfinance
- [ARCHITECTURE.md](ARCHITECTURE.md) - Arsitektur aplikasi
- [QUICKSTART.md](QUICKSTART.md) - Panduan cepat memulai

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Yahoo Finance** untuk data gratis dan reliable
- **yfinance library** oleh Ran Aroussi
- **Streamlit** untuk framework yang luar biasa
- **Indonesian trading community**

---

**Happy Swing Trading! 📈💰**

*Trade with discipline, manage your risk, and never stop learning!*

**Ingat**: Modal yang Anda input menentukan potential profit Anda. Invest wisely! 🎯
