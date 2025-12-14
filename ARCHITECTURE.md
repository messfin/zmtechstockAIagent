# 🏗️ System Architecture - AI Stock Analysis Platform

## 📊 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌─────────────────────────┐    ┌──────────────────────────┐   │
│  │   Streamlit Web App     │    │  Command Line Interface  │   │
│  │   (main.py)             │    │  (full_analysis.py)      │   │
│  │                         │    │                          │   │
│  │  • Beautiful UI         │    │  • Direct execution      │   │
│  │  • Interactive charts   │    │  • Script integration    │   │
│  │  • Real-time metrics    │    │  • Python API            │   │
│  │  • Report download      │    │  • Batch processing      │   │
│  └──────────┬──────────────┘    └───────────┬──────────────┘   │
│             │                                │                   │
└─────────────┼────────────────────────────────┼───────────────────┘
              │                                │
              └────────────┬───────────────────┘
                           │
              ┌────────────▼────────────┐
              │   Core Analysis Engine  │
              │   (FullStockAnalyzer)   │
              │   in full_analysis.py   │
              └────────────┬────────────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
┌───────▼────────┐  ┌──────▼──────┐  ┌───────▼────────┐
│  Yahoo Finance │  │  Google AI  │  │  Data Processing│
│  Data Source   │  │  Analysis   │  │  & Indicators   │
└────────────────┘  └─────────────┘  └────────────────┘
```

## 🔄 Data Flow

```
1. USER INPUT
   ↓
   Stock Ticker (e.g., "AAPL") + Time Period (e.g., "1y")
   ↓

2. YAHOO FINANCE DATA FETCH
   ↓
   • Historical price data (OHLCV)
   • Fundamental metrics (P/E, P/B, etc.)
   • Company information
   ↓

3. TECHNICAL INDICATOR CALCULATION
   ↓
   • RSI (14-period)
   • MACD (12,26,9)
   • EMAs (9, 20, 50, 100, 200)
   • Bollinger Bands (20, 2σ)
   • Volume MA (20-period)
   • VWAP
   • Heikin-Ashi Candles
   • SARIMA Forecast
   ↓

4. EVENT & LEVEL CALCULATION
   ↓
   • Earnings Dates (Markers)
   • Pivot points
   • Resistance levels (R1, R2, R3)
   • Support levels (S1, S2, S3)
   ↓

5. DATA AGGREGATION
   ↓
   Comprehensive data structure with:
   • Price data
   • Technical indicators
   • Fundamental metrics
   • Support/resistance levels
   • Volume analysis
   • Trend analysis
   ↓

6. AI PROMPT GENERATION
   ↓
   Structured prompt with all data points
   ↓

7. GOOGLE GENERATIVE AI PROCESSING
   ↓
   Gemini Pro model analyzes data and generates:
   • Recommendation (Buy/Hold/Sell)
   • Investment thesis
   • Technical analysis interpretation
   • Fundamental assessment
   • Risk factors
   • Price target
   • Trading strategy
   ↓

8. REPORT FORMATTING
   ↓
   Professional equity research note format
   ↓

9. OUTPUT TO USER
   ↓
   • Display in UI / Console
   • Download as file
   • Use in further analysis
```

## 🗂️ File Structure & Relationships

```
d:\sa -AI\
│
├── 📄 full_analysis.py ⭐ CORE ENGINE
│   └── class FullStockAnalyzer
│       ├── __init__(api_key)
│       ├── fetch_stock_data(ticker, period)
│       │   ├── _calculate_indicators()
│       │   ├── _extract_fundamentals()
│       │   ├── _calculate_support_resistance()
│       │   ├── _get_latest_indicators()
│       │   ├── _analyze_volume()
│       │   └── _analyze_trend()
│       ├── generate_analysis_report(stock_data)
│       │   └── _prepare_data_summary()
│       └── analyze_stock(ticker, period) → Full Report
│
├── 🌐 main.py ⭐ WEB INTERFACE
│   ├── Streamlit UI configuration
│   ├── Custom CSS styling
│   ├── Sidebar (API key, ticker input)
│   ├── Main display area
│   │   ├── Quick metrics cards
│   │   ├── Full report display
│   │   ├── Technical charts
│   │   └── Support/resistance levels
│   └── Download functionality
│
├── 🧪 example_usage.py → EXAMPLES & TESTING
│   ├── Example 1: Quick multi-stock analysis
│   ├── Example 2: Full AI report generation
│   └── Example 3: Accessing specific data points
│
├── 📦 requirements.txt → DEPENDENCIES
│   ├── streamlit (UI framework)
│   ├── pandas (Data manipulation)
│   ├── plotly (Charts)
│   ├── yfinance (Stock data)
│   ├── numpy (Math operations)
│   ├── google-generativeai (AI analysis)
│   ├── python-dotenv (Environment variables)
│   ├── curl-cffi (Advanced data fetching)
│   ├── statsmodels (SARIMA forecasting)
│   ├── python-docx (Word export)
│   └── fpdf (PDF export)
│
├── 📚 Documentation Files:
│   ├── AI_ANALYSIS_README.md → Complete documentation
│   ├── QUICK_SETUP.md → 5-minute setup guide
│   ├── IMPLEMENTATION_SUMMARY.md → This summary
│   └── ARCHITECTURE.md → System architecture (this file)
│
└── 🔧 Configuration & Support:
    ├── config.py → Application settings
    └── .env (user creates) → API keys
