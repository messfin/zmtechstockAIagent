"""
Full Stock Analysis Module using Google Generative AI
Generates comprehensive analytical reports with Buy/Sell signals
"""

import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import google.generativeai as genai
import json
import os
from typing import Dict, Any, Optional


class FullStockAnalyzer:
    """
    Comprehensive stock analyzer that combines Yahoo Finance data
    with Google Generative AI for professional equity research reports.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the analyzer with Google AI API key.
        
        Args:
            api_key: Google AI API key (if None, reads from environment variable GOOGLE_API_KEY)
        """
        self.api_key = api_key or os.getenv('GOOGLE_API_KEY')
        if not self.api_key:
            raise ValueError("Google API key is required. Set GOOGLE_API_KEY environment variable or pass it directly.")
        
        genai.configure(api_key=self.api_key)
        # Updated to use available Gemini 2.0 Flash model
        self.model = genai.GenerativeModel('gemini-2.0-flash')
        
    def fetch_stock_data(self, ticker: str, period: str = "1y") -> Dict[str, Any]:
        """
        Fetch comprehensive stock data from Yahoo Finance.
        
        Args:
            ticker: Stock ticker symbol
            period: Time period (e.g., "1y", "6mo", "3mo")
            
        Returns:
            Dictionary containing stock data and metrics
        """
        try:
            stock = yf.Ticker(ticker)
            
            # Get historical price data
            hist = stock.history(period=period)
            
            # Get stock info
            info = stock.info
            
            # Calculate technical indicators
            data = self._calculate_indicators(hist)
            
            # Get fundamental data
            fundamentals = self._extract_fundamentals(info)
            
            # Get recent price action
            current_price = data['Close'].iloc[-1]
            prev_close = data['Close'].iloc[-2] if len(data) > 1 else current_price
            price_change = ((current_price - prev_close) / prev_close) * 100
            
            # Calculate support and resistance levels
            support_resistance = self._calculate_support_resistance(data)
            
            return {
                'ticker': ticker,
                'current_price': float(current_price),
                'price_change': float(price_change),
                'historical_data': data,
                'fundamentals': fundamentals,
                'support_resistance': support_resistance,
                'technical_indicators': self._get_latest_indicators(data),
                'volume_analysis': self._analyze_volume(data),
                'trend_analysis': self._analyze_trend(data)
            }
            
        except Exception as e:
            raise Exception(f"Error fetching data for {ticker}: {str(e)}")
    
    def _calculate_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calculate technical indicators."""
        data = df.copy()
        
        # Moving Averages
        data['EMA9'] = data['Close'].ewm(span=9, adjust=False).mean()
        data['EMA20'] = data['Close'].ewm(span=20, adjust=False).mean()
        data['EMA50'] = data['Close'].ewm(span=50, adjust=False).mean()
        data['EMA200'] = data['Close'].ewm(span=200, adjust=False).mean()
        data['SMA20'] = data['Close'].rolling(window=20).mean()
        data['SMA50'] = data['Close'].rolling(window=50).mean()
        
        # MACD
        exp1 = data['Close'].ewm(span=12, adjust=False).mean()
        exp2 = data['Close'].ewm(span=26, adjust=False).mean()
        data['MACD'] = exp1 - exp2
        data['Signal_Line'] = data['MACD'].ewm(span=9, adjust=False).mean()
        data['MACD_Histogram'] = data['MACD'] - data['Signal_Line']
        
        # RSI
        delta = data['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        data['RSI'] = 100 - (100 / (1 + rs))
        
        # Bollinger Bands
        data['BB_Middle'] = data['Close'].rolling(window=20).mean()
        bb_std = data['Close'].rolling(window=20).std()
        data['BB_Upper'] = data['BB_Middle'] + (bb_std * 2)
        data['BB_Lower'] = data['BB_Middle'] - (bb_std * 2)
        
        # ATR (Average True Range)
        high_low = data['High'] - data['Low']
        high_close = np.abs(data['High'] - data['Close'].shift())
        low_close = np.abs(data['Low'] - data['Close'].shift())
        ranges = pd.concat([high_low, high_close, low_close], axis=1)
        true_range = np.max(ranges, axis=1)
        data['ATR'] = true_range.rolling(14).mean()
        
        # Stochastic Oscillator
        low_14 = data['Low'].rolling(window=14).min()
        high_14 = data['High'].rolling(window=14).max()
        data['%K'] = 100 * ((data['Close'] - low_14) / (high_14 - low_14))
        data['%D'] = data['%K'].rolling(window=3).mean()
        
        return data
    
    def _extract_fundamentals(self, info: dict) -> Dict[str, Any]:
        """Extract key fundamental metrics."""
        return {
            'market_cap': info.get('marketCap', 'N/A'),
            'pe_ratio': info.get('trailingPE', 'N/A'),
            'forward_pe': info.get('forwardPE', 'N/A'),
            'peg_ratio': info.get('pegRatio', 'N/A'),
            'price_to_book': info.get('priceToBook', 'N/A'),
            'dividend_yield': info.get('dividendYield', 'N/A'),
            'beta': info.get('beta', 'N/A'),
            'earnings_growth': info.get('earningsQuarterlyGrowth', 'N/A'),
            'revenue_growth': info.get('revenueGrowth', 'N/A'),
            'profit_margin': info.get('profitMargins', 'N/A'),
            'debt_to_equity': info.get('debtToEquity', 'N/A'),
            'current_ratio': info.get('currentRatio', 'N/A'),
            '52w_high': info.get('fiftyTwoWeekHigh', 'N/A'),
            '52w_low': info.get('fiftyTwoWeekLow', 'N/A'),
            'avg_volume': info.get('averageVolume', 'N/A'),
            'sector': info.get('sector', 'N/A'),
            'industry': info.get('industry', 'N/A')
        }
    
    def _calculate_support_resistance(self, data: pd.DataFrame) -> Dict[str, float]:
        """Calculate support and resistance levels."""
        recent_data = data.tail(60)  # Last 60 days
        
        # Use pivot points
        high = recent_data['High'].max()
        low = recent_data['Low'].min()
        close = data['Close'].iloc[-1]
        
        pivot = (high + low + close) / 3
        
        r1 = 2 * pivot - low
        r2 = pivot + (high - low)
        r3 = high + 2 * (pivot - low)
        
        s1 = 2 * pivot - high
        s2 = pivot - (high - low)
        s3 = low - 2 * (high - pivot)
        
        return {
            'resistance_1': float(r1),
            'resistance_2': float(r2),
            'resistance_3': float(r3),
            'support_1': float(s1),
            'support_2': float(s2),
            'support_3': float(s3),
            'pivot': float(pivot),
            '52w_high': float(recent_data['High'].max()),
            '52w_low': float(recent_data['Low'].min())
        }
    
    def _get_latest_indicators(self, data: pd.DataFrame) -> Dict[str, float]:
        """Get the latest values of technical indicators."""
        latest = data.iloc[-1]
        return {
            'rsi': float(latest['RSI']),
            'macd': float(latest['MACD']),
            'macd_signal': float(latest['Signal_Line']),
            'macd_histogram': float(latest['MACD_Histogram']),
            'ema9': float(latest['EMA9']),
            'ema20': float(latest['EMA20']),
            'ema50': float(latest['EMA50']),
            'ema200': float(latest['EMA200']),
            'bb_upper': float(latest['BB_Upper']),
            'bb_middle': float(latest['BB_Middle']),
            'bb_lower': float(latest['BB_Lower']),
            'atr': float(latest['ATR']),
            'stoch_k': float(latest['%K']),
            'stoch_d': float(latest['%D'])
        }
    
    def _analyze_volume(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Analyze volume patterns."""
        recent = data.tail(20)
        avg_volume = recent['Volume'].mean()
        current_volume = data['Volume'].iloc[-1]
        volume_ratio = current_volume / avg_volume if avg_volume > 0 else 1
        
        return {
            'current_volume': float(current_volume),
            'avg_volume_20d': float(avg_volume),
            'volume_ratio': float(volume_ratio),
            'volume_trend': 'High' if volume_ratio > 1.5 else 'Normal' if volume_ratio > 0.7 else 'Low'
        }
    
    def _analyze_trend(self, data: pd.DataFrame) -> Dict[str, str]:
        """Analyze price trends."""
        current = data.iloc[-1]
        
        # Short-term trend (9 EMA vs 20 EMA)
        short_trend = 'Bullish' if current['EMA9'] > current['EMA20'] else 'Bearish'
        
        # Medium-term trend (20 EMA vs 50 EMA)
        medium_trend = 'Bullish' if current['EMA20'] > current['EMA50'] else 'Bearish'
        
        # Long-term trend (50 EMA vs 200 EMA)
        long_trend = 'Bullish' if current['EMA50'] > current['EMA200'] else 'Bearish'
        
        # Overall trend
        trends = [short_trend, medium_trend, long_trend]
        bullish_count = trends.count('Bullish')
        
        if bullish_count == 3:
            overall = 'Strong Bullish'
        elif bullish_count == 2:
            overall = 'Bullish'
        elif bullish_count == 1:
            overall = 'Bearish'
        else:
            overall = 'Strong Bearish'
        
        return {
            'short_term': short_trend,
            'medium_term': medium_trend,
            'long_term': long_trend,
            'overall': overall
        }
    
    def generate_analysis_report(self, stock_data: Dict[str, Any]) -> str:
        """
        Generate a comprehensive analytical report using Google Generative AI.
        
        Args:
            stock_data: Dictionary containing all stock data and metrics
            
        Returns:
            Formatted professional equity research report
        """
        
        # Prepare the data summary for the AI
        data_summary = self._prepare_data_summary(stock_data)
        
        # Create the prompt for the AI
        prompt = f"""
You are a senior equity research analyst at a top-tier investment bank. Your task is to analyze the following stock data and provide a comprehensive research note with a clear Buy/Hold/Sell recommendation.

STOCK DATA:
{data_summary}

INSTRUCTIONS:
1. Analyze all the technical and fundamental data provided
2. Provide a clear recommendation (BUY, HOLD, or SELL) with a conviction level (High/Medium/Low)
3. Use professional financial terminology (e.g., valuation compression, technical consolidation, risk-reward profile)
4. Structure your response EXACTLY as follows:

═══════════════════════════════════════════════════════════════
                    EQUITY RESEARCH NOTE
═══════════════════════════════════════════════════════════════

TICKER: {stock_data['ticker']}
CURRENT PRICE: ${stock_data['current_price']:.2f}
DATE: {datetime.now().strftime('%B %d, %Y')}

-------------------------------------------------------------------
I. RECOMMENDATION
-------------------------------------------------------------------
[Provide clear Buy/Hold/Sell rating with conviction level]

-------------------------------------------------------------------
II. INVESTMENT THESIS
-------------------------------------------------------------------
[Provide 3-5 paragraphs explaining:]
- Fundamental analysis and valuation assessment
- Technical setup and momentum indicators
- Key catalysts or risks
- Risk-reward profile at current levels

-------------------------------------------------------------------
III. TECHNICAL ANALYSIS
-------------------------------------------------------------------
[Analyze:]
- RSI conditions and what they indicate
- MACD signals and momentum
- Moving average alignment and trend strength
- Volume patterns and significance
- Bollinger Bands positioning

-------------------------------------------------------------------
IV. FUNDAMENTAL ASSESSMENT
-------------------------------------------------------------------
[Evaluate:]
- Valuation metrics (P/E, PEG, P/B ratios)
- Growth metrics and earnings trends
- Financial health indicators
- Sector positioning

-------------------------------------------------------------------
V. RISK FACTORS
-------------------------------------------------------------------
[Identify 3-5 key risks to the thesis]

-------------------------------------------------------------------
VI. PRICE TARGET & TIMELINE
-------------------------------------------------------------------
[Provide price target and expected timeframe]

-------------------------------------------------------------------
VII. ZMtech ANALYSIS - KEY LEVELS
-------------------------------------------------------------------
RESISTANCE LEVELS:
• R3 (Strong): $[value] - [brief explanation]
• R2 (Moderate): $[value] - [brief explanation]
• R1 (Immediate): $[value] - [brief explanation]

SUPPORT LEVELS:
• S1 (Immediate): $[value] - [brief explanation]
• S2 (Moderate): $[value] - [brief explanation]
• S3 (Strong): $[value] - [brief explanation]

PIVOT POINT: $[value]

TRADING STRATEGY:
[Provide specific entry, stop-loss, and target levels]

═══════════════════════════════════════════════════════════════

Remember to:
- Use specific numbers from the data
- Be authoritative and professional
- Provide actionable insights
- Justify your recommendation with concrete evidence
"""
        
        try:
            # Generate the report
            response = self.model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            raise Exception(f"Error generating AI analysis: {str(e)}")
    
    def _prepare_data_summary(self, stock_data: Dict[str, Any]) -> str:
        """Prepare a formatted summary of stock data for the AI."""
        
        summary = f"""
TICKER: {stock_data['ticker']}
CURRENT PRICE: ${stock_data['current_price']:.2f}
PRICE CHANGE (1D): {stock_data['price_change']:.2f}%

TECHNICAL INDICATORS:
- RSI (14): {stock_data['technical_indicators']['rsi']:.2f}
- MACD: {stock_data['technical_indicators']['macd']:.4f}
- MACD Signal: {stock_data['technical_indicators']['macd_signal']:.4f}
- MACD Histogram: {stock_data['technical_indicators']['macd_histogram']:.4f}
- EMA9: ${stock_data['technical_indicators']['ema9']:.2f}
- EMA20: ${stock_data['technical_indicators']['ema20']:.2f}
- EMA50: ${stock_data['technical_indicators']['ema50']:.2f}
- EMA200: ${stock_data['technical_indicators']['ema200']:.2f}
- Bollinger Upper: ${stock_data['technical_indicators']['bb_upper']:.2f}
- Bollinger Middle: ${stock_data['technical_indicators']['bb_middle']:.2f}
- Bollinger Lower: ${stock_data['technical_indicators']['bb_lower']:.2f}
- ATR: ${stock_data['technical_indicators']['atr']:.2f}
- Stochastic %K: {stock_data['technical_indicators']['stoch_k']:.2f}
- Stochastic %D: {stock_data['technical_indicators']['stoch_d']:.2f}

TREND ANALYSIS:
- Short-term: {stock_data['trend_analysis']['short_term']}
- Medium-term: {stock_data['trend_analysis']['medium_term']}
- Long-term: {stock_data['trend_analysis']['long_term']}
- Overall: {stock_data['trend_analysis']['overall']}

VOLUME ANALYSIS:
- Current Volume: {stock_data['volume_analysis']['current_volume']:,.0f}
- 20-Day Avg Volume: {stock_data['volume_analysis']['avg_volume_20d']:,.0f}
- Volume Ratio: {stock_data['volume_analysis']['volume_ratio']:.2f}x
- Volume Trend: {stock_data['volume_analysis']['volume_trend']}

SUPPORT & RESISTANCE LEVELS:
- Resistance 3: ${stock_data['support_resistance']['resistance_3']:.2f}
- Resistance 2: ${stock_data['support_resistance']['resistance_2']:.2f}
- Resistance 1: ${stock_data['support_resistance']['resistance_1']:.2f}
- Pivot Point: ${stock_data['support_resistance']['pivot']:.2f}
- Support 1: ${stock_data['support_resistance']['support_1']:.2f}
- Support 2: ${stock_data['support_resistance']['support_2']:.2f}
- Support 3: ${stock_data['support_resistance']['support_3']:.2f}

FUNDAMENTAL METRICS:
- Market Cap: {self._format_value(stock_data['fundamentals']['market_cap'])}
- P/E Ratio: {self._format_value(stock_data['fundamentals']['pe_ratio'])}
- Forward P/E: {self._format_value(stock_data['fundamentals']['forward_pe'])}
- PEG Ratio: {self._format_value(stock_data['fundamentals']['peg_ratio'])}
- Price/Book: {self._format_value(stock_data['fundamentals']['price_to_book'])}
- Dividend Yield: {self._format_value(stock_data['fundamentals']['dividend_yield'], is_percentage=True)}
- Beta: {self._format_value(stock_data['fundamentals']['beta'])}
- Earnings Growth: {self._format_value(stock_data['fundamentals']['earnings_growth'], is_percentage=True)}
- Revenue Growth: {self._format_value(stock_data['fundamentals']['revenue_growth'], is_percentage=True)}
- Profit Margin: {self._format_value(stock_data['fundamentals']['profit_margin'], is_percentage=True)}
- Debt/Equity: {self._format_value(stock_data['fundamentals']['debt_to_equity'])}
- Current Ratio: {self._format_value(stock_data['fundamentals']['current_ratio'])}
- 52W High: ${self._format_value(stock_data['fundamentals']['52w_high'])}
- 52W Low: ${self._format_value(stock_data['fundamentals']['52w_low'])}
- Sector: {stock_data['fundamentals']['sector']}
- Industry: {stock_data['fundamentals']['industry']}
"""
        return summary
    
    def _format_value(self, value, is_percentage: bool = False) -> str:
        """Format value for display."""
        if value == 'N/A' or value is None:
            return 'N/A'
        
        try:
            if is_percentage:
                return f"{float(value) * 100:.2f}%"
            elif isinstance(value, (int, float)):
                if value > 1_000_000_000:
                    return f"${value / 1_000_000_000:.2f}B"
                elif value > 1_000_000:
                    return f"${value / 1_000_000:.2f}M"
                else:
                    return f"{value:.2f}"
            else:
                return str(value)
        except:
            return str(value)
    
    def analyze_stock(self, ticker: str, period: str = "1y") -> str:
        """
        Main method to analyze a stock and generate a complete report.
        
        Args:
            ticker: Stock ticker symbol
            period: Time period for historical data
            
        Returns:
            Complete professional equity research report
        """
        print(f"Fetching data for {ticker}...")
        stock_data = self.fetch_stock_data(ticker, period)
        
        print("Generating AI-powered analysis...")
        report = self.generate_analysis_report(stock_data)
        
        return report


def main():
    """Example usage of the FullStockAnalyzer."""
    # Initialize the analyzer (make sure GOOGLE_API_KEY is set in environment)
    analyzer = FullStockAnalyzer()
    
    # Analyze a stock
    ticker = input("Enter stock ticker (e.g., AAPL): ").upper()
    
    try:
        report = analyzer.analyze_stock(ticker)
        print("\n" + "="*80)
        print(report)
        print("="*80)
        
        # Optionally save to file
        save = input("\nSave report to file? (y/n): ").lower()
        if save == 'y':
            filename = f"{ticker}_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"Report saved to {filename}")
            
    except Exception as e:
        print(f"Error: {str(e)}")


if __name__ == "__main__":
    main()
