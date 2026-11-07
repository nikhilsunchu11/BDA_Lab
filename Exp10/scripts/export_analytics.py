import pandas as pd
from impala.dbapi import connect
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

load_dotenv()

#-----------------------------------------------
# 1. CONNECT TO IMPALA
#-----------------------------------------------

print("Connecting to Impala...")

impala_connection = connect(
    host="172.22.0.2",
    port=21050,
    database="exp10_db",
    auth_mechanism="NOSASL"
)

cursor = impala_connection.cursor()
print("Impala connection successful.")

#-----------------------------------------------
# 2. CONNECT TO POSTGRESQL
#-----------------------------------------------

DATABASE_URL = (
    f"postgresql+psycopg2://{os.getenv('PGUSER')}:"
    f"{os.getenv('PGPASSWORD')}@{os.getenv('PGHOST')}:"
    f"{os.getenv('PGPORT')}/{os.getenv('PGDATABASE')}"
)

pg_engine = create_engine(DATABASE_URL)

with pg_engine.connect() as connection:
    connection.execute(text("SELECT 1"))

print("PostgreSQL connection successful.")

#-----------------------------------------------
# 3. HELPER FUNCTION TO FETCH DATA
#-----------------------------------------------

def fetch_dataframe(query):
    cursor.execute(query)
    rows = cursor.fetchall()
    columns = [column[0] for column in cursor.description]
    return pd.DataFrame(rows, columns=columns)


#-----------------------------------------------
# 4. EXTRACT EVENT DISTRIBUTION
#-----------------------------------------------

print("\nExtracting event distribution...")

event_df = fetch_dataframe("""
    SELECT
        event_type,
        COUNT(*) AS total_events
    FROM ecommerce_events_clean
    GROUP BY event_type
""")

#-----------------------------------------------
# 5. EXTRACT DAILY PURCHASE TRENDS
#-----------------------------------------------

print("Extracting daily purchase trends...")

daily_df = fetch_dataframe("""
    SELECT
        SUBSTR(event_time, 1, 10) AS purchase_date,
        COUNT(*) AS purchase_events,
        ROUND(SUM(price), 2) AS daily_purchase_value
    FROM ecommerce_events_clean
    WHERE event_type = 'purchase'
    GROUP BY SUBSTR(event_time, 1, 10)
    ORDER BY purchase_date
""")

daily_df["purchase_date"] = pd.to_datetime(
    daily_df["purchase_date"]
).dt.date

# --------------------------------------------------
# 6. EXTRACT CATEGORY PERFORMANCE
# --------------------------------------------------

print("Extracting category performance...")

category_df = fetch_dataframe("""
    SELECT
        category_code,
        SUM(CASE WHEN event_type = 'view' THEN 1 ELSE 0 END)
            AS total_views,
        SUM(CASE WHEN event_type = 'purchase' THEN 1 ELSE 0 END)
            AS purchase_events,
        ROUND(
            SUM(
                CASE
                    WHEN event_type = 'purchase' THEN price
                    ELSE 0
                END
            ), 2
        ) AS total_purchase_value
    FROM ecommerce_events_clean
    WHERE category_code IS NOT NULL
      AND TRIM(category_code) != ''
    GROUP BY category_code
""")

# --------------------------------------------------
# 7. LOAD DATA INTO POSTGRESQL
# --------------------------------------------------

print("\nLoading analytics into PostgreSQL...")

with pg_engine.begin() as connection:

    # Clear previous analytics
    connection.execute(text("""
        TRUNCATE TABLE
            event_summary,
            daily_purchase_trends,
            category_performance
    """))

    # Insert event distribution
    event_df.to_sql(
        "event_summary",
        connection,
        if_exists="append",
        index=False
    )

    # Insert daily trends
    daily_df.to_sql(
        "daily_purchase_trends",
        connection,
        if_exists="append",
        index=False
    )

    # Insert category performance
    category_df.to_sql(
        "category_performance",
        connection,
        if_exists="append",
        index=False
    )

# --------------------------------------------------
# 8. DISPLAY EXPORT SUMMARY
# --------------------------------------------------

print("\n========== EXPORT SUMMARY ==========")
print(f"Event summary rows: {len(event_df)}")
print(f"Daily trend rows: {len(daily_df)}")
print(f"Category performance rows: {len(category_df)}")
print("Analytics successfully exported to PostgreSQL.")

# --------------------------------------------------
# 9. CLOSE CONNECTIONS
# --------------------------------------------------

cursor.close()
impala_connection.close()
pg_engine.dispose()

print("\nAll connections closed.")
