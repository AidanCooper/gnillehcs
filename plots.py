"""matplotlib plots for Streamlit app"""

import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch

plt.style.use("style.mplstyle")


def plot_map_and_similarity_score(schelling, mean_similarity_score, n_iterations):
    plt.close()
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
    cmap = ListedColormap([colours[i] for i in range(len(schelling.groups))])
    ax[0].pcolor(schelling.map, cmap=cmap, edgecolors="w", linewidths=1)
    ax[0].axis("off")
    legend_elements = [
        Patch(
            facecolor=colours[i + 1],
            label=f"Group {i+1} (threshold={schelling.thresholds[i+1]:.2f})",
        )
        for i in range(len(schelling.groups) - 1)
    ]
    ax[0].legend(handles=legend_elements, loc=(0, len(schelling.groups) * -0.06))

    # similarity score plot
    ax[1].set_xlabel("iteration", size=14)
    ax[1].set_ylabel("similarity ratio", size=14)
    ax[1].set_xlim([0, n_iterations])
    ax[1].set_ylim([0, 1])
    ax[1].set_title("Mean Similarity Score")
    ax[1].plot(range(1, len(mean_similarity_score) + 1), mean_similarity_score, c="k")
    ax[1].text(
        1, 0.95, f"Similarity Ratio: {mean_similarity_score[-1]:.4f}", fontsize=14
    )
    ax[1].grid()
    return fig, ax


def plot_thresholds(threshold_vals, n_iterations):
    plt.close()
    fig, ax = plt.subplots(1, 1, figsize=(16, 6))
    for group in threshold_vals:
        ax.plot(range(1, len(group) + 1), group)
    ax.set_xlabel("iteration", size=14)
    ax.set_ylabel("threshold", size=14)
    ax.set_xlim([0, n_iterations])
    ax.set_ylim([-1, 1])
    ax.set_title("Group Thresholds")
    ax.grid()
    return fig, ax
