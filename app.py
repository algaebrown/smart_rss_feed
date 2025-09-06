import streamlit as st
from src.ingest import ingest_newsletters_from_feed
from src.formatter import format_newsletter_for_email
from src.embedding import compute_embeddings
from src.clustering import tsne_cluster
from src.grouping import group_by_cosine_similarity, plotly_cosine_dendrogram
import pandas as pd
import plotly.express as px
from datetime import datetime

st.set_page_config(page_title="Smart Newsletter Dashboard", layout="wide")
st.title("Smart Newsletter Dashboard")

feed_path = st.text_input("RSS/XML Feed Path", value="data/master_feed.xml")

col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input("Start Date", value=None)
with col2:
    end_date = st.date_input("End Date", value=None)

if st.button("Load Newsletters"):
    newsletters = ingest_newsletters_from_feed(feed_path)
    if newsletters:
        # Filter by date
        if start_date:
            newsletters = [n for n in newsletters if n.publication_date.date() >= start_date]
        if end_date:
            newsletters = [n for n in newsletters if n.publication_date.date() <= end_date]
        st.success(f"Loaded {len(newsletters)} newsletters.")
        # Embedding and t-SNE visualization
        if newsletters:
            st.subheader("t-SNE Visualization of News Embeddings")
            texts = [n.title + " " + n.content for n in newsletters]
            embeddings = compute_embeddings(texts)
            X_embedded = tsne_cluster(embeddings, perplexity=3)
            df_vis = pd.DataFrame(X_embedded, columns=["x", "y"])
            df_vis["title"] = [n.title for n in newsletters]
            # Plot with Plotly for interactive hover (title only)
            fig = px.scatter(
                df_vis,
                x="x",
                y="y",
                hover_name="title",
                title="t-SNE Clustering of Newsletters",
                width=600,
                height=600
            )
            st.plotly_chart(fig, use_container_width=True)
            # Grouping by cosine similarity
            st.subheader("Grouped Articles (Cosine Similarity > 0.7)")
            groups = group_by_cosine_similarity(embeddings, threshold=0.7)
            for group_id, indices in groups.items():
                with st.expander(f"Group {group_id+1} ({len(indices)} articles)"):
                    for idx in indices:
                        n = newsletters[idx]
                        st.markdown(f"**Title:** {n.title}")
                        st.markdown(f"**Date:** {n.publication_date.strftime('%A, %d %B %Y %H:%M')}")
                        st.markdown(f"**URL:** [{n.url}]({n.url})" if n.url else "**URL:** N/A")
                        st.markdown(f"**Content:**\n\n{n.content}", unsafe_allow_html=True)
                        st.markdown("---")
            # Interactive Dendrogram Visualization
            st.subheader("Interactive Cosine Similarity Dendrogram")
            dendro_fig = plotly_cosine_dendrogram(embeddings, [n.title for n in newsletters])
            st.plotly_chart(dendro_fig, use_container_width=True)
        else:
            st.warning("No newsletters found in the selected date range.")
        # Show newsletter details
        for i, n in enumerate(newsletters, 1):
            with st.expander(f"{i}. {n.title}"):
                st.markdown(f"**Date:** {n.publication_date.strftime('%A, %d %B %Y %H:%M')}")
                st.markdown(f"**URL:** [{n.url}]({n.url})" if n.url else "**URL:** N/A")
                st.markdown(f"**Content:**\n\n{n.content}", unsafe_allow_html=True)
    else:
        st.warning("No newsletters found in the feed.")
else:
    st.info("Enter the feed path and click 'Load Newsletters' to view.")
