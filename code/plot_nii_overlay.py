#!/usr/bin/env python

"""
Example usage:

python plot_nii_overlay.py /path/to/my/data.nii.gz \
                           /path/to/my/image.png \
                           -b /path/to/reference/data.nii.gz \
                           -v 1 \
                           --cmap inferno \
                           -- t Title of the plot \
                           --alpha 0.5 \
                           --threshold 10

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
    parser.add_argument('-v', '--volume', type=int,
                        help="Single 3D volume from a 4D stack to show")
    parser.add_argument('--cmap', default='viridis', help="Colormap for visualization")
    parser.add_argument('-t', '--title', type=str,
                        help="Title for the image")
    parser.add_argument('--alpha', default=0.8, help="Opacity for overlay visualization")
    parser.add_argument('--threshold', default=20, help="Threshold for the plot")

    results = parser.parse_args()

    im = nib.load(results.in_nii)
    if results.volume is not None:
        v = results.volume
        im = nib.Nifti1Image(im.get_fdata()[:,:,:,v], header=im.header, affine=im.affine)

    lb = np.percentile(np.sort(np.unique(im.get_fdata())), float(results.threshold))

    if results.background:
        bg = nib.load(results.background)
        title_font_size = max(10, min(20, 1000 / len(results.title)))
        plot_stat_map(im, bg_img = bg, output_file=results.plot_loc,
                      black_bg=True, threshold=lb, title=results.title, cmap=results.cmap, alpha=float(results.alpha))
    else:
        title_font_size = max(10, min(20, 1000 / len(results.title)))
        plot_stat_map(im, output_file=results.plot_loc,
                      black_bg=True, threshold=lb, title=results.title, cmap=results.cmap, alpha=float(results.alpha))


if __name__ == "__main__":
    main()

