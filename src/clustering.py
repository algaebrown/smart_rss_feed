import numpy as np
from sklearn.manifold import TSNE
from typing import List
import matplotlib.pyplot as plt


def tsne_cluster(embeddings: List[List[float]], perplexity: int = 3) -> np.ndarray:
    X = np.array(embeddings)
    X_embedded = TSNE(
        n_components=2, learning_rate="auto", init="random", perplexity=perplexity
    ).fit_transform(X)
    return X_embedded


def plot_tsne(X_embedded: np.ndarray, show: bool = True, save_path: str = None):
    plt.figure(figsize=(8, 6))
    plt.plot(X_embedded[:, 0], X_embedded[:, 1], "o")
    plt.title("t-SNE Clustering")
    if save_path:
        plt.savefig(save_path)
    if show:
        plt.show()
