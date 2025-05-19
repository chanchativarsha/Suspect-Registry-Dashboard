import streamlit as st
import plotly.express as px
import pandas as pd
import sqlite3
import warnings
import time

warnings.filterwarnings('ignore')

# Page Configuration
st.set_page_config(page_title="📊 Suspect Registry Dashboard", page_icon="📈", layout="wide")

# Inject Custom CSS for Styling
st.markdown("""
    <style>
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #1f2630;
        color: white;
    }
    [data-testid="stSidebar"] label {
        color: #38bdf8;
        font-weight: 600;
    }
    [data-testid="stSidebar"] .stMarkdown h1,
    [data-testid="stSidebar"] .stMarkdown h2 {
        color: white;
    }

    /* Form Input Customization */
    .stSelectbox > div, .stMultiSelect > div, .stTextInput > div, .stNumberInput > div {
        background-color: #2c333b !important;
        color: white !important;
        border-radius: 10px;
        border: 1px solid #444;
    }
    .css-1wa3eu0-placeholder, .css-1okebmr-indicatorSeparator {
        color: #ccc !important;
    }
    
    /* Header Banner Styling */
    .header-banner {
        background-color: #004080;
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        color: white;
        font-size: 32px;
        font-weight: bold;
        box-shadow: 0px 4px 8px rgba(0,0,0,0.3);
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 15px;
    }

    /* Dark Mode Cards */
    .dark-card {
        background-color: #1f2630;
        padding: 12px 18px;
        border-radius: 12px;
        margin-bottom: 10px;
        color: white;
        box-shadow: 0px 2px 6px rgba(0,0,0,0.3);
    }
    .dark-card .column-name {
        font-size: 16px;
        font-weight: 600;
    }
    .dark-card .value {
        font-size: 26px;
        color: #38bdf8;
    }
    </style>
""", unsafe_allow_html=True)

# I4C Logo and Header Banner
i4c_logo_url = "data:image/jpeg;base64,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"

st.markdown(f"""
    <div class='header-banner'>
        <img src='{i4c_logo_url}' width='125' height='100'>
         Suspect Registry Dashboard
    </div>
""", unsafe_allow_html=True)

time.sleep(1)


# Inject Dark Theme to Sidebar
st.markdown("""
    <style>
    [data-testid="stSidebar"] {
        background-color: #1f2630;
        color: white;
    }
    [data-testid="stSidebar"] label {
        color: #38bdf8;
        font-weight: 600;
    }
    [data-testid="stSidebar"] .stMarkdown h1,
    [data-testid="stSidebar"] .stMarkdown h2,
    [data-testid="stSidebar"] .stMarkdown h3,
    [data-testid="stSidebar"] .stMarkdown h4 {
        color: white;
    }
    .stSelectbox > div, .stMultiSelect > div, .stTextInput > div, .stNumberInput > div {
        background-color: #2c333b !important;
        color: white !important;
        border-radius: 10px;
        border: 1px solid #444;
    }
    .css-1wa3eu0-placeholder, .css-1okebmr-indicatorSeparator {
        color: #ccc !important;
    }
    .block-container:has([data-testid="stSidebar"]) {
        box-shadow: none !important;
    }
    button:disabled {
        background-color: #2c333b !important;
        color: #38bdf8 !important;
        border: 1px solid #444 !important;
        opacity: 1 !important;
    }
    [data-testid="collapsedControl"] {
        background-color: #2c333b !important;
        border: 1px solid #555 !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.6);
    }
    [data-testid="collapsedControl"] svg {
        stroke: #38bdf8 !important;
        width: 22px;
        height: 18px;
    }
    </style>
""", unsafe_allow_html=True)


time.sleep(1)

# Sidebar Navigation
st.sidebar.markdown("---")
st.sidebar.button("📈 Dashboard", disabled=True)
st.sidebar.markdown("---")

