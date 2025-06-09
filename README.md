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
- 📉 Live price chart for the selected asset

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
   - Rolling return windows (up to 30 days)  
   - Labeling whether the next day's return is positive (UP) or not (DOWN)

3. **Model Training**  
   - Uses a `RandomForestClassifier` with 600 estimators and a max depth of 100  
   - Trained on 80% of the data, tested on the most recent 20%

4. **Prediction & Decision Logic**  
   - Predicts if tomorrow's price will go UP or DOWN  
   - If confidence ≥ 55%, suggests **Buy** or **Sell**  
   - Otherwise, it recommends **Hold**

---

## 💻 GUI

A custom-built **Streamlit GUI** was developed to make the tool accessible via a modern browser interface.

### The GUI includes:

- A dropdown to select supported stocks and cryptocurrencies  
- An "Analyze" button to trigger model inference  
- Display of:
  - Selected asset name
  - Buy/Sell/Hold recommendation
  - Prediction direction (UP/DOWN)
  - Model confidence
  - Model accuracy  
- A live line chart showing recent price movement

> This GUI was designed and implemented entirely by me to demonstrate practical deployment of machine learning in finance.

---

## 🚀 Live Demo

*Coming soon*

---

## 🚧 Upcoming Work
  
- Support more timeframes
- Support more stocks, coins, and markets

---

## 📂 How to Run

1. Install the requirements:
    - pip install -r requirements.txt
2. Launch the program:
    - streamlit run AI_Stock_Indicator.py
    
---

## 📬 Contact

**Elio** – Computer Science student at AUB  
If you’re a recruiter or mentor interested in my work, feel free to reach out via [LinkedIn](www.linkedin.com/in/elio-ishak-b702a0330) or GitHub.

---