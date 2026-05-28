# 📊 Panduan Analisa Fundamental

## Overview

Fitur **Analisa Fundamental** telah ditambahkan untuk membantu filter saham berdasarkan kualitas fundamental, bukan hanya sinyal teknikal. Ini membantu menghindari saham gorengan atau saham dengan fundamental lemah.

## 🎯 Tujuan

1. **Menghindari saham gorengan**: Filter saham dengan kualitas fundamental buruk
2. **Kombinasi Teknikal + Fundamental**: Strategi lebih robust dan reliable
3. **Risk Management**: Trading di saham berkualitas mengurangi risiko
4. **Confidence**: Meningkatkan keyakinan dalam trading decision

## 📈 Metrik Fundamental yang Digunakan

### 1. **EPS (Earnings Per Share)**
- **Definisi**: Laba per saham perusahaan
- **Penggunaan**: Filter saham profitable vs rugi
- **Kriteria**:
  - ✅ EPS > 0: Perusahaan profitable
  - ❌ EPS < 0: Perusahaan rugi (hindari)

### 2. **PE Ratio (Price to Earnings)**
- **Definisi**: Rasio harga saham terhadap earning
- **Penggunaan**: Mengukur valuasi (mahal/murah)
- **Kriteria**:
  - ✅ PE < 15: Undervalued (murah)
  - ℹ️ PE 15-25: Wajar
  - ⚠️ PE > 25: Overvalued (mahal)

### 3. **PB Ratio (Price to Book)**
- **Definisi**: Rasio harga saham terhadap nilai buku
- **Penggunaan**: Valuasi berdasarkan aset bersih
- **Kriteria**:
  - ✅ PB < 1: Trading di bawah nilai buku
  - ℹ️ PB 1-3: Valuasi wajar
  - ⚠️ PB > 3: Premium valuasi tinggi

### 4. **Profit Margin**
- **Definisi**: Persentase profit dari revenue
- **Penggunaan**: Efisiensi operasional perusahaan
- **Kriteria**:
  - ✅ Margin > 10%: Excellent
  - ℹ️ Margin 5-10%: Good
  - ⚠️ Margin < 5%: Low/risky

### 5. **ROE (Return on Equity)**
- **Definisi**: Return yang dihasilkan dari modal pemegang saham
- **Penggunaan**: Efektivitas penggunaan modal
- **Kriteria**:
  - ✅ ROE > 15%: Excellent
  - ℹ️ ROE 10-15%: Good
  - ⚠️ ROE < 10%: Below average

### 6. **Market Cap**
- **Definisi**: Kapitalisasi pasar (harga × jumlah saham)
- **Penggunaan**: Ukuran dan likuiditas perusahaan
- **Kriteria**:
  - > 1 Triliun: Large cap (lebih stabil)
  - 500B - 1T: Mid cap
  - 100B - 500B: Small cap
  - < 100B: Micro cap (lebih volatile)

## 🚀 Cara Menggunakan

### Di Halaman Scan Harian

1. **Aktifkan Filter**:
   - Centang "Aktifkan Filter Fundamental" di sidebar
   
2. **Pilih Kriteria**:
   ```
   ☑️ EPS Positif (Profitable) - RECOMMENDED
   ☐ Filter PE Ratio (opsional)
      └─ PE Maksimum: 25
   ☐ Filter PB Ratio (opsional)
      └─ PB Maksimum: 3.0
   ☐ Filter Profit Margin (opsional)
      └─ Minimum: 5%
   ☐ Filter Market Cap (opsional)
      └─ Minimum: 1 Triliun
   ```

3. **Jalankan Scan**:
   - Sistem akan filter watchlist berdasarkan kriteria
   - Hanya saham yang memenuhi kriteria akan di-scan
   
4. **Lihat Hasil**:
   - Hasil scan menampilkan saham yang lolos filter
   - Pilih saham untuk melihat detail fundamental
   - Interpretasi otomatis (🟢 Baik, 🟡 Sedang, 🔴 Rendah)

### Di Halaman Backtest

1. **Aktifkan Analisa**:
   - Centang "Cek Fundamental Saham" di sidebar
   
2. **Jalankan Backtest**:
   - Sebelum backtest, sistem menampilkan fundamental
   - Review kualitas fundamental saham
   - Kualitas baik = confidence lebih tinggi pada hasil backtest
   
3. **Interpretasi**:
   - 🟢 Berkualitas Baik: Fundamental solid, hasil backtest lebih reliable
   - 🟡 Kualitas Sedang: Review detail metrik
   - 🔴 Kualitas Rendah: Hati-hati, fundamental lemah

## 💡 Recommended Filter Settings

### Conservative (Risk Averse)
```
✅ EPS Positif
✅ PE Ratio < 20
✅ PB Ratio < 2.5
✅ Profit Margin > 5%
✅ Market Cap > 1 Triliun
```
**Hasil**: Saham blue chip, fundamental solid, risiko rendah