# 📂 Load from SQLite DB
db_path = "D:/RRU/Sem 8/I4C-BANK-SUSPECT REGISTRY-PROJECT/I4C-BANK-SUSPECT REGISTRY-PROJECT/new_suspect_file2.db"
try:
    conn = sqlite3.connect(db_path)

    df = pd.read_sql_query("SELECT * FROM new_suspect_file2", conn)


    conn.close()

    # Dashboard Header Metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("📄 Number of Records", len(df))

    if "bank_name" in df.columns:
        if col2.button("🏦 Unique Banks: " + str(df["bank_name"].nunique())):
            st.subheader("🏦 List of Unique Banks")
            st.write(df["bank_name"].unique())

    if "source" in df.columns:
        if col3.button("📌 Unique Sources: " + str(df["source"].nunique())):
            st.subheader("📌 List of Unique Sources")
            st.write(df["source"].unique())

    # Date filtering
    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"], errors='coerce')
        df = df.dropna(subset=["Date"])
        df["Month_Year"] = df["Date"].dt.to_period("M").astype(str)
        unique_months_years = sorted(df["Month_Year"].unique())

        selected_months = st.sidebar.multiselect("📅 Select Month and Year", options=["All"] + unique_months_years, default=["All"])
        if "All" not in selected_months:
            df = df[df["Month_Year"].isin(selected_months)]

    # Unique Records Count
    st.subheader("📌 Unique Records Count")

    st.markdown("""
        <style>
        .dark-card {
            background-color: #1f2630;
            padding: 12px 18px;
            border-radius: 12px;
            margin-bottom: 10px;
            color: #ffffff;
            box-shadow: 0 2px 6px rgba(0,0,0,0.3);
        }
        .dark-card .column-name {
            font-size: 16px;
            font-weight: 600;
        }
        .dark-card .value {
            font-size: 26px;
            color: #38bdf8;
        }
        </style>
    """, unsafe_allow_html=True)

   # Exclude certain columns
    excluded_columns = ["Date", "Month_Year"]
    unique_counts = df.drop(columns=excluded_columns, errors='ignore').nunique().reset_index()
    unique_counts.columns = ["Column", "Unique Values"]

    # 🆕 Display Unique Fields as Boxes in a *5-Column Grid Layout*
    st.markdown("### 🧾 Unique Fields")

    num_cols = 5  # Ensure exactly 5 fields per row
    rows = [unique_counts.iloc[i:i+num_cols] for i in range(0, len(unique_counts), num_cols)]

    for row in rows:
        cols = st.columns(num_cols)
        for idx, (col_name, unique_value) in enumerate(zip(row["Column"], row["Unique Values"])):
            with cols[idx]:
                st.markdown(f"""
                    <div style='background-color: #1f2630; padding: 12px; border-radius: 12px; 
                                text-align: center; margin-bottom: 10px; color: #ffffff; 
                                box-shadow: 0 2px 6px rgba(0,0,0,0.3); width: 100%;'>
                        <div style='font-size: 14px; font-weight: 600;'>{col_name}</div>
                        <div style='font-size: 24px; color: #38bdf8;'>{unique_value}</div>
                    </div>
                """, unsafe_allow_html=True)

    # Bar Chart
    fig = px.bar(unique_counts, x="Column", y="Unique Values", text="Unique Values",
                 labels={"Column": "Column", "Unique Values": "Unique Values"},
                 template="plotly_dark", color_discrete_sequence=["#4CAF50"], height=400)
    st.plotly_chart(fig, use_container_width=True)

    # Market Overview
    st.subheader("📊 Market Overview")
    col4, col5 = st.columns(2)

    with col4:
        st.subheader("📌 Records by Source")
        records_by_source = df["source"].value_counts().reset_index()
        records_by_source.columns = ["Source", "Records"]
        fig_source = px.bar(records_by_source, x="Source", y="Records", text="Records",
                            template="plotly_dark", color_discrete_sequence=["#008CBA"],
                            labels={"Source": "Source", "Records": "Records Count"}, height=400)
        st.plotly_chart(fig_source, use_container_width=True)

    with col5:
        st.subheader("🏦 Records by Bank")
        records_by_bank = df["bank_name"].value_counts().reset_index()
        records_by_bank.columns = ["Bank", "Records"]
        fig_bank = px.bar(records_by_bank, x="Bank", y="Records", text="Records",
                          template="plotly_dark", color_discrete_sequence=["#FF9800"],
                          labels={"Bank": "Bank", "Records": "Records Count"}, height=400)
        st.plotly_chart(fig_bank, use_container_width=True)

    # Top Contributing Banks
    st.markdown("## 🥇 Top Contributing Banks")

    st.markdown("""
        <style>
            .dark-scorecard {
                background-color: #1f2630;
                padding: 12px 18px;
                border-radius: 12px;
                margin-bottom: 10px;
                color: #ffffff;
                box-shadow: 0 2px 6px rgba(0,0,0,0.3);
            }
            .dark-scorecard .bank-name {
                font-size: 16px;
                font-weight: 600;
            }
            .dark-scorecard .count {
                font-size: 26px;
                color: #38bdf8;
            }
        </style>
    """, unsafe_allow_html=True)

    col6, col7 = st.columns([3, 1])

    with col6:
        top_bank = df["bank_name"].value_counts().reset_index()
        top_bank.columns = ["Bank", "Count"]
        fig_top = px.bar(
            top_bank, x="Count", y="Bank",
            orientation="h", text="Count",
            template="plotly_dark", height=400,
            color_discrete_sequence=["#38bdf8"]
        )
        st.plotly_chart(fig_top, use_container_width=True)

    with col7:
        st.markdown("### 🔢 Scorecard")
        view_more_banks = st.checkbox("🔍 View More Banks", key="scorecard_view_more")
        visible_banks = top_bank.head(10) if view_more_banks else top_bank.head(2)

        for _, row in visible_banks.iterrows():
            st.markdown(f"""
                <div class='dark-scorecard'>
                    <div class='bank-name'>{row["Bank"]}</div>
                    <div class='count'>{row["Count"]}</div>
                </div>
            """, unsafe_allow_html=True)

    # Sidebar: Advanced Filtering
    st.sidebar.header("🔎 Advanced Filtering")
    selected_column = st.sidebar.selectbox("📌 Select Column for Analysis",
                                           ["account_holder_name", "email_address_of_suspect", "phone_number_of_suspect",
                                            "ifsc_code", "account_number", "cin_number"])

    if selected_column in df.columns:
        top_values = df[selected_column].value_counts().head(10).index.tolist()
        selected_value = st.sidebar.selectbox("🔍 Select Most Repeated Value", top_values)
        filtered_data = df[df[selected_column] == selected_value]
        st.write(f"### 🔍 Showing data for {selected_column}: {selected_value}")
        st.dataframe(filtered_data)

except Exception as e:
    st.error(f"❌ Error loading database: {e}")