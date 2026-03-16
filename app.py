import streamlit as st
import pandas as pd
import yfinance as yf

st.title("📈 NIFTY Stock Price Comparison Dashboard")

# -----------------------------
# Ticker List (sample)
# You can extend to full NIFTY500
# -----------------------------
tickers = [
"RELIANCE.NS","TCS.NS","HDFCBANK.NS","INFY.NS","ICICIBANK.NS",
"HINDUNILVR.NS","ITC.NS","LT.NS","SBIN.NS","BHARTIARTL.NS",
"KOTAKBANK.NS","ASIANPAINT.NS","AXISBANK.NS","MARUTI.NS",
"SUNPHARMA.NS","TITAN.NS","ULTRACEMCO.NS","NESTLEIND.NS",
"BAJFINANCE.NS","POWERGRID.NS","NTPC.NS","ONGC.NS",
"ADANIENT.NS","ADANIPORTS.NS","WIPRO.NS","HCLTECH.NS",
"TATASTEEL.NS","TATAMOTORS.NS","COALINDIA.NS","JSWSTEEL.NS"
]

st.write("Total Stocks:", len(tickers))

# -----------------------------
# Download Data
# -----------------------------
start_date = st.date_input("Download Start Date")
end_date = st.date_input("Download End Date")

if st.button("Download Market Data"):

    with st.spinner("Downloading stock data..."):

        data = yf.download(
            tickers,
            start=start_date,
            end=end_date,
            auto_adjust=True
        )

        # Extract Close prices
        close_prices = data["Close"]

        st.session_state["data"] = close_prices

    st.success("Data downloaded successfully")

# -----------------------------
# Compare Prices
# -----------------------------
if "data" in st.session_state:

    df = st.session_state["data"]

    st.subheader("Select Dates for Comparison")

    date1 = st.date_input("Date 1")
    date2 = st.date_input("Date 2")

    if st.button("Compare All Stocks"):

        results = []

        for ticker in df.columns:

            try:

                # nearest previous trading day
                price1 = df[ticker].loc[:str(date1)].iloc[-1]
                price2 = df[ticker].loc[:str(date2)].iloc[-1]

                change = price2 - price1
                pct_change = (change / price1) * 100

                results.append({
                    "Ticker": ticker,
                    "Price_Date1": round(price1,2),
                    "Price_Date2": round(price2,2),
                    "Change": round(change,2),
                    "Percent_Change": round(pct_change,2)
                })

            except:
                continue

        result_df = pd.DataFrame(results)

        result_df = result_df.sort_values(
            "Percent_Change",
            ascending=False
        )

        # -----------------------------
        # Market Comparison
        # -----------------------------
        st.subheader("📊 Market Comparison")
        st.dataframe(result_df, use_container_width=True)

        # -----------------------------
        # Top Gainers
        # -----------------------------
        st.subheader("🚀 Top Gainers")
        st.dataframe(result_df.head(10), use_container_width=True)

        # -----------------------------
        # Top Losers
        # -----------------------------
        st.subheader("📉 Top Losers")
        st.dataframe(result_df.tail(10), use_container_width=True)
