# Architecture Documentation

## 🏗️ Application Architecture

### Overview

Swing Trader IDX menggunakan **modular architecture** dengan **separation of concerns** untuk maintainability dan scalability.

```
┌─────────────────────────────────────────────────────┐
│                  Presentation Layer                  │
│                    (Streamlit UI)                    │
├─────────────────────────────────────────────────────┤
│  Home.py  │  Scan  │  Backtest  │  Journal  │ Settings │
└─────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────┐
│                  Business Logic Layer                │
│                    (Core Modules)                    │
├─────────────────────────────────────────────────────┤
│         Config Management  │  Data Fetching          │
│         (Environment Vars) │  (Cached API Calls)     │
└─────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────┐
│                   Utility Layer                      │
│                  (Helper Functions)                  │
├─────────────────────────────────────────────────────┤
│ Indicators │ Strategy │ Risk │ Backtest │ Journal   │
└─────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────┐
│                    Data Layer                        │
│              (External Data Sources)                 │
├─────────────────────────────────────────────────────┤
│         Yahoo Finance  │  GOAPI  │  Local Files     │
└─────────────────────────────────────────────────────┘
```

## 📂 Directory Structure

### 1. Presentation Layer (`pages/`)

**Purpose**: User interface dan interaction handling

**Files**:
- `Home.py` - Main entry point, landing page
- `1_📊_Scan_Harian.py` - Daily signal scanner UI
- `2_📈_Backtest.py` - Backtesting interface
- `3_📓_Journal.py` - Trading journal viewer
- `4_⚙️_Settings.py` - Configuration management UI

**Responsibilities**:
- Render UI components
- Handle user input
- Display results
- Manage session state
- Call business logic functions

**Dependencies**: `core/`, `utils/`, `streamlit`

### 2. Business Logic Layer (`core/`)

**Purpose**: Core business logic dan data management

**Files**:
- `config.py` - Configuration management
- `data.py` - Data fetching dengan caching

#### `config.py` Architecture

```python
class Config:
    """Centralized configuration management"""
    
    # Environment-based settings
    API_GOAPI_KEY = os.getenv("GOAPI_KEY")
    DEFAULT_CAPITAL = float(os.getenv("DEFAULT_CAPITAL", "100000000"))
    
    # File paths
    WATCHLIST_PATH = BASE_DIR / "watchlist.txt"
    JOURNAL_PATH = BASE_DIR / "trades_journal.csv"
    
    # Trading parameters
    DEFAULT_EMA_FAST = 20
    DEFAULT_EMA_SLOW = 50
    
    @classmethod
    def validate(cls):
        """Validate configuration on startup"""
        pass
```

#### `data.py` Architecture

```python
@st.cache_data(ttl=3600)  # Cache for 1 hour
def get_history_yf(symbol: str, start: str, end: str) -> pd.DataFrame:
    """Fetch historical data with caching"""
    pass

@st.cache_data(ttl=300)  # Cache for 5 minutes
def get_realtime_goapi(symbol: str) -> dict:
    """Fetch real-time data with caching"""
    pass

@st.cache_data
def load_watchlist() -> list:
    """Load watchlist with caching"""
    pass
```

**Key Features**:
- Environment variable support
- Path management
- Validation on startup
- Centralized configuration
- Strategic caching (different TTL for different data types)
- Error handling dan logging

### 3. Utility Layer (`utils/`)

**Purpose**: Reusable helper functions dan algorithms

**Files**:
- `indicators.py` - Technical indicators (EMA, RSI)
- `strategy.py` - Trading signal generation
- `risk.py` - Risk management calculations
- `backtest.py` - Backtesting engine
- `journal.py` - Trading journal management

#### Module Relationships

```
strategy.py
    ├── depends on: indicators.py, config.py
    └── used by: pages (Scan, Backtest)

backtest.py
    ├── depends on: strategy.py, risk.py
    └── used by: Backtest page

risk.py
    ├── depends on: config.py
    └── used by: strategy.py, backtest.py, Scan page

journal.py
    ├── depends on: config.py
    └── used by: Journal page, backtest.py
```

## 🔄 Data Flow

### Scan Harian Flow

```
User Input (Capital, Settings)
        │
        ▼
Load Watchlist (cached)
        │
        ▼
For each symbol:
    │
    ├─→ Fetch Historical Data (cached, TTL 10min)
    │       │
    │       ▼
    ├─→ Generate Signals (strategy.py)
    │       │
    │       ▼
    ├─→ Calculate Position Size (risk.py)
    │       │
    │       ▼
    └─→ Aggregate Results
            │
            ▼
    Display in UI (Streamlit)
            │
            ▼
    Store in Session State
```

### Backtest Flow

```
User Input (Symbol, Period, Parameters)
        │
        ▼
Fetch Historical Data (cached, TTL 1hr)
        │
        ▼
Generate Signals (strategy.py)
        │
        ▼
Run Backtest (backtest.py)
    │
    ├─→ Entry Logic (position_size from risk.py)
    │
    ├─→ Exit Logic (SL/TP calculation)
    │
    └─→ Calculate Metrics (profit factor, drawdown)
            │
            ▼
    Display Results (charts, tables)
            │
            ▼
    Store in Session State
```

### Journal Flow

