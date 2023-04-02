from schelling import Schelling
from plots import plot_map_and_similarity_score


def main():
    population = 2500
    groups = 4
    pct_empty = 0.2
    threshold = [0.4, 0.42, 0.44, -0.46]
    n_iterations = 25
    schelling = Schelling(
        population=population,
        groups=groups,
        thresholds=threshold,
        pct_empty=pct_empty,
    )
    mean_similarity_scores = []
    for _ in range(n_iterations):
        schelling.run()
        mean_similarity_scores.append(schelling.mean_similarity_score())

    fig_map, ax_map = plot_map_and_similarity_score(
        schelling, mean_similarity_scores, n_iterations
    )
    fig_map.savefig("plots/map.png", dpi=1600)


if __name__ == "__main__":
    main()
