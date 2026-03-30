#Crypto Dashboard webapp
import datetime
import streamlit as st
import requests
import pandas as pd

#Titles
st.title("Crypto Market Dashboard")
st.caption("Welcome, this app utilise the CoinParpirka Crypto API.")
st.caption("This is using the free API so there is a 1 day delay on selected calls.")

#Dictionary mapping of cryptos stored in box and what the request would require
cryptoMap = {
    "Bitcoin": "btc-bitcoin",
    "Ethereum": "eth-ethereum",
    "Solana": "sol-solana",
    "BNB": "bnb-binance-coin",
    "Cardano": "ada-cardano",
    "DogeCoin": "doge-dogecoin"
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
endTime = datetime.datetime.utcnow()
startTime = endTime - datetime.timedelta(days=7)  # last 7 days

#Formatting of time
start_str = startTime.strftime("%Y-%m-%dT%H:%M:%SZ")
end_str = endTime.strftime("%Y-%m-%dT%H:%M:%SZ")

urlHistorical = f"https://api.coinpaprika.com/v1/tickers/{ticker}/historical?start={start_str}&end={end_str}&quote=usd&interval=1d"
responseHistorical = requests.get(urlHistorical)

historicalPrice = responseHistorical.json()

#Debug for html response commented out
#st.write(responseHistorical.text)

# Parse into df and format if possible
HistoricalDF = pd.DataFrame()  # empty df by default
if isinstance(historicalPrice, list) and len(historicalPrice) > 0:
    HistoricalDF = pd.DataFrame(historicalPrice)
    HistoricalDF["timestamp"] = pd.to_datetime(HistoricalDF["timestamp"])
    HistoricalDF.set_index("timestamp", inplace=True)
    st.subheader(f"7 Day Historical {selectedCrypto} (1 Day Delay)")
    st.line_chart(HistoricalDF[["price"]])
else:
    st.warning("No historical data available for this coin/interval")

#Call for information from the coin 
st.subheader(f"{selectedCrypto} Info:")
urlInfo = f"https://api.coinpaprika.com/v1/coins/{ticker}"
coinInfo = requests.get(urlInfo).json()

#Basic Information
st.write("Name:", coinInfo["name"])
st.write("Symbol:", coinInfo["symbol"])
st.write("Rank:", coinInfo["rank"])
st.write("Type:", coinInfo["type"])

#Description - IF applicable
if coinInfo.get("description"):
    st.write(coinInfo["description"])

# Events
st.subheader(f"{selectedCrypto} Events:")

urlEvents = f"https://api.coinpaprika.com/v1/coins/{ticker}/events"
coinEvents = requests.get(urlEvents).json()

if isinstance(coinEvents, list) and len(coinEvents) > 0:
    for event in coinEvents:
        with st.container():
            st.markdown(f"### {event['name']}")
            st.write(f"📅 Date: {event['date']}")
            
            if event.get("description"):
                st.write(event["description"])
            
            if event.get("link"):
                st.markdown(f"[More Info]({event['link']})")
            
            st.divider()
else:
    st.info("No events available for this coin.")