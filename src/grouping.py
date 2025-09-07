import numpy as np
from typing import List, Dict
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import linkage, dendrogram
import plotly.figure_factory as ff

def group_by_cosine_similarity(embeddings: List[List[float]], threshold: float = 0.7) -> Dict[int, List[int]]:
    X = np.array(embeddings)
    sim_matrix = cosine_similarity(X)
    n = len(embeddings)
    groups = []
    assigned = set()
    for i in range(n):
        if i in assigned:
            continue
        group = [i]
        assigned.add(i)
        for j in range(i+1, n):
            if sim_matrix[i, j] > threshold and j not in assigned:
                group.append(j)
                assigned.add(j)
        groups.append(group)
    # Return as dict: group_id -> list of indices
    return {idx: group for idx, group in enumerate(groups)}

def plot_cosine_dendrogram(embeddings, titles, figsize=(10, 6), save_path=None, show=True):
    # Compute cosine distance matrix
    from sklearn.metrics.pairwise import cosine_distances
    X = np.array(embeddings)
    dist_matrix = cosine_distances(X)
    # Hierarchical clustering
    Z = linkage(dist_matrix, method='average')
    fig, ax = plt.subplots(figsize=figsize)
    dendrogram(
        Z,
        labels=titles,
        orientation='right',
        leaf_font_size=10,
        ax=ax
    )
    ax.set_title('Cosine Similarity Dendrogram')
    if save_path:
        plt.savefig(save_path)
    if show:
        plt.show()
    return fig, ax

def plotly_cosine_dendrogram(embeddings, titles):
    from sklearn.metrics.pairwise import cosine_distances
    import numpy as np
    X = np.array(embeddings)
    dist_matrix = cosine_distances(X)
    fig = ff.create_dendrogram(dist_matrix, labels=titles, orientation='top', color_threshold=None)
    fig.update_layout(width=900, height=600, title='Cosine Similarity Dendrogram (Interactive)')
    return fig

def render_similar_articles(selected_article, all_articles, threshold=0.7):
    """
    Given a selected article and a list of all articles (with .embedding),
    return a list of (article, similarity) tuples for articles with cosine similarity > threshold.
    The selected_article itself is excluded from the results.
    """
    import numpy as np
    from sklearn.metrics.pairwise import cosine_similarity
    if not hasattr(selected_article, 'embedding') or selected_article.embedding is None:
        return []
    selected_emb = np.array(selected_article.embedding).reshape(1, -1)
    results = {}
    for art in all_articles:
        if art is selected_article or not hasattr(art, 'embedding') or art.embedding is None or art.user_selected is True:
            # Skip articles already selected by user
            continue
        sim = cosine_similarity(selected_emb, np.array(art.embedding).reshape(1, -1))[0, 0]
        if sim > threshold:
            results[art.title] = (art, sim)
    # Sort by similarity descending
    return results
