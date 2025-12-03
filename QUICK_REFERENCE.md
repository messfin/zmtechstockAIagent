# 🚀 Quick Reference Card - AI Stock Analysis Platform

## ⚡ Quick Start (3 Steps)

```powershell
# 1. Set API key
$env:GOOGLE_API_KEY="your-google-ai-api-key-here"

# 2. Install dependencies
pip install -r requirements.txt

# 3. Launch app
streamlit run analysis_app.py
```

**Get API Key (FREE)**: https://makersuite.google.com/app/apikey

---

## 📋 Common Commands

### Launch Web Interface

```powershell
streamlit run analysis_app.py
```

### Run Example Script

```powershell
python example_usage.py
```

### Quick Analysis from CLI

```powershell
python full_analysis.py
```

### Install Dependencies

```powershell
pip install -r requirements.txt
```

---

## 🐍 Python Code Snippets

### Basic Usage

```python
from full_analysis import FullStockAnalyzer

# Initialize
analyzer = FullStockAnalyzer()

# Analyze and print report
report = analyzer.analyze_stock("AAPL", "1y")
print(report)
```

### Get Data Only (No AI Report)

```python
from full_analysis import FullStockAnalyzer

analyzer = FullStockAnalyzer()
data = analyzer.fetch_stock_data("TSLA", "6mo")

# Access indicators
print(f"RSI: {data['technical_indicators']['rsi']}")
print(f"Price: ${data['current_price']:.2f}")
print(f"Trend: {data['trend_analysis']['overall']}")
```

### Save Report to File

```python
from full_analysis import FullStockAnalyzer
from datetime import datetime

analyzer = FullStockAnalyzer()
report = analyzer.analyze_stock("MSFT", "1y")

filename = f"MSFT_{datetime.now().strftime('%Y%m%d')}.txt"
with open(filename, 'w', encoding='utf-8') as f:
    f.write(report)
```

### Batch Analysis

```python
from full_analysis import FullStockAnalyzer

analyzer = FullStockAnalyzer()
stocks = ["AAPL", "GOOGL", "MSFT", "TSLA", "NVDA"]

for ticker in stocks:
    print(f"\n{'='*60}\nAnalyzing {ticker}...\n{'='*60}")
    report = analyzer.analyze_stock(ticker, "3mo")
    print(report)
```

---

## 📊 Key Features Quick List

✅ **Technical Analysis**

- RSI, MACD, EMAs (9,20,50,200)
- Bollinger Bands, ATR, Stochastic
- Volume analysis, Trend detection

✅ **Fundamental Metrics**

- P/E, PEG, P/B ratios
- Earnings/Revenue growth
- Profit margins, Debt/Equity

✅ **AI-Powered Insights**

- Buy/Hold/Sell recommendations
- Investment thesis
- Price targets
- Risk assessment

✅ **Support/Resistance**

- Pivot points
- 3 resistance levels
- 3 support levels

✅ **Professional Output**

- Research note format
- Financial terminology
- Downloadable reports

---

## 🎯 Report Sections

Every report includes:

1. **RECOMMENDATION** - Buy/Hold/Sell + conviction
2. **INVESTMENT THESIS** - Detailed rationale
3. **TECHNICAL ANALYSIS** - Indicator interpretation
4. **FUNDAMENTAL ASSESSMENT** - Valuation & growth
5. **RISK FACTORS** - Key risks identified
6. **PRICE TARGET & TIMELINE** - Specific targets
7. **ZMTECH ANALYSIS - KEY LEVELS** - Support/resistance

---

## 🔧 Troubleshooting Quick Fix

| Problem          | Solution                                      |
| ---------------- | --------------------------------------------- |
| API key error    | Set `$env:GOOGLE_API_KEY="key"`               |
| Module not found | Run `pip install -r requirements.txt`         |
| Invalid ticker   | Verify ticker symbol is correct               |
| Slow generation  | Normal, AI takes 30-60 seconds                |
| Import error     | Ensure in correct directory: `cd "d:\sa -AI"` |

---

## 📁 Important Files

| File                    | Purpose                 |
| ----------------------- | ----------------------- |
| `full_analysis.py`      | Core analysis engine    |
| `analysis_app.py`       | Streamlit web interface |
| `example_usage.py`      | Usage examples          |
| `requirements.txt`      | Dependencies list       |
| `AI_ANALYSIS_README.md` | Full documentation      |
| `QUICK_SETUP.md`        | Setup guide             |

