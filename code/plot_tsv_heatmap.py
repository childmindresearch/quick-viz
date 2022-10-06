#!/usr/bin/env python

from argparse import ArgumentParser
import matplotlib.pyplot as plt
import numpy as np



def main():
    parser = ArgumentParser()
    parser.add_argument('in_tsv')
    parser.add_argument('plot_loc')

    results = parser.parse_args()

    mat = np.loadtxt(results.in_tsv, delimiter='\t')
    fig = plt.imshow(mat)

    plt.savefig(results.plot_loc)


if __name__ == "__main__":
    main()

