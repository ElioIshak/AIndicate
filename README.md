# 📈 AI Stock/Crypto Indicator: AIndicate

---
**Project Name:** AI Stock/Crypto Indicator  
**Start Date:** May 2025  
**Last Updated:** June 2025  
**Author:** Elio (CS student at AUB)
---

AIndicate is an AI-powered indicator for analyzing and forecasting stock and cryptocurrency markets using machine learning with Python.  
It provides data-driven buy/sell/hold recommendations based on historical market data and a trained AI model, delivered through an interactive web app.

---

## ⭐ Features

- 📊 Multiple stock and crypto assets supported  
- ⌛ Real-time and historical analysis via Yahoo Finance  
- 🤖 AI-powered prediction engine using Random Forest  
- 📺 Interactive GUI built with Streamlit  
- 💰 Buy/Sell/Hold decision logic with confidence scoring  
- 📉 Price chart for the selected asset

---

## 🧠 My Inspiration

As a computer science student at the American University of Beirut, I’ve always admired the potential of artificial intelligence and the intricacies of the financial markets.

This project was born from my desire to combine both worlds — computer science and finance.  
During HarvardX's **CS109xa: Machine Learning and AI with Python** course, I was inspired to build a tool that could learn from market history and offer simple, actionable trading insights.

---

## 📖 My Journey

Before building this tool, I focused on gaining a solid understanding of machine learning.  
I completed the CS109xa course, then deepened my knowledge through additional reading, hands-on experimentation, and scikit-learn documentation.

Once I mastered decision trees and ensemble learning, I applied those skills to develop a real-world application:  
AIndicate — an AI model trained to forecast stock and crypto price movement.

This process helped me not only understand the theory behind ML models, but also how to apply and deploy them independently.

---

## 🔧 How the Indicator Works

1. **Data Collection**  
   Historical data is fetched from Yahoo Finance using the `yfinance` Python library.

2. **Feature Engineering**  
   - Daily return calculations  
   - Rolling return windows (up to 60 days)  
   - Labeling whether the next day's return is positive (UP) or not (DOWN)

3. **Model Training**  
   - Uses a `RandomForestClassifier` with 600 estimators and a max depth of 100  
   - Trained on 80% of the data, tested on the most recent 20%

4. **Prediction & Decision Logic**  
   - Predicts if tomorrow's price will go UP or DOWN  
   - If confidence ≥ 55%, suggests **Buy** or **Sell**  
   - Otherwise, it recommends **Hold**

---

## 📌 Features Used

AIndicate uses a diverse set of engineered features that help the AI model identify price trends, momentum, and market volatility:

1. Technical Indicators:

- RSI (Relative Strength Index): 
   **Measures recent price gains/losses to detect if an asset is overbought or oversold -> useful for spotting potential reversals.**

- SMA (Simple Moving Averages ~ 10-day and 30-day):
   **Smooth out price noise to capture overall trend direction.**

- SMA Crossover Signal:
   **Indicates bullish or bearish momentum when short-term and long-term SMAs cross —> widely used in trading strategies.**

- MACD & MACD Signal Line:
   **Capture momentum shifts by comparing short- and long-term EMAs —> helpful for detecting trend changes.**

- Stochastic RSI:
   **Increases the sensitivity of RSI by analyzing its own momentum —> highlights quick shifts in price strength.**

- EMA (Exponential Moving Average):
   **Averages price with more weight on recent data —> reacts faster to price movements than SMA.**

- Bollinger Bands (Upper, Lower, Width):
   **Measure volatility and potential price breakouts or pullbacks using dynamic price bands.**

2. Price & Volatility Features:

- Daily Return:
   **Measures daily percentage change in price —> forms the core signal for trend direction.**

- Volume:
   **Reflects trading activity —> spikes in volume often confirm the strength of price movements.**

- Open-to-Close Return (OC Return):
   **Captures intraday sentiment by comparing the day’s open and close prices.**

- Daily Range (High–Low / Close):
   **Reflects the strength of daily price movement —> useful for detecting strong market activity.**

- Rolling Standard Deviation (10-day):
   **Tracks recent volatility levels —> helps detect unstable or uncertain market periods.**

3. Lagged Historical Features (past 60 days):

- For each of the above metrics, past 60 days of values are included to allow the model to detect temporal patterns and trends — just like a trader would analyze historical charts to make decisions.

---

## 💻 GUI

A custom-built **Streamlit GUI** was developed to make the tool accessible via a modern browser interface.

### The GUI includes:

- A dropdown to select supported stocks and cryptocurrencies  
- A "Run Indicator" button to trigger model inference  
- Display of:
  - Buy/Sell/Hold recommendation
  - Prediction direction (UP/DOWN)
  - Model confidence
  - Model accuracy  
- A live line chart showing recent price movement

> This GUI was designed and implemented entirely by me to demonstrate practical deployment of machine learning in finance.

---

## 🧠 Smart Notification System

AIndicate supports a smart notification system that allows users to:

- Select specific stocks or crypto assets.
- Receive real-time alerts when the AI model generates strong Buy or Sell signals (with confidence ≥ 55%).
- Get recommendations by email.

> This feature aims to make the model's predictions actionable and user-centric.

---

## 🚀 Live Demo

Try the app live:  
👉 [Open App](https://aindicate.streamlit.app/)

---

## 🚧 Upcoming Work
  
- ✅ Hyperparameter tuning using RandomizedSearchCV to improve model performance and reliability
- 🕒 Support multiple timeframes (e.g. intraday, weekly trends) for more flexible analysis
- 🌍 Expand market coverage to include more global stocks, crypto assets, and financial instruments

---

## 📂 How to Run

1. Install the requirements:
    - pip install -r requirements.txt
2. Launch the program:
    - streamlit run AI_Stock_Indicator.py
    
---

## 📬 Contact

**Elio** – Computer Science student at AUB  
If you’re a recruiter or mentor interested in my work, feel free to reach out via [LinkedIn](https://www.linkedin.com/in/elio-ishak-b702a0330) or GitHub.

---

## ⚖️ License

This project is licensed under the **MIT License** © 2025 Elio Ishak.  
You are free to use, modify, and extend this code **with proper attribution**.  
However, redistribution or publication under your name without credit is **not permitted**.

Please see the [LICENSE](./LICENSE) file for full legal terms.

---
