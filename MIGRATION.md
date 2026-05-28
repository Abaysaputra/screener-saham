# Migration Guide - Old to New Structure

## 📋 Overview

Aplikasi Swing Trader IDX telah direfactor untuk mengikuti **best practices** Python Streamlit framework.

## 🔄 Perubahan Struktur

### Old Structure
```
swing_trader/
├── app.py                 # Monolithic app
├── cli.py                 # CLI functions
├── config.py              # Hardcoded config
├── data.py                # No caching
├── indicators.py
├── strategy.py
├── backtest.py
├── risk.py
├── journal.py
└── watchlist.txt
```

### New Structure (Best Practice)
```
swing_trader/
├── Home.py                       # Main entry point
├── pages/                        # Multi-page app
│   ├── 1_📊_Scan_Harian.py
│   ├── 2_📈_Backtest.py
│   ├── 3_📓_Journal.py
│   └── 4_⚙️_Settings.py
├── core/                         # Core business logic
│   ├── __init__.py
│   ├── config.py                # Environment-based config
│   └── data.py                  # Cached data fetching
├── utils/                        # Utility functions
│   ├── __init__.py
│   ├── indicators.py
│   ├── strategy.py
│   ├── risk.py
│   ├── backtest.py
│   └── journal.py
├── .streamlit/                   # Streamlit config
│   └── config.toml
├── .env.example                  # Environment template
├── requirements.txt
├── README.md
├── INSTALL.md
└── run.py                        # Quick start script
```

## 🎯 Keuntungan Refactoring

### 1. **Multi-Page App**
- **Old**: Single page dengan radio button
- **New**: Proper multi-page dengan navigation
- **Benefit**: Better UX, cleaner code, easier maintenance

### 2. **Configuration Management**
- **Old**: Hardcoded values di config.py
- **New**: Environment variables dengan .env
- **Benefit**: Flexible, secure, environment-specific configs

### 3. **Caching Strategy**
- **Old**: No caching, API calls repeated
- **New**: `@st.cache_data` untuk semua data fetching
- **Benefit**: Faster app, reduced API calls, better performance

### 4. **Modular Architecture**
- **Old**: Mixed concerns dalam satu file
- **New**: Separated core logic, utils, and UI
- **Benefit**: Easier testing, maintainable, scalable

### 5. **Session State Management**
- **Old**: No state persistence
- **New**: Proper session state untuk scan results
- **Benefit**: Better user experience, data persistence

### 6. **Error Handling & Logging**
- **Old**: Basic error handling
- **New**: Comprehensive logging dan error handling
- **Benefit**: Easier debugging, better monitoring

### 7. **Type Hints**
- **Old**: No type hints
- **New**: Type hints di semua functions
- **Benefit**: Better IDE support, fewer bugs

## 📝 Breaking Changes

### Import Statements

**Old:**
```python
from data import get_history_yf
from strategy import generate_signals
from backtest import backtest_risk_based
from risk import position_size
from journal import log_trades
from config import DEFAULT_RISK_PER_TRADE
```

**New:**
```python
from core.data import get_history_yf
from core.config import Config
from utils.strategy import generate_signals
from utils.backtest import backtest_risk_based
from utils.risk import position_size
from utils.journal import log_trades
```

### Configuration Access

**Old:**
```python
from config import DEFAULT_RISK_PER_TRADE, DEFAULT_EMA_FAST

risk = DEFAULT_RISK_PER_TRADE
ema_fast = DEFAULT_EMA_FAST
```

**New:**
```python
from core.config import Config

risk = Config.DEFAULT_RISK_PER_TRADE
ema_fast = Config.DEFAULT_EMA_FAST
```

### Data Fetching

**Old:**
```python
# No caching
def get_history_yf(symbol, start, end):
    return yf.download(symbol, start, end)
```

**New:**
```python
# Dengan caching
@st.cache_data(ttl=3600)
def get_history_yf(symbol: str, start: str, end: str) -> pd.DataFrame:
    return yf.download(symbol, start, end, progress=False)
```

### Watchlist Loading

**Old:**
```python
def load_watchlist():
    with open("watchlist.txt") as f:
        return [line.strip() for line in f]
```

**New:**
```python
@st.cache_data
def load_watchlist() -> list:
    with Config.WATCHLIST_PATH.open() as f:
        return [line.strip().upper() for line in f if line.strip()]
```

## 🔧 Migration Steps

