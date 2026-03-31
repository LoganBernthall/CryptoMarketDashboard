#Create callable class for CoinPaprika API usage
import requests
import datetime

class Api:
    
    def currentPrice(tickerCode):
        #Get coin prices when ticker code parsed
        url = f"https://api.coinpaprika.com/v1/tickers/{tickerCode}"
        response = requests.get(url)
        price = response.json()["quotes"]["USD"]["price"]

        return price
    
    def candlestickChart(tickerCode):
        #Get coin candlestick when ticker code parsed
        url = f"https://api.coinpaprika.com/v1/coins/{tickerCode}/ohlcv/latest"
        response = requests.get(url)
        chartData = response.json()
        
        return chartData

    def historicalPrice(tickerCode):
        #Get historical prices when ticker code is parsed - ATTENTION THIS IS THE FREE API, 7 DAY DELAY TO VALUES  
        endTime = datetime.datetime.utcnow()
        startTime = endTime - datetime.timedelta(days=7)  # last 7 days

        #Formatting of time
        start_str = startTime.strftime("%Y-%m-%dT%H:%M:%SZ")
        end_str = endTime.strftime("%Y-%m-%dT%H:%M:%SZ")

        urlHistorical = f"https://api.coinpaprika.com/v1/tickers/{tickerCode}/historical?start={start_str}&end={end_str}&quote=usd&interval=1d"
        responseHistorical = requests.get(urlHistorical)

        historicalPrice = responseHistorical.json()

        return historicalPrice
    
    def coinInformation(tickerCode):
        #Get coin information when ticker code is parsed
        urlInfo = f"https://api.coinpaprika.com/v1/coins/{tickerCode}"
        coinInfo = requests.get(urlInfo).json()

        return coinInfo
    
    def coinEvents(tickerCode):
        #Get coin events when ticker code is parsed
        urlEvents = f"https://api.coinpaprika.com/v1/coins/{tickerCode}/events"
        coinEvents = requests.get(urlEvents).json()

        return coinEvents