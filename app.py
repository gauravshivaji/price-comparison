import streamlit as st
import pandas as pd
import yfinance as yf

st.title("📈 NIFTY Stock Comparison Dashboard")

# Ticker list
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

start_date = st.date_input("Download Start Date")
end_date = st.date_input("Download End Date")

if st.button("Download Market Data"):

    data = yf.download(
        tickers,
        start=start_date,
        end=end_date,
        group_by="ticker",
        auto_adjust=True
    )

    st.session_state["data"] = data
    st.success("Data Downloaded Successfully")

if "data" in st.session_state:

    df = st.session_state["data"]

    date1 = st.date_input("Select First Date")
    date2 = st.date_input("Select Second Date")

    if st.button("Compare All Stocks"):

        results = []

        for ticker in tickers:

            try:

                price1 = df[ticker].loc[str(date1)]["Close"]
                price2 = df[ticker].loc[str(date2)]["Close"]

                change = price2 - price1
                pct_change = (change / price1) * 100

                results.append([
                    ticker,
                    price1,
                    price2,
                    change,
                    pct_change
                ])

            except:
                pass

        result_df = pd.DataFrame(
            results,
            columns=[
                "Ticker",
                "Price_Date1",
                "Price_Date2",
                "Change",
                "Percent_Change"
            ]
        )

        result_df = result_df.sort_values(
            "Percent_Change",
            ascending=False
        )

        st.subheader("📊 Market Comparison")
        st.dataframe(result_df)

        st.subheader("🚀 Top Gainers")
        st.dataframe(result_df.head(10))

        st.subheader("📉 Top Losers")
        st.dataframe(result_df.tail(10))
