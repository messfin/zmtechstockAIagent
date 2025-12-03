import pandas as pd
import talib
import mplfinance as mpf
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

# Sample Data
dates = [datetime(2024, 3, i+1) for i in range(10)]
open_prices  = [100, 102, 105, 107, 106, 108, 110, 111, 109, 108]
high_prices  = [103, 106, 108, 109, 108, 110, 113, 114, 110, 109]
low_prices   = [99, 101, 104, 106, 105, 107, 109, 110, 107, 106]
close_prices = [102, 105, 107, 106, 108, 109, 112, 109, 108, 107]

# Create DataFrame
df = pd.DataFrame({'Date': dates, 'Open': open_prices, 'High': high_prices,
                   'Low': low_prices, 'Close': close_prices})
df.set_index('Date', inplace=True)

# Calculate Moving Averages
df['MA_50'] = df['Close'].rolling(window=5).mean()
df['MA_200'] = df['Close'].rolling(window=10).mean()

# Calculate RSI
def calculate_rsi(data, periods=14):
    delta = data.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=periods).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=periods).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

df['RSI'] = calculate_rsi(df['Close'], periods=14)

# Detect Doji and Hammer patterns
df['Doji'] = talib.CDLDOJI(df['Open'], df['High'], df['Low'], df['Close'])
df['Hammer'] = talib.CDLHAMMER(df['Open'], df['High'], df['Low'], df['Close'])

# Print detected patterns
detected_doji = df[df['Doji'] != 0].index
detected_hammer = df[df['Hammer'] != 0].index

print(f"Doji Candles Detected on: {list(detected_doji)}")
print(f"Hammer Candles Detected on: {list(detected_hammer)}")

# Create the figure
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), gridspec_kw={'height_ratios': [3, 1]})

# Prepare all addplots
apds = [
    mpf.make_addplot(df['MA_50'], color='blue', linestyle='dashed', ax=ax1),
    mpf.make_addplot(df['MA_200'], color='red', linestyle='dashed', ax=ax1)
]

# Add pattern markers
for idx in detected_doji:
    apds.append(mpf.make_addplot(df.loc[idx, 'Close'], scatter=True, markersize=100, marker='o', color='blue', ax=ax1))

for idx in detected_hammer:
    apds.append(mpf.make_addplot(df.loc[idx, 'Close'], scatter=True, markersize=100, marker='^', color='green', ax=ax1))

# Plot Candlestick Chart
mpf.plot(df, type='candle', style='charles',
         addplot=apds,
         ax=ax1,
         volume=False,
         ylabel='Price',
         show_nontrading=False)

# Add legend to first subplot
ax1.legend(['50-Day MA', '200-Day MA', 'Doji', 'Hammer'])
ax1.set_title("Candlestick Chart with Patterns and Moving Averages")

# Plot RSI Indicator on second subplot
ax2.plot(df.index, df['RSI'], label="RSI (14)", color="purple")
ax2.axhline(70, linestyle="dashed", color="red", label="Overbought (70)")
ax2.axhline(30, linestyle="dashed", color="green", label="Oversold (30)")
ax2.set_ylabel("RSI Value")
ax2.set_title("Relative Strength Index (RSI)")
ax2.legend()

# Add overall title
plt.suptitle("Technical Analysis Dashboard", y=0.95)

plt.tight_layout()
plt.show()
