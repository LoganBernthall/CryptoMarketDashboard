#Crypto Dashboard webapp

import streamlit as st
import requests

st.title("Crypto Market Dashboard")
st.caption("Welcome, this app utilise the CoinParpirka Crypto API")

#Dictionary mapping of cryptos stored in box and what the request would require
cryptoMap = {
    "Bitcoin": "btc-bitcoin",
    "Ethereum": "eth-ethereum",
    "Solana": "sol-solana",
    "BNB": "bnb-binance-coin"
}


selectedCrypto = st.selectbox("Choose a cryptocurrency", list(cryptoMap.keys()))

# Get API ticker
ticker = cryptoMap[selectedCrypto]
# Call API
url = f"https://api.coinpaprika.com/v1/tickers/{ticker}"
response = requests.get(url)

price = response.json()["quotes"]["USD"]["price"]

st.subheader("Price:")
st.metric(label=selectedCrypto, value=f"${price:,.2f}")

st.subheader("Historical:")
urlHistorical = f"https://api.coinpaprika.com/v1/tickers/{ticker}/historical?end=NOW&limit=1000&quote=usd&interval=5m"
historicalPrice = response.json()
st.metric(label=selectedCrypto, value=f"${historicalPrice:,.2f}")