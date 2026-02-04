import pandas as pd
from pathlib import Path
import streamlit as st
from .crime_categories import CRIME_PATTERNS


@st.cache_data
def load_data():
    """Load and validate compiled crime data (try parquet first for speed)"""
    try:
        if "compiled_data" not in st.session_state:
            with st.spinner("Loading crime data..."):
                parquet_path = Path("data/processed/compiled_data.parquet")
                if parquet_path.exists():
                    try:
                        df = pd.read_parquet(parquet_path)
                    except Exception:
                        df = compile_data()
                else:
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
    descriptions = df["OFFENSE_DESCRIPTION"].fillna("").astype(str)

    categories = pd.Series("other", index=df.index)

    for category, pattern in CRIME_PATTERNS.items():
        mask = descriptions.str.contains(pattern, case=False, na=False, regex=True)
        categories.loc[mask] = category

    return categories


def format_dates(df):
    """Format date column to datetime"""

    df["OCCURRED_ON_DATE"] = pd.to_datetime(df["OCCURRED_ON_DATE"], errors="coerce")

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


def clean_data(df):
    """Clean and filter the dataframe"""
    df["YEAR"] = pd.to_numeric(df["YEAR"], errors="coerce").astype("Int64")
    df = df[df["YEAR"] != 2025]

    columns_to_drop = []
    if "UCR_PART" in df.columns:
        columns_to_drop.append("UCR_PART")
    if "OFFENSE_CODE_GROUP" in df.columns:
        columns_to_drop.append("OFFENSE_CODE_GROUP")
    if columns_to_drop:
        df = df.drop(columns=columns_to_drop)


    df["OFFENSE_DESCRIPTION"] = df["OFFENSE_DESCRIPTION"].str.replace(
        "NEGLIGIENT", "NEGLIGENT", regex=False
    )

    return df


def compile_data():
    """Compile raw data files into single dataset"""
    data_folder = Path("data/raw")

    if not data_folder.exists():
        st.error(f"Data folder not found: {data_folder}")
        raise FileNotFoundError(f"Data folder not found: {data_folder}")

    dfs = []
    for fp in data_folder.glob("*.csv"):
        try:
            df = pd.read_csv(fp, low_memory=False)
            df = clean_data(df)
            dfs.append(df)
        except Exception as e:
            st.warning(f"Failed to read {fp.name}: {e}")

    if not dfs:
        raise FileNotFoundError("No CSV files found in data folder")

    compiled_df = pd.concat(dfs, ignore_index=True)

    processed_dir = Path("data/processed")
    processed_dir.mkdir(parents=True, exist_ok=True)
    compiled_path = processed_dir / "compiled_data.parquet"
    try:
        compiled_df.to_parquet(compiled_path, index=False)
    except Exception:
        pass

    return compiled_df
