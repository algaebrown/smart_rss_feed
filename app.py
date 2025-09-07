import streamlit as st
from src.ingest import ingest_newsletters_from_feed
from src.visualization import compute_and_assign_embeddings_tsne, tsne_visualization
from src.llm_tagging import filter_newsletters_with_ai
from src.grouping import render_similar_articles
from src.web_search import find_full_text
import pandas as pd
import datetime
import logging

logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

st.set_page_config(page_title="Smart Newsletter Dashboard", layout="wide")
st.title("Smart Newsletter Dashboard")

# --- Load Newsletters and Compute Embeddings/tSNE on Startup ---
import datetime
feed_path = st.text_input("RSS/XML Feed Path", value="data/master_feed.xml")

if 'newsletters' not in st.session_state:
    newsletters = ingest_newsletters_from_feed(feed_path)
    compute_and_assign_embeddings_tsne(newsletters, perplexity=3)
    st.session_state['newsletters'] = newsletters[:30]  # Limit to first 30 for performance
else:
    newsletters = st.session_state['newsletters']

# --- Date Filter ---
today = datetime.date.today()
st.sidebar.header("Date Filter")
start_date = st.sidebar.date_input("Start Date", value=today)
end_date = st.sidebar.date_input("End Date", value=today)

def apply_date_filter(newsletters, start_date, end_date):
    for n in newsletters:
        n.filters = n.filters or {}
        n.filters['date_filter'] = (
            (not start_date or n.publication_date.date() >= start_date)
            and (not end_date or n.publication_date.date() <= end_date)
        )
apply_date_filter(newsletters, start_date, end_date)

# --- Keyword Filter ---
st.sidebar.header("Keyword Filter")
def apply_keyword_filter(newsletters, keyword):
    keyword_lower = keyword.lower()
    for n in newsletters:
        n.filters = n.filters or {}
        match = keyword_lower in n.title.lower()
        n.filters[f"{keyword}"] = {"match": match}
    return newsletters
keyword = st.sidebar.text_input("Keyword to filter (title, case-insensitive)", value="")
if keyword:
    if st.sidebar.button(f"Apply Keyword Filter: '{keyword}'"):
        newsletters = apply_keyword_filter(newsletters, keyword)
        st.session_state['newsletters'] = newsletters
        st.sidebar.success(f"Keyword filter '{keyword}' applied to newsletters.")

# --- AI Filter ---
st.sidebar.header("AI Filtering")
ai_provider = st.sidebar.selectbox(
    "Choose AI Provider",
    ["OpenAI", "Claude", "Google", "Ollama (local)"],
    index=2  # Default to 'Google'
)
openai_api_key = st.sidebar.text_input("OpenAI API Key", type="password") if ai_provider == "OpenAI" else None
claude_api_key = st.sidebar.text_input("Claude API Key", type="password") if ai_provider == "Claude" else None
gemini_api_key = st.sidebar.text_input("Gemini API Key", type="password") if ai_provider == "Google" else None
ollama_url = st.sidebar.text_input("Ollama URL", value="http://localhost:11434/api/generate") if ai_provider == "Ollama (local)" else None
user_prompt = st.sidebar.text_area("AI Filter Prompt", help="e.g. Show me newsletters about AI published last week")
ai_filter_key = st.sidebar.text_input("AI Filter Name", value="AI_filter", help="Name for this AI filter (e.g. 'AI_filter', 'topic_filter', etc.)")
if user_prompt and ai_filter_key and st.sidebar.button("Apply AI Filter"):
    filter_newsletters_with_ai(
        newsletters, user_prompt, ai_provider,
        {
            "openai": openai_api_key,
            "claude": claude_api_key,
            "gemini": gemini_api_key
        },
        ollama_url=ollama_url,
        filter_key=ai_filter_key
    )
    st.session_state['newsletters'] = newsletters
    st.sidebar.success(f"AI filter '{ai_filter_key}' applied to newsletters.")

# --- Filter Selection for Display ---
st.sidebar.header("Filter Selection")
unique_filters = set()
for n in newsletters:
    if hasattr(n, 'filters') and n.filters:
        unique_filters.update(n.filters.keys())
selected_filters = st.sidebar.multiselect(
    "Select filters to show articles (AND logic):",
    sorted(unique_filters),
    default=[]
)
def filter_articles(newsletters, selected_filters):
    if not selected_filters:
        return newsletters
    filtered = []
    for n in newsletters:
        if all(
            (n.filters.get(f) is True) or
            (isinstance(n.filters.get(f), dict) and n.filters.get(f).get('match') is True)
            for f in selected_filters
        ):
            filtered.append(n)
    return filtered

filtered_newsletters = filter_articles(newsletters, selected_filters)

# --- Show Articles Button and Display ---


# --- Persistent Show/Hide Articles Logic ---
if 'show_articles' not in st.session_state:
    st.session_state['show_articles'] = False

if st.sidebar.button("Show Articles"):
    st.session_state['show_articles'] = True
if st.sidebar.button("Hide Articles"):
    st.session_state['show_articles'] = False

if st.session_state['show_articles']:
    col_header, col_btns = st.columns([0.7, 0.3])
    with col_header:
        st.subheader("Filtered Articles")
    with col_btns:
        select_all = st.button("Select All", key="select_all_btn")
        deselect_all = st.button("Deselect All", key="deselect_all_btn")
    if not filtered_newsletters:
        st.info("No articles match the selected filters.")
    else:
        for n in filtered_newsletters:
            # if user_selected is not an attribute of n
            if not hasattr(n, 'user_selected'):
                n.user_selected = False

            with st.container():
                col1, col2 = st.columns([0.05, 0.95])
                with col1:
                    checked = st.checkbox("", key=f"select_{n.title}", value=n.user_selected)
                with col2:
                    st.markdown(f"### <a href='{n.url}' target='_blank'>{n.title}</a>", unsafe_allow_html=True)
                    st.markdown(f"<div style='margin-bottom:1em'>{n.content}</div>", unsafe_allow_html=True)
                if checked:
                    n.user_selected = True
                else:
                    n.user_selected = False
        # Handle select/deselect all
        if select_all:
            for n in filtered_newsletters:
                n.user_selected = True
        if deselect_all:
            for n in filtered_newsletters:
                n.user_selected = False


# --- Similar Articles Sidebar Section ---
st.sidebar.header("Find Similar Articles as selected article")
selected_articles = [n for n in newsletters if n.user_selected]
deselected_articles = [n for n in newsletters if not n.user_selected and n.filters['date_filter'] is True]
sim_threshold = st.sidebar.slider("Cosine similarity threshold", min_value=0.0, max_value=1.0, value=0.7, step=0.01, key="similarity_threshold")

if st.sidebar.button("Show Similar Articles"):
    similar_articles = {}
    for n in selected_articles:
        results = render_similar_articles(n, deselected_articles, threshold=sim_threshold)
        # update the dict if similarity > existing similarity
        for art, sim in results.values():
            if art.title not in similar_articles or sim > similar_articles[art.title][1]:
                similar_articles[art.title] = (art,sim)
    st.session_state['similar_articles'] = similar_articles
    
        
if 'similar_articles' in st.session_state:
    st.header("Similar Articles to Selected Articles")
    for art, sim in st.session_state['similar_articles'].values():
        with st.container():
            col1, col2 = st.columns([0.05, 0.95])
            with col1:
                checked = st.checkbox("", key=f"select_similar_{art.title}", value=art.user_selected)
            with col2:
                st.markdown(f"### <a href='{art.url}' target='_blank'>{art.title}</a> (Similarity: {sim:.2f})", unsafe_allow_html=True)
                st.markdown(f"<div style='margin-bottom:1em'>{art.content}</div>", unsafe_allow_html=True)
            if checked:
                art.user_selected = True
            else:
                art.user_selected = False

# --- get full text for selected articles if not already present ---
def fetch_all_full_text(newsletters):
    for n in newsletters:
        if n.user_selected and not n.full_text:
            try:
                n.full_text = find_full_text(n.url, n.title)
            except Exception as e:
                logging.error(f"Error fetching full text for {n.url}: {e}")
# --- Export Selected Articles as CSV ---
st.sidebar.header("Export")


def export_as_csv(newsletters):
    fetch_all_full_text(newsletters)
    export_list = [n for n in newsletters if n.user_selected]
    if not export_list:
        st.sidebar.warning("No articles selected for export.")
        return
    df = pd.DataFrame([
        {
            'title': n.title,
            'content': n.content,
            'publication_date': n.publication_date,
            'url': n.url,
            'embedding': n.embedding,
            'tsne': n.tsne,
            'filters': n.filters,
            'date': n.publication_date.strftime('%Y-%m-%d %H:%M'),
            'full_text': n.full_text
        } for n in export_list
    ])
    csv = df.to_csv(index=False)
    st.sidebar.download_button("Download CSV", csv, file_name="selected_newsletters.csv", mime="text/csv")
if st.sidebar.button("Export Selected as CSV"):
    export_as_csv(newsletters)

# --- Export Selected Articles as Markdown ---
def export_as_markdown(newsletters):
    fetch_all_full_text(newsletters)
    export_list = [n for n in newsletters if n.user_selected]
    if not export_list:
        st.sidebar.warning("No articles selected for export.")
        return
    md = []
    for n in export_list:
        title_line = f"### [{n.title}]({n.url})" if n.url else f"### {n.title}"
        date_line = f"**Date:** {n.publication_date.strftime('%Y-%m-%d %H:%M')}"
        content_line = n.content
        md.append(f"{title_line}\n{date_line}\n\n{content_line}\n\n---\n")
        # add full text if available
        if n.full_text:
            md.append(f"**Full Text:**\n\n{n.full_text}\n\n---\n")
    markdown_str = "\n".join(md)
    st.sidebar.download_button("Download Markdown", markdown_str, file_name="selected_newsletters.md", mime="text/markdown")

if st.sidebar.button("Export Selected as Markdown"):
    export_as_markdown(newsletters)