```

## 🧩 Component Breakdown

### 1. FullStockAnalyzer Class

**Purpose**: Core analysis engine

**Key Methods**:

```python
# Initialize with API key
analyzer = FullStockAnalyzer(api_key="...")

# Fetch comprehensive stock data
data = analyzer.fetch_stock_data("AAPL", "1y")
# Returns: {ticker, price, fundamentals, technicals, support/resistance, ...}

# Generate AI analysis report
report = analyzer.generate_analysis_report(data)
# Returns: Professional formatted research note text

# One-step complete analysis
report = analyzer.analyze_stock("AAPL", "1y")
# Returns: Complete report ready for display/save
```

**Internal Methods**:

- `_calculate_indicators()` → All technical calculations
- `_extract_fundamentals()` → Parse Yahoo Finance info
- `_calculate_support_resistance()` → Pivot point method
- `_get_latest_indicators()` → Current indicator values
- `_analyze_volume()` → Volume patterns and trends
- `_analyze_trend()` → Short/medium/long-term trends
- `_prepare_data_summary()` → Format data for AI prompt
- `_format_value()` → Human-readable number formatting

### 2. Streamlit Web App

**Layout**:

```
┌─────────────────────────────────────────────────────────┐
│  Header: "ZMtech AI Stock Analysis Platform"           │
├───────────┬─────────────────────────────────────────────┤
│           │  Quick Metrics Bar:                         │
│ Sidebar:  │  ┌──────┬──────┬──────┬──────┬──────┐      │
│           │  │Price │ RSI  │Trend │Volume│MACD  │      │
│ • API Key │  └──────┴──────┴──────┴──────┴──────┘      │
│ • Ticker  │                                             │
│ • Period  │  Full Equity Research Report:               │
│ • Mode    │  ┌─────────────────────────────────────┐   │
│ • Toggles │  │ I. RECOMMENDATION                   │   │
│           │  │ II. INVESTMENT THESIS               │   │
│ Info Box  │  │ III. TECHNICAL ANALYSIS             │   │
│           │  │ IV. FUNDAMENTAL ASSESSMENT          │   │
│           │  │ V. RISK FACTORS                     │   │
│           │  │ VI. PRICE TARGET                    │   │
│           │  │ VII. ZMTECH ANALYSIS - KEY LEVELS   │   │
│           │  └─────────────────────────────────────┘   │
│           │  [Download: Text | Word | PDF]              │
│           │                                             │
│           │  Technical Charts:                          │
│           │  ┌─────────────────────────────────────┐   │
│           │  │ Price + EMAs + Bollinger Bands      │   │
│           │  │ + Earnings Markers ("E")            │   │
│           │  │ + Support/Resistance Lines          │   │
│           │  ├─────────────────────────────────────┤   │
│           │  │ Volume Bars + Volume MA             │   │
│           │  ├─────────────────────────────────────┤   │
│           │  │ MACD Indicator                      │   │
│           │  ├─────────────────────────────────────┤   │
│           │  │ RSI Indicator                       │   │
│           │  └─────────────────────────────────────┘   │
│           │                                             │
│           │  Key Price Levels (Summary):                │
│           │  ┌─────────────┬─────────────────┐         │
│           │  │ Resistance  │ Support         │         │
│           │  │ • R3: $XXX  │ • S1: $XXX      │         │
│           │  │ • R2: $XXX  │ • S2: $XXX      │         │
│           │  │ • R1: $XXX  │ • S3: $XXX      │         │
│           │  └─────────────┴─────────────────┘         │
└───────────┴─────────────────────────────────────────────┘
```

### 3. Technical Indicator Module

**Calculations** (in `_calculate_indicators`):

```python
# Moving Averages
EMA9 = Close.ewm(span=9).mean()
EMA20 = Close.ewm(span=20).mean()
EMA50 = Close.ewm(span=50).mean()
EMA200 = Close.ewm(span=200).mean()

