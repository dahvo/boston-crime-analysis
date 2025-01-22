import streamlit as st


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

    render_markdown()


if __name__ == "__main__":
    main()
