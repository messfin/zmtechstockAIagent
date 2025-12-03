import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import yfinance as yf
from datetime import datetime, timedelta
import numpy as np
from statsmodels.tsa.statespace.sarimax import SARIMAX
import warnings
import base64
import os
import ntplib
from time import ctime, sleep

try:
    from curl_cffi import requests
    CURL_CFFI_AVAILABLE = True
except ImportError:
    CURL_CFFI_AVAILABLE = False

warnings.filterwarnings('ignore')

# Set page config
st.set_page_config(page_title="Advanced Stock Analysis", layout="wide")

@st.cache_resource
def get_yfinance_session():
    """Create a curl_cffi session with Chrome impersonation for yfinance"""
    if CURL_CFFI_AVAILABLE:
        try:
            session = requests.Session(impersonate="chrome")
            # Mark that curl-cffi is working (prevents showing the tip)
            if 'curl_cffi_working' not in st.session_state:
                st.session_state.curl_cffi_working = True
            return session
        except Exception as e:
            if 'curl_cffi_warning' not in st.session_state:
                st.warning(f"Failed to create curl_cffi session: {e}. Using default requests.")
                st.session_state.curl_cffi_warning = True
            return None
    else:
        # Only show tip if curl-cffi is not available AND we haven't shown it yet
        # AND curl-cffi is not marked as working
        if 'curl_cffi_working' not in st.session_state and 'curl_cffi_info' not in st.session_state:
            st.info("💡 Tip: Install curl-cffi for better rate limit handling: `pip install curl-cffi`")
            st.session_state.curl_cffi_info = True
    return None

