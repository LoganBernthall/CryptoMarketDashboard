#Crypto Dashboard webapp
import datetime
import streamlit as st
import requests
import pandas as pd

#Titles
st.title("Crypto Market Dashboard")
st.caption("Welcome, this app utilise the CoinParpirka Crypto API")

#Dictionary mapping of cryptos stored in box and what the request would require
cryptoMap = {
    "Bitcoin": "btc-bitcoin",
    "Ethereum": "eth-ethereum",
    "Solana": "sol-solana",
    "BNB": "bnb-binance-coin"
}

#User select crypro from list
selectedCrypto = st.selectbox("Choose a cryptocurrency", list(cryptoMap.keys()))

# Get API ticker
ticker = cryptoMap[selectedCrypto]

# Call API for current price
url = f"https://api.coinpaprika.com/v1/tickers/{ticker}"
response = requests.get(url)
price = response.json()["quotes"]["USD"]["price"]
st.subheader("Price:")
st.metric(label=selectedCrypto, value=f"${price:,.2f}")

## Call API for historical
st.subheader(f"Historical 7 Days of {selectedCrypto}")

endTime = datetime.datetime.utcnow()
startTime = endTime - datetime.timedelta(days=7)  # last 7 days

urlHistorical = f"https://api.coinpaprika.com/v1/tickers/{ticker}/historical?start={startTime.isoformat()}Z&end={endTime.isoformat()}Z&quote=usd&interval=5m"

responseHistorical = requests.get(urlHistorical)

historicalPrice = responseHistorical.json()

# Parse into df and format if possible
HistoricalDF = pd.DataFrame()  # empty df by default
if isinstance(historicalPrice, list) and len(historicalPrice) > 0:
    HistoricalDF = pd.DataFrame(historicalPrice)
    HistoricalDF["timestamp"] = pd.to_datetime(HistoricalDF["timestamp"])
    HistoricalDF.set_index("timestamp", inplace=True)
    st.subheader(f"Historical {selectedCrypto}")
    st.line_chart(HistoricalDF[["price"]])
else:
    st.warning("No historical data available for this coin/interval")
