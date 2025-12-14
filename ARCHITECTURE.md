# 🏗️ System Architecture - AI Stock Analysis Platform

## 📊 High-Level Architecture

The ZMtech Stock Analysis Platform is a hybrid system comprising a web-based Stock Analysis Dashboard and standalone Desktop Analytics Tools.

```mermaid
graph TD
    User((User))
    
    subgraph "Web Application"
        Main[main.py (Entry Point)]
        Config[conf.toml / secrets.toml]
        LazyLoader[Lazy Loading Mechanism]
        FullAnalysis[full_analysis.py (Core Engine)]
        StreamlitUI[Streamlit UI]
        
        Main --> Config
        Main --> LazyLoader
        LazyLoader --> Power
        LazyLoader --> FullAnalysis
        FullAnalysis --> StreamlitUI
    end
    
    subgraph "Desktop Tools"
        EarningsApp[earnings_sector_compare.py]
        UnifiedApp[earnings.py]
        TkinterUI[Tkinter UI]
        
        EarningsApp --> TkinterUI
        UnifiedApp --> TkinterUI
    end
    
    subgraph "External Services"
        YF[Yahoo Finance API]
        GenAI[Google Gemini AI]
    end
    
    User --> Main
    User --> EarningsApp
    
    FullAnalysis --> YF
    FullAnalysis --> GenAI
    
    EarningsApp --> YF
    UnifiedApp --> YF
```

## 🔄 Core Components

### 1. Web Application (`main.py`)
The primary interface for general stock analysis.
*   **Entry Point**: `main.py` serves as the robust entry point.
*   **Lazy Loading**: Implements a custom module loading system to handle `FullStockAnalyzer` imports gracefully, ensuring compatibility with Streamlit Cloud and local environments.
*   **UI Framework**: Built with Streamlit, featuring a "CNBC-style" dark finance theme.
*   **Features**:
    *   Real-time stock data fetching.
    *   Interactive Plotly charts (Candlestick, Volume, RSI, MACD).
    *   AI-powered equity research reports.
    *   Word/PDF report generation.

### 2. Analysis Engine (`full_analysis.py`)
The heavy lifter for the web application.
*   **Class**: `FullStockAnalyzer`
*   **Responsibilities**:
    *   Data aggregation (Price, Fundamentals, Technicals).
    *   Technical Indicator calculation (RSI, MACD, Bollinger Bands, ATR, Stochastic, Ichimoku).
    *   Support/Resistance level identification (Pivot points).
    *   Prompt engineering for Google Gemini AI.

### 3. Desktop Analytics Tools (`earnings_sector_compare.py` & `earnings.py`)
Standalone GUI applications for specialized analysis.
*   **Framework**: Python `tkinter` for native desktop UI.
*   **Features**:
    *   **Earnings Analysis**: Compare stock performance around earnings dates (Pre/Post 1d, 3d, 5d).
    *   **Sector Comparison**: Analyze peer performance during earnings.
    *   **Options Analysis**: Implied Volatility (IV) smile plotting and option chain visualization.
    *   **Outputs**: Exports charts (PNG) and data (CSV) to `earnings_analysis/` directory.

### 4. Utility Scripts
*   `check_models.py`: Diagnostic tool to verify Google Gemini API keys and list available models (specifically checking for 'flash' models).

## 🗂️ File Structure

```
zmtechstockAIagent/
├── .streamlit/
│   ├── config.toml       # UI Theme configuration
│   └── secrets.toml      # API Keys (Git-ignored)
├── earnings_analysis/    # Output directory for desktop tool reports
├── main.py              # 🚀 WEB APP ENTRY POINT
├── full_analysis.py     # 🧠 CORE ANALYSIS LOGIC
├── earnings_sector_compare.py # 📉 DESKTOP APP (Earnings)
├── earnings.py          # 📉 DESKTOP APP (Unified)
├── check_models.py      # 🛠️ DIAGNOSTIC TOOL
└── ARCHITECTURE.md      # This file
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
python earnings_sector_compare.py
# OR
python earnings.py
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