```
Load Journal Data (journal.py)
        │
        ▼
Calculate Statistics (compute_stats)
        │
        ▼
Generate Visualizations (Plotly)
    │
    ├─→ Equity Curve
    ├─→ R-Multiple Distribution
    ├─→ Win/Loss Pie Chart
    └─→ PnL Bar Chart
            │
            ▼
    Apply Filters & Sorting
            │
            ▼
    Display in UI
```

## 🎯 Design Patterns

### 1. Singleton Pattern (Config)

```python
class Config:
    """Single source of truth for configuration"""
    # All settings as class attributes
    # Accessed via Config.SETTING_NAME
```

**Benefits**:
- Centralized configuration
- Easy to access from anywhere
- No multiple instances

### 2. Caching Pattern (Data)

```python
@st.cache_data(ttl=3600)
def expensive_operation():
    """Cache results to avoid repeated expensive calls"""
    pass
```

**Benefits**:
- Improved performance
- Reduced API calls
- Better user experience

### 3. Factory Pattern (Risk Calculations)

```python
def position_size(capital, entry, stop, risk_pct=None):
    """Factory for creating position size calculations"""
    if risk_pct is None:
        risk_pct = Config.DEFAULT_RISK_PER_TRADE
    # Calculate and return
```

**Benefits**:
- Flexible parameter handling
- Default values from config
- Reusable across modules

### 4. Strategy Pattern (Signal Generation)

```python
def generate_signals(df, rsi_max=70.0):
    """Strategy for generating trading signals"""
    # Different strategies can be implemented
    # Current: EMA Crossover + RSI
    pass
```

**Benefits**:
- Easy to swap strategies
- Encapsulated logic
- Testable components

## 🔐 Security Considerations

### 1. Environment Variables

```python
# Sensitive data NOT in code
API_KEY = os.getenv("GOAPI_KEY")  # From .env file

# .env is in .gitignore
# .env.example provided as template
```

### 2. Input Validation

```python
# Validate user inputs
if not symbol or len(symbol) < 3:
    raise ValueError("Invalid symbol")

# Sanitize file paths
path = Path(user_input).resolve()
if not path.is_relative_to(BASE_DIR):
    raise ValueError("Invalid path")
```

### 3. Error Handling

```python
try:
    result = risky_operation()
except Exception as e:
    logger.error(f"Error: {str(e)}")
    st.error("User-friendly message")
    # Graceful degradation
```

## 📊 Performance Optimization

### 1. Caching Strategy

| Data Type | TTL | Reason |
|-----------|-----|--------|
| Historical Data | 1 hour | Changes infrequently |
| Real-time Data | 5 minutes | Needs freshness |
| Watchlist | No expiry | User-managed |
| Config | No expiry | Static |

### 2. Lazy Loading

```python
# Only fetch when needed
if st.button("Run Scan"):
    # Fetch data here, not on page load
    data = fetch_data()
```

### 3. Progress Indicators

```python
progress_bar = st.progress(0)
for i, item in enumerate(items):
    process(item)
    progress_bar.progress((i + 1) / len(items))
```

## 🧪 Testing Strategy

### Unit Tests Structure (Recommended)

```
tests/
├── test_indicators.py      # Test EMA, RSI calculations
├── test_strategy.py         # Test signal generation
├── test_risk.py             # Test position sizing
├── test_backtest.py         # Test backtest engine
└── test_config.py           # Test configuration
```

### Example Test

```python
def test_ema_calculation():
    """Test EMA calculation"""
    prices = pd.Series([100, 101, 102, 103, 104])
    ema_20 = ema(prices, 20)
    
    assert isinstance(ema_20, pd.Series)
    assert len(ema_20) == len(prices)
    assert not ema_20.isnull().all()
```

## 🚀 Deployment Options

### 1. Streamlit Cloud

```bash
# Push to GitHub
git push origin main

# Deploy on streamlit.io
# Point to Home.py
```

### 2. Docker

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8501

CMD ["streamlit", "run", "Home.py"]
```

### 3. Local Server

```bash
# Run on server
streamlit run Home.py --server.address 0.0.0.0 --server.port 8501
```

## 📈 Scalability

### Horizontal Scaling

- Stateless design allows multiple instances
- Session state handled by Streamlit
- Shared data via external storage (optional)

### Vertical Scaling

- Optimize caching TTL
- Batch processing for watchlist
- Async data fetching (future enhancement)

## 🔮 Future Enhancements

### 1. Database Integration

```python
# Replace CSV with database
from sqlalchemy import create_engine

engine = create_engine('postgresql://...')
trades.to_sql('trades', engine)
```

### 2. Real-time Streaming

```python
# WebSocket for real-time updates
@st.cache_resource
def get_websocket_connection():
    return websocket.connect("wss://...")
```

### 3. API Layer

```python
# REST API for external access
from fastapi import FastAPI

app = FastAPI()

@app.get("/api/scan")
def scan_signals():
    # Return JSON
    pass
```

## 📚 References

- [Streamlit Documentation](https://docs.streamlit.io)
- [Python Best Practices](https://docs.python-guide.org)
- [Software Architecture Patterns](https://www.oreilly.com/library/view/software-architecture-patterns/9781491971437/)

---

**Architecture Version**: 2.0.0
**Last Updated**: January 2026
