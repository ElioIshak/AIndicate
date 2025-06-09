import numpy as np                                        
import yfinance as yf                                      


import streamlit as st
from streamlit import image

from sklearn.ensemble import RandomForestClassifier         
from sklearn.model_selection import train_test_split
    
from sklearn.metrics import accuracy_score



# The supported stocks and crypto coins

supported_stocks_symbols =  ['AAPL','MSFT','AMZN','GOOGL','META','TSLA','NVDA',
                            'MC.PA','SAP.DE','SIE.DE','SHEL.L','ULVR.L','ASML.AS','ROG.SW',
                            'BTC-USD','ETH-USD','SOL-USD','DOGE-USD']

supported_stocks_names =    ["Apple Inc.","Microsoft Corporation","Amazon Inc.","Alphabet Inc. (Google)","Meta Platforms Inc.","Tesla Inc.","NVIDIA Corporation",
                            "LVMH Moët Hennessy Louis Vuitton SE","SAP SE","Siemens AG","Shell plc","Unilever plc","ASML Holding N.V.","Roche Holding AG",
                            "Bitcoin","Ethereum","Solana","Dogecoin"]



# The main indicator program function

def run_ai_indicator(symbol):
    
    # Instead of using a common start date for all assets, our indicator uses all the data possible for each asset individually

    data = yf.download(symbol, period='max')    # Download data from Yahoo Finance

    if data.empty:                                      # Checking if there is any available data for the specified asset
        print("No available data for "+symbol+".")
        return

    data['Return'] = data['Close'].pct_change()     # Creating a new column the data table (Return) that holds the percentage change in the closing prices from the day before

    # Return's values for the past 30 days
    for index in range(1, 31):
        data[f'Return_{index}'] = data['Return'].shift(index)

    data['Target'] = (data['Return'].shift(-1)>0).astype(int)   # Cleaning the dataset from NaN values

    features = [f'Return_{i}' for i in range(1, 31)]
    X = data[features]      # X contains the Returns of the past 10 days
    y = data['Target']  # y contains the Target column (if tomorrow goes up or down)

    # Train_Test_Split : 80% training data to teach the model and 20% testing data to evaluate how well it learned
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

    # We do not shuffle to preserve the chronological order.

    model = RandomForestClassifier(n_estimators=600, max_depth=100, random_state=2)
    model.fit(X_train, y_train)

    y_predict = model.predict(X_test)   # Prediction for the price if it will go up or down on the test data
    accuracy = accuracy_score(y_test, y_predict)

    recent_day_row = X_test.iloc[-1:]   # Data of the most recent day
    recent_day_prediction = model.predict(recent_day_row)[0]    # up = 1 or down = 0
    recent_day_confidence = model.predict_proba(recent_day_row)[0][recent_day_prediction]   # confidence: [%down, %up] (0 for down, 1 for up) to get the confidence for our prediction

    if recent_day_prediction==1 and recent_day_confidence>=0.55:
        action = "Buy"
    elif recent_day_prediction==0 and recent_day_confidence>=0.55:
        action = "Sell"
    else:
        action = "Hold"

    print(f"Indication for {symbol}:")
    print(f"1. Action: {action}")
    print(f"2. Accuracy: {accuracy:.2f}")
    print(f"3. Prediction: {'UP' if recent_day_prediction == 1 else 'DOWN'}")
    print(f"4. Confidence: {recent_day_confidence:.2f}")

    result = {
        "action": action,
        "accuracy": round(accuracy, 2),
        "prediction": "UP" if recent_day_prediction == 1 else "DOWN",
        "confidence": round(recent_day_confidence, 2),
    }
    return result



# Simple Streamlit GUI

title = st.title("AIndicate: AI Stock/Crypto Indicator")

options = st.selectbox("Choose a Stock or Crypto coin", supported_stocks_names)
run_button = st.button("Run Indicator")

result = []

if run_button:
    result = run_ai_indicator(supported_stocks_symbols[supported_stocks_names.index(options)])

if result:
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Action", f"{result['action']}", "")
    col2.metric("Prediction", f"{result['prediction']}", "")
    col3.metric("Accuracy", f"{result['accuracy']}", "")
    col4.metric("Confidence", f"{result['confidence']}", "")

    data = yf.download(supported_stocks_symbols[supported_stocks_names.index(options)], period='30d', interval='1d')
    st.line_chart(data['Close'])







