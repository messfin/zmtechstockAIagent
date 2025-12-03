# 🚀 Setup Guide for ZMtech Stock Analysis Platform

## Overview

This unified platform combines advanced technical analysis with AI-powered equity research in one application.

## 📋 Prerequisites

- Python 3.8 or higher
- pip package manager
- Google AI API key (FREE)

## ⚡ Quick Setup (5 Minutes)

### Step 1: Install Dependencies

```powershell
pip install -r requirements.txt
```

### Step 2: Get Your Google AI API Key (FREE)

1. Visit: https://makersuite.google.com/app/apikey
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the key (starts with "AIza...")

### Step 3: Configure API Key

**Choose ONE of the following methods:**

#### Option A: Streamlit Secrets (Recommended for Production)

1. Edit `.streamlit/secrets.toml`
2. Replace the placeholder with your actual API key:
   ```toml
   GOOGLE_API_KEY = "AIza...your-actual-api-key"
   ```
3. Save the file

#### Option B: Environment File (Recommended for Development)

1. Copy the template:

   ```powershell
   copy .env.example .env
   ```

2. Edit `.env` and add your key:

   ```
   GOOGLE_API_KEY=AIza...your-actual-api-key
   ```

3. Save the file

#### Option C: PowerShell Environment Variable (Quick Test)

```powershell
$env:GOOGLE_API_KEY="AIza...your-actual-api-key"
```

**Note:** This only works for the current PowerShell session

### Step 4: Run the Application

```powershell
streamlit run main.py
```

The app will open in your default browser at `http://localhost:8501`

## 🎯 Usage

### Analysis Modes

The platform offers three analysis modes:

1. **Technical Analysis**

   - Advanced charting with candlesticks or Heikin-Ashi
   - 15+ technical indicators (RSI, MACD, EMAs, Bollinger Bands, etc.)
   - Buy/Sell signal detection
   - SARIMA price forecasting
   - Volume analysis

2. **AI-Powered Research**

   - Professional equity research reports
   - Buy/Hold/Sell recommendations with conviction levels
   - Investment thesis with professional terminology
   - Technical and fundamental analysis interpretation
   - Risk assessment
   - Price targets and trading strategy
   - Support/Resistance levels (ZMtech Analysis)

3. **Combined Analysis**
   - Both technical charts AND AI research report
   - Complete comprehensive view
   - Best for in-depth analysis

### Quick Start Guide

1. **Launch the app:** `streamlit run main.py`
2. **Select Analysis Mode** in the sidebar
3. **Enter stock ticker** (e.g., AAPL, TSLA, MSFT)
4. **Choose date range** for analysis
5. **Configure chart options** (if using Technical Analysis)
6. **Click "Generate Analysis"**
7. **Review results** - charts and/or AI report
8. **Download reports** if needed

## 📊 Features

### Technical Analysis Features

- Multiple chart types (Regular/Heikin-Ashi)
- Moving averages (EMA 9, 20, 50, 100, 200)
- VWAP (Volume Weighted Average Price)
- MACD with histogram
- RSI with overbought/oversold levels
- Volume analysis with moving average
- Buy/Sell signal detection
- SARIMA forecasting
- Interactive Plotly charts

### AI Research Features

- Institutional-quality research reports
- Clear Buy/Hold/Sell ratings
- High/Medium/Low conviction levels
- Professional financial terminology
- Technical indicator interpretation
- Fundamental metrics analysis
- Risk factor identification
- Price targets with timeframes
- Support/Resistance levels (R1-R3, S1-S3)
- Trading strategy recommendations
- Downloadable reports

## 🔐 Security & Configuration

### API Key Priority Order

The app checks for API keys in this priority:

1. **Streamlit secrets** (`.streamlit/secrets.toml`)
2. **Environment variables** (`.env` file or system)
3. **User input** (sidebar in the app)

### Protecting Your Secrets

✅ **Included in .gitignore:**

- `.streamlit/secrets.toml`
- `.env`
- All generated reports
- Python cache files

✅ **Safe to commit:**

- `.streamlit/secrets.toml` (template with placeholder)
- `.env.example` (template)
- `.gitignore` (protection file)
- All source code

### Best Practices

- ✅ Never commit actual API keys to version control
- ✅ Use `.streamlit/secrets.toml` for Streamlit Cloud deployment
- ✅ Use `.env` for local development
- ✅ Keep `.gitignore` up to date
- ✅ Rotate API keys if compromised
- ✅ Don't share your secrets files

## 🔧 Troubleshooting

### "API key not found" error

