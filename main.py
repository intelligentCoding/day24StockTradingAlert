import os

import requests
from twilio.rest import Client
from dotenv import load_dotenv

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
load_dotenv('.env')

# call the stock endpoint
stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": os.getenv("api_access_key")
}
response = requests.get(STOCK_ENDPOINT, params=stock_params)
# STEP#1 get yesterday's closing stock price
data = response.json()["Time Series (Daily)"]
data_list = [value for (key, value) in data.items()]
yesterday_data = data_list[0]
yesterday_closing_price = yesterday_data["4. close"]

# STEP#2 day before data
day_before_yesterday_data = data_list[1]
day_before_yesterday_closing_price = day_before_yesterday_data["4. close"]

# STEP#3 now we will get the difference, positive difference
difference = float(yesterday_closing_price) - float(day_before_yesterday_closing_price)

up_down = ""
if difference > 0:
    up_down = "⬆"
else:
    up_down = "⬇"

# STEP#4 difference in percentage
difference_percentage = round((difference / float(yesterday_closing_price)) * 100)

# STEP#5 if difference is greater than 5 get news
print(difference_percentage)
if abs(difference_percentage) > 1:
    news_params = {
        "apikey": os.getenv("news_api_key"),
        "qInTitle": COMPANY_NAME
    }
    news_response = requests.get(NEWS_ENDPOINT, params=news_params)
    articles = news_response.json()["articles"]
    # get three articles
    three_articles = articles[:3]
    # STEP#6 get heading and content of 3 articles
    formatted_articles = [f"\n\n{STOCK_NAME} : {up_down} {difference_percentage}%\nHeadlines: {article['title']}. \nBrief: {article['description']}" for article in
                          three_articles]
    # STEP#7 send text message using twillio
    client = Client(os.getenv("account_sid"), os.getenv("auth_token"))
    for article in formatted_articles:
        message = client.messages \
            .create(
            body=article,
            from_='+18317696055',
            to='YOUR_PHONE_NUMBER'
        )
