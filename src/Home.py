import streamlit as st

metadata = {
    "title": "Boston Crime Analysis Dashboard",
    "description": "Interactive dashboard analyzing crime patterns in Boston using BPD incident reports from 2020-2024. Features comprehensive crime analysis, temporal patterns, and geographic distribution.",
    "image": "https://raw.githubusercontent.com/dahvo/boston-crime-analysis/main/src/content/Screenshot.png",
    "url": "https://dahvo-boston-crime-analysis-srchome-zidpiq.streamlit.app",
}


def inject_metadata():
    meta_tags = [
        f'<title>{metadata["title"]}</title>',
        '<meta charset="utf-8">',
        f'<meta name="description" content="{metadata["description"]}">',
        f'<meta property="og:title" content="{metadata["title"]}">',
        f'<meta property="og:description" content="{metadata["description"]}">',
        f'<meta property="og:image" content="{metadata["image"]}">',
        f'<meta property="og:url" content="{metadata["url"]}">',
        '<meta property="og:type" content="website">',
    ]

    meta_html = "\n".join(meta_tags)
    st.markdown(meta_html, unsafe_allow_html=True)


@st.cache_data
def load_content():
    with open("src/content/home.md", "r", encoding="utf-8") as f:
        return f.read()


def render_markdown():
    st.markdown(load_content())


def main():
    st.set_page_config(
        page_title=metadata["title"],
        page_icon="🚔",
        layout="wide",
        menu_items={
            "About": metadata["description"],
            "Get Help": metadata["url"],
        },
    )

    inject_metadata()

    content = load_content()
    st.markdown(content)


if __name__ == "__main__":
    main()
