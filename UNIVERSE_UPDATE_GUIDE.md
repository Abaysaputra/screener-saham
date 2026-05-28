# Universe Data Update Guide

## 📊 Tentang idx_universe.csv

File `idx_universe.csv` berisi daftar seluruh saham IDX yang akan digunakan oleh **Universe Filter**. File ini perlu diupdate secara berkala untuk memastikan data market cap, volume, dan harga terkini.

## 📋 Format File

```csv
Symbol,Name,Sector,MarketCap,AvgVolume,LastPrice
BBCA,Bank Central Asia,Banking,1200000000000000,15000000,10200
```

### Kolom yang Diperlukan:

- **Symbol**: Kode saham (tanpa .JK suffix)
- **Name**: Nama perusahaan
- **Sector**: Sektor industri
- **MarketCap**: Kapitalisasi pasar dalam Rupiah (numeric)
- **AvgVolume**: Volume rata-rata harian (numeric)
- **LastPrice**: Harga terakhir dalam Rupiah (numeric)

## 🔄 Cara Update Data

### Opsi 1: Manual Update (Simple)

1. Buka `idx_universe.csv` dengan Excel/Text Editor
2. Update kolom `MarketCap`, `AvgVolume`, dan `LastPrice` dengan data terbaru
3. Simpan file
4. Refresh aplikasi Streamlit

### Opsi 2: Scraping dari IDX/RTI (Advanced)

Anda bisa membuat script Python untuk scraping data dari:

- **IDX Website**: https://www.idx.co.id/
- **RTI (Real Time Information)**: Platform data market IDX
- **Bloomberg/Reuters**: Jika ada akses

### Opsi 3: Menggunakan yfinance (Automated)

Buat script untuk auto-update universe menggunakan yfinance:

```python
import yfinance as yf
import pandas as pd

# List semua symbol IDX
symbols = ["BBCA.JK", "BBRI.JK", "BMRI.JK", ...]  # Tambahkan semua

data = []
for symbol in symbols:
    ticker = yf.Ticker(symbol)
    info = ticker.info
    
    data.append({
        "Symbol": symbol.replace(".JK", ""),
        "Name": info.get("longName", ""),
        "Sector": info.get("sector", "Unknown"),
        "MarketCap": info.get("marketCap", 0),
        "AvgVolume": info.get("averageVolume", 0),
        "LastPrice": info.get("currentPrice", 0)
    })

df = pd.DataFrame(data)
df.to_csv("idx_universe.csv", index=False)
```

## 📅 Rekomendasi Update Schedule

- **Weekly**: Update `LastPrice` dan `AvgVolume`
- **Monthly**: Update `MarketCap` (untuk corporate action)
- **Quarterly**: Review dan tambah/hapus saham baru/delisting

## 🏢 Sektor yang Tersedia

File default mencakup sektor-sektor utama:

- Banking
- Consumer Goods
- Telecommunications
- Automotive
- Healthcare
- Materials
- Energy
- Agriculture
- Infrastructure
- Property
- Retail
- Media
- Finance
- Technology
- Transportation
- Trade

## ➕ Menambah Saham Baru

Untuk menambah saham baru:

1. Dapatkan data dari yfinance atau sumber terpercaya
2. Tambahkan baris baru di akhir CSV:
   ```csv
   NEWSYM,New Company,Sector,1000000000000,500000,1500
   ```
3. Pastikan format numeric benar (tanpa koma atau titik ribuan)
4. Simpan dan reload aplikasi

## 🗑️ Menghapus Saham (Delisting)

Untuk saham yang delisting:

1. Hapus baris saham tersebut dari CSV
2. Atau tandai dengan market cap = 0
3. Universe Filter akan otomatis skip saham dengan data tidak valid

## ⚠️ Catatan Penting

1. **Market Cap dalam Rupiah**: Gunakan nilai penuh (misal 1T = 1000000000000)
2. **Volume dalam Shares**: Bukan dalam Rupiah
3. **Last Price**: Harga per lembar saham
4. **No Special Characters**: Hindari karakter khusus di nama perusahaan
5. **Consistent Sector Names**: Gunakan nama sektor yang konsisten

## 🔍 Validasi Data

Setelah update, lakukan validasi:

1. Buka **Universe Filter** page
2. Periksa jumlah total saham
3. Cek distribusi sektor
4. Test dengan terapkan filter sederhana
5. Pastikan tidak ada error atau data missing

## 🚀 Tips Optimasi

- **Minimal Data**: Hapus saham dengan volume < 50K untuk efisiensi
- **Focus Sectors**: Jika trading specific sector, hapus sector lain
- **Market Cap Threshold**: Pertimbangkan hapus micro cap < 10M jika tidak trading
- **Regular Cleanup**: Hapus saham illiquid atau suspended

## 📞 Troubleshooting

**Q: Data tidak muncul di Universe Filter?**
- Cek format CSV, pastikan header benar
- Pastikan numeric column tidak ada text
- Reload Streamlit (Ctrl+R)

**Q: Filter tidak bekerja dengan benar?**
- Pastikan MarketCap dan AvgVolume dalam format numeric
- Jangan gunakan format currency (Rp, koma, titik)
- Gunakan nilai absolut penuh

**Q: Bagaimana dapatkan daftar lengkap saham IDX?**
- Download dari IDX official: https://www.idx.co.id/data-pasar/data-saham/daftar-saham/
- Atau scrape dari finacial portal (investing.com, tradingview)

## 📚 Resources

- IDX Official: https://www.idx.co.id/
- Yahoo Finance: https://finance.yahoo.com/
- yfinance docs: https://pypi.org/project/yfinance/

---

**Update terakhir**: Sesuaikan file ini dengan tanggal update terakhir Anda!
