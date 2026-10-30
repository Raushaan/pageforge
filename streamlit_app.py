"""The PageForge web app. Run: streamlit run streamlit_app.py"""
import streamlit as st
import streamlit.components.v1 as components

from app.generator import generate_page
from app.llm import DEFAULT_MODEL
from app.prompts import active_version, list_versions
from app.renderer import render_page

st.set_page_config(page_title="PageForge", layout="wide")
st.title("PageForge")
st.caption("Describe a page. A local LLM plans it, Pydantic checks it, Jinja2 builds it.")

with st.sidebar:
    st.header("Settings")
    versions = list_versions()
    version = st.selectbox("Prompt version", versions, index=versions.index(active_version()))
    model = st.text_input("Ollama model", value=DEFAULT_MODEL)
    use_schema = st.toggle("Force JSON schema", value=True,
                           help="Off = the model only has to return JSON, not our exact shape.")

request = st.text_area("What page do you want?",
                       placeholder="A landing page for a family-run bakery in Oakland with a contact section")

if st.button("Generate page", type="primary", disabled=not request.strip()):
    with st.spinner("Generating with the local model..."):
        result = generate_page(request, prompt_version=version, model=model,
                               use_schema=use_schema, source="app")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Valid", "Yes" if result.success else "No")
    c2.metric("Attempts", result.attempts)
    c3.metric("Latency", f"{result.latency_s:.1f} s")
    c4.metric("Tokens", result.prompt_tokens + result.completion_tokens)

    if result.success:
        html = render_page(result.layout)
        st.download_button("Download HTML", html, file_name="page.html", mime="text/html")
        components.html(html, height=800, scrolling=True)
        with st.expander("Layout JSON"):
            st.json(result.layout.model_dump())
    else:
        st.error(result.error)
        with st.expander("Raw model output"):
            for i, raw in enumerate(result.raw_outputs, 1):
                st.code(raw, language="json")