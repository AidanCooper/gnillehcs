"""Streamlit app for Schelling's model of segregation"""

import streamlit as st

from plots import plot_map_and_similarity_score, plot_thresholds
from schelling import Schelling
from help import dynamic_help, threshold_help, n_neighbours_help, htl_help

# Streamlit App
st.title("Gnillehcs' Model of Integration")

# configurables
population = st.sidebar.slider("Number of homes", 100, 10_000, 2500)
n_groups = st.sidebar.number_input("Number of groups", 2, 8)
dynamic_thresholds = st.sidebar.checkbox("Dynamic thresholds", help=dynamic_help)
directions = []
thresholds = []
boxes = []
for n, g in enumerate(range(n_groups)):
    if dynamic_thresholds:
        col1, col2 = st.sidebar.columns(2)
        boxes.append(
            col1.checkbox(f"Group {g + 1}: High-to-Low", value=True, help=htl_help)
        )
        htl = -1 if boxes[n] else 1  # high-to-low (-1) or low-to-high (+1)
        thresholds.append(
            col2.slider(
                f"Thresholds {g+1}",
                -1.0,
                1.0,
                [0.1 + 0.02 * n, 0.65 + 0.02 * n],
                help=threshold_help,
            )[::htl]
        )
    else:
        thresholds.append(
            [
                st.sidebar.slider(
                    f"Threshold Group {g+1}",
                    -1.0,
                    1.0,
                    0.4 + 0.02 * n,
                    help=threshold_help,
                )
            ]
        )

pct_empty = st.sidebar.slider("Percent of homes that are empty", 0.01, 0.99, 0.2)
n_iterations = st.sidebar.number_input("Number of iterations", 1, value=20)
n_neighbours = st.sidebar.number_input(
    "Depth of neighbourhood",
    1,
    value=1,
    help=n_neighbours_help,
)

# instantiate Schelling's model of segregation
schelling = Schelling(
    population,
    groups=n_groups,
    thresholds=[t[0] for t in thresholds],
    pct_empty=pct_empty,
    n_neighbours=n_neighbours,
)

# track mean similarity scores
mean_similarity_score = []
mean_similarity_score.append(schelling.mean_similarity_score())

# track threshold values
threshold_vals = []
deltas = []
for threshold in schelling.thresholds[1:]:
    threshold_vals.append([threshold])
if dynamic_thresholds:
    for threshold in thresholds:
        deltas.append((threshold[0] - threshold[1]) / n_iterations)
else:
    deltas.append(0)

# plot map and similarity score
fig_map, ax_map = plot_map_and_similarity_score(
    schelling, mean_similarity_score, n_iterations
)
plots_top = st.pyplot(fig_map)

# plot thresholds
if dynamic_thresholds:
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
            if dynamic_thresholds:
                schelling.thresholds[g + 1] -= deltas[g]

        # plot map and similarity score
        fig_map, ax_map = plot_map_and_similarity_score(
            schelling, mean_similarity_score, n_iterations
        )
        plots_top.pyplot(fig_map)

        # plot thresholds
        if dynamic_thresholds:
            fig_thresholds, ax_thresholds = plot_thresholds(
                threshold_vals, n_iterations
            )
            plot_bottom.pyplot(fig_thresholds)

        # plot progress
        progress_bar.progress((i + 1.0) / n_iterations)
