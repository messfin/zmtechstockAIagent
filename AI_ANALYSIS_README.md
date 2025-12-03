# ZMtech AI Stock Analysis Platform

Professional equity research reports powered by Google Generative AI and Yahoo Finance.

## 🌟 Overview

This platform combines real-time market data from Yahoo Finance with advanced AI analysis from Google's Generative AI to produce institutional-quality equity research reports with clear Buy/Hold/Sell recommendations.

## ✨ Features

### 📊 Comprehensive Technical Analysis

- **RSI (Relative Strength Index)** - Overbought/oversold conditions
- **MACD** - Trend momentum and direction
- **Moving Averages** - EMA 9, 20, 50, 200
- **Bollinger Bands** - Volatility and price extremes
- **ATR (Average True Range)** - Volatility measurement
- **Stochastic Oscillator** - Momentum indicator
- **Volume Analysis** - Trading activity patterns

### 💼 Fundamental Metrics

- Valuation ratios (P/E, PEG, Price/Book)
- Growth metrics (Earnings, Revenue)
- Financial health (Debt/Equity, Current Ratio)
- Profitability margins
- Market positioning (Sector, Industry)

### 🎯 Support & Resistance Analysis

- Multiple resistance levels (R1, R2, R3)
- Multiple support levels (S1, S2, S3)
- Pivot point calculation
- 52-week high/low tracking

### 🤖 AI-Powered Insights

- **Clear Recommendations** - Buy/Hold/Sell with conviction levels
- **Investment Thesis** - Detailed rationale with professional terminology
- **Risk Assessment** - Key risk factors identified
- **Price Targets** - Specific targets with timeframes
- **Trading Strategy** - Entry, stop-loss, and target levels

## 🚀 Quick Start

### Prerequisites

