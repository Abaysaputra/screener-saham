# Swing Trader IDX - Installation Guide

## 📋 Prerequisites

Sebelum memulai, pastikan Anda sudah menginstall:

- **Python 3.8 atau lebih baru**
  - Download: https://www.python.org/downloads/
  - Untuk Windows: Centang "Add Python to PATH" saat instalasi

- **pip** (biasanya sudah include dengan Python)
  - Cek dengan: `python --version` dan `pip --version`

## 🚀 Langkah Instalasi

### Opsi 1: Quick Start (Recommended)

1. **Buka Terminal/Command Prompt di folder aplikasi**

2. **Jalankan script setup:**
   ```bash
   python run.py
   ```
   
   Script ini akan otomatis:
   - Install semua dependencies
   - Setup watchlist default
   - Menjalankan aplikasi

3. **Aplikasi akan terbuka di browser:**
   ```
   http://localhost:8501
   ```

### Opsi 2: Manual Installation

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Setup Watchlist** (opsional)
   
   Edit file `watchlist.txt`:
   ```
   BBCA
   BBRI
   BMRI
   TLKM
   ASII
   ```

3. **Setup Configuration** (opsional)
   
   Copy `.env.example` ke `.env`:
   ```bash
   copy .env.example .env  # Windows
   cp .env.example .env    # Linux/Mac
   ```
   
   Edit `.env` sesuai kebutuhan.

4. **Jalankan Aplikasi**
   ```bash
   streamlit run Home.py
   ```

## ⚙️ Konfigurasi

### Environment Variables (.env)

```env
# API Configuration
GOAPI_KEY=your_api_key_here      # Dapatkan dari goapi.io
GOAPI_BASE_URL=https://api.goapi.io

# Trading Parameters
DEFAULT_EMA_FAST=20               # EMA fast period
DEFAULT_EMA_SLOW=50               # EMA slow period
DEFAULT_RSI_PERIOD=14             # RSI period
DEFAULT_RISK_PER_TRADE=0.015      # 1.5% risk per trade
LOT_SIZE=100                      # BEI lot size

# App Configuration
DEFAULT_CAPITAL=100000000         # Default capital
```

### Watchlist (watchlist.txt)

Format: Satu kode saham per baris, tanpa .JK

```
BBCA
BBRI
BMRI
TLKM
ASII
UNVR
ICBP
```

## 🔧 Troubleshooting

### Error: "Module not found"

**Solusi:**
```bash
pip install -r requirements.txt --upgrade
```

### Error: "Port 8501 already in use"

**Solusi:**
```bash
# Gunakan port lain
streamlit run Home.py --server.port 8502
```

### Error: "No data found for symbol"

**Kemungkinan penyebab:**
- Kode saham salah
- Koneksi internet bermasalah
- Yahoo Finance sedang down

**Solusi:**
- Cek kode saham di watchlist
- Pastikan koneksi internet aktif
- Tunggu beberapa saat dan coba lagi

### Aplikasi Lambat

**Solusi:**
- Kurangi jumlah saham di watchlist
- Kurangi periode backtest
- Clear cache di Settings > Clear Cache

## 📱 Akses dari Perangkat Lain

Untuk akses dari HP/tablet di jaringan yang sama:

1. **Cek IP address komputer Anda:**
   ```bash
   ipconfig          # Windows
   ifconfig          # Linux/Mac
   ```

2. **Jalankan dengan network access:**
   ```bash
   streamlit run Home.py --server.address 0.0.0.0
   ```

3. **Akses dari perangkat lain:**
   ```
   http://IP_KOMPUTER_ANDA:8501
   ```

## 🔄 Update Aplikasi

Jika ada update baru:

1. **Download versi terbaru**

2. **Update dependencies:**
   ```bash
   pip install -r requirements.txt --upgrade
   ```

3. **Backup data Anda:**
   - watchlist.txt
   - trades_journal.csv
   - .env

4. **Copy file baru dan restore data**

## 💡 Tips

1. **Virtual Environment** (recommended):
   ```bash
   # Create
   python -m venv venv
   
   # Activate
   venv\Scripts\activate     # Windows
   source venv/bin/activate  # Linux/Mac
   
   # Install
   pip install -r requirements.txt
   ```

2. **Auto-restart on code change:**
   ```bash
   streamlit run Home.py --server.runOnSave true
   ```

3. **Hide Streamlit menu:**
   ```bash
   streamlit run Home.py --server.headless true
   ```

## 📞 Support

Jika mengalami masalah:

1. Cek dokumentasi: README.md
2. Cek error message di terminal
3. Buka issue di GitHub
4. Email: support@example.com

## ✅ Verifikasi Instalasi

Cek apakah instalasi berhasil:

```bash
# Cek Python version
python --version

# Cek installed packages
pip list | grep streamlit
pip list | grep pandas
pip list | grep yfinance

# Test import
python -c "import streamlit; import pandas; import yfinance; print('OK')"
```

Jika semua OK, Anda siap trading! 🚀📈
