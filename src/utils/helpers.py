import pandas as pd
import os
from pathlib import Path
import streamlit as st
import re
from .crime_categories import CRIME_PATTERNS

# Pre-compile patterns at module load
COMPILED_PATTERNS = {
    category: re.compile(pattern, flags=re.IGNORECASE)
    for category, pattern in CRIME_PATTERNS.items()
}


def categorize_crimes_vectorized(df):
    """Vectorized crime categorization"""
    descriptions = df["OFFENSE_DESCRIPTION"].fillna("UNKNOWN").astype(str)

    categories = pd.Series("other", index=df.index)

    for category, pattern in COMPILED_PATTERNS.items():
        mask = descriptions.apply(lambda x: bool(pattern.search(x)))
        categories[mask] = category

    return categories


def read_csv_chunked(file_path, chunk_size=50000):
    """Read large CSV files in chunks and combine them"""
    chunks = []
    with st.spinner("Reading data in chunks..."):
        for chunk in pd.read_csv(file_path, chunksize=chunk_size, low_memory=False):
            chunks.append(chunk)
    return pd.concat(chunks, ignore_index=True)


@st.cache_data
def load_data():
    """Load and validate compiled crime data"""
    data_path = "data/processed/compiled_data.csv"

    try:
        if not os.path.exists(data_path):
            with st.spinner("Compiling data from source files..."):
                process_data()

        df = read_csv_chunked(data_path)

        if len(df) < 350000:
            with st.spinner("Recompiling data..."):
                df = process_data()
        return df

    except Exception as e:
        raise ValueError(f"Error loading data: {str(e)}")


def process_data():
    """Preprocess and save compiled data"""
    output_file = "data/processed/compiled_data.csv"

    df = compile_data()

    df = clean_data(df)
    df["CATEGORY"] = categorize_crimes_vectorized(df)
    df["DISTRICT_NAME"] = df["DISTRICT"].map(get_district_mapping())

    ensure_dir(os.path.dirname(output_file))
    df.to_csv(output_file, index=False)

    return df


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


def get_map_bounds(df):
    """Calculate map center and zoom from data bounds"""
    lat_min = df["Lat"].min()
    lat_max = df["Lat"].max()
    long_min = df["Long"].min()
    long_max = df["Long"].max()

    center_lat = (lat_min + lat_max) / 2
    center_long = (long_min + long_max) / 2

    return center_lat, center_long


def clean_data(df):
    """Clean and filter the dataframe"""
    df = df[df["YEAR"].astype(int) != 2025]

    columns_to_drop = []
    if "UCR_PART" in df.columns:
        columns_to_drop.append("UCR_PART")
    if "OFFENSE_CODE_GROUP" in df.columns:
        columns_to_drop.append("OFFENSE_CODE_GROUP")

    if columns_to_drop:
        df = df.drop(columns=columns_to_drop)

    return df


def ensure_dir(directory):
    Path(directory).mkdir(parents=True, exist_ok=True)


def compile_data():
    """Compile raw data files into single dataset"""
    data_folder = "data/raw"

    try:
        compiled_df = pd.DataFrame()
        file_count = 0

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
