"""Streamlit app for Schelling's model of segregation"""

import streamlit as st

from plots import plot_map_and_similarity_score, plot_thresholds
from schelling import Schelling

# Streamlit App
st.title("Schelling's Model of Segregation")

# configurables
population = st.sidebar.slider("Number of homes", 100, 10_000, 2500)
n_groups = st.sidebar.number_input("Number of groups", 2, 8)
thresholds = []
for g in range(n_groups):
    thresholds.append(st.sidebar.slider(f"Threshold Group {g+1}", -1.0, 1.0, 0.4))
pct_empty = st.sidebar.slider("Percent of homes that are empty", 0.01, 0.99, 0.2)
n_iterations = st.sidebar.number_input("Number of iterations", 10)
n_neighbours = st.sidebar.number_input("Depth of neighbourhood to consider", 1)

# instantiate Schelling's model of segregation
schelling = Schelling(
    population,
    groups=n_groups,
    thresholds=thresholds,
    pct_empty=pct_empty,
    n_neighbours=n_neighbours,
)

# track mean similarity scores
mean_similarity_score = []
mean_similarity_score.append(schelling.mean_similarity_score())

# track threshold values
threshold_vals = []
for threshold in schelling.thresholds[1:]:
    threshold_vals.append([threshold])

# plot map and similarity score
fig_map, ax_map = plot_map_and_similarity_score(
    schelling, mean_similarity_score, n_iterations
)
plots_top = st.pyplot(fig_map)

# plot thresholds
fig_thresholds, ax_thresholds = plot_thresholds(threshold_vals, n_iterations)
plot_bottom = st.pyplot(fig_thresholds)

# plot progress
progress_bar = st.progress(0)

# run model
if st.sidebar.button("Run"):
    for i in range(n_iterations):
        schelling.run()

        # update mean similarity scores and thresholds
        mean_similarity_score.append(schelling.mean_similarity_score())
        for g, t in enumerate(schelling.thresholds[1:]):
            threshold_vals[g].append(t)

        # plot map and similarity score
        fig_map, ax_map = plot_map_and_similarity_score(
            schelling, mean_similarity_score, n_iterations
        )
        plots_top.pyplot(fig_map)

        # plot thresholds
        fig_thresholds, ax_thresholds = plot_thresholds(threshold_vals, n_iterations)
        plot_bottom.pyplot(fig_thresholds)

        # plot progress
        progress_bar.progress((i + 1.0) / n_iterations)
