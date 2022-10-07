#!/usr/bin/env python

"""
Example usage:

python plot_nii_similarity.py /path/to/my/data1.nii.gz \
                              /path/to/my/data2.nii.gz \
                              /path/to/my/image.png

"""

from argparse import ArgumentParser
from nilearn.maskers import NiftiMasker
from nistats.reporting import compare_niimgs
import matplotlib.pyplot as plt
import nibabel as nib
import numpy as np


def main():
    parser = ArgumentParser("Produce a 3D intensity view of a brain on another")
    parser.add_argument('im1', help="First 3D Nifti data to compare")
    parser.add_argument('im2', help="Second 3D Nifti data to compare")
    parser.add_argument('plot_loc', help="Target location for plot")

    results = parser.parse_args()

    im1 = nib.load(results.im1)
    im2 = nib.load(results.im2)

    masker = NiftiMasker()
    masker.fit(im1)

    compare_niimgs([im1], [im2], masker,
                   ref_label=results.im1, src_label=results.im2)
    plt.savefig(results.plot_loc)


if __name__ == "__main__":
    main()

