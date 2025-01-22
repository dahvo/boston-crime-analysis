import streamlit as st

meta_tags = """
<meta property="og:title" content="Boston Crime Analysis Dashboard">
<meta property="og:description" content="Interactive dashboard analyzing crime patterns in Boston using BPD incident reports from 2020-2024. Features comprehensive crime analysis, temporal patterns, and geographic distribution.">
<meta property="og:image" content="src/content/Screenshot.png">
<meta property="og:url" content="https://boston-crime-analysis.streamlit.app">
<meta property="og:type" content="website">
"""


def inject_meta_tags():
    st.markdown(meta_tags, unsafe_allow_html=True)


@st.cache_data
def load_content():
    with open("src/content/home.md", "r", encoding="utf-8") as f:
        return f.read()


def render_markdown():
    st.markdown(load_content())


@st.cache_data
def load_html():
    with open("src/content/home.html", "r", encoding="utf-8") as f:
        file = f.read()
        print()
        return file


def main():
    st.set_page_config(
        page_title="Boston Crime Analysis",
        page_icon="🚔",
    )

    inject_meta_tags()
    render_markdown()


if __name__ == "__main__":
    main()
