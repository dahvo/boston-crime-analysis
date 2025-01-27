import streamlit as st
import pandas as pd
import plotly.express as px
from utils.helpers import load_data, get_district_mapping
from utils.crime_categories import CRIME_PATTERNS
import calendar
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium
from utils.crime_categories import CATEGORY_DISPLAY_NAMES


def calculate_yearly_change(df, category):
    """Calculate average yearly change for a category"""
    yearly_counts = df[df["CATEGORY"] == category].groupby("YEAR").size().sort_index()

    if len(yearly_counts) < 2:
        return 0

    yearly_changes = yearly_counts.pct_change() * 100
    return yearly_changes.mean()


@st.cache_data
def load_heatmap_data(data):
    """Prepare and cache heatmap data for faster rendering"""
    valid_locations = data.dropna(subset=["Lat", "Long"])
    if len(valid_locations) == 0:
        return None

    category_data = {}
    for category in valid_locations["CATEGORY"].unique():
        cat_data = valid_locations[valid_locations["CATEGORY"] == category]
        heat_data = [[row["Lat"], row["Long"]] for _, row in cat_data.iterrows()]
        if heat_data:
            category_data[category] = heat_data

    return category_data


def render_category_heatmap(data):
    """Render heatmap of shooting locations"""
    category_data = load_heatmap_data(data)

    if category_data is None:
        st.warning("No valid location data available for heatmap")
        return

    m = folium.Map(
        location=[42.32000, -71.057083], zoom_start=11, tiles="OpenStreetMap"
    )

    for category, heat_data in category_data.items():
        fg = folium.FeatureGroup(name=str(category))
        HeatMap(heat_data, radius=14, blur=10, max_zoom=13).add_to(fg)
        fg.add_to(m)

    folium.LayerControl(collapsed=False).add_to(m)
    st_folium(m)


def geographical_analysis(data):

    district_mapping = get_district_mapping()
    data = data.copy()
    data["District Name"] = data["DISTRICT"].map(district_mapping)

    district_categories = (
        data.groupby(["DISTRICT", "District Name", "CATEGORY"])
        .size()
        .reset_index(name="Count")
        .pivot(index=["DISTRICT", "District Name"], columns="CATEGORY", values="Count")
        .fillna(0)
    )

    district_categories["Total"] = district_categories.sum(axis=1)
    district_categories = district_categories.sort_values("Total", ascending=True)
    district_categories = district_categories.drop("Total", axis=1)

    district_categories = district_categories.reset_index()
    district_categories["District Label"] = district_categories.apply(
        lambda x: f"{x['DISTRICT']} - {x['District Name']}", axis=1
    )

    fig_district = px.bar(
        district_categories,
        y="District Label",
        x=district_categories.columns[3:],
        orientation="h",
        title="Crime Categories by District",
        labels={"value": "Number of Incidents", "variable": "Category"},
        color_discrete_sequence=px.colors.qualitative.Set3,
    )

    fig_district.update_layout(
        showlegend=True,
        legend_title="Crime Categories",
        barmode="stack",
        height=600,
        yaxis={"title": "District"},
    )

    fig_district.for_each_trace(
        lambda t: t.update(name=CATEGORY_DISPLAY_NAMES.get(t.name, t.name))
    )

    st.plotly_chart(fig_district, use_container_width=True)


def render_category_breakdown(data):
    with st.expander("View Complete Categorization Details"):
        categorization_df = (
            data.groupby(["OFFENSE_DESCRIPTION", "CATEGORY"])
            .size()
            .reset_index(name="Count")
            .sort_values(["CATEGORY", "Count"], ascending=[True, False])
        )

        total_by_category = categorization_df.groupby("CATEGORY")["Count"].transform(
            "sum"
        )
        categorization_df["% of category"] = (
            categorization_df["Count"] / total_by_category * 100
        ).round(2)

        unique_categories = categorization_df["CATEGORY"].unique()
        yearly_changes = {
            cat: calculate_yearly_change(data, cat) for cat in unique_categories
        }

        categorization_df["% Change YoY"] = (
            categorization_df["CATEGORY"].map(yearly_changes).round(2)
        )

        categorization_df = categorization_df.sort_values(
            ["Count", "CATEGORY"], ascending=[False, True]
        )

        st.text("Search for specific offense descriptions:")
        search = st.text_input(
            "Search", key="offense_search", label_visibility="collapsed"
        )
        categorization_df["Category"] = display_categories(
            categorization_df["CATEGORY"]
        )
        display_cols = [
            "OFFENSE_DESCRIPTION",
            "Category",
            "Count",
            f"% of category",
            "% Change YoY",
        ]
        if search:
            filtered_df = categorization_df[
                categorization_df["OFFENSE_DESCRIPTION"].str.contains(
                    search, case=False
                )
            ]
            st.dataframe(filtered_df[display_cols], use_container_width=True)
        else:
            st.dataframe(categorization_df[display_cols], use_container_width=True)


def temporal_analysis(data):
    tab1, tab2, tab3 = st.tabs(["Daily", "Monthly", "Yearly"])

    with tab1:
        daily_crimes = (
            data["DAY_OF_WEEK"]
            .value_counts()
            .reindex(
                [
                    "Monday",
                    "Tuesday",
                    "Wednesday",
                    "Thursday",
                    "Friday",
                    "Saturday",
                    "Sunday",
                ]
            )
        )
        fig_daily = px.bar(
            x=daily_crimes.index,
            y=daily_crimes.values,
            title="Incidents by Day of Week",
            labels={"x": "Day of the week", "y": "Number of Incidents"},
        )
        st.plotly_chart(fig_daily, use_container_width=True)

    with tab2:
        monthly_crimes = data["MONTH"].value_counts().sort_index()
        month_names = {i: calendar.month_name[i] for i in monthly_crimes.index}
        monthly_crimes.index = monthly_crimes.index.map(month_names)

        fig_monthly = px.line(
            x=monthly_crimes.index,
            y=monthly_crimes.values,
            title="Monthly Crime Trend",
            labels={"x": "Month", "y": "Number of Incidents"},
        )
        st.plotly_chart(fig_monthly, use_container_width=True)

    with tab3:
        yearly_crimes = data["YEAR"].value_counts().sort_index()
        fig_yearly = px.bar(
            x=yearly_crimes.index,
            y=yearly_crimes.values,
            title="Yearly Distribution",
            labels={"x": "Year", "y": "Number of Incidents"},
        )
        st.plotly_chart(fig_yearly, use_container_width=True)


def crime_patterns(data):
    top_crimes = data["CATEGORY"].value_counts()
    fig_crimes = px.pie(
        values=top_crimes.values,
        names=display_categories(top_crimes.index),
        title="Crime Categories Distribution",
    )
    st.plotly_chart(fig_crimes, use_container_width=True)


def display_categories(series):
    """Convert category codes to display names"""
    return series.map(CATEGORY_DISPLAY_NAMES)


def show_insights():
    st.title("Crime Data Insights")
    df = load_data()

    # 1. Basic Statistics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Incidents", len(df))
    with col2:
        st.metric("Unique Crime Types", df["OFFENSE_CODE"].nunique())
    with col3:
        st.metric("Districts Covered", df["DISTRICT"].nunique())

    # 2. Time Analysis
    st.subheader("Temporal Patterns")
    temporal_analysis(df)

    # 3. Crime Patterns
    st.subheader("Crime Categories")
    crime_patterns(df)

    # Add categorization breakdown
    render_category_breakdown(df)

    # 4. Geographic Analysis
    st.subheader("Geographic Distribution")
    geographical_analysis(df)

    # 5. Cateorical Heatmap
    st.subheader("Categorical Incidents Heatmap")
    render_category_heatmap(df)


if __name__ == "__main__":
    st.set_page_config(
        page_title="Boston Crime Analysis",
        initial_sidebar_state="expanded",
    )
    show_insights()
