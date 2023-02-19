from schelling import Schelling


def main():
    population = 10000
    groups = 5
    pct_empty = 0.2
    threshold = 0.4
    n_iterations = 20
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


if __name__ == "__main__":
    main()
