# 🏗️ System Architecture - ZMtech Stock Analysis Platform

## 📊 High-Level Architecture
```
┌─────────────────────────────────────────────────────────────────┐
│                    ZMTECH PLATFORM ECOSYSTEM                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────────────┐    ┌──────────────────────────┐    │
│  │   Web Application       │    │   Desktop Analytical     │    │
│  │   (Streamlit)           │    │   Tools (Tkinter)        │    │
│  │   • main.py             │    │   • Earnings Apps        │    │
│  │   • Interactive Charts  │    │   • Sector Compare       │    │
│  │   • AI Reports          │    │   • Options Chain        │    │
│  └──────────┬──────────────┘    └───────────┬──────────────┘    │
│             │                               │                   │
└─────────────┼───────────────────────────────┼───────────────────┘
              │                               │
              ▼                               ▼
     ┌──────────────────────────────────────────────────┐
     │              CORE ANALYSIS ENGINE                │
     │              (full_analysis.py)                  │
     │           • Data Aggregation                     │
     │           • Technical Indicators                 │
     │           • AI Prompt Engineering                │
     └────────────────────────┬─────────────────────────┘
                              │
           ┌──────────────────┼──────────────────┐
           ▼                  ▼                  ▼
    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
    │ Yahoo Finance│   │ Google Gemini│   │ File System │
    │ (Market Data)│   │ (Intelligence)│   │ (Cache/Logs)│
    └─────────────┘    └─────────────┘    └─────────────┘
```

## 🔄 Data Flow
```
1. USER ORCHESTRATION
   ↓
   • Web App: Select Ticker, Period, Analysis Mode
   • Desktop: Select Earnings Date, Reference Tickers
   ↓

2. DATA ACQUISITION LAYER (yfinance)
   ↓
   • Historical OHLCV Data
   • Fundamental Metrics (P/E, PEG, Debt/Equity)
   • Option Chains (for Desktop Tools)
   • Sector Peer Data
   ↓

3. ANALYTICS ENGINE (full_analysis.py)
   ↓
   • Technical Calculation: RSI, MACD, Bollinger Bands, ATR
   • Statistical Modeling: Standard Deviation, Regression
   • Price Levels: Pivot Points, Support/Resistance (S1-S3, R1-R3)
   ↓

4. INTELLIGENCE LAYER (Google Gemini)
   ↓
   • Prompt Construction: Injecting formatted market data
   • Persona Adoption: "Senior Sell-Side Equity Research Analyst"
   • Report Generation: 8-Section Institutional Note
   ↓

5. VISUALIZATION & OUTPUT
   ↓
   • Streamlit: Interactive Plotly Charts (Candlestick, Volume, Signals)
   • Desktop: Matplotlib Static Charts (Earnings Compare)
   • Export: Formatted Word (.docx) and PDF (.pdf) Reports
```

## 🗂️ File Structure & Relationships
```
c:\zmtechstockAIagent\
│
├── 🧠 full_analysis.py ⭐ CORE ENGINE
│   └── class FullStockAnalyzer
│       ├── fetch_stock_data(ticker, period)
│       │   ├── _calculate_indicators()
│       │   └── _extract_fundamentals()
│       └── generate_analysis_report(data)
│           └── returns Formatted Sell-Side Report
│
├── 🚀 main.py ⭐ WEB DIRECTORY
│   ├── Lazy Loading Mechanism (Module optimization)
│   ├── Streamlit UI Configuration
│   ├── Interactive Charting (Plotly)
│   └── Report Export Logic (PDF/Word)
│
├── 📉 Earnings Tools (Desktop)
│   ├── earnings_sector_compare.py
│   │   ├── Sector/Peer Comparison
│   │   └── Static Chart Export
│   └── earnings.py
│       ├── Unified Dashboard
│       └── Options Volatility Analysis
│
├── ⚙️ Configuration
│   ├── check_models.py (Diagnostic)
│   ├── .streamlit/
│   │   └── secrets.toml (API Keys)
│   └── requirements.txt
│
└── 📄 Documentation
    └── ARCHITECTURE.md (This file)
```

## 🧩 Component Breakdown

### 1. FullStockAnalyzer Class (full_analysis.py)
**Purpose**: Central logic for data processing and AI interaction.

**Key Methods**:
```python
# Initialize
analyzer = FullStockAnalyzer(api_key="...")

# Fetch & Process
data = analyzer.fetch_stock_data("NVDA", "1y")
# Returns: Dict with Price, Technicals, Fundamentals, SR Levels

# Generate Institutional Report
report = analyzer.generate_analysis_report(data)
# Uses "Senior Sell-Side Analyst" persona
```

### 2. Streamlit Web App (main.py)
**Layout**:
```
┌─────────────────────────────────────────────────────────┐
│  Header: "ZMtech Stock Analysis Platform"               │
├───────────┬─────────────────────────────────────────────┤
│ Sidebar:  │  Metric Dashboard:                          │
│           │  ┌──────┬──────┬──────┬───────┐            │
│ • API Key │  │Price │ RSI  │ MACD │Volume │            │
│ • Ticker  │  └──────┴──────┴──────┴───────┘            │
│ • Mode    │                                             │
│           │  Tabs / Analysis Views:                     │
│           │  ┌───────────────┬───────────────────────┐  │
│           │  │ AI Research   │ Technical Charts      │  │
│           │  │ Note          │ (Interactive)         │  │
│           │  │               │                       │  │
│           │  │ (8 Sections)  │ • Candlestick/Line    │  │
│           │  │ • Thesis      │ • EMAs / Bands        │  │
│           │  │ • Valuation   │ • Volume / Signals    │  │
│           │  │ • Strategy    │                       │  │
│           │  └───────────────┴───────────────────────┘  │
│           │                                             │
│           │  [Download .docx] [Download .pdf]           │
└───────────┴─────────────────────────────────────────────┘
```

### 3. Desktop Earnings Tools
**Purpose**: Specialized analysis for earnings events and volatility.

**Capabilities**:
*   **Event Study**: Analyze price action -5d to +5d around earnings.
*   **Peer Comparison**: Overlay competitor returns and volume.
*   **Options Visualization**: Plot Volatility Smiles and Skew.
*   **Export**: Generates high-res PNG charts for presentations.

## 🔐 Security & Configuration
*   **API Security**: Google Gemini API key managed via `st.secrets` or environment variables.
*   **Data Integrity**: Fallback mechanisms for missing data points in `yfinance`.
*   **Validation**: Input sanitization for Tickers and dates.

## ⚡ Performance Optimization
*   **Lazy Loading**: Custom `LazyLoader` in `main.py` prevents loading heavy libraries (like Matplotlib/Plotly) until specifically needed, speeding up startup.
*   **Caching**: Streamlit `@st.cache_data` used for stock data calls and AI response generation (TTL encoded).