# MACD
EMA12 = Close.ewm(span=12).mean()
EMA26 = Close.ewm(span=26).mean()
MACD = EMA12 - EMA26
Signal = MACD.ewm(span=9).mean()
Histogram = MACD - Signal

# RSI
delta = Close.diff()
gain = delta.where(delta > 0, 0).rolling(14).mean()
loss = -delta.where(delta < 0, 0).rolling(14).mean()
RS = gain / loss
RSI = 100 - (100 / (1 + RS))

# Bollinger Bands
BB_Middle = Close.rolling(20).mean()
BB_Std = Close.rolling(20).std()
BB_Upper = BB_Middle + (2 * BB_Std)
BB_Lower = BB_Middle - (2 * BB_Std)

# Volume Moving Average
Vol_MA = Volume.rolling(20).mean()

# VWAP (Volume Weighted Average Price)
Typical_Price = (High + Low + Close) / 3
Volume_Price = Typical_Price * Volume
VWAP = Volume_Price.cumsum() / Volume.cumsum()

# Heikin-Ashi
HA_Close = (Open + High + Low + Close) / 4
HA_Open = (Previous_HA_Open + Previous_HA_Close) / 2
HA_High = max(High, HA_Open, HA_Close)
HA_Low = min(Low, HA_Open, HA_Close)

# ATR
High_Low = High - Low
High_Close = abs(High - Close.shift())
Low_Close = abs(Low - Close.shift())
True_Range = max(High_Low, High_Close, Low_Close)
ATR = True_Range.rolling(14).mean()

# Stochastic
Low_14 = Low.rolling(14).min()
High_14 = High.rolling(14).max()
%K = 100 * ((Close - Low_14) / (High_14 - Low_14))
%D = %K.rolling(3).mean()
```

### 4. Support/Resistance Module

**Calculation** (in `_calculate_support_resistance`):

```python
# Pivot Point Method
high = recent_60_days['High'].max()
low = recent_60_days['Low'].min()
close = today['Close']

pivot = (high + low + close) / 3

# Resistance Levels
R1 = (2 * pivot) - low
R2 = pivot + (high - low)
R3 = high + 2 * (pivot - low)

# Support Levels
S1 = (2 * pivot) - high
S2 = pivot - (high - low)
S3 = low - 2 * (high - pivot)
```

### 5. AI Integration Module

**Prompt Structure**:

```
PROMPT = f"""
You are a senior equity research analyst...

STOCK DATA:
{comprehensive_technical_fundamental_data}

INSTRUCTIONS:
1. Analyze all data provided
2. Clear recommendation (BUY/HOLD/SELL)
3. Use professional terminology
4. Structure response with:
   - Recommendation
   - Investment Thesis
   - Technical Analysis
   - Fundamental Assessment
   - Risk Factors
   - Price Target
   - ZMtech Analysis (Key Levels)
"""

response = genai.model.generate_content(PROMPT)
return response.text
```

## 🔐 Security & Configuration

### API Key Management

```
Priority order:
1. Direct parameter: FullStockAnalyzer(api_key="...")
2. Environment variable: GOOGLE_API_KEY
3. .env file: GOOGLE_API_KEY=...
4. Streamlit secrets: .streamlit/secrets.toml
5. User input in UI sidebar
```

### Data Privacy

- No data stored permanently
- API calls made directly to services
- Reports saved only if user chooses
- No telemetry or tracking

## 📊 Data Schema

### Stock Data Dictionary Structure

```python
stock_data = {
    'ticker': str,                    # e.g., "AAPL"
    'current_price': float,          # e.g., 175.50
    'price_change': float,           # e.g., 2.35 (%)

    'historical_data': DataFrame,    # OHLCV + indicators

    'fundamentals': {
        'market_cap': int,
        'pe_ratio': float,
        'forward_pe': float,
        'peg_ratio': float,
        'price_to_book': float,
        'dividend_yield': float,
        'beta': float,
        'earnings_growth': float,
        'revenue_growth': float,
        'profit_margin': float,
        'debt_to_equity': float,
        'current_ratio': float,
        '52w_high': float,
        '52w_low': float,
        'sector': str,
        'industry': str
    },

    'technical_indicators': {
        'rsi': float,
        'macd': float,
        'macd_signal': float,
        'macd_histogram': float,
        'ema9': float,
        'ema20': float,
        'ema50': float,
        'ema200': float,
        'bb_upper': float,
        'bb_middle': float,
        'bb_lower': float,
        'atr': float,
        'stoch_k': float,
        'stoch_d': float
    },

    'support_resistance': {
        'resistance_3': float,
        'resistance_2': float,
        'resistance_1': float,
        'pivot': float,
        'support_1': float,
        'support_2': float,
        'support_3': float,
        '52w_high': float,
        '52w_low': float
    },

    'volume_analysis': {
        'current_volume': int,
        'avg_volume_20d': int,
        'volume_ratio': float,
        'volume_trend': str  # "High" | "Normal" | "Low"
    },

    'trend_analysis': {
        'short_term': str,    # "Bullish" | "Bearish"
        'medium_term': str,   # "Bullish" | "Bearish"
        'long_term': str,     # "Bullish" | "Bearish"
        'overall': str        # "Strong Bullish" | "Bullish" | "Bearish" | "Strong Bearish"
    }
}
```

## ⚡ Performance Optimization

### Caching Strategy

```python
# Streamlit caching for data fetches
@st.cache_data(ttl=300)  # 5-minute cache
def fetch_stock_data(ticker, period):
    # Expensive Yahoo Finance call
    return data

