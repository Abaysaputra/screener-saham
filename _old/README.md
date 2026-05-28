# Old Files Archive

Folder ini berisi file-file lama dari versi sebelum refactoring.

## File yang Dipindahkan

- `app.py` - Old Streamlit app (diganti dengan `Home.py` dan multi-page structure)
- `cli.py` - Command line interface (functionality sudah ada di app baru)
- `config.py` - Old configuration (diganti dengan `core/config.py`)
- `data.py` - Old data module (diganti dengan `core/data.py`)
- `indicators.py` - Old indicators (diganti dengan `utils/indicators.py`)
- `strategy.py` - Old strategy (diganti dengan `utils/strategy.py`)
- `backtest.py` - Old backtest (diganti dengan `utils/backtest.py`)
- `risk.py` - Old risk management (diganti dengan `utils/risk.py`)
- `journal.py` - Old journal (diganti dengan `utils/journal.py`)

## Kenapa Dipindahkan?

File-file ini dipindahkan ke folder `_old/` sebagai backup setelah refactoring ke struktur yang lebih baik mengikuti best practices Python/Streamlit.

## Versi Baru

Struktur baru:
```
swing_trader/
├── Home.py                  # Main entry point
├── pages/                   # Multi-page app
│   ├── 1_📊_Scan_Harian.py
│   ├── 2_📈_Backtest.py
│   ├── 3_📓_Journal.py
│   └── 4_⚙️_Settings.py
├── core/                    # Business logic
│   ├── config.py
│   └── data.py
└── utils/                   # Utilities
    ├── indicators.py
    ├── strategy.py
    ├── risk.py
    ├── backtest.py
    └── journal.py
```

## Apakah Aman Dihapus?

Ya, file-file ini aman untuk dihapus setelah Anda memverifikasi bahwa aplikasi baru berjalan dengan baik.

**Rekomendasi**: Simpan folder ini sampai Anda yakin semua fitur berfungsi dengan baik di versi baru.

## Migration Notes

Lihat file [MIGRATION.md](../MIGRATION.md) di root folder untuk panduan lengkap migrasi dari kode lama ke kode baru.

---

**Date Archived**: January 10, 2026
**Reason**: Refactoring to best practices structure
