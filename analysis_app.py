"""
Professional Stock Analysis Dashboard with AI-Powered Reports
Using Google Generative AI and Yahoo Finance Data
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime
import os
import re
from full_analysis import FullStockAnalyzer

# Try to import curl_cffi for better rate limit handling
try:
    from curl_cffi import requests
    CURL_CFFI_AVAILABLE = True
except ImportError:
    CURL_CFFI_AVAILABLE = False

# Page configuration
st.set_page_config(
    page_title="ZMtech AI Stock Analysis",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
    }
    .stApp {
        background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%);
    }
    h1, h2, h3 {
        color: #ffffff;
        font-family: 'Arial', sans-serif;
    }
    .stButton>button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: bold;
        border-radius: 10px;
        border: none;
        padding: 0.5rem 2rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.4);
    }
    .reportview-container {
        background: rgba(255,255,255,0.05);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 20px;
    }
    .metric-card {
        background: rgba(255,255,255,0.1);
        backdrop-filter: blur(10px);
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        border: 1px solid rgba(255,255,255,0.2);
    }
    .report-container {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        color: #ffffff;
        padding: 30px;
        border-radius: 15px;
        font-family: 'Courier New', monospace;
        box-shadow: 0 8px 32px rgba(0,0,0,0.5);
        border: 1px solid rgba(255,255,255,0.1);
        margin: 20px 0;
    }
    .sidebar .sidebar-content {
        background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
    }
    .stTextInput>div>div>input {
        background: rgba(255,255,255,0.1);
        color: white;
        border: 1px solid rgba(255,255,255,0.2);
        border-radius: 5px;
    }
    .stSelectbox>div>div>select {
        background: rgba(255,255,255,0.1);
        color: white;
        border: 1px solid rgba(255,255,255,0.2);
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

def format_report_text(report: str) -> str:
    """Format report text to highlight section headers"""
    # Format section headers with bold styling
    formatted = report
    
    # Format VI. PRICE TARGET & TIMELINE
    formatted = re.sub(
        r'(VI\.\s*PRICE TARGET\s*&\s*TIMELINE)',
        r'<strong style="color: #0066cc; font-size: 18px; font-weight: 700;">\1</strong>',
        formatted,
        flags=re.IGNORECASE
    )
    
    # Format VII. ZMtech ANALYSIS - KEY LEVELS
    formatted = re.sub(
        r'(VII\.\s*ZMtech\s*ANALYSIS\s*-\s*KEY\s*LEVELS)',
        r'<strong style="color: #0066cc; font-size: 18px; font-weight: 700;">\1</strong>',
        formatted,
        flags=re.IGNORECASE
    )
    
    # Format other section headers (I. through V.)
    formatted = re.sub(
        r'^([IVX]+\.\s+[A-Z][A-Z\s&]+)$',
        r'<strong style="color: #0066cc; font-size: 18px; font-weight: 700;">\1</strong>',
        formatted,
        flags=re.MULTILINE | re.IGNORECASE
    )
    
    return formatted

# Title and header
st.markdown("""
    <h1 style='text-align: center; font-size: 3em; margin-bottom: 0;'>
        📊 ZMtech AI Stock Analysis Platform
    </h1>
    <p style='text-align: center; color: #888; font-size: 1.2em; margin-top: 0;'>
        Professional Equity Research Powered by Google Generative AI
    </p>