# Avoid re-computing indicators
# Store in DataFrame, calculate once
```

### Async Considerations

```python
# Currently synchronous pipeline:
# User → Fetch → Calculate → AI → Display

# Future async optimization:
# User → [Fetch + Calculate in parallel] → AI → Display
```

## 🧪 Testing Strategy

### Manual Testing Checklist

```
□ Web app launches without errors
□ API key validation works
□ Stock data fetch succeeds
□ Technical indicators calculate correctly
□ AI report generates successfully
□ Charts render properly
□ Download functionality works
□ Multiple stocks tested
□ Edge cases handled (invalid ticker, etc.)
```

### Example Test Script

```python
# test_analysis.py
from full_analysis import FullStockAnalyzer

def test_basic_analysis():
    analyzer = FullStockAnalyzer()

    # Test data fetch
    data = analyzer.fetch_stock_data("AAPL", "1mo")
    assert data['ticker'] == "AAPL"
    assert 'current_price' in data

    # Test indicators
    assert 'rsi' in data['technical_indicators']
    assert 0 <= data['technical_indicators']['rsi'] <= 100

    # Test AI report
    report = analyzer.analyze_stock("AAPL", "1mo")
    assert "RECOMMENDATION" in report
    assert "ZMTECH ANALYSIS" in report

    print("✅ All tests passed!")

test_basic_analysis()
```

## 🚀 Deployment Options

### Local Deployment (Current)

```bash
streamlit run main.py
# Runs on localhost:8501
```

### Streamlit Cloud Deployment

```bash
1. Push code to GitHub
2. Connect Streamlit Cloud to repo
3. Set GOOGLE_API_KEY in secrets
4. Deploy!
```

### Docker Deployment

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["streamlit", "run", "main.py"]
```

### Heroku Deployment

```bash
# Procfile
web: streamlit run --server.port=$PORT main.py

# Deploy
git push heroku main
```

## 📈 Scalability Considerations

### Current Limits

- Single-user desktop application
- Synchronous processing
- No database (stateless)
- API rate limits (Google AI free tier)

### Future Scaling

```
1. Add database (PostgreSQL/MongoDB)
   → Store historical analyses
   → Cache expensive calculations

2. Implement queue system (Celery/Redis)
   → Handle multiple concurrent requests
   → Background job processing

3. Add caching layer (Redis)
   → Cache stock data (5-15 min TTL)
   → Cache AI responses (1 hour TTL)

4. Load balancing
   → Multiple Streamlit instances
   → Round-robin distribution

5. Upgrade to paid API tiers
   → Higher rate limits
   → Better performance
```

## 🎯 Success Criteria

The system successfully:

1. ✅ Fetches real-time Yahoo Finance data
2. ✅ Calculates 15+ technical indicators accurately
3. ✅ Extracts comprehensive fundamental metrics
4. ✅ Computes support/resistance levels
5. ✅ Integrates Google Generative AI seamlessly
6. ✅ Generates professional research reports
7. ✅ Provides clear Buy/Hold/Sell recommendations
8. ✅ Includes "ZMtech Analysis" section
9. ✅ Offers beautiful Streamlit interface
10. ✅ Enables report downloads
11. ✅ Handles errors gracefully
12. ✅ Performs consistently across stocks

## 📝 Conclusion

This architecture provides:

- **Modularity**: Each component has clear responsibilities
- **Extensibility**: Easy to add new features
- **Reliability**: Robust error handling
- **Performance**: Optimized for desktop use
- **User Experience**: Professional UI/UX
- **Maintainability**: Well-documented code

**The system is production-ready for personal/educational use!**

---

**ZMtech AI Stock Analysis Platform**
_Professional equity research at your fingertips_ 📊
