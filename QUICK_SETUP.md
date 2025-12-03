# Quick Setup Guide for AI Stock Analysis Platform

## 🚀 5-Minute Setup

### Step 1: Get Your Google AI API Key (FREE)

1. Visit: https://makersuite.google.com/app/apikey
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the key (starts with "AIza...")

### Step 2: Install Dependencies

Open PowerShell in this directory and run:

```powershell
pip install -r requirements.txt
```

### Step 3: Set Your API Key

**Option A: Quick Test (PowerShell)**

```powershell
$env:GOOGLE_API_KEY="your-api-key-here"
```

**Option B: Permanent Setup (Recommended)**

Create a file named `.env` in this directory with:

```
GOOGLE_API_KEY=your-api-key-here
```

### Step 4: Run the Application

**Web Interface (Recommended):**

```powershell
streamlit run analysis_app.py
```

**Command Line:**

```powershell
python example_usage.py
```

**Direct Analysis:**

```powershell
python full_analysis.py
```

## 📊 Quick Test

Test the installation with this one-liner:

```powershell
$env:GOOGLE_API_KEY="your-key"; python -c "from full_analysis import FullStockAnalyzer; print(FullStockAnalyzer().analyze_stock('AAPL'))"
```

## 🎯 What You Get

After setup, you can instantly generate professional equity research reports with:

✅ Buy/Hold/Sell recommendations
✅ Investment thesis and rationale  
✅ Technical indicator analysis (RSI, MACD, EMAs, etc.)
✅ Fundamental metrics (P/E, PEG, margins, growth)
✅ Support & resistance levels
✅ Risk assessment
✅ Price targets
✅ Trading strategy

## 🖥️ Using the Web Interface

The Streamlit web app (`analysis_app.py`) provides:

- 📊 Beautiful interactive charts
- 🎨 Professional dark theme UI
- 📈 Real-time price data
- 🤖 AI-generated research reports
- 💾 Download reports as files
- 🎯 Visual support/resistance levels

## 💡 Example Commands

### PowerShell Quick Analysis

```powershell
# Set API key for current session
$env:GOOGLE_API_KEY="your-api-key-here"

# Run web interface
streamlit run analysis_app.py

# Run examples
python example_usage.py

# Analyze specific stock
python -c "from full_analysis import FullStockAnalyzer; a = FullStockAnalyzer(); print(a.analyze_stock('TSLA', '6mo'))"
```

### Python Script

```python
from full_analysis import FullStockAnalyzer

# Initialize
analyzer = FullStockAnalyzer()

# Get full report
report = analyzer.analyze_stock("AAPL", period="1y")
print(report)

# Save to file
with open("AAPL_report.txt", "w") as f:
    f.write(report)
```

## 🔧 Troubleshooting

### "API key not found" error

- Make sure you set the environment variable
- Or enter it in the Streamlit sidebar
- Or create a `.env` file

### "Module not found" error

```powershell
pip install -r requirements.txt
```

### Slow performance

- First run is slower (AI initialization)
- Normal analysis takes 30-60 seconds
- Be patient during "Generating AI analysis..."

### Import errors

Make sure you're in the correct directory:

```powershell
cd "d:\sa -AI"
```

## 📖 Files Overview

- `full_analysis.py` - Core analysis engine with AI
- `analysis_app.py` - Streamlit web interface
- `example_usage.py` - Example scripts
- `AI_ANALYSIS_README.md` - Full documentation
- `requirements.txt` - Python dependencies

## 🎓 Learning the Platform

1. **Start with the web interface:** Most user-friendly

   ```powershell
   streamlit run analysis_app.py
   ```

2. **Try example script:** See various usage patterns

   ```powershell
   python example_usage.py
   ```

3. **Read full docs:** Check `AI_ANALYSIS_README.md`

4. **Customize:** Modify code to fit your needs

## ⚡ Pro Tips

1. **Save your API key permanently** in `.env` file
2. **Bookmark common stocks** for quick analysis
3. **Compare multiple timeframes** (3mo vs 1y)
4. **Download reports** for later reference
5. **Focus on the "ZMtech Analysis"** section for key levels

## 🎯 Next Steps

Once setup is complete:

1. Open the web app: `streamlit run analysis_app.py`
2. Enter your API key in the sidebar
3. Type a stock ticker (e.g., AAPL)
4. Click "Generate Analysis"
5. Review your professional equity research report!

## ⚠️ Important Notes

- **Free API limits:** Google AI has generous free tier
- **Rate limits:** Don't analyze hundreds of stocks in rapid succession
- **Not financial advice:** For educational purposes only
- **Data accuracy:** Yahoo Finance data has occasional issues

## 📞 Need Help?

1. Check `AI_ANALYSIS_README.md` for detailed docs
2. Review error messages carefully
3. Verify API key is correct
4. Ensure internet connection is stable

---

**Ready to analyze stocks like a professional equity analyst!** 🚀

Start with:

```powershell
streamlit run analysis_app.py
```