### Step 1: Backup Data
```bash
# Backup your important files
copy watchlist.txt watchlist.txt.backup
copy trades_journal.csv trades_journal.csv.backup
copy .env .env.backup  # if exists
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Create .env File
```bash
copy .env.example .env
# Edit .env with your settings
```

### Step 4: Update Import Statements

If you have custom scripts:
```python
# Replace old imports
# from config import DEFAULT_RISK_PER_TRADE
# with
from core.config import Config
risk = Config.DEFAULT_RISK_PER_TRADE
```

### Step 5: Test Application
```bash
python run.py
# or
streamlit run Home.py
```

### Step 6: Verify Features
- ✅ Scan Harian works
- ✅ Backtest works
- ✅ Journal loads correctly
- ✅ Settings accessible
- ✅ Watchlist editable

## 📊 Feature Comparison

| Feature | Old App | New App |
|---------|---------|---------|
| Multi-page | ❌ Radio button | ✅ Native pages |
| Caching | ❌ None | ✅ Full caching |
| Configuration | ❌ Hardcoded | ✅ .env support |
| Session State | ❌ No | ✅ Yes |
| Error Handling | ⚠️ Basic | ✅ Comprehensive |
| Logging | ❌ No | ✅ Yes |
| Type Hints | ❌ No | ✅ Yes |
| Documentation | ⚠️ Minimal | ✅ Complete |
| Visualization | ⚠️ Basic | ✅ Interactive (Plotly) |
| Settings Page | ❌ No | ✅ Yes |
| Watchlist UI | ❌ File only | ✅ In-app editor |
| Download Results | ❌ No | ✅ CSV export |
| Metrics Display | ⚠️ Basic | ✅ Rich metrics |

## 🚀 New Features

1. **Interactive Charts** - Plotly charts dengan zoom, pan, hover
2. **Settings Page** - Manage watchlist dan configuration dari UI
3. **Download Results** - Export scan dan backtest results ke CSV
4. **Equity Curve** - Visual equity growth dalam journal
5. **Performance Metrics** - Comprehensive statistics
6. **Progress Indicators** - Real-time progress saat scan
7. **Filter & Sort** - Journal filtering dan sorting
8. **Quick Start Script** - run.py untuk easy setup
9. **Documentation** - Complete README dan INSTALL guide

## 💡 Best Practices Implemented

### 1. Separation of Concerns
- **Core**: Business logic
- **Utils**: Reusable utilities
- **Pages**: UI components

### 2. DRY (Don't Repeat Yourself)
- Reusable functions
- Shared utilities
- Consistent patterns

### 3. Configuration Management
- Environment variables
- Default values
- Easy customization

### 4. Performance Optimization
- Data caching
- Efficient queries
- Lazy loading

### 5. User Experience
- Progress indicators
- Error messages
- Help text
- Tooltips

### 6. Code Quality
- Type hints
- Docstrings
- Consistent naming
- Comments where needed

## 🐛 Known Issues & Solutions

### Issue 1: Old journal format
**Solution**: Journal otomatis compatible dengan old format

### Issue 2: Watchlist case sensitivity
**Solution**: Otomatis convert ke uppercase

### Issue 3: Cache tidak clear
**Solution**: Button "Clear Cache" di Settings

## 📚 Additional Resources

- [Streamlit Documentation](https://docs.streamlit.io)
- [Best Practices Guide](https://docs.streamlit.io/library/advanced-features)
- [Caching Documentation](https://docs.streamlit.io/library/advanced-features/caching)
- [Multi-page Apps](https://docs.streamlit.io/library/get-started/multipage-apps)

## ❓ FAQ

**Q: Apakah data lama saya aman?**
A: Ya! Journal format tetap sama dan backward compatible.

**Q: Apakah perlu install ulang dependencies?**
A: Ya, ada beberapa dependency baru (plotly, python-dotenv).

**Q: Apakah API keys lama masih bisa dipakai?**
A: Ya, pindahkan ke file .env dengan format baru.

**Q: Bagaimana jika ada bug?**
A: Report di GitHub Issues atau rollback ke version lama.

**Q: Apakah strategi trading berubah?**
A: Tidak, strategi tetap sama (EMA crossover + RSI).

## 🎓 Next Steps

Setelah migrasi:

1. ✅ Test semua fitur
2. ✅ Setup .env dengan API keys
3. ✅ Customize watchlist
4. ✅ Review new Settings page
5. ✅ Explore new visualizations
6. ✅ Try export features
7. ✅ Read updated documentation

---

**Happy Trading dengan aplikasi yang lebih baik! 📈🚀**
