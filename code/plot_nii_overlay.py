#!/usr/bin/env python

"""
Example usage:

python plot_nii_overlay.py /path/to/my/data.nii.gz \
                           /path/to/my/data_tsv_image.png \
                           -b /path/to/reference/data.nii.gz

"""

from argparse import ArgumentParser
from nilearn.plotting import plot_stat_map
import matplotlib.pyplot as plt
import nibabel as nib
import numpy as np


def main():
    parser = ArgumentParser("Produce a 3D intensity view of a brain on another")
    parser.add_argument('in_nii', help="3D Nifti data to visualize")
    parser.add_argument('plot_loc', help="Target location for plot")
    parser.add_argument('-b', '--background', help="Background (reference) image")


    # TODO:
    #  - accept function option, to turn 4D data into 3D (e.g., mean)
    #  - accept coordinates option to ensure reproduc- and customiz-ability

    results = parser.parse_args()

    im = nib.load(results.in_nii)
    lb = np.percentile(np.sort(np.unique(im.get_fdata())), 20)
    if results.background:
        bg = nib.load(results.background)
        plot_stat_map(im, bg_img = bg, output_file=results.plot_loc,
                      black_bg=True, threshold=lb)
    else:
        plot_stat_map(im, output_file=results.plot_loc,
                      black_bg=True, threshold=lb)


if __name__ == "__main__":
    main()

