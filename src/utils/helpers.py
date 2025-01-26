import pandas as pd
import os
from pathlib import Path
import streamlit as st
import re
from .crime_categories import CRIME_PATTERNS
import tempfile


@st.cache_data
def load_data():
    """Load and validate compiled crime data"""
    try:
        if "compiled_data" not in st.session_state:
            with st.spinner("Compiling data from source files..."):
                df = compile_data()
                df = clean_data(df)
                df = format_dates(df)
                df["CATEGORY"] = categorize_crimes_vectorized(df)
                df["DISTRICT_NAME"] = df["DISTRICT"].map(get_district_mapping())
                st.session_state["compiled_data"] = df

        return st.session_state["compiled_data"]

    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        raise


def categorize_crimes_vectorized(df):
    """Vectorized crime categorization"""

    COMPILED_PATTERNS = {
        category: re.compile(pattern, flags=re.IGNORECASE)
        for category, pattern in CRIME_PATTERNS.items()
    }

    descriptions = df["OFFENSE_DESCRIPTION"].fillna("UNKNOWN").astype(str)

    categories = pd.Series("other", index=df.index)

    for category, pattern in COMPILED_PATTERNS.items():
        mask = descriptions.apply(lambda x: bool(pattern.search(x)))
        categories[mask] = category

    return categories


def format_dates(df):
    """Format date column to datetime"""

    df["OCCURRED_ON_DATE"] = pd.to_datetime(df["OCCURRED_ON_DATE"], errors="coerce")

    return df


def read_csv_chunked(file_path, chunk_size=50000):
    """Read large CSV files in chunks and combine them"""
    chunks = []
    with st.spinner("Reading data in chunks..."):
        for chunk in pd.read_csv(file_path, chunksize=chunk_size, low_memory=False):
            chunks.append(chunk)
    return pd.concat(chunks, ignore_index=True)


def get_district_mapping():
    return {
        "A1": "Downtown/Beacon Hill",
        "A15": "Charlestown",
        "A7": "East Boston",
        "B2": "Roxbury",
        "B3": "Mattapan",
        "C6": "South Boston",
        "C11": "Dorchester",
        "D4": "South End",
        "D14": "Brighton",
        "E5": "West Roxbury",
        "E13": "Jamaica Plain",
        "E18": "Hyde Park",
    }


def clean_data(df):
    """Clean and filter the dataframe"""
    # Drop rows outside of the year range
    df = df[df["YEAR"].astype(int) != 2025]

    # Drop empty columns
    columns_to_drop = []
    if "UCR_PART" in df.columns:
        columns_to_drop.append("UCR_PART")
    if "OFFENSE_CODE_GROUP" in df.columns:
        columns_to_drop.append("OFFENSE_CODE_GROUP")
    if columns_to_drop:
        df = df.drop(columns=columns_to_drop)

    # Remove a typo from the underlying dataset
    df["OFFENSE_DESCRIPTION"] = df["OFFENSE_DESCRIPTION"].str.replace(
        "NEGLIGIENT", "NEGLIGENT"
    )

    return df


def compile_data():
    """Compile raw data files into single dataset"""
    data_folder = "data/raw"

    try:
        compiled_df = pd.DataFrame()
        file_count = 0

        if not os.path.exists(data_folder):
            st.error(f"Data folder not found: {data_folder}")
            raise FileNotFoundError(f"Data folder not found: {data_folder}")

        for filename in os.listdir(data_folder):
            if filename.endswith(".csv"):
                file_path = os.path.join(data_folder, filename)
                df = pd.read_csv(file_path, low_memory=False)
                cleaned_df = clean_data(df)
                compiled_df = pd.concat([compiled_df, cleaned_df], ignore_index=True)
                file_count += 1

        if file_count == 0:
            raise FileNotFoundError("No CSV files found in data folder")

        return compiled_df

    except Exception as e:
        st.error(f"Error compiling data: {str(e)}")
        raise