---

## 🌐 Web Interface Guide

1. **Sidebar**:

   - Enter Google AI API key (if not in environment)
   - Enter stock ticker (e.g., AAPL)
   - Select time period (1mo - 5y)
   - Click "Generate Analysis"

2. **Main Area**:
   - Quick metrics (Price, RSI, Trend, Volume, MACD)
   - Full equity research report
   - Technical charts with indicators
   - Support/resistance levels
   - Download button

---

## 💡 Pro Tips

1. **Set API key once**:

   ```powershell
   # Add to PowerShell profile for persistence
   notepad $PROFILE
   # Add: $env:GOOGLE_API_KEY="your-key"
   ```

2. **Create .env file**:

   ```
   GOOGLE_API_KEY=your-key-here
   ```

3. **Quick test**:

   ```powershell
   python -c "from full_analysis import FullStockAnalyzer; print('✅ Setup OK!')"
   ```

4. **Save common stocks**:

   ```python
   # my_watchlist.py
   from full_analysis import FullStockAnalyzer

   WATCHLIST = ["AAPL", "TSLA", "MSFT"]
   analyzer = FullStockAnalyzer()

   for stock in WATCHLIST:
       print(analyzer.analyze_stock(stock, "1mo"))
   ```

---

## 📈 Indicator Reference

| Indicator       | Meaning             | Good Value                   |
| --------------- | ------------------- | ---------------------------- |
| RSI             | Overbought/Oversold | <30 oversold, >70 overbought |
| MACD            | Momentum            | MACD > Signal = Bullish      |
| EMA9 vs EMA20   | Short-term trend    | EMA9 > EMA20 = Bullish       |
| Volume          | Activity            | High volume = Strong move    |
| Bollinger Bands | Volatility          | Price near lower = oversold  |

---

## ⚠️ Remember

- **Not financial advice** - Educational purposes only
- **Verify data** - Double-check critical decisions
- **Consult professionals** - For investment advice
- **Understand risks** - Trading involves risk

---

## 📞 Quick Support

**Check in order:**

1. Error message (read carefully!)
2. QUICK_SETUP.md (setup issues)
3. AI_ANALYSIS_README.md (detailed docs)
4. ARCHITECTURE.md (technical details)

---

## 🎓 Learning Path

**Beginner**:

1. Run `streamlit run analysis_app.py`
2. Enter ticker and analyze
3. Read generated reports

**Intermediate**:

1. Run `python example_usage.py`
2. Modify ticker/period in examples
3. Understand indicator values

**Advanced**:

1. Import `FullStockAnalyzer` in your scripts
2. Customize calculations in `full_analysis.py`
3. Modify AI prompts for different analysis styles

---

## 🔗 Useful URLs

- **Google AI API**: https://makersuite.google.com/app/apikey
- **Yahoo Finance**: https://finance.yahoo.com
- **Streamlit Docs**: https://docs.streamlit.io

---

## ✅ Checklist for First Run

- [ ] Python 3.8+ installed
- [ ] Google AI API key obtained
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] API key set (environment variable or .env file)
- [ ] In correct directory (`d:\sa -AI`)
- [ ] Run `streamlit run analysis_app.py`
- [ ] Enter ticker and analyze
- [ ] Review report
- [ ] Download if desired

---

## 🎯 One-Liner Examples

**Quick analysis**:

```powershell
python -c "from full_analysis import FullStockAnalyzer; print(FullStockAnalyzer().analyze_stock('AAPL'))"
```

**Get RSI only**:

```powershell
python -c "from full_analysis import FullStockAnalyzer; d=FullStockAnalyzer().fetch_stock_data('AAPL','1mo'); print(f'RSI: {d[\"technical_indicators\"][\"rsi\"]:.2f}')"
```

**Check trend**:

```powershell
python -c "from full_analysis import FullStockAnalyzer; d=FullStockAnalyzer().fetch_stock_data('TSLA','3mo'); print(f'Trend: {d[\"trend_analysis\"][\"overall\"]}')"
```

---

**🚀 Happy Analyzing! 📊**

_Print this card for quick reference while coding_