1. **Python 3.8+** installed
2. **Google AI API Key** (free from [Google AI Studio](https://makersuite.google.com/app/apikey))

### Installation

1. Clone or navigate to the project directory:

```bash
cd "d:\sa -AI"
```

2. Install required packages:

```bash
pip install -r requirements.txt
```

3. Set up your Google AI API key (choose one method):

**Option A: Environment Variable (Recommended)**

```bash
# Windows PowerShell
$env:GOOGLE_API_KEY="your-api-key-here"

# Windows Command Prompt
set GOOGLE_API_KEY=your-api-key-here

# Linux/Mac
export GOOGLE_API_KEY="your-api-key-here"
```

**Option B: .env File**
Create a `.env` file in the project directory:

```
GOOGLE_API_KEY=your-api-key-here
```

**Option C: Streamlit Secrets**
Create `.streamlit/secrets.toml`:

```toml
GOOGLE_API_KEY = "your-api-key-here"
```

### Running the Application

**Streamlit Web Interface (Recommended):**

```bash
streamlit run analysis_app.py
```

**Command Line Interface:**

```bash
python full_analysis.py
```

## 📖 Usage Guide

### Web Interface

1. Launch the Streamlit app
2. Enter your Google AI API key in the sidebar (if not set as environment variable)
3. Enter a stock ticker symbol (e.g., AAPL, TSLA, MSFT)
4. Select the analysis period (1mo to 5y)
5. Click "🚀 Generate Analysis"
6. Review the comprehensive report
7. Download the report as a text file

### Command Line

```python
from full_analysis import FullStockAnalyzer

# Initialize with API key
analyzer = FullStockAnalyzer(api_key="your-api-key")

# Or use environment variable
analyzer = FullStockAnalyzer()

# Analyze a stock
report = analyzer.analyze_stock("AAPL", period="1y")
print(report)
```

## 📋 Report Sections

The generated report includes:

### I. Recommendation

- Clear Buy/Hold/Sell rating
- Conviction level (High/Medium/Low)

### II. Investment Thesis

- Fundamental analysis and valuation
- Technical setup and momentum
- Key catalysts or risks
- Risk-reward profile

### III. Technical Analysis

- RSI conditions and interpretation
- MACD signals and momentum
- Moving average alignment
- Volume patterns
- Bollinger Bands positioning

### IV. Fundamental Assessment

- Valuation metrics analysis
- Growth metrics and trends
- Financial health indicators
- Sector positioning

### V. Risk Factors

- Key risks to the investment thesis

### VI. Price Target & Timeline

- Specific price target
- Expected timeframe

### VII. ZMtech Analysis - Key Levels

- Resistance levels (R1, R2, R3)
- Support levels (S1, S2, S3)
- Pivot point
- Trading strategy with entry/exit levels

## 🎨 Features Showcase

### Professional Formatting

- Institutional-quality research note format
- Professional financial terminology
- Structured analysis sections
- Clear visual hierarchy

### Interactive Charts

- Candlestick price charts
- Moving averages overlay
- Bollinger Bands visualization
- Volume bars
- RSI indicator

### Real-Time Metrics

- Current price with daily change
- RSI status (Overbought/Oversold/Neutral)
- Trend direction (Bullish/Bearish)
- Volume analysis
- MACD signal

## 🔧 Configuration

### Analysis Parameters

Edit `full_analysis.py` to customize:

- Technical indicator periods
- Support/resistance calculation method
- Volume analysis thresholds

### UI Customization

Edit `analysis_app.py` to customize:

- Color scheme
- Chart layout
- Metrics display
- Report formatting

## 📊 Example Output

```
═══════════════════════════════════════════════════════════════
                    EQUITY RESEARCH NOTE
═══════════════════════════════════════════════════════════════

TICKER: AAPL
CURRENT PRICE: $175.50
DATE: December 03, 2025

-------------------------------------------------------------------
I. RECOMMENDATION
-------------------------------------------------------------------
BUY (High Conviction)

The stock exhibits strong bullish momentum with favorable
technical and fundamental indicators...

[Full detailed analysis continues...]
```

## 🛠️ Troubleshooting

### Common Issues

**"Google API key is required" error:**

- Ensure API key is set in environment variable or passed directly
- Verify the key is valid and active

**Data fetch errors:**

- Check internet connection
- Verify ticker symbol is correct
- Try a different time period

**Module not found errors:**

- Run `pip install -r requirements.txt`
- Ensure you're in the correct directory

**Slow analysis generation:**

- Normal for first run (30-60 seconds)
- Google AI processing time varies
- Larger time periods take longer

## 📚 API Documentation

### FullStockAnalyzer Class

```python
analyzer = FullStockAnalyzer(api_key: Optional[str] = None)
```

**Methods:**

- `fetch_stock_data(ticker: str, period: str = "1y")` - Get stock data
- `generate_analysis_report(stock_data: Dict)` - Generate AI report
- `analyze_stock(ticker: str, period: str = "1y")` - Complete analysis

## 🔐 Security Notes

- Never commit API keys to version control
- Use environment variables for sensitive data
- Keep `.env` files in `.gitignore`
- Rotate API keys periodically

## ⚠️ Disclaimer

This platform is for **informational and educational purposes only**.

- Not financial advice
- Not investment recommendations
- Past performance doesn't guarantee future results
- Always consult a licensed financial advisor
- Perform your own due diligence
- Understand the risks before investing

## 🤝 Contributing

Contributions welcome! Areas for improvement:

- Additional technical indicators
- More fundamental metrics
- Enhanced AI prompts
- UI/UX improvements
- Performance optimizations

## 📄 License

This project is for educational purposes. Use at your own risk.

## 🆘 Support

For issues or questions:

1. Check the troubleshooting section
2. Review the documentation
3. Verify your setup matches requirements

## 🔄 Updates

### Version 1.0.0 (Current)

- Initial release
- Google Generative AI integration
- Comprehensive technical analysis
- Professional report formatting
- Interactive Streamlit interface
- Support/resistance calculation
- Volume and trend analysis

---

**Built with ❤️ using:**

- Google Generative AI (Gemini Pro)
- Yahoo Finance (yfinance)
- Streamlit
- Plotly
- Pandas & NumPy

**ZMtech Analysis Platform** - Professional equity research at your fingertips 📊
