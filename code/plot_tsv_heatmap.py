#!/usr/bin/env python

"""
Example usage:

python plot_tsv_heatmap.py /path/to/my/data.tsv /path/to/my/image.png

"""

from argparse import ArgumentParser
import matplotlib.pyplot as plt
import numpy as np


def main():
    parser = ArgumentParser("Produce a heatmap from a TSV")
    parser.add_argument('in_tsv', help="TSV data to visualize")
    parser.add_argument('plot_loc', help="Target location for plot")
    # TODO:
    #  - accept delimiter option
    #  - accept scaling options

    results = parser.parse_args()

    mat = np.loadtxt(results.in_tsv, delimiter='\t')
    fig = plt.imshow(mat)

    plt.savefig(results.plot_loc)


if __name__ == "__main__":
    main()