### Balanced (Recommended)
```
✅ EPS Positif
✅ PE Ratio < 25
✅ Market Cap > 500 Miliar
```
**Hasil**: Balance antara quality dan opportunity

### Growth (Aggressive)
```
✅ EPS Positif
✅ Profit Margin > 10%
```
**Hasil**: Fokus pada profitability dan growth potential

## 🎓 Best Practices

### 1. **Kombinasi dengan Teknikal**
```
Teknikal (EMA, RSI) → Timing entry/exit
Fundamental → Kualitas dan safety
```

### 2. **Jangan Terlalu Ketat**
- Filter terlalu ketat → hasil scan bisa kosong
- Start dengan EPS Positif saja
- Tambah filter lain secara bertahap

### 3. **Context Matters**
- Bear market: Perkuat filter fundamental
- Bull market: Bisa relaks sedikit
- Sector rotation: Sesuaikan dengan sektor

### 4. **Review Manual**
- Filter otomatis bukan 100% sempurna
- Tetap review detail fundamental
- Cross-check dengan news dan reports

### 5. **Long-term Thinking**
- Fundamental untuk hold time > 3-7 hari
- Scalping/intraday → teknikal lebih penting
- Swing trading → fundamental + teknikal = best

## ⚠️ Limitasi

### 1. **Data Availability**
- Data dari Yahoo Finance (yfinance)
- Tidak semua saham punya data lengkap
- IDX stocks might have limited data

### 2. **Data Lag**
- Fundamental data bisa delayed
- Quarterly reports → update tidak real-time
- Untuk real-time, cek sumber official (IDX, quarterly reports)

### 3. **Tidak Menggantikan Research**
- Filter otomatis = screening awal
- Tetap butuh research mendalam
- Read financial statements!

### 4. **Market Sentiment**
- Fundamental bagus ≠ harga naik instantly
- Market sentiment tetap penting
- Technical timing tetap diperlukan

## 📊 Contoh Workflow

### Scenario: Swing Trading IDX

1. **Setup Filter**:
   ```
   - EPS Positif: ✅
   - PE < 25: ✅
   - Market Cap > 1T: ✅
   ```

2. **Scan Watchlist**:
   ```
   Watchlist: 50 saham
   Lolos filter fundamental: 25 saham
   Ada sinyal BUY: 8 saham
   ```

3. **Review Fundamental**:
   ```
   Saham A: 🟢 Berkualitas Baik
   - EPS: 250 (positive)
   - PE: 18 (wajar)
   - PB: 2.1 (wajar)
   - Margin: 12% (excellent)
   → TRADE ✅
   
   Saham B: 🔴 Kualitas Rendah
   - EPS: -50 (rugi)
   - PE: N/A
   - PB: 0.8 (murah, tapi rugi)
   - Margin: -5% (negatif)
   → SKIP ❌
   ```

4. **Execute**:
   - Trade hanya saham dengan fundamental 🟢 atau 🟡
   - Skip saham 🔴 kecuali yakin sekali

## 🔧 Technical Details

### Module: `utils/fundamental.py`

**Main Functions**:
- `get_fundamental_data(symbol)`: Fetch data dari yfinance
- `check_fundamental_criteria(fundamentals, criteria)`: Filter checker
- `get_fundamental_summary(fundamentals)`: Quality rating
- `format_fundamental_display(fundamentals)`: Format untuk display

**Caching**: 1 hour TTL untuk efisiensi

**Data Source**: Yahoo Finance via yfinance library

## 🎯 Next Steps

1. **Test dengan Data Real**: Run scan dengan filter aktif
2. **Compare Results**: Bandingkan dengan/tanpa filter
3. **Track Performance**: Apakah fundamental filter improve win rate?
4. **Adjust Criteria**: Fine-tune berdasarkan hasil

## 📚 Resources

- **Yahoo Finance**: https://finance.yahoo.com
- **IDX Official**: https://www.idx.co.id
- **Financial Statements**: Lihat quarterly reports
- **Fundamental Analysis Books**: 
  - "The Intelligent Investor" - Benjamin Graham
  - "One Up On Wall Street" - Peter Lynch

## 💬 FAQ

**Q: Apakah wajib menggunakan filter fundamental?**
A: Tidak wajib, tapi strongly recommended untuk swing trading. Untuk scalping/intraday bisa skip.

**Q: Filter mana yang paling penting?**
A: EPS Positif. Ini filter paling basic untuk hindari saham rugi.

**Q: Kenapa hasil scan jadi sedikit setelah pakai filter?**
A: Normal. Filter fundamental memang mengurangi jumlah, tapi quality lebih baik.

**Q: Bagaimana jika data fundamental tidak tersedia?**
A: Saham akan di-skip. Bisa disable filter atau tambah saham dengan data lengkap.

**Q: Apakah filter fundamental 100% accurate?**
A: Tidak. Ini screening tool, bukan holy grail. Tetap butuh research manual.

---

**Version**: 1.0  
**Last Updated**: 2026-01-17  
**Maintained by**: Swing Trader App Team