- Check that you've added your key to `.streamlit/secrets.toml` or `.env`
- Verify the key is correct (starts with "AIza...")
- Make sure you saved the file after editing
- Restart the Streamlit app

### "No module named..." error

```powershell
pip install -r requirements.txt
```

### "Invalid ticker symbol" error

- Verify the ticker is correct
- Check that it's traded on supported exchanges
- Try a different ticker to test

### Slow AI generation

- Normal! AI analysis takes 30-60 seconds
- Be patient during "Generating AI analysis..."
- First run may be slower

### Data download errors

- Yahoo Finance may rate limit
- Wait 1-2 minutes and try again
- Try a different date range
- Check your internet connection

## 📁 File Structure

```
d:\sa -AI\
├── main.py                      ← Main combined application
├── full_analysis.py             ← AI analysis engine
├── requirements.txt             ← Python dependencies
├── .gitignore                   ← Git protection
├── .env.example                 ← Environment template
├── .streamlit/
│   └── secrets.toml            ← Streamlit secrets (add your key)
└── Documentation files...
```

## 🌐 Deployment

### Local Deployment

```powershell
streamlit run main.py
```

### Streamlit Cloud Deployment

1. Push code to GitHub (secrets won't be committed due to .gitignore)
2. Go to https://share.streamlit.io
3. Connect your GitHub repo
4. In Streamlit Cloud settings, add secrets:
   ```
   GOOGLE_API_KEY = "your-key"
   ```
5. Deploy!

### Docker Deployment

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "main.py", "--server.port=8501"]
```

## 📚 Documentation

- **SETUP_GUIDE.md** (this file) - Setup instructions
- **QUICK_REFERENCE.md** - Quick commands and snippets
- **AI_ANALYSIS_README.md** - AI features documentation
- **ARCHITECTURE.md** - Technical architecture
- **IMPLEMENTATION_SUMMARY.md** - Complete features overview

## 💡 Tips

### Make API Key Permanent (PowerShell)

Add to your PowerShell profile:

```powershell
# Edit profile
notepad $PROFILE

# Add this line:
$env:GOOGLE_API_KEY="your-api-key"

# Save and restart PowerShell
```

### Create Watchlist

Create a file `my_stocks.txt`:

```
AAPL
GOOGL
MSFT
TSLA
NVDA
```

Then analyze them in batch mode!

### Keyboard Shortcuts in App

- **Ctrl + R** - Refresh/reload
- **Ctrl + Click** on chart - Open in new window
- **Scroll** - Zoom charts

## ⚠️ Important Notes

### Not Financial Advice

This platform is for **educational and informational purposes only**. It does not constitute investment advice. Always:

- Perform your own due diligence
- Consult licensed financial professionals
- Understand the risks involved
- Verify data from multiple sources

### Rate Limits

- Yahoo Finance: May rate limit if too many requests
- Google AI: Free tier has usage limits
- Wait between requests if rate limited

### Data Accuracy

- Data from Yahoo Finance may have delays
- Technical indicators are historical (lagging)
- AI analysis is interpretive, not deterministic
- Always cross-reference important data

## 🆘 Getting Help

### Check in Order:

1. Error message (read carefully!)
2. This setup guide
3. QUICK_REFERENCE.md for commands
4. AI_ANALYSIS_README.md for features
5. ARCHITECTURE.md for technical details

### Common Solutions

| Problem          | Solution                                   |
| ---------------- | ------------------------------------------ |
| API key error    | Add to `.streamlit/secrets.toml` or `.env` |
| Module not found | Run `pip install -r requirements.txt`      |
| Invalid ticker   | Verify ticker symbol is correct            |
| Slow generation  | Normal, AI takes 30-60s                    |
| Rate limited     | Wait 1-2 minutes and retry                 |

## ✅ Verification Checklist

Before first run:

- [ ] Python 3.8+ installed
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Google AI API key obtained
- [ ] API key added to `.streamlit/secrets.toml` OR `.env`
- [ ] File saved
- [ ] In correct directory (`d:\sa -AI`)

Test run:

- [ ] `streamlit run main.py` executes without errors
- [ ] App opens in browser
- [ ] API key detected (green checkmark in sidebar)
- [ ] Can enter ticker and see quick metrics
- [ ] Can generate technical analysis
- [ ] Can generate AI research report
- [ ] Can download reports

## 🎉 You're Ready!

Run the app:

```powershell
streamlit run main.py
```

Enjoy professional stock analysis! 📊🚀

---

**ZMtech Stock Analysis Platform**
_Where Technical Analysis Meets Artificial Intelligence_

For questions or issues, review the documentation files in the project directory.
