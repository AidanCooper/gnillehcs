"""Streamlit app for Schelling's model of segregation"""

import matplotlib.pyplot as plt
import streamlit as st
from matplotlib.colors import ListedColormap

from schelling import Schelling

plt.style.use("style.mplstyle")

# Streamlit App

st.title("Schelling's Model of Segregation")

population = st.sidebar.slider("Number of homes", 100, 10_000, 2500)
n_groups = st.sidebar.number_input("Number of groups", 2)
pct_empty = st.sidebar.slider("Percent of homes that are empty", 0.01, 0.99, 0.2)
threshold = st.sidebar.slider("Threshold", 0.0, 1.0, 0.4)
n_iterations = st.sidebar.number_input("Number of iterations", 10)
n_neighbours = st.sidebar.number_input("Depth of neighbourhood to consider", 1)


# Instantiate Schelling's model of segregation
schelling = Schelling(
    population,
    groups=n_groups,
    thresholds=threshold,
    pct_empty=pct_empty,
    n_neighbours=n_neighbours,
)
mean_similarity_score = []
mean_similarity_score.append(schelling.mean_similarity_score())


def plot():
    fig, ax = plt.subplots(1, 2, figsize=(16, 6))

    # map plot
    colours = [
        "white",
        "#003f5c",
        "#d45087",
        "#ffa600",
        "#665191",
        "#ff7c43",
        "#2f4b7c",
        "#f95d6a",
        "#a05195",
    ]
    cmap = ListedColormap([colours[i] for i in range(n_groups + 1)])
    ax[0].pcolor(schelling.map, cmap=cmap, edgecolors="w", linewidths=1)
    ax[0].axis("off")

    # similarity score plot
    ax[1].set_xlabel("iteration")
    ax[1].set_xlim([0, n_iterations])
    ax[1].set_ylim([0, 1])
    ax[1].set_title("Mean Similarity Score")
    ax[1].plot(range(1, len(mean_similarity_score) + 1), mean_similarity_score)
    ax[1].text(
        1, 0.95, f"Similarity Ratio: {mean_similarity_score[-1]:.4f}", fontsize=10
    )
    ax[1].grid()
    return fig, ax


fig, ax = plot()
plots = st.pyplot(fig)
progress_bar = st.progress(0)

if st.sidebar.button("Run"):
    for i in range(n_iterations):
        schelling.run()
        mean_similarity_score.append(schelling.mean_similarity_score())
        fig, ax = plot()
        plots.pyplot(fig)
        progress_bar.progress((i + 1.0) / n_iterations)
