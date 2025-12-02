import datetime as dt

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st
import yfinance as yf


st.set_page_config(
    page_title="Real-Time Market Dashboard",
    page_icon="📈",
    layout="wide",
)

st.title("📈 Real-Time Stock & Crypto Dashboard")
st.caption("Built with Python + Streamlit + yfinance")


@st.cache_data(ttl=300)
def load_price_data(tickers: list[str], start: dt.date, end: dt.date) -> pd.DataFrame:
    """
    ดึงข้อมูลราคาจาก yfinance
    คืนค่าเป็น DataFrame แบบ multi-column: (Date index, columns: Ticker-Field)
    """
    if not tickers:
        return pd.DataFrame()

    data = yf.download(
        tickers=tickers,
        start=start,
        end=end,
        auto_adjust=True,
        progress=False,
    )

    if isinstance(data.columns, pd.MultiIndex):
      
        close = data["Close"]
        vol = data["Volume"]
    else:
        close = data[["Close"]].copy()
        vol = data[["Volume"]].copy()

    close.columns = [f"{c}" for c in close.columns]
    vol.columns = [f"{c}" for c in vol.columns]

    return pd.concat(
        {
            "Close": close,
            "Volume": vol,
        },
        axis=1,
    )


def prepare_long_format(price_df: pd.DataFrame) -> pd.DataFrame:
    """แปลง DataFrame ให้เป็น long format สำหรับ plotly"""
    if price_df.empty:
        return price_df

    close = price_df["Close"].copy()
    vol = price_df["Volume"].copy()

    close_long = (
        close.reset_index()
        .melt(id_vars="Date", var_name="Symbol", value_name="Close")
    )
    vol_long = (
        vol.reset_index()
        .melt(id_vars="Date", var_name="Symbol", value_name="Volume")
    )

    merged = pd.merge(close_long, vol_long, on=["Date", "Symbol"], how="left")
    return merged


def calc_returns_summary(merged: pd.DataFrame) -> pd.DataFrame:
    """คำนวณ %Change ช่วงเวลาที่เลือก สำหรับแต่ละ Symbol"""
    if merged.empty:
        return pd.DataFrame()

    summary_rows = []
    for symbol, df_sym in merged.groupby("Symbol"):
        df_sym_sorted = df_sym.sort_values("Date")
        first_price = df_sym_sorted["Close"].iloc[0]
        last_price = df_sym_sorted["Close"].iloc[-1]
        if first_price and not np.isnan(first_price):
            pct_change = (last_price - first_price) / first_price * 100
        else:
            pct_change = np.nan

        latest_row = df_sym_sorted.iloc[-1]
        summary_rows.append(
            {
                "Symbol": symbol,
                "Last Close": last_price,
                "Change % (Period)": pct_change,
                "Last Volume": latest_row["Volume"],
                "Last Date": latest_row["Date"],
            }
        )

    return pd.DataFrame(summary_rows).sort_values("Symbol")



st.sidebar.header("⚙️ Settings")

mode = st.sidebar.radio(
    "Asset Type",
    options=["Stocks", "Crypto"],
    index=0,
)

default_stock_symbols = ["AAPL", "MSFT", "NVDA", "META", "TSLA", "GOOGL"]
default_crypto_symbols = ["BTC-USD", "ETH-USD", "SOL-USD", "XAUUSD=X"]

if mode == "Stocks":
    symbols = st.sidebar.multiselect(
        "Select stock symbols:",
        options=default_stock_symbols,
        default=["AAPL", "NVDA"],
        help="พิมพ์ Symbol เพิ่มเองได้ เช่น AMZN, NFLX ฯลฯ",
    )
else:
    symbols = st.sidebar.multiselect(
        "Select crypto symbols:",
        options=default_crypto_symbols,
        default=["BTC-USD"],
        help="พิมพ์ Symbol เพิ่มเองได้ เช่น DOGE-USD, BNB-USD ฯลฯ",
    )

today = dt.date.today()
period_option = st.sidebar.selectbox(
    "Time range:",
    ["1M", "3M", "6M", "1Y", "Custom"],
    index=1,
)

if period_option == "1M":
    start_date = today - dt.timedelta(days=30)
elif period_option == "3M":
    start_date = today - dt.timedelta(days=90)
elif period_option == "6M":
    start_date = today - dt.timedelta(days=180)
elif period_option == "1Y":
    start_date = today - dt.timedelta(days=365)
else:
    start_date = st.sidebar.date_input("Start date:", today - dt.timedelta(days=90))
end_date = st.sidebar.date_input("End date:", today)

st.sidebar.subheader("Chart Options")
show_volume = st.sidebar.checkbox("Show volume chart", value=True)
log_scale = st.sidebar.checkbox("Log scale (price)", value=False)

st.sidebar.markdown("---")
st.sidebar.caption("Data from Yahoo Finance via yfinance (5 min cached)")


if not symbols:
    st.warning("กรุณาเลือกอย่างน้อย 1 Symbol จาก Sidebar")
    st.stop()

price_df = load_price_data(symbols, start_date, end_date)

if price_df.empty:
    st.error("ไม่พบข้อมูลสำหรับ Symbol/ช่วงเวลานี้")
    st.stop()

merged = prepare_long_format(price_df)
summary_df = calc_returns_summary(merged)


st.subheader("Market Overview")

kpi_cols = st.columns(min(4, len(symbols)))
for i, symbol in enumerate(symbols[:4]):
    col = kpi_cols[i]
    df_sym = summary_df[summary_df["Symbol"] == symbol]
    if df_sym.empty:
        continue

    row = df_sym.iloc[0]
    last_close = row["Last Close"]
    pct_change = row["Change % (Period)"]

    col.metric(
        label=f"{symbol} (Period Change)",
        value=f"{last_close:,.2f}",
        delta=f"{pct_change:,.2f}%",
    )


st.markdown("### 📉 Price Chart")

fig_price = px.line(
    merged,
    x="Date",
    y="Close",
    color="Symbol",
    hover_data=["Volume"],
)

fig_price.update_layout(
    xaxis_title="Date",
    yaxis_title="Close Price",
    legend_title="Symbol",
)

if log_scale:
    fig_price.update_yaxes(type="log")

st.plotly_chart(fig_price, use_container_width=True)


if show_volume:
    st.markdown("### 📊 Volume")
    fig_vol = px.bar(
        merged,
        x="Date",
        y="Volume",
        color="Symbol",
        barmode="group",
    )
    fig_vol.update_layout(
        xaxis_title="Date",
        yaxis_title="Volume",
        legend_title="Symbol",
    )
    st.plotly_chart(fig_vol, use_container_width=True)


st.markdown("### 📋 Summary (Period)")

summary_display = summary_df.copy()
summary_display["Last Close"] = summary_display["Last Close"].map(
    lambda x: f"{x:,.2f}"
)
summary_display["Change % (Period)"] = summary_display["Change % (Period)"].map(
    lambda x: f"{x:,.2f}%"
)
summary_display["Last Volume"] = summary_display["Last Volume"].map(
    lambda x: f"{x:,.0f}"
)

st.dataframe(
    summary_display.set_index("Symbol"),
    use_container_width=True,
)

st.caption("Tip: ลองเพิ่ม Symbol เองใน Sidebar เช่น AMZN, NFLX, DOGE-USD แล้วดูกราฟเทียบกันได้เลย")
