"""
Example script demonstrating the AI Stock Analysis functionality
"""

import os
from full_analysis import FullStockAnalyzer
from datetime import datetime

def main():
    """
    Example usage of the FullStockAnalyzer with multiple stocks
    """
    
    print("=" * 80)
    print("ZMtech AI Stock Analysis - Example Usage")
    print("=" * 80)
    print()
    
    # Check for API key
    api_key = os.getenv('GOOGLE_API_KEY')
    
    if not api_key:
        print("❌ ERROR: Google API key not found!")
        print()
        print("Please set your GOOGLE_API_KEY environment variable:")
        print()
        print("Windows PowerShell:")
        print('  $env:GOOGLE_API_KEY="your-api-key-here"')
        print()
        print("Windows Command Prompt:")
        print('  set GOOGLE_API_KEY=your-api-key-here')
        print()
        print("Linux/Mac:")
        print('  export GOOGLE_API_KEY="your-api-key-here"')
        print()
        print("Or create a .env file with:")
        print("  GOOGLE_API_KEY=your-api-key-here")
        print()
        return
    
    # Initialize the analyzer
    print("🤖 Initializing AI Stock Analyzer...")
    try:
        analyzer = FullStockAnalyzer()
        print("✅ Analyzer initialized successfully")
        print()
    except Exception as e:
        print(f"❌ Error initializing analyzer: {e}")
        return
    
    # Example stocks to analyze
    stocks = ["AAPL", "TSLA", "MSFT"]
    
    print("=" * 80)
    print("EXAMPLE 1: Quick Analysis of Multiple Stocks")
    print("=" * 80)
    print()
    
    for ticker in stocks:
        print(f"📊 Analyzing {ticker}...")
        try:
            # Fetch data only (without full AI report)
            stock_data = analyzer.fetch_stock_data(ticker, period="6mo")
            
            # Display quick summary
            print(f"\n{ticker} Quick Summary:")
            print(f"  • Current Price: ${stock_data['current_price']:.2f}")
            print(f"  • 1D Change: {stock_data['price_change']:.2f}%")
            print(f"  • RSI: {stock_data['technical_indicators']['rsi']:.2f}")
            print(f"  • Trend: {stock_data['trend_analysis']['overall']}")
            print(f"  • Volume: {stock_data['volume_analysis']['volume_trend']}")
            print()
            
        except Exception as e:
            print(f"  ❌ Error analyzing {ticker}: {e}")
            print()
    
    print("=" * 80)
    print("EXAMPLE 2: Full AI-Powered Analysis Report")
    print("=" * 80)
    print()
    
    # Get user input for detailed analysis
    ticker = input("Enter a stock ticker for detailed analysis (or press Enter for AAPL): ").upper()
    if not ticker:
        ticker = "AAPL"
    
    period = input("Enter period (1mo/3mo/6mo/1y/2y/5y, default: 1y): ")
    if not period:
        period = "1y"
    
    print()
    print(f"🔍 Generating comprehensive AI analysis for {ticker}...")
    print("⏳ This may take 30-60 seconds...")
    print()
    
    try:
        # Generate full report
        report = analyzer.analyze_stock(ticker, period=period)
        
        # Display the report
        print("\n" + "=" * 80)
        print(report)
        print("=" * 80 + "\n")
        
        # Ask to save
        save = input("💾 Save report to file? (y/n): ").lower()
        if save == 'y':
            filename = f"{ticker}_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"✅ Report saved to: {filename}")
        
    except Exception as e:
        print(f"❌ Error generating report: {e}")
    
    print()
    print("=" * 80)
    print("EXAMPLE 3: Accessing Specific Data Points")
    print("=" * 80)
    print()
    
    try:
        print(f"📊 Fetching detailed data for {ticker}...")
        stock_data = analyzer.fetch_stock_data(ticker, period="1y")
        
        print(f"\n{ticker} - Detailed Technical Indicators:")
        print("-" * 60)
        ti = stock_data['technical_indicators']
        print(f"  RSI (14):           {ti['rsi']:.2f}")
        print(f"  MACD:               {ti['macd']:.4f}")
        print(f"  MACD Signal:        {ti['macd_signal']:.4f}")
        print(f"  MACD Histogram:     {ti['macd_histogram']:.4f}")
        print(f"  EMA 9:              ${ti['ema9']:.2f}")
        print(f"  EMA 20:             ${ti['ema20']:.2f}")
        print(f"  EMA 50:             ${ti['ema50']:.2f}")
        print(f"  EMA 200:            ${ti['ema200']:.2f}")
        print(f"  Bollinger Upper:    ${ti['bb_upper']:.2f}")
        print(f"  Bollinger Lower:    ${ti['bb_lower']:.2f}")
        print(f"  ATR:                ${ti['atr']:.2f}")
        print(f"  Stochastic %K:      {ti['stoch_k']:.2f}")
        print(f"  Stochastic %D:      {ti['stoch_d']:.2f}")
        
        print(f"\n{ticker} - Support & Resistance Levels:")
        print("-" * 60)
        sr = stock_data['support_resistance']
        print(f"  Resistance 3:       ${sr['resistance_3']:.2f}")
        print(f"  Resistance 2:       ${sr['resistance_2']:.2f}")
        print(f"  Resistance 1:       ${sr['resistance_1']:.2f}")
        print(f"  Pivot Point:        ${sr['pivot']:.2f}")
        print(f"  Support 1:          ${sr['support_1']:.2f}")
        print(f"  Support 2:          ${sr['support_2']:.2f}")
        print(f"  Support 3:          ${sr['support_3']:.2f}")
        
        print(f"\n{ticker} - Fundamental Metrics:")
        print("-" * 60)
        fund = stock_data['fundamentals']
        print(f"  Sector:             {fund['sector']}")
        print(f"  Industry:           {fund['industry']}")
        print(f"  P/E Ratio:          {fund['pe_ratio']}")
        print(f"  PEG Ratio:          {fund['peg_ratio']}")
        print(f"  Price/Book:         {fund['price_to_book']}")
        print(f"  Beta:               {fund['beta']}")
        print(f"  Profit Margin:      {fund['profit_margin']}")
        
        print(f"\n{ticker} - Volume Analysis:")
        print("-" * 60)
        vol = stock_data['volume_analysis']
        print(f"  Current Volume:     {vol['current_volume']:,.0f}")
        print(f"  Avg Volume (20D):   {vol['avg_volume_20d']:,.0f}")
        print(f"  Volume Ratio:       {vol['volume_ratio']:.2f}x")
        print(f"  Volume Trend:       {vol['volume_trend']}")
        
        print(f"\n{ticker} - Trend Analysis:")
        print("-" * 60)
        trend = stock_data['trend_analysis']
        print(f"  Short-term:         {trend['short_term']}")
        print(f"  Medium-term:        {trend['medium_term']}")
        print(f"  Long-term:          {trend['long_term']}")
        print(f"  Overall:            {trend['overall']}")
        
    except Exception as e:
        print(f"❌ Error fetching data: {e}")
    
    print()
    print("=" * 80)
    print("✅ Examples completed!")
    print("=" * 80)
    print()
    print("💡 Tip: Use the Streamlit app for a better visual experience:")
    print("   streamlit run analysis_app.py")
    print()


if __name__ == "__main__":
    main()
