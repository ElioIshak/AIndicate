import ta.momentum
import ta.trend
import ta.volatility
import yfinance as yf                                      
import ta

import streamlit as st
import pandas as pd
import csv
import os
import smtplib
import schedule
import time

from email.message import EmailMessage
from sklearn.ensemble import RandomForestClassifier         
from sklearn.model_selection import train_test_split

from dotenv import load_dotenv  # Used to Load the Email and Password from .env
    
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
    
    data['RSI'] = ta.momentum.RSIIndicator(data['Close'].squeeze(), window=30).rsi()  # Calculating RSI over 30 days
    
    data['SMA_30'] = data['Close'].rolling(window=30).mean()   # Calculating SMA over 30 days
    data['SMA_10'] = data['Close'].rolling(window=10).mean()    # Calculating SMA over 10 days
    data['SMA_Crossover'] = (data['SMA_10']>data['SMA_30']).astype(int) # SMA Crossover
    
    # MACD - Momentum indicator
    data['MACD'] = ta.trend.MACD(data['Close'].squeeze()).macd()
    data['MACD_signal'] = ta.trend.MACD(data['Close'].squeeze()).macd_signal()

    # Stochastic RSI - Momentum indicator
    data['Stochastic_RSI'] = ta.momentum.StochRSIIndicator(data['Close'].squeeze()).stochrsi()

    # EMA - Trend indicator 
    data['EMA'] = data['Close'].ewm(span=10).mean() # over 10 days

    # Open-Close Return
    data['OC_Return'] = (data['Close'] - data['Open']) / data['Open']

    # Daily Range
    data['Range'] = (data['High'] - data['Low']) / data['Close']

    # Rolling Standard Deviation - Voltality indicator
    data['Rolling_STD'] = data['Close'].rolling(10).std()

    # Bollinger Bands - Voltality indicator
    bollinger_bands = ta.volatility.BollingerBands(data['Close'].squeeze(), window=30)
    data['BB_Upper'] = bollinger_bands.bollinger_hband()
    data['BB_Lower'] = bollinger_bands.bollinger_lband()
    data['BB_Width'] = data['BB_Upper'] - data['BB_Lower']

    # Lagging the Features values
    for index in range(1, 61):
        data[f'Return_{index}'] = data['Return'].shift(index)
        data[f'Volume_{index}'] = data['Volume'].shift(index)
        data[f'RSI_{index}'] = data['RSI'].shift(index)
        data[f'SMA_10_{index}'] = data['SMA_10'].shift(index)
        data[f'SMA_30_{index}'] = data['SMA_30'].shift(index)
        data[f'SMA_Crossover_{index}'] = data['SMA_Crossover'].shift(index)
        data[f'OC_Return_{index}'] = data['OC_Return'].shift(index)
        data[f'Range_{index}'] = data['Range'].shift(index)
        data[f'Rolling_STD_{index}'] = data['Rolling_STD'].shift(index)
        data[f'MACD_{index}'] = data['MACD'].shift(index)
        data[f'MACD_signal_{index}'] = data['MACD_signal'].shift(index)
        data[f'BB_Upper_{index}'] = data['BB_Upper'].shift(index)
        data[f'BB_Lower_{index}'] = data['BB_Lower'].shift(index)
        data[f'BB_Width_{index}'] = data['BB_Width'].shift(index)

    data['Target'] = (data['Return'].shift(-1)>0).astype(int)   # Adding Target column (0 = down and 1 = up) for prices
    data.dropna(inplace=True)

    features = ([f'RSI_{i}' for i in range(1, 61)] +
                [f'SMA_10_{i}' for i in range(1, 61)] +
                [f'SMA_30_{i}' for i in range(1, 61)] +
                [f'SMA_Crossover_{i}' for i in range(1, 61)] +
                [f'Volume_{i}' for i in range(1, 61)] +
                [f'Return_{i}' for i in range(1, 61)] +
                [f'Rolling_STD_{i}' for i in range(1, 61)] +
                [f'MACD_{i}' for i in range(1, 61)] +
                [f'MACD_signal_{i}' for i in range(1, 61)] +
                [f'BB_Upper_{i}' for i in range(1, 61)] +
                [f'BB_Lower_{i}' for i in range(1, 61)] +
                [f'BB_Width_{i}' for i in range(1, 61)] +
                [f'OC_Return_{i}' for i in range(1, 61)] +
                [f'Range_{i}' for i in range(1, 61)])

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

# Simple Streamlit GUI And Smart Notification System

title = st.title("AIndicate: AI Stock/Crypto Indicator")

options = st.selectbox("Choose a Stock or Crypto coin", supported_stocks_names)
run_button = st.button("Run Indicator")

user_email = st.text_area("Enter Your Email")
selected_assets = st.multiselect("Select Assets", supported_stocks_names)
submit_button = st.button("Submit")

file_name = "USERS_SUBMISSIONS.csv"
file_exists = os.path.isfile("USERS_SUBMISSIONS.csv")
with open(file_name, mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Email", "Stocks"])

if submit_button:
    if not user_email or not selected_assets:
        st.error("Please enter your email and select at least one stock or crypto asset.")
        
    else:
        df = pd.read_csv(file_name)

        if user_email in df['Email'].values:
            df.loc[df['Email'] == user_email, 'Stocks'] = ','.join(selected_assets)
        else:
            new_row = pd.DataFrame([[user_email, ','.join(selected_assets)]], columns=['Email', 'Stocks'])
            df = pd.concat([df, new_row], ignore_index=True)

        df.to_csv(file_name, index=False)
        st.success("Successful Submission!")


load_dotenv()
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

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

def build_email(signals):
    built_email = "Hey, \n"
    built_email += "This email is being sent with the latest AIndicate suggestions: \n\n"
    built_email += "-------------------------------------------------------------------------\n"
    built_email += "   Stock/Crypto                   Action                   Confidence\n"
    built_email += "-------------------------------------------------------------------------\n"
    
    for signal in signals:
        built_email += f"{signal['Stock']:<15}{signal['Action']:<15}{signal['Confidence']}\n"
        built_email += "-------------------------------------------------------------------------\n"

    built_email += "\n\n"
    built_email += "AIndicate \n"
    built_email += "https://aindicate.streamlit.app/"

    return built_email

def send_alert(Email, Subject, Body):
    message = EmailMessage()
    message['Subject'] = Subject
    message['From'] = 'aindicate.ai.indicator@gmail.com'
    message['To'] = Email
    message.set_content(Body)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(message)

def notification_system():

    file = pd.read_csv(file_name)

    for index, row in file.iterrows():
        stocks_signals = []
        email = row["Email"]
        stocks = row["Stocks"].split(',')

        for stock in stocks:
            result = run_ai_indicator(supported_stocks_symbols[supported_stocks_names.index(stock)])
            if result['action'] in ["Buy", "Sell"]:
                stocks_signals.append({"Stock": stock, "Action": result['action'], "Confidence": result['confidence']})

        if stocks_signals:
            message = build_email(stocks_signals)
            send_alert(email, Subject="AIndicate Alert", Body=message)


    



