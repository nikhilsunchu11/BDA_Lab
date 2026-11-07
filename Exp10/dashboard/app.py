
import os

import pandas as pd
import plotly.express as px
import streamlit as st
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="E-Commerce Intelligence Dashboard",
    page_icon="",
    layout="wide"
)

load_dotenv()

# --------------------------------------------------
# DATABASE CONNECTION
# --------------------------------------------------

DATABASE_URL = (
    f"postgresql+psycopg2://{os.getenv('PGUSER')}:"
    f"{os.getenv('PGPASSWORD')}@{os.getenv('PGHOST')}:"
    f"{os.getenv('PGPORT')}/{os.getenv('PGDATABASE')}"
)

@st.cache_resource
def get_engine():
    return create_engine(DATABASE_URL)

engine = get_engine()

# --------------------------------------------------
# DATA RETRIEVAL
# --------------------------------------------------

@st.cache_data(ttl=60)
def load_data():
    with engine.connect() as conn:
        events = pd.read_sql(
            text("SELECT * FROM event_summary"),
            conn
        )

        daily = pd.read_sql(
            text("""
                SELECT *
                FROM daily_purchase_trends
                ORDER BY purchase_date
            """),
            conn
        )

        categories = pd.read_sql(
            text("""
                SELECT *
                FROM category_performance
            """),
            conn
        )

    return events, daily, categories

try:
    events, daily, categories = load_data()
except Exception as error:
    st.error(f"Database connection failed: {error}")
    st.stop()

# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.title("E-Commerce Intelligence Dashboard")
st.caption(
    "Analytics based on the available dataset: "
    "October 1-18, 2019"
)

st.divider()

# --------------------------------------------------
# KEY PERFORMANCE INDICATORS
# --------------------------------------------------

event_counts = dict(
    zip(events["event_type"], events["total_events"])
)

total_events = int(events["total_events"].sum())
total_views = int(event_counts.get("view", 0))
total_carts = int(event_counts.get("cart", 0))
total_purchases = int(event_counts.get("purchase", 0))

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Events", f"{total_events:,}")
col2.metric("Product Views", f"{total_views:,}")
col3.metric("Add to Cart", f"{total_carts:,}")
col4.metric("Purchases", f"{total_purchases:,}")

st.divider()

# --------------------------------------------------
# EVENT DISTRIBUTION
# --------------------------------------------------

st.subheader("Event Distribution")

left, right = st.columns(2)

with left:
    fig_events = px.pie(
        events,
        names="event_type",
        values="total_events",
        hole=0.45,
        title="Distribution of E-Commerce Events"
    )

    st.plotly_chart(fig_events, use_container_width=True)

# --------------------------------------------------
# DAILY PURCHASE TRENDS
# --------------------------------------------------

with right:
    fig_daily = px.line(
        daily,
        x="purchase_date",
        y="purchase_events",
        markers=True,
        title="Daily Purchase Events"
    )

    fig_daily.update_layout(
        xaxis_title="Date",
        yaxis_title="Purchase Events"
    )

    st.plotly_chart(fig_daily, use_container_width=True)

# --------------------------------------------------
# DAILY PURCHASE VALUE
# --------------------------------------------------

st.info(
    "Data coverage: October 1–18, 2019. "
    "October 18 contains only 1,084 purchase events, "
    "so its daily total should be interpreted as partial."
)

st.subheader("Daily Purchase Value")

fig_value = px.bar(
    daily,
    x="purchase_date",
    y="daily_purchase_value",
    title="Recorded Purchase Value by Date",
    labels={
        "purchase_date": "Date",
        "daily_purchase_value": "Recorded Value"
    }
)

st.plotly_chart(fig_value, use_container_width=True)

# --------------------------------------------------
# CATEGORY PERFORMANCE
# --------------------------------------------------

st.subheader("Category Performance")

top_views = categories.nlargest(10, "total_views")

fig_views = px.bar(
    top_views.sort_values("total_views"),
    x="total_views",
    y="category_code",
    orientation="h",
    title="Top 10 Categories by Views",
    labels={
        "total_views": "Total Views",
        "category_code": "Category"
    }
)

st.plotly_chart(fig_views, use_container_width=True)

top_purchases = categories.nlargest(
    10, "purchase_events"
)

fig_purchases = px.bar(
    top_purchases.sort_values("purchase_events"),
    x="purchase_events",
    y="category_code",
    orientation="h",
    title="Top 10 Categories by Purchase Events",
    labels={
        "purchase_events": "Purchase Events",
        "category_code": "Category"
    }
)

st.plotly_chart(fig_purchases, use_container_width=True)

# --------------------------------------------------
# CATEGORY DATA TABLE
# --------------------------------------------------

with st.expander("View Category Analytics Data"):
    st.dataframe(
        categories.sort_values(
            "total_views",
            ascending=False
        ),
        use_container_width=True
    )

st.divider()

st.caption(
    "Data source: Hive and Impala | "
    "Analytics storage: PostgreSQL | "
    "Dashboard: Streamlit"
)
