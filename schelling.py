"""Schelling's model of segregation"""

from typing import Union, List

import numpy as np


class Schelling:
    """Schelling's model of segregation

    Attributes
    ----------
    n_population : int
        The number of homes to simulate. A map will be created as a 2D grid containing
        this number of cells (rounded down to the nearest square number).
    groups : Union[int, List[float]]
        Providing an integer will produce that many groups (of equal size). A list of
        floats is interpreted as percentages of the population that belong to each
        group. If a list of floats is provided, they must be positive and sum to less
        than 1. The remainder will be used to overwrite the `pct_empty` attribute.
    thresholds: Union[float, List[float]]
        Providing a float will specify the similarity threshold to be used by all
        groups. A list of floats can be provided to specify the similarity thresholds
        for each group individually. If a list of floats is provided, it must be of
        equal length to the number of groups.
    pct_empty : float
        The percentage of homes that are empty. This attribute will be overwritten if
        `groups` is provided a list of floats.
    n_neighbours : int
        The depth of a home's neighbourhood to consider when computing the similarity
        score. E.g. n_neighbours=2 considers a 5x5 grid of homes, where the home being
        evaluated is at the centre.

    Methods
    -------
    run()
        Run a single iteration of Schelling's model of segregation.
    mean_similarity_score()
        Compute the mean similarity score across all homes in the population.
    """

    def __init__(
        self,
        population: int,
        groups: Union[int, List[float]] = 2,
        thresholds: Union[float, List[float]] = 0.5,
        pct_empty: float = 0.25,
        n_neighbours: int = 2,
    ) -> None:
        assert population > 0, "population must be a positive integer"
        self.population = population

        assert pct_empty > 0 and pct_empty < 1, "pct_empty must be between 0 and 1"
        self.pct_empty = pct_empty

        if isinstance(groups, int):
            self.groups = [self.pct_empty] + [
                (1 - self.pct_empty) / groups for _ in range(groups)
            ]
        else:
            assert sum([v > 0 and v < 1 for v in groups]) == len(
                groups
            ), "Group values must be between 0 and 1"
            assert sum(groups) < 1, "The sum of groups must be less than 1"
            self.pct_empty = 1 - sum(groups)
            self.groups = [self.pct_empty] + groups

        if isinstance(thresholds, float):
            assert (
                thresholds > 0 and thresholds < 1
            ), "Threshold must be between 0 and 1"
            self.thresholds = [thresholds for _ in self.groups]
        else:
            assert sum([v > 0 and v < 1 for v in thresholds]) == len(
                thresholds
            ), "Threshold values must be between 0 and 1"
            assert (
                len(thresholds) == len(self.groups) - 1
            ), "The count of threshold values must match the count of groups"
            self.thresholds = [None] + thresholds

        assert n_neighbours > 0, "n_neighbours must be a positive integer"
        self.n_neighbours = n_neighbours

        # Initialise map
        self.length = int(np.sqrt(self.population))
        self.homes = np.random.choice(
            [n for n in range(len(groups) + 1)], size=self.length**2, p=self.groups
        )
        self.map = np.reshape(self.homes, (self.length, self.length))

    def run(self):
        ...


if __name__ == "__main__":
    s = Schelling(
        36,
        groups=[0.3, 0.2, 0.1],
        thresholds=[0.21134, 0.3, 0.1],
        pct_empty=0.15,
    )
    print(s.groups)
    print(s.thresholds)
    print(s.pct_empty)
    print(s.map)