# Add custom CSS for CNBC-style finance theme
def add_bg_from_local():
    # Get the directory where your script is located
    current_dir = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(current_dir, "background_v2.png")
    
    try:
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
            
        st.markdown(
            f"""
            <style>
            /* CNBC-style dark finance theme */
            .stApp {{
                background: #000000;
                background-image: linear-gradient(rgba(0, 0, 0, 0.85), rgba(0, 0, 0, 0.85)), url(data:image/png;base64,{encoded_string});
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
                background-attachment: fixed;
            }}
            
            /* Main content containers */
            .main .block-container {{
                background-color: rgba(26, 26, 26, 0.95);
                padding: 2rem;
                border-radius: 8px;
            }}
            
            .element-container, .stMarkdown, .stDataFrame {{
                background-color: rgba(26, 26, 26, 0.9);
                padding: 1rem;
                border-radius: 8px;
                border: 1px solid rgba(255, 255, 255, 0.1);
            }}
            
            /* Text colors - CNBC style */
            h1, h2, h3, h4, h5, h6 {{
                color: #ffffff !important;
                font-family: 'Helvetica Neue', Arial, sans-serif;
                font-weight: 600;
            }}
            
            p, label, div, span {{
                color: #e0e0e0 !important;
            }}
            
            /* Sidebar styling */
            .css-1d391kg {{
                background-color: #1a1a1a;
            }}
            
            [data-testid="stSidebar"] {{
                background-color: #1a1a1a;
            }}
            
            [data-testid="stSidebar"] .css-1d391kg {{
                background-color: #1a1a1a;
            }}
            
            /* Buttons - CNBC blue */
            .stButton>button {{
                background-color: #0066cc;
                color: #ffffff;
                font-weight: 600;
                border-radius: 4px;
                border: none;
                padding: 0.5rem 1.5rem;
                transition: all 0.2s ease;
            }}
            
            .stButton>button:hover {{
                background-color: #0052a3;
                transform: translateY(-1px);
                box-shadow: 0 4px 8px rgba(0, 102, 204, 0.3);
            }}
            
            /* Input fields */
            .stTextInput>div>div>input {{
                background-color: rgba(26, 26, 26, 0.8);
                color: #ffffff;
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 4px;
            }}
            
            .stSelectbox>div>div>select {{
                background-color: rgba(26, 26, 26, 0.8);
                color: #ffffff;
                border: 1px solid rgba(255, 255, 255, 0.2);
            }}
            
            /* Metrics - CNBC style */
            [data-testid="stMetricValue"] {{
                color: #ffffff !important;
                font-weight: 700;
            }}
            
            [data-testid="stMetricLabel"] {{
                color: #b0b0b0 !important;
            }}
            
            /* Data tables */
            .stDataFrame {{
                background-color: rgba(26, 26, 26, 0.9);
            }}
            
            table {{
                color: #ffffff;
            }}
            
            /* Positive/negative colors */
            .positive {{
                color: #00ff00 !important;
            }}
            
            .negative {{
                color: #ff0000 !important;
            }}
            
            /* Streamlit widgets */
            .stSlider {{
                color: #ffffff;
            }}
            
            /* Markdown text */
            .stMarkdown {{
                color: #e0e0e0;
            }}
            
            /* Info boxes */
            .stInfo {{
                background-color: rgba(0, 102, 204, 0.2);
                border-left: 4px solid #0066cc;
            }}
            
            .stSuccess {{
                background-color: rgba(0, 255, 0, 0.1);
                border-left: 4px solid #00ff00;
            }}
            
            .stError {{
                background-color: rgba(255, 0, 0, 0.1);
                border-left: 4px solid #ff0000;
            }}
            
            .stWarning {{
                background-color: rgba(255, 193, 7, 0.1);
                border-left: 4px solid #ffc107;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )
    except Exception as e:
        st.error(f"Error loading background image: {str(e)}")

# Call the function to set the background
add_bg_from_local()

def calculate_ema(data, period):
    return data['Close'].ewm(span=period, adjust=False).mean()

def calculate_vwap(df):
    # Reset index to handle date
    df = df.copy()  # Create a copy to avoid modifying original
    typical_price = (df['High'] + df['Low'] + df['Close']) / 3
    volume_price = typical_price * df['Volume']
    cumulative_volume = df['Volume'].cumsum()
    cumulative_volume_price = volume_price.cumsum()
    return cumulative_volume_price / cumulative_volume

def calculate_macd(data):
    exp1 = data['Close'].ewm(span=12, adjust=False).mean()
    exp2 = data['Close'].ewm(span=26, adjust=False).mean()
    macd = exp1 - exp2
    signal = macd.ewm(span=9, adjust=False).mean()
    return macd, signal

def calculate_rsi(data, periods=14):
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=periods).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=periods).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def generate_signals(df):
    """Generate buy and sell signals"""
    df = df.copy()
    
    # MACD Line crosses above Signal Line (Buy)
    df['Buy_Signal'] = ((df['MACD'] > df['Signal']) & 
                        (df['MACD'].shift(1) <= df['Signal'].shift(1)) & 
                        (df['RSI'] < 70)).astype(int)
    
    # MACD Line crosses below Signal Line (Sell)
    df['Sell_Signal'] = ((df['MACD'] < df['Signal']) & 
                         (df['MACD'].shift(1) >= df['Signal'].shift(1)) & 
                         (df['RSI'] > 30)).astype(int)
    
    return df

def calculate_heikin_ashi(df):
    """Calculate Heikin-Ashi candlestick data"""
    ha_close = (df['Open'] + df['High'] + df['Low'] + df['Close']) / 4
    
    # Initialize ha_open series with the first value
    ha_open = pd.Series([(df['Open'].iloc[0] + df['Close'].iloc[0]) / 2], index=[df.index[0]])
    
    # Calculate subsequent ha_open values
    for i in range(1, len(df)):
        next_value = pd.Series(
            [(ha_open.iloc[-1] + ha_close.iloc[i-1]) / 2],
            index=[df.index[i]]
        )
        ha_open = pd.concat([ha_open, next_value])
    
    ha_high = pd.concat([df['High'], ha_open, ha_close], axis=1).max(axis=1)
    ha_low = pd.concat([df['Low'], ha_open, ha_close], axis=1).min(axis=1)
    
    return pd.DataFrame({
        'HA_Open': ha_open,
        'HA_High': ha_high,
        'HA_Low': ha_low,
        'HA_Close': ha_close
    }, index=df.index)

def forecast_sarima(data, periods=30):
    """Generate SARIMA forecast"""
    model = SARIMAX(data['Close'], order=(1, 1, 1), seasonal_order=(1, 1, 1, 12))
    results = model.fit()
    forecast = results.forecast(steps=periods)
    return forecast

def _download_stock_data_internal(ticker, start_date, end_date):
    """Internal download function that can be cached"""
    session = get_yfinance_session()
    
    try:
        # Try Ticker.history() first as it's often more reliable
        if session:
            ticker_obj = yf.Ticker(ticker, session=session)
        else:
            ticker_obj = yf.Ticker(ticker)
        data = ticker_obj.history(start=start_date, end=end_date)
        
        if data is not None and not data.empty:
            # Fix MultiIndex columns
            if isinstance(data.columns, pd.MultiIndex):
                data.columns = data.columns.get_level_values(0)
            return data
        
        # Fallback to yf.download()
        if session:
            data = yf.download(
                ticker,
                start=start_date.strftime('%Y-%m-%d'),
                end=end_date.strftime('%Y-%m-%d'),
                progress=False,
                session=session
            )
        else:
            data = yf.download(
                ticker,
                start=start_date.strftime('%Y-%m-%d'),
                end=end_date.strftime('%Y-%m-%d'),
                progress=False
            )
        
        if data is not None and not data.empty:
            if isinstance(data.columns, pd.MultiIndex):
                data.columns = data.columns.get_level_values(0)
            return data
            
    except Exception:
        pass
    
    return None

@st.cache_data(ttl=300)  # Cache successful downloads for 5 minutes
def download_stock_data_cached(ticker, start_date, end_date):
    """Cached wrapper for stock data download - accepts date objects"""
    return _download_stock_data_internal(ticker, start_date, end_date)

def download_stock_data_with_retry(ticker, start_date, end_date, max_retries=5):
    """Download stock data with retry logic and fallback methods"""
    # First check cache (cache accepts date objects)
    cached_data = download_stock_data_cached(ticker, start_date, end_date)
    if cached_data is not None and not cached_data.empty:
        return cached_data
    
    # If not in cache, try downloading with retries
    session = get_yfinance_session()
    
    for attempt in range(max_retries):
        try:
            if attempt == 0:
                # First try: Use Ticker.history() method
                if session:
                    ticker_obj = yf.Ticker(ticker, session=session)
                else:
                    ticker_obj = yf.Ticker(ticker)
                data = ticker_obj.history(start=start_date, end=end_date)
            else:
                # Subsequent tries: Use yf.download() with longer waits
                wait_time = min(10 * attempt, 60)  # 10, 20, 30, 40, 50 seconds (capped at 60)
                if attempt > 1:
                    st.info(f"⏳ Waiting {wait_time} seconds before retry {attempt + 1}/{max_retries}...")
                    sleep(wait_time)
                
                if session:
                    data = yf.download(
                        ticker,
                        start=start_date.strftime('%Y-%m-%d'),
                        end=end_date.strftime('%Y-%m-%d'),
                        progress=False,
                        session=session
                    )
                else:
                    data = yf.download(
                        ticker,
                        start=start_date.strftime('%Y-%m-%d'),
                        end=end_date.strftime('%Y-%m-%d'),
                        progress=False
                    )
            
            # Check if we got valid data
            if data is not None and not data.empty:
                # Fix MultiIndex columns
                if isinstance(data.columns, pd.MultiIndex):
                    data.columns = data.columns.get_level_values(0)
                return data
                
        except Exception as e:
            error_str = str(e)
            if "Rate" in error_str or "rate" in error_str.lower() or "Too Many Requests" in error_str:
                if attempt < max_retries - 1:
                    wait_time = min(10 * (attempt + 1), 60)  # Longer waits
                    st.warning(f"⚠️ Rate limited by Yahoo Finance. Waiting {wait_time} seconds before retry {attempt + 2}/{max_retries}...")
                    sleep(wait_time)
                    continue
                else:
                    # Last attempt failed
                    st.error("❌ Unable to download data due to rate limiting.")
                    st.info("💡 **Suggestions:**")
                    st.info("1. Wait 1-2 minutes and refresh the page")
                    st.info("2. Yahoo Finance limits requests - try again in a few moments")
                    st.info("3. The rate limit is temporary and will reset shortly")
                    return None
            else:
                # For other errors, log and continue
                if attempt < max_retries - 1:
                    st.warning(f"Attempt {attempt + 1} failed: {error_str}. Retrying...")
                    sleep(3)
                    continue
                else:
                    st.error(f"Failed to download data: {error_str}")
                    return None
    
    # If all retries failed
    st.error("❌ All download attempts failed. Please try again in a few minutes.")
    return None

@st.cache_data
def load_stock_data(symbol, start, end):
    try:
        # Validate inputs
        if not symbol:
            st.error("Please enter a stock symbol")
            return None
            
        # Download data with explicit parameters and debug info
        st.write(f"Attempting to download data for {symbol} from {start} to {end}")
        df = yf.download(
            tickers=symbol,
            start=start,
            end=end,
            progress=False
        )
        
        # Fix MultiIndex columns by selecting the first level
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
        
        # Debug information
        st.write(f"Downloaded data shape: {df.shape if df is not None else 'None'}")
        
        # Check if data is empty or None
        if df is None or df.empty:
            st.error(f"No data found for symbol '{symbol}' in the selected date range")
            return None
            
        # Check if we have enough data for calculations
        if len(df) < 26:  # Minimum length needed for MACD
            st.error(f"Not enough data points for '{symbol}'. Please select a longer date range")
            return None

        # Reset index to handle date
        df = df.copy()  # Create a copy to avoid modifying original
        
        # Calculate technical indicators
        df['EMA9'] = calculate_ema(df, 9)
        df['EMA20'] = calculate_ema(df, 20)
        df['EMA50'] = calculate_ema(df, 50)  # Add 50 EMA
        df['EMA100'] = calculate_ema(df, 100)  # Add 100 EMA
        df['VWAP'] = calculate_vwap(df)
        macd, signal = calculate_macd(df)
        df['MACD'] = macd
        df['Signal'] = signal
        df['RSI'] = calculate_rsi(df)
        
        # Add Heikin-Ashi data
        ha_df = calculate_heikin_ashi(df)
        df = pd.concat([df, ha_df], axis=1)
        
        # Generate buy/sell signals
        df = generate_signals(df)
        
        # Verify all required columns exist
        required_columns = ['Open', 'High', 'Low', 'Close', 'Volume', 
                          'EMA9', 'EMA20', 'VWAP', 'MACD', 'Signal', 'RSI']
        for col in required_columns:
            if col not in df.columns:
                st.error(f"Missing required column: {col}")
                return None
        
        return df
        
    except Exception as e:
        st.error(f"Error loading data for '{symbol}': {str(e)}")
        st.write("Debug info:", e.__class__.__name__)
        st.write("Error details:", str(e))
        if isinstance(e, ValueError):
            st.write("Please check if the stock symbol is correct")
        return None

# Main content
st.title('Advanced Stock Analysis Dashboard')

# Date inputs with validation
today = datetime.today().date()  # Convert to date
min_date = today - timedelta(days=365*10)  # 10 years ago

# Debug output
st.write(f"Today's date: {today}")

# Sidebar inputs with additional validation
st.sidebar.header('User Input Parameters')
ticker = st.sidebar.text_input("Stock Symbol", "AAPL").upper().strip()

# Validate ticker
if not ticker:
    st.error("Please enter a stock symbol")
    st.stop()

# First date input
start_date = st.sidebar.date_input(
    "Start Date", 
    value=today - timedelta(days=365),  # Default to 1 year ago
    min_value=min_date,
    max_value=today
)

# Second date input with stricter validation
end_date = st.sidebar.date_input(
    "End Date", 
    value=min(today, start_date + timedelta(days=365)),  # Default to either today or 1 year from start
    min_value=start_date,
    max_value=today
)

# Additional validation
if end_date > today:
    st.error("End date cannot be in the future")
    st.stop()

# Load data with progress indicator
with st.spinner(f'Loading data for {ticker}...'):
    try:
        # Ensure end date is today or earlier
        download_end = min(end_date, today)
        
        # Add one day to end_date to include the last day in the range
        download_end = download_end + timedelta(days=1)
        
        data = download_stock_data_with_retry(
            ticker,
            start_date,
            download_end
        )
        
        # Check if data download was successful
        if data is None:
            st.error("Failed to download data. This may be due to rate limiting or network issues. Please try again in a few moments.")
            st.stop()
        
        # Verify no future dates in the data
        if not data.empty:
            last_valid_date = data.index.max().date()
            if last_valid_date > today:
                data = data[data.index.date <= today]
        
        if data.empty:
            st.error("No data available for the selected date range")
            st.stop()
        
        # Debug output
        st.write(f"Data date range: {data.index.min().date()} to {data.index.max().date()}")
        
        # Fix MultiIndex columns by selecting the first level
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.get_level_values(0)
        
        # Debug information
        st.write(f"Data shape: {data.shape}")
        st.write(f"Columns: {data.columns.tolist()}")
        
        # Reset index to handle date
        data = data.copy()  # Create a copy to avoid modifying original
        
        # Calculate indicators with error checking
        try:
            data['EMA9'] = calculate_ema(data, 9)
            data['EMA20'] = calculate_ema(data, 20)
            data['EMA50'] = calculate_ema(data, 50)
            data['EMA100'] = calculate_ema(data, 100)
            data['VWAP'] = calculate_vwap(data)
            macd, signal = calculate_macd(data)
            data['MACD'] = macd
            data['Signal'] = signal
            data['RSI'] = calculate_rsi(data)
            
            # Add Heikin-Ashi data
            ha_df = calculate_heikin_ashi(data)
            data = pd.concat([data, ha_df], axis=1)
            
            # Generate signals
            data = generate_signals(data)
            
        except KeyError as ke:
            st.error(f"Error calculating indicators: Missing column {ke}")
            st.write("Available columns:", data.columns.tolist())
            st.stop()
        except Exception as e:
            st.error(f"Error calculating indicators: {str(e)}")
            st.stop()
        
        # Verify we have all required columns
        required_columns = ['Open', 'High', 'Low', 'Close', 'Volume', 
                          'EMA9', 'EMA20', 'VWAP', 'MACD', 'Signal', 'RSI']
        missing_columns = [col for col in required_columns if col not in data.columns]
        
        if missing_columns:
            st.error(f"Missing required columns: {missing_columns}")
            st.write("Available columns:", data.columns.tolist())
            st.stop()
            
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        st.write("Debug info:", e.__class__.__name__)
        st.write("Full error:", str(e))
        st.stop()

if data is not None:
    # Add chart type selector
    chart_type = st.sidebar.selectbox(
        "Select Chart Type",
        ["Regular Candlestick", "Heikin-Ashi"]
    )
    
    # Add forecast option
    show_forecast = st.sidebar.checkbox("Show SARIMA Forecast")
    if show_forecast:
        forecast_periods = st.sidebar.slider("Forecast Periods", 5, 60, 30)
        forecast = forecast_sarima(data, periods=forecast_periods)

    # Create subplots
    fig = make_subplots(rows=4, cols=1, 
                        shared_xaxes=True,
                        vertical_spacing=0.05,
                        row_heights=[0.5, 0.15, 0.15, 0.15])

    # Main price chart (row 1)
    if chart_type == "Regular Candlestick":
        candlestick_data = dict(
            x=data.index,
            open=data['Open'],
            high=data['High'],
            low=data['Low'],
            close=data['Close'],
            name='Price'
        )
    else:  # Heikin-Ashi
        candlestick_data = dict(
            x=data.index,
            open=data['HA_Open'],
            high=data['HA_High'],
            low=data['HA_Low'],
            close=data['HA_Close'],
            name='Heikin-Ashi'
        )

    fig.add_trace(go.Candlestick(
        **candlestick_data,
        increasing_line_color='green',
        decreasing_line_color='red'
    ), row=1, col=1)

    # Add SARIMA forecast if enabled
    if show_forecast:
        fig.add_trace(go.Scatter(
            x=pd.date_range(start=data.index[-1], periods=len(forecast)+1)[1:],
            y=forecast,
            name='SARIMA Forecast',
            line=dict(color='orange', dash='dash'),
            hovertemplate='Forecast: %{y:.2f}<extra></extra>',
            showlegend=True,  # Explicitly set showlegend to True
            legendgroup='forecast'  # Add a legend group
        ), row=1, col=1)

    # Get real-time current price - Modified to handle errors gracefully
    try:
        session = get_yfinance_session()
        if session:
            current_data = yf.Ticker(ticker, session=session)
        else:
            current_data = yf.Ticker(ticker)
        current_price = current_data.info.get('regularMarketPrice')
        if current_price is None:
            current_price = data['Close'].iloc[-1]  # Use last closing price if real-time price unavailable
        
        # Create a line for current price
        fig.add_trace(go.Scatter(
            x=data.index,
            y=[current_price] * len(data.index),
            name='Current Price',
            line=dict(color='black', width=1, dash='solid'),
            hovertemplate=f'Current Price: ${current_price:.2f}<extra></extra>'
        ), row=1, col=1)

        # Add annotation for current price
        fig.add_annotation(
            x=data.index[-1],
            y=current_price,
            text=f'${current_price:.2f}',
            showarrow=False,
            yshift=10,
            xshift=50,
            font=dict(size=12, color='black'),
            row=1, col=1
        )
    except Exception as e:
        st.warning(f"Could not fetch real-time price: {str(e)}")
        current_price = data['Close'].iloc[-1]  # Use last closing price as fallback

    # Add EMAs
    fig.add_trace(go.Scatter(
        x=data.index,
        y=data['EMA9'],
        name='9 EMA',
        line=dict(color='blue', width=1),
        showlegend=True
    ), row=1, col=1)

    fig.add_trace(go.Scatter(
        x=data.index,
        y=data['EMA20'],
        name='20 EMA',
        line=dict(color='orange', width=1),
        showlegend=True
    ), row=1, col=1)

    fig.add_trace(go.Scatter(
        x=data.index,
        y=data['EMA50'],
        name='50 EMA',
        line=dict(color='purple', width=1),
        showlegend=True
    ), row=1, col=1)

    fig.add_trace(go.Scatter(
        x=data.index,
        y=data['EMA100'],
        name='100 EMA',
        line=dict(color='brown', width=1),
        showlegend=True
    ), row=1, col=1)

    fig.add_trace(go.Scatter(
        x=data.index,
        y=data['VWAP'],
        name='VWAP',
        line=dict(color='purple', width=1)
    ), row=1, col=1)

    # Get earnings dates
    try:
        earnings_dates = current_data.earnings_dates
        if earnings_dates is not None and not earnings_dates.empty:
            # Convert timezones to UTC for consistent comparison
            earnings_dates.index = earnings_dates.index.tz_localize(None)
            data.index = data.index.tz_localize(None)
            
            # Filter earnings dates within our date range
            earnings_dates = earnings_dates[
                (earnings_dates.index >= data.index[0]) & 
                (earnings_dates.index <= data.index[-1])
            ]
            
            # Add earnings markers
            if not earnings_dates.empty:
                fig.add_trace(go.Scatter(
                    x=earnings_dates.index,
                    y=[data['High'].max()] * len(earnings_dates),  # Place markers at top of chart
                    mode='markers+text',
                    marker=dict(
                        symbol='star',
                        size=12,
                        color='gold',
                        line=dict(color='black', width=1)
                    ),
                    text=['📊'] * len(earnings_dates),  # Earnings emoji
                    textposition='top center',
                    name='Earnings Dates',
                    hovertemplate='Earnings Date: %{x}<extra></extra>'
                ), row=1, col=1)

                # Add annotations for earnings dates
                for date in earnings_dates.index:
                    fig.add_annotation(
                        x=date,
                        y=data['High'].max(),
                        text='Earnings',
                        showarrow=True,
                        arrowhead=1,
                        arrowsize=1,
                        arrowwidth=2,
                        arrowcolor='gold',
                        font=dict(size=10, color='black'),
                        yshift=20,
                        row=1, col=1
                    )
    except Exception as e:
        st.warning(f"Could not load earnings dates: {str(e)}")

    # Add buy signals
    buy_mask = data['Buy_Signal'] == 1
    if buy_mask.any():
        buy_signals = data[buy_mask]
        fig.add_trace(go.Scatter(
            x=buy_signals.index,
            y=buy_signals['Low'] * 0.99,
            mode='markers+text',
            marker=dict(
                symbol='triangle-up',
                size=15,
                color='green',
                line=dict(width=2, color='darkgreen')
            ),
            text='BUY',
            textposition='bottom center',
            textfont=dict(size=12, color='green'),
            name='Buy Signal'
        ), row=1, col=1)

    # Add sell signals
    sell_mask = data['Sell_Signal'] == 1
    if sell_mask.any():
        sell_signals = data[sell_mask]
        fig.add_trace(go.Scatter(
            x=sell_signals.index,
            y=sell_signals['High'] * 1.01,
            mode='markers+text',
            marker=dict(
                symbol='triangle-down',
                size=15,
                color='red',
                line=dict(width=2, color='darkred')
            ),
            text='SELL',
            textposition='top center',
            textfont=dict(size=12, color='red'),
            name='Sell Signal'
        ), row=1, col=1)

    # Update the main chart y-axis
    fig.update_yaxes(title_text="Price", row=1, col=1)

    # Update layout to ensure legend is visible
    fig.update_layout(
        title=f'{ticker} Technical Analysis',
        yaxis_title="Price",
        height=800,
        showlegend=True,
        xaxis_rangeslider_visible=False,
        plot_bgcolor='white',
        paper_bgcolor='white',
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=1.01,
            bgcolor='rgba(255, 255, 255, 0.8)'  # Semi-transparent white background
        )
    )

    # Make sure candlesticks are visible
    fig.update_layout(
        yaxis=dict(
            autorange=True,
            fixedrange=False
        )
    )

    # Add Volume (row 2)
    colors = ['green' if close > open else 'red' 
             for close, open in zip(data['Close'], data['Open'])]
    
    fig.add_trace(go.Bar(
        x=data.index,
        y=data['Volume'],
        name='Volume',
        marker=dict(
            color=colors,
            line=dict(color=colors, width=1)
        )
    ), row=2, col=1)

    # Add volume moving average
    volume_ma = data['Volume'].rolling(window=20).mean()
    fig.add_trace(go.Scatter(
        x=data.index,
        y=volume_ma,
        name='Volume MA (20)',
        line=dict(color='blue', width=1)
    ), row=2, col=1)

    # MACD (row 3)
    fig.add_trace(go.Scatter(
        x=data.index,
        y=data['MACD'],
        name='MACD',
        line=dict(color='blue', width=1)
    ), row=3, col=1)

    fig.add_trace(go.Scatter(
        x=data.index,
        y=data['Signal'],
        name='Signal',
        line=dict(color='orange', width=1)
    ), row=3, col=1)

    # Add MACD histogram
    colors = ['red' if val < 0 else 'green' for val in data['MACD'] - data['Signal']]
    fig.add_trace(go.Bar(
        x=data.index,
        y=data['MACD'] - data['Signal'],
        marker_color=colors,
        name='MACD Histogram'
    ), row=3, col=1)

    # Add buy signals on MACD
    buy_mask = data['Buy_Signal'] == 1
    if buy_mask.any():
        buy_signals = data[buy_mask]
        fig.add_trace(go.Scatter(
            x=buy_signals.index,
            y=buy_signals['MACD'],
            mode='markers+text',
            marker=dict(
                symbol='triangle-up',
                size=12,
                color='green',
                line=dict(width=2, color='darkgreen')
            ),
            text='BUY',
            textposition='bottom center',
            textfont=dict(size=10, color='green'),
            name='MACD Buy',
            showlegend=False
        ), row=3, col=1)

    # Add sell signals on MACD
    sell_mask = data['Sell_Signal'] == 1
    if sell_mask.any():
        sell_signals = data[sell_mask]
        fig.add_trace(go.Scatter(
            x=sell_signals.index,
            y=sell_signals['MACD'],
            mode='markers+text',
            marker=dict(
                symbol='triangle-down',
                size=12,
                color='red',
                line=dict(width=2, color='darkred')
            ),
            text='SELL',
            textposition='top center',
            textfont=dict(size=10, color='red'),
            name='MACD Sell',
            showlegend=False
        ), row=3, col=1)

    # Add annotations for crossovers
    for idx, row in buy_signals.iterrows():
        fig.add_annotation(
            x=idx,
            y=row['MACD'],
            text='↑',
            showarrow=False,
            font=dict(size=14, color='green'),
            row=3, col=1
        )

    for idx, row in sell_signals.iterrows():
        fig.add_annotation(
            x=idx,
            y=row['MACD'],
            text='↓',
            showarrow=False,
            font=dict(size=14, color='red'),
            row=3, col=1
        )

    # RSI (row 4)
    fig.add_trace(go.Scatter(
        x=data.index,
        y=data['RSI'],
        name='RSI',
        line=dict(color='purple', width=1)
    ), row=4, col=1)

    # Add RSI buy signals
    if buy_mask.any():
        fig.add_trace(go.Scatter(
            x=buy_signals.index,
            y=buy_signals['RSI'],
            mode='markers',
            marker=dict(
                symbol='triangle-up',
                size=8,
                color='green',
                line=dict(width=1, color='darkgreen')
            ),
            name='RSI Buy',
            showlegend=False
        ), row=4, col=1)

    # Add RSI sell signals
    if sell_mask.any():
        fig.add_trace(go.Scatter(
            x=sell_signals.index,
            y=sell_signals['RSI'],
            mode='markers',
            marker=dict(
                symbol='triangle-down',
                size=8,
                color='red',
                line=dict(width=1, color='darkred')
            ),
            name='RSI Sell',
            showlegend=False
        ), row=4, col=1)

    # Add RSI levels
    fig.add_shape(
        type='line',
        x0=data.index[0],
        x1=data.index[-1],
        y0=70,
        y1=70,
        line=dict(color='red', width=1, dash='dash'),
        row=4,
        col=1
    )

    fig.add_shape(
        type='line',
        x0=data.index[0],
        x1=data.index[-1],
        y0=30,
        y1=30,
        line=dict(color='green', width=1, dash='dash'),
        row=4,
        col=1
    )

    # Update RSI axis range
    fig.update_yaxes(range=[0, 100], row=4, col=1)

    # Update layout
    fig.update_layout(
        title=f'{ticker} Technical Analysis',
        xaxis_title="Date",
        height=1000,  # Increased height
        showlegend=True,
        xaxis_rangeslider_visible=False,
        plot_bgcolor='white',
        paper_bgcolor='white'
    )

    # Update y-axes grid lines
    fig.update_yaxes(
        gridcolor='lightgrey',
        gridwidth=0.1,
        zerolinecolor='lightgrey',
        zerolinewidth=1
    )

    # Update x-axes grid lines
    fig.update_xaxes(
        gridcolor='lightgrey',
        gridwidth=0.1,
        zerolinecolor='lightgrey',
        zerolinewidth=1
    )

    # Update y-axis labels
    fig.update_yaxes(title_text="Price", row=1, col=1)
    fig.update_yaxes(title_text="Volume", row=2, col=1)
    fig.update_yaxes(title_text="MACD", row=3, col=1)
    fig.update_yaxes(title_text="RSI", row=4, col=1)

    # Display the plot
    st.plotly_chart(fig, use_container_width=True)

    # Statistics and Analysis
    st.subheader('Technical Indicators Summary')
    col1, col2, col3 = st.columns(3)
    
    with col1:
        current_rsi = float(data['RSI'].iloc[-1])
        st.metric("RSI", f"{current_rsi:.2f}", 
                 "Overbought > 70, Oversold < 30")
    
    with col2:
        current_macd = float(data['MACD'].iloc[-1])
        current_signal = float(data['Signal'].iloc[-1])
        macd_signal = "Bullish" if current_macd > current_signal else "Bearish"
        st.metric("MACD Signal", macd_signal)
    
    with col3:
        current_close = float(data['Close'].iloc[-1])
        current_ema = float(data['EMA20'].iloc[-1])
        trend = "Bullish" if current_close > current_ema else "Bearish"
        st.metric("Trend (20 EMA)", trend)

    # Add strategy performance metrics
    st.subheader('Strategy Performance Metrics')
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Buy Signals", len(data[data['Buy_Signal'] == 1]))
    
    with col2:
        st.metric("Total Sell Signals", len(data[data['Sell_Signal'] == 1]))
    
    with col3:
        vwap_position = "Above VWAP" if data['Close'].iloc[-1] > data['VWAP'].iloc[-1] else "Below VWAP"
        st.metric("VWAP Position", vwap_position)
    
    with col4:
        ha_trend = "Bullish" if data['HA_Close'].iloc[-1] > data['HA_Open'].iloc[-1] else "Bearish"
        st.metric("Heikin-Ashi Trend", ha_trend)

    # Export data option
    if st.button('Export Data to CSV'):
        csv = data.to_csv()
        st.download_button(
            label="Download Data",
            data=csv,
            file_name=f'{ticker}_technical_analysis.csv',
            mime='text/csv'
        )
else:
    st.error("No data available for the selected stock symbol and date range.")