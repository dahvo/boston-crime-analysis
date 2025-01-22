import streamlit as st

# Define metadata as a dictionary for cleaner management
metadata = {
    "title": "Boston Crime Analysis Dashboard",
    "description": "Interactive dashboard analyzing crime patterns in Boston using BPD incident reports from 2020-2024. Features comprehensive crime analysis, temporal patterns, and geographic distribution.",
    "image": "https://raw.githubusercontent.com/dahvo/boston-crime-analysis/main/src/content/Screenshot.png",
    "url": "https://dahvo-boston-crime-analysis-srchome-zidpiq.streamlit.app",
}


def inject_custom_html():
    custom_html = f"""
        <head>
            <title>{metadata['title']}</title>
            <meta property="og:title" content="{metadata['title']}">
            <meta property="og:description" content="{metadata['description']}">
            <meta property="og:image" content="{metadata['image']}">
            <meta property="og:url" content="{metadata['url']}">
            <meta property="og:type" content="website">
        </head>
    """
    st.markdown(custom_html, unsafe_allow_html=True)


@st.cache_data
def load_content():
    with open("src/content/home.md", "r", encoding="utf-8") as f:
        return f.read()


def render_markdown():
    st.markdown(load_content())


def main():
    # Configure the page with the same metadata
    st.set_page_config(
        page_title=metadata["title"],
        page_icon="🚔",
        menu_items={"About": metadata["description"]},
    )

    inject_custom_html()
    render_markdown()


if __name__ == "__main__":
    main()
