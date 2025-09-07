from embedding import compute_embeddings
from clustering import tsne_cluster
from grouping import group_by_cosine_similarity, plotly_cosine_dendrogram
import pandas as pd
import plotly.express as px
import streamlit as st


def compute_and_assign_embeddings_tsne(newsletters, perplexity=3):
    if not newsletters:
        return
    texts = [n.title + " " + n.content for n in newsletters]
    embeddings = compute_embeddings(texts)
    for n, emb in zip(newsletters, embeddings):
        n.embedding = emb
    X_embedded = tsne_cluster(embeddings, perplexity=perplexity)
    for n, tsne_coords in zip(newsletters, X_embedded):
        n.tsne = list(tsne_coords)


def tsne_visualization(newsletters, color_by=None):
    """
    Visualizes t-SNE clustering for the given newsletters using their attributes.
    Optionally colors by a filter key (color_by).
    """
    st.subheader("t-SNE Visualization of News Embeddings")
    embeddings = [n.embedding for n in newsletters]
    tsne_coords = [n.tsne for n in newsletters]
    if any(e is None for e in embeddings) or any(t is None for t in tsne_coords):
        texts = [n.title + " " + n.content for n in newsletters]
        embeddings = compute_embeddings(texts)
        X_embedded = tsne_cluster(embeddings, perplexity=3)
        for n, emb, tsne_val in zip(newsletters, embeddings, X_embedded):
            n.embedding = emb
            n.tsne = list(tsne_val)
        tsne_coords = [n.tsne for n in newsletters]
    df_vis = pd.DataFrame(tsne_coords, columns=["x", "y"])
    df_vis["title"] = [n.title for n in newsletters]
    # Add color column if color_by or color_override is specified
    color_arg = None
    if (
        hasattr(tsne_visualization, "color_override")
        and tsne_visualization.color_override is not None
    ):
        df_vis["color"] = tsne_visualization.color_override
        color_arg = "color"
    elif color_by:

        def get_color_val(n):
            if hasattr(n, "filters") and n.filters and color_by in n.filters:
                val = n.filters[color_by]
                # If the filter value is a dict with 'match', use that
                if isinstance(val, dict) and "match" in val:
                    return val["match"]
                return val
            return None

        df_vis["color"] = [get_color_val(n) for n in newsletters]
        color_arg = "color"
    fig = px.scatter(
        df_vis,
        x="x",
        y="y",
        hover_name="title",
        color=color_arg,
        title=f"t-SNE Clustering of Newsletters"
        + (
            f" (colored by tag)"
            if hasattr(tsne_visualization, "color_override")
            and tsne_visualization.color_override is not None
            else (f" (colored by '{color_by}')" if color_by else "")
        ),
        width=600,
        height=600,
    )
    st.plotly_chart(fig, use_container_width=True)


# --- Grouped Articles Function ---
def grouped_articles(newsletters):
    embeddings = [n.embedding for n in newsletters]
    st.subheader("Grouped Articles (Cosine Similarity > 0.7)")
    groups = group_by_cosine_similarity(embeddings, threshold=0.7)
    for group_id, indices in groups.items():
        with st.expander(f"Group {group_id+1} ({len(indices)} articles)"):
            for idx in indices:
                n = newsletters[idx]
                st.markdown(f"**Title:** {n.title}")
                st.markdown(
                    f"**Date:** {n.publication_date.strftime('%A, %d %B %Y %H:%M')}"
                )
                st.markdown(f"**URL:** [{n.url}]({n.url})" if n.url else "**URL:** N/A")
                st.markdown(f"**Content:**\n\n{n.content}", unsafe_allow_html=True)
                st.markdown("---")


# --- Dendrogram Visualization Function ---
def dendrogram_visualization(newsletters):
    st.subheader("Interactive Cosine Similarity Dendrogram")
    embeddings = [n.embedding for n in newsletters]
    dendro_fig = plotly_cosine_dendrogram(embeddings, [n.title for n in newsletters])
    st.plotly_chart(dendro_fig, use_container_width=True)
