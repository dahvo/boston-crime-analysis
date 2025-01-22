import streamlit as st
import folium
from folium.plugins import HeatMap
from streamlit_folium import folium_static
import plotly.express as px
import pandas as pd
import calendar
from utils.helpers import load_data, get_district_mapping


@st.cache_data
def get_shootings_data(df):
    return df[df["SHOOTING"] == 1]


def create_map():
    """Create a new map instance"""
    return folium.Map(
        location=[42.32000, -71.057083], zoom_start=11, tiles="OpenStreetMap"
    )


def render_shooting_heatmap(data):
    valid_locations = data.dropna(subset=["Lat", "Long"])

    if len(valid_locations) == 0:
        st.warning("No valid location data available for heatmap")
        return

    m = create_map()

    years = valid_locations["YEAR"].unique()
    for year in years:
        year_data = valid_locations[valid_locations["YEAR"] == year]
        heat_data = [[row["Lat"], row["Long"]] for _, row in year_data.iterrows()]

        if heat_data:
            fg = folium.FeatureGroup(name=str(year))
            HeatMap(heat_data, radius=14, blur=10, max_zoom=13).add_to(fg)
            fg.add_to(m)

    folium.LayerControl().add_to(m)
    folium_static(m)


def geographical_analysis(data):

    district_stats = (
        data.groupby(["DISTRICT", "DISTRICT_NAME"])
        .size()
        .reset_index(name="Count")
        .sort_values("Count", ascending=False)
    )

    fig_district = px.bar(
        district_stats,
        x="DISTRICT",
        y="Count",
        title="Shootings by District",
        hover_data=["DISTRICT_NAME"],
    )
    st.plotly_chart(fig_district, use_container_width=True)

    district_details = district_stats.merge(
        pd.DataFrame(
            {
                "DISTRICT": get_district_mapping().keys(),
                "District Name": get_district_mapping().values(),
            }
        ),
        on="DISTRICT",
        how="right",
    ).fillna(0)

    district_details["% of Total Shootings"] = (
        district_details["Count"] / len(data) * 100
    ).round(2)

    with st.expander("View District Details"):
        st.dataframe(
            district_details[
                ["DISTRICT", "District Name", "Count", "% of Total Shootings"]
            ],
            use_container_width=True,
        )


def temporal_analysis(data):

    tab1, tab2, tab3 = st.tabs(["Daily", "Monthly", "Yearly"])

    with tab1:
        hourly = data["HOUR"].value_counts().sort_index()
        fig_hourly = px.bar(
            x=hourly.index,
            y=hourly.values,
            title="Shootings by Hour of Day",
            labels={"x": "Hour (24h)", "y": "Number of Incidents"},
        )
        st.plotly_chart(fig_hourly, use_container_width=True)

        dow_counts = (
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
        fig_dow = px.bar(
            x=dow_counts.index,
            y=dow_counts.values,
            title="Shootings by Day of Week",
            labels={"x": "Day of the Week", "y": "Number of Incidents"},
        )
        st.plotly_chart(fig_dow, use_container_width=True)

    with tab2:
        monthly = data["MONTH"].value_counts().sort_index()
        month_names = {i: calendar.month_name[i] for i in monthly.index}
        monthly.index = monthly.index.map(month_names)
        fig_monthly = px.line(
            x=monthly.index,
            y=monthly.values,
            title="Monthly Distribution",
            markers=True,
        )
        st.plotly_chart(fig_monthly, use_container_width=True)

    with tab3:
        yearly = data["YEAR"].value_counts().sort_index()
        fig_yearly = px.bar(
            x=yearly.index,
            y=yearly.values,
            title="Yearly Distribution",
            labels={"x": "Year", "y": "Number of Incidents"},
        )
        st.plotly_chart(fig_yearly, use_container_width=True)


def offense_analysis(data):

    offense_counts = data["OFFENSE_DESCRIPTION"].value_counts().head(10)
    fig_offense = px.pie(
        values=offense_counts.values,
        names=offense_counts.index,
        title="Top Shooting-Related Offense Types",
    )
    st.plotly_chart(fig_offense, use_container_width=True)


def show_insights():
    st.title("Boston Shootings Analysis")
    df = load_data()
    shootings = get_shootings_data(df)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Shootings", len(shootings))
    with col2:
        st.metric("Districts Affected", shootings["DISTRICT"].nunique())
    with col3:
        shooting_rate = round((len(shootings) / len(df) * 100), 2)
        st.metric(f"% of Total Crime", f"{shooting_rate}%")

    st.subheader("Temporal Patterns")
    temporal_analysis(shootings)

    st.subheader("Geographic Distribution")
    geographical_analysis(shootings)

    st.subheader("Shooting Hotspots")
    render_shooting_heatmap(shootings)

    st.subheader("Offense Analysis")
    offense_analysis(shootings)


if __name__ == "__main__":
    st.set_page_config(page_title="Boston Shootings Analysis")
    show_insights()
