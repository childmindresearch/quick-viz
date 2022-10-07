#!/usr/bin/env python

"""
Example usage:

python plot_nii_3dheatmap.py /path/to/my/data.nii.gz /path/to/my/data_tsv_image.png

"""

from argparse import ArgumentParser
from nilearn.plotting import plot_img
import matplotlib.pyplot as plt
import nibabel as nib


def main():
    parser = ArgumentParser("Produce a 3D intensity view of the brain")
    parser.add_argument('in_nii', help="3D Nifti data to visualize")
    parser.add_argument('plot_loc', help="Target location for plot")

    # TODO:
    #  - accept function option, to turn 4D data into 3D (e.g., mean)
    #  - accept coordinates option to ensure reproduc- and customiz-ability
    #  - support contrasting images

    results = parser.parse_args()

    im = nib.load(results.in_nii)
    plot_img(im, black_bg=False, output_file=results.plot_loc)


if __name__ == "__main__":
    main()

