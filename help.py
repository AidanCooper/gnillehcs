dynamic_help = """
Optionally specify start and end thresholds for each group. If selected, the groups'
thresholds will change linearly throughout the simulation between these values. The
High-to-Low checkboxes configure whether to use the high or low value of the range
sliders as the start and end points for each group
"""

threshold_help = """
Thresholds are percentages, with values between -1.00 an 1.00. A negative threshold is
interpreted as a 'diversity-seeking' group. That is, rather than moving when their
neighbourhood has similarity below their absolute threshold value (as per the
conventional Schelling segregation model), they move when their neigbourhood has
similarity above their absolute threshold value.
"""

n_neighbours_help = """
The depth of a home's neighbourhood to consider when computing the similarity score.
E.g. n_neighbours=2 considers a 5x5 grid of homes, where the home being evaluated is at
the centre.
"""

htl_help = """
If checked, the high value of this group's range slider will be used as the start
threshold, and the low value will be used as the end threshold. The group's threshold
will change linearly between these values over the course of the simulation.
"""