""", unsafe_allow_html=True)

st.markdown("---")

# Sidebar configuration
with st.sidebar:
    st.markdown("### ⚙️ Configuration")
    
    # API Key input
    api_key = st.text_input(
        "Google AI API Key",
        type="password",
        value=os.getenv('GOOGLE_API_KEY', ''),
        help="Enter your Google AI API key or set GOOGLE_API_KEY environment variable"
    )
    
    st.markdown("---")
    
    # Stock selection
    st.markdown("### 📈 Stock Selection")
    ticker = st.text_input(
        "Stock Ticker",
        value="AAPL",
        help="Enter the stock ticker symbol (e.g., AAPL, TSLA, MSFT)"
    ).upper()
    
    period = st.selectbox(
        "Analysis Period",
        options=["1mo", "3mo", "6mo", "1y", "2y", "5y"],
        index=3,
        help="Select the historical data period"
    )
    
    st.markdown("---")
    
    # Analysis button
    analyze_button = st.button("🚀 Generate Analysis", use_container_width=True)
    
    st.markdown("---")
    
    # Information
    st.markdown("### ℹ️ About")
    st.info("""
    This platform combines:
    - **Yahoo Finance** real-time data
    - **Google Generative AI** analysis
    - **Professional** equity research format
    
    Features:
    - Buy/Sell/Hold recommendations
    - Technical & fundamental analysis
    - Support/resistance levels
    - Risk assessment
    - Price targets
    """)

# Main content area
if not api_key:
    st.warning("⚠️ Please enter your Google AI API key in the sidebar to proceed.")
    st.info("""
    **How to get a Google AI API Key:**
    1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
    2. Sign in with your Google account
    3. Click "Create API Key"
    4. Copy and paste it in the sidebar
    
    Alternatively, you can set it as an environment variable: `GOOGLE_API_KEY`
    """)
else:
    if analyze_button:
        try:
            with st.spinner(f"🔍 Analyzing {ticker}... This may take 30-60 seconds..."):
                # Initialize analyzer with curl_cffi session if available
                session = None
                if CURL_CFFI_AVAILABLE:
                    try:
                        session = requests.Session(impersonate="chrome")
                    except Exception:
                        session = None
                
                analyzer = FullStockAnalyzer(api_key=api_key, session=session)
                
                # Fetch stock data
                with st.status("Fetching market data...", expanded=True) as status:
                    st.write("📊 Retrieving historical data from Yahoo Finance...")
                    stock_data = analyzer.fetch_stock_data(ticker, period)
                    st.write("✅ Data retrieved successfully")
                    
                    st.write("🧮 Calculating technical indicators...")
                    st.write("✅ Technical analysis complete")
                    
                    st.write("🤖 Generating AI-powered analysis...")
                    report = analyzer.generate_analysis_report(stock_data)
                    st.write("✅ Analysis complete")
                    
                    status.update(label="✅ Analysis Complete!", state="complete", expanded=False)
                
                # Display key metrics
                st.markdown("### 📊 Quick Metrics")
                col1, col2, col3, col4, col5 = st.columns(5)
                
                with col1:
                    st.metric(
                        "Current Price",
                        f"${stock_data['current_price']:.2f}",
                        f"{stock_data['price_change']:.2f}%"
                    )
                
                with col2:
                    rsi = stock_data['technical_indicators']['rsi']
                    rsi_status = "🔴 Overbought" if rsi > 70 else "🟢 Oversold" if rsi < 30 else "🟡 Neutral"
                    st.metric("RSI (14)", f"{rsi:.1f}", rsi_status)
                
                with col3:
                    trend = stock_data['trend_analysis']['overall']
                    trend_emoji = "🟢" if "Bullish" in trend else "🔴"
                    st.metric("Trend", f"{trend_emoji} {trend}")
                
                with col4:
                    volume_trend = stock_data['volume_analysis']['volume_trend']
                    st.metric("Volume", volume_trend, f"{stock_data['volume_analysis']['volume_ratio']:.2f}x avg")
                
                with col5:
                    macd_signal = "🟢 Bullish" if stock_data['technical_indicators']['macd_histogram'] > 0 else "🔴 Bearish"
                    st.metric("MACD Signal", macd_signal)
                
                st.markdown("---")
                
                # Display the full report
                st.markdown("### 📑 Full Equity Research Report")
                
                # Format and display the report
                formatted_report = format_report_text(report)
                st.markdown(f"""
                <div class="report-container">
                    <div style="color: #ffffff; font-size: 14px; line-height: 1.6; white-space: pre-wrap; word-wrap: break-word; font-family: 'Courier New', monospace;">
{formatted_report}
                    </div>
                """, unsafe_allow_html=True)
                
                # Download button
                st.download_button(
                    label="📥 Download Report",
                    data=report,
                    file_name=f"{ticker}_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain"
                )
                
                # Technical chart
                st.markdown("### 📈 Technical Chart")
                
                # Create price chart
                fig = make_subplots(
                    rows=3, cols=1,
                    shared_xaxes=True,
                    vertical_spacing=0.05,
                    row_heights=[0.6, 0.2, 0.2],
                    subplot_titles=('Price & Moving Averages', 'Volume', 'RSI')
                )
                
                hist_data = stock_data['historical_data']
                
                # Candlestick chart
                fig.add_trace(
                    go.Candlestick(
                        x=hist_data.index,
                        open=hist_data['Open'],
                        high=hist_data['High'],
                        low=hist_data['Low'],
                        close=hist_data['Close'],
                        name='Price'
                    ),
                    row=1, col=1
                )
                
                # Add EMAs
                colors = {'EMA9': '#ffeb3b', 'EMA20': '#00bcd4', 'EMA50': '#ff9800', 'EMA200': '#f44336'}
                for ema in ['EMA9', 'EMA20', 'EMA50', 'EMA200']:
                    fig.add_trace(
                        go.Scatter(
                            x=hist_data.index,
                            y=hist_data[ema],
                            name=ema,
                            line=dict(color=colors[ema], width=1.5)
                        ),
                        row=1, col=1
                    )
                
                # Add Bollinger Bands
                fig.add_trace(
                    go.Scatter(
                        x=hist_data.index,
                        y=hist_data['BB_Upper'],
                        name='BB Upper',
                        line=dict(color='rgba(250,250,250,0.3)', width=1, dash='dash')
                    ),
                    row=1, col=1
                )
                
                fig.add_trace(
                    go.Scatter(
                        x=hist_data.index,
                        y=hist_data['BB_Lower'],
                        name='BB Lower',
                        line=dict(color='rgba(250,250,250,0.3)', width=1, dash='dash'),
                        fill='tonexty',
                        fillcolor='rgba(250,250,250,0.1)'
                    ),
                    row=1, col=1
                )
                
                # Volume
                colors_vol = ['red' if hist_data['Close'].iloc[i] < hist_data['Open'].iloc[i] else 'green' 
                             for i in range(len(hist_data))]
                fig.add_trace(
                    go.Bar(
                        x=hist_data.index,
                        y=hist_data['Volume'],
                        name='Volume',
                        marker_color=colors_vol,
                        opacity=0.7
                    ),
                    row=2, col=1
                )
                
                # RSI
                fig.add_trace(
                    go.Scatter(
                        x=hist_data.index,
                        y=hist_data['RSI'],
                        name='RSI',
                        line=dict(color='#9c27b0', width=2)
                    ),
                    row=3, col=1
                )
                
                # Add RSI levels
                fig.add_hline(y=70, line_dash="dash", line_color="red", opacity=0.5, row=3, col=1)
                fig.add_hline(y=30, line_dash="dash", line_color="green", opacity=0.5, row=3, col=1)
                fig.add_hline(y=50, line_dash="dot", line_color="gray", opacity=0.3, row=3, col=1)
                
                # Update layout
                fig.update_layout(
                    title=f"{ticker} Technical Analysis",
                    xaxis_title="Date",
                    template='plotly_dark',
                    height=900,
                    showlegend=True,
                    hovermode='x unified',
                    plot_bgcolor='rgba(0,0,0,0.3)',
                    paper_bgcolor='rgba(0,0,0,0.1)'
                )
                
                fig.update_xaxes(rangeslider_visible=False)
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Support and Resistance levels
                st.markdown("### 🎯 Key Price Levels")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("#### 🔴 Resistance Levels")
                    sr = stock_data['support_resistance']
                    st.markdown(f"""
                    - **R3 (Strong):** ${sr['resistance_3']:.2f}
                    - **R2 (Moderate):** ${sr['resistance_2']:.2f}
                    - **R1 (Immediate):** ${sr['resistance_1']:.2f}
                    """)
                
                with col2:
                    st.markdown("#### 🟢 Support Levels")
                    st.markdown(f"""
                    - **S1 (Immediate):** ${sr['support_1']:.2f}
                    - **S2 (Moderate):** ${sr['support_2']:.2f}
                    - **S3 (Strong):** ${sr['support_3']:.2f}
                    """)
                
                st.info(f"**Pivot Point:** ${sr['pivot']:.2f}")
                
        except Exception as e:
            st.error(f"❌ Error during analysis: {str(e)}")
            st.info("Please check your API key and ticker symbol, then try again.")
    
    else:
        # Welcome screen
        st.markdown("""
        <div style='text-align: center; padding: 50px;'>
            <h2>👈 Enter a stock ticker in the sidebar and click "Generate Analysis"</h2>
            <p style='font-size: 1.1em; color: #888; margin-top: 20px;'>
                Get professional equity research reports with:
            </p>
            <div style='display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin-top: 30px;'>
                <div class='metric-card'>
                    <h3>📊 Technical Analysis</h3>
                    <p>RSI, MACD, Moving Averages, Bollinger Bands, and more</p>
                </div>
                <div class='metric-card'>
                    <h3>💼 Fundamental Metrics</h3>
                    <p>P/E, PEG, Profit Margins, Growth Rates, Financial Health</p>
                </div>
                <div class='metric-card'>
                    <h3>🎯 Key Levels</h3>
                    <p>Support & Resistance zones, Pivot Points, Entry/Exit strategies</p>
                </div>
                <div class='metric-card'>
                    <h3>🤖 AI-Powered Insights</h3>
                    <p>Buy/Sell recommendations with conviction levels and price targets</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 20px;'>
    <p>⚡ Powered by Google Generative AI & Yahoo Finance | ZMtech Analysis Platform</p>
    <p style='font-size: 0.8em;'>Disclaimer: This is for informational purposes only. Not investment advice. Please consult a financial advisor.</p>
</div>
""", unsafe_allow_html=True)
