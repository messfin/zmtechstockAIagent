# 🏗️ System Architecture - AI Stock Analysis Platform

## 📊 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌─────────────────────────┐    ┌──────────────────────────┐   │
│  │   Streamlit Web App     │    │  Command Line Interface  │   │
│  │   (analysis_app.py)     │    │  (full_analysis.py)      │   │
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
   • EMAs (9, 20, 50, 200)
   • Bollinger Bands (20, 2σ)
   • ATR (14-period)
   • Stochastic (%K, %D)
   ↓

4. SUPPORT/RESISTANCE CALCULATION
   ↓
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
├── 🌐 analysis_app.py ⭐ WEB INTERFACE
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
│   └── python-dotenv (Environment variables)
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
│ • Button  │  ┌─────────────────────────────────────┐   │
│           │  │ I. RECOMMENDATION                   │   │
│ Info Box  │  │ II. INVESTMENT THESIS               │   │
│           │  │ III. TECHNICAL ANALYSIS             │   │
│           │  │ IV. FUNDAMENTAL ASSESSMENT          │   │
│           │  │ V. RISK FACTORS                     │   │
│           │  │ VI. PRICE TARGET                    │   │
│           │  │ VII. ZMTECH ANALYSIS - KEY LEVELS   │   │
│           │  └─────────────────────────────────────┘   │
│           │  [Download Button]                          │
│           │                                             │
│           │  Technical Charts:                          │
│           │  ┌─────────────────────────────────────┐   │
│           │  │ Price + EMAs + Bollinger Bands      │   │
│           │  ├─────────────────────────────────────┤   │
│           │  │ Volume Bars                         │   │
│           │  ├─────────────────────────────────────┤   │
│           │  │ RSI Indicator                       │   │
│           │  └─────────────────────────────────────┘   │
│           │                                             │
│           │  Support/Resistance Levels:                 │
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

## 🔐 Configuration & Security

### API Key Management
The system uses a fallback strategy to locate the `GOOGLE_API_KEY`:
1.  **Streamlit Secrets**: `.streamlit/secrets.toml` (Primary for Cloud/Local).
2.  **Environment Variables**: `.env` file or System Env.
3.  **UI Input**: User can manually enter key in the sidebar.

### Caching
*   **Web App**: Uses `@st.cache_data` and `@st.cache_resource` to minimize API calls to Yahoo Finance and store session objects.
*   **Desktop Apps**: Implements local dictionary-based caching for stock data queries.

## 🚀 Deployment

### Web Application
Run locally:
```bash
streamlit run analysis_app.py
# Runs on localhost:8501
```

### Desktop Tools
Run as standard Python scripts:
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
CMD ["streamlit", "run", "analysis_app.py"]
```

### Heroku Deployment

```bash
# Procfile
web: streamlit run --server.port=$PORT analysis_app.py

# Deploy
git push heroku main
```

## 🔄 Data Flow (Web App)

1.  **User Input**: Ticker, Date Range, Analysis Mode.
2.  **Data Acquisition**: `yfinance` fetches OHLCV and fundamental data.
3.  **Processing**: `pandas` calculates technical indicators.
4.  **AI Analysis**: Aggregated data sent to Google Gemini Pro via `google-generativeai`.
5.  **Visualization**: Streamlit renders metrics and Plotly charts.
6.  **Reporting**: AI text formatted into Downloadable Word/PDF documents.

## 🚧 Known Issues / Notes
*   **Desktop Tools**: `earnings_sector_compare.py` and `earnings.py` currently contain git merge conflict markers (`<<<<<<< HEAD`) which may affect execution. Ensure these are resolved before running.
