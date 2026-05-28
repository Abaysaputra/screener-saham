# Quick Start Guide

## 🚀 Cara Menjalankan Aplikasi (Refactored Version)

### Opsi 1: Using Python Script (Recommended)

```bash
python run.py
```

Script ini akan otomatis:
- ✅ Check dan install dependencies
- ✅ Setup watchlist default (jika belum ada)
- ✅ Check konfigurasi .env
- ✅ Menjalankan aplikasi Streamlit

### Opsi 2: Using Streamlit Directly

```bash
streamlit run Home.py
```

### Opsi 3: Custom Configuration

```bash
# Dengan port custom
streamlit run Home.py --server.port 8502

# Dengan network access
streamlit run Home.py --server.address 0.0.0.0

# Kombinasi
streamlit run Home.py --server.port 8502 --server.address 0.0.0.0
```

## 📱 Akses Aplikasi

Setelah running, aplikasi bisa diakses di:

- **Local**: http://localhost:8501
- **Network** (jika enable): http://YOUR_IP:8501

## 🔧 First Time Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Setup Watchlist (Optional)

Edit `watchlist.txt`:
```
BBCA
BBRI
BMRI
TLKM
ASII
```

### 3. Setup Environment (Optional)

Copy `.env.example` to `.env`:
```bash
copy .env.example .env  # Windows
cp .env.example .env    # Linux/Mac
```

Edit `.env` untuk custom settings.

### 4. Run!

```bash
python run.py
```

## 📊 Navigasi Aplikasi

Aplikasi memiliki 5 halaman utama:

1. **🏠 Home** - Landing page dengan overview
2. **📊 Scan Harian** - Scan sinyal BUY dari watchlist
3. **📈 Backtest** - Test strategi pada data historis
4. **📓 Journal** - Analisis trading journal
5. **⚙️ Settings** - Konfigurasi dan watchlist management

## 💡 Tips

### Clear Cache

Jika data tidak update atau ada error:
1. Go to **Settings** page
2. Click **"Clear Cache"**
3. Atau press `C` di keyboard (Streamlit shortcut)

### Update Watchlist

**Cara 1**: Edit file `watchlist.txt` manually
**Cara 2**: Gunakan Settings page untuk manage dari UI

### Check Logs

Jika ada error, check terminal untuk detailed error messages.

## 🔄 Update Dependencies

```bash
pip install -r requirements.txt --upgrade
```

## 🐛 Troubleshooting

### "ModuleNotFoundError"
```bash
pip install -r requirements.txt
```

### "Port already in use"
```bash
streamlit run Home.py --server.port 8502
```

### "No data found"
- Check internet connection
- Check symbol di watchlist
- Try again later (Yahoo Finance might be down)

## 📖 More Help

- Read: [README.md](README.md)
- Install Guide: [INSTALL.md](INSTALL.md)
- Migration: [MIGRATION.md](MIGRATION.md)

---

**Happy Trading! 📈💰**
