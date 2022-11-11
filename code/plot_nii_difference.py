"""
Example usage:

python plot_nii_difference.py \
    -o vol_diff.png \
    --images /path/to/vol1.nii.gz /path/to/vol2.nii.gz \
    --masks /path/to/mask1.nii.gz /path/to/mask2.nii.gz \
    --labels vol1 vol2
"""

import argparse
import logging
import os
import pprint
from typing import List, Tuple, Optional

from matplotlib import pyplot as plt
from matplotlib.figure import Figure
from matplotlib.axes import Axes
from matplotlib.colors import LinearSegmentedColormap
import nibabel as nib
from nilearn import plotting as nilplt
from nilearn import image as nilimg

from viz_utils import find_value_lims, apply_mask

plt.rcParams["figure.dpi"] = 150

logging.basicConfig(
    format="%(asctime)s %(levelname)-8s %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
)


def main(args: argparse.Namespace):
    logging.info("Args:\n%s", pprint.pformat(args.__dict__))

    logging.info("Loading images")
    imgs = [nib.load(path) for path in args.images]
    assert len(imgs) == 2, "only two images supported"
    assert imgs[0].ndim == imgs[1].ndim, "both images should have the same ndim"
    assert len(args.labels) == 2, "two labels are required"

    if imgs[0].ndim == 4:
        # NOTE: indexing a 4d '.nii.gz' is slow bc you have to gunzip the whole file.
        # h5 with compressed chunks might be better..
        logging.info("Indexing images at %d", args.index)
        imgs[0] = nilimg.index_img(imgs[0], args.index)
        imgs[1] = nilimg.index_img(imgs[1], args.index + args.index_offset)
        index = args.index
    else:
        index = None

    if args.masks is not None:
        for ii, path in enumerate(args.masks):
            if os.path.exists(path):
                logging.info("Applying mask to image %d", ii)
                mask = nib.load(path)
                imgs[ii] = apply_mask(imgs[ii], mask)

    logging.info("Resampling img2 -> img1")
    img1, img2 = imgs
    img1 = nilimg.reorder_img(img1, resample=False)
    img2 = nilimg.reorder_img(img2, resample=False)
    img2 = nilimg.resample_to_img(img2, img1)

    cut_coords = tuple(float(val.strip()) for val in args.cut_coords.split(","))

    f, axs = plt.subplots(3, 1, figsize=(9, 9))
    logging.info("Plotting image")
    plot_difference_triplet(
        img1=img1,
        img2=img2,
        labels=args.labels,
        fig=f,
        axs=axs,
        index=index,
        cut_coords=cut_coords,
        vmax=args.vmax,
        colorbar=args.colorbar,
        fname=args.out,
    )

    logging.info("Done")


def plot_difference_triplet(
    *,
    img1: nib.Nifti1Image,
    img2: nib.Nifti1Image,
    labels: List[str],
    fig: Optional[Figure] = None,
    axs: Optional[List[Axes]] = None,
    index: Optional[int] = None,
    cut_coords: Tuple[float, float, float] = (1.0, 0.0, 0.0),
    vmin: Optional[float] = None,
    vmax: Optional[float] = None,
    colorbar: bool = False,
    fname: Optional[str] = None,
):
    """
    Plot `img1`, `img2`, and the difference `img1 - img2`.

    Args:
        img1: First volume.
        img2: Second volume.
        labels: List of two labels, one per volume.
        fig: Optional figure to plot into.
        axs: Optional list of three axes to plot into.
        index: Optional volume index (just for labeling).
        cut_coords: Ortho viewer cut coordinates. See
            `nilearn.plotting.plot_epi` for details.
        vmin: Optional vmin.
        vmax: Optional vmax.
        colorbar: Show the colorbar.
        fname: Optional image filename.
    """
    assert len(labels) == 2, "two labels expected"
    if fig is None:
        fig, axs = plt.subplots(3, 1, figsize=(9, 9))
    else:
        assert axs is not None, "axs is required with fig is provided"
        assert len(axs) == 3, "three Axes required"
        fig.clear()

    if vmin is None:
        vmin = 0.0
    if vmax is None:
        _, vmax1 = find_value_lims(img1.get_fdata())
        _, vmax2 = find_value_lims(img2.get_fdata())
        vmax = max(vmax1, vmax2)

    title = labels[0] if index is None else f"{labels[0]} ({index:04d})"
    nilplt.plot_epi(
        img1,
        figure=fig,
        axes=axs[0],
        colorbar=colorbar,
        cut_coords=cut_coords,
        draw_cross=True,
        vmin=vmin,
        vmax=vmax,
        cmap="gray",
        title=title,
    )

    nilplt.plot_epi(
        img2,
        figure=fig,
        axes=axs[1],
        colorbar=colorbar,
        cut_coords=cut_coords,
        draw_cross=True,
        vmin=vmin,
        vmax=vmax,
        cmap="gray",
        title=labels[1],
    )

    diff = nib.Nifti1Image(img1.dataobj - img2.dataobj, img1.affine)
    nilplt.plot_epi(
        diff,
        figure=fig,
        axes=axs[2],
        colorbar=colorbar,
        cut_coords=cut_coords,
        draw_cross=True,
        vmin=-vmax,
        vmax=vmax,
        cmap=LinearSegmentedColormap.from_list(
            "cold_hot",
            ["cyan", "blue", "black", "red", "yellow"],
        ),
        title="difference",
    )

    if fname is not None:
        fig.savefig(fname, bbox_inches="tight", facecolor="black")


if __name__ == "__main__":
    parser = argparse.ArgumentParser("plot_nii_difference")
    parser.add_argument(
        "--out", "-o", metavar="PATH", required=True, type=str,
        help="path to output image"
    )
    parser.add_argument(
        "--images", "-i", metavar="PATH", required=True, type=str, nargs=2,
        help="paths to two images"
    )
    parser.add_argument(
        "--masks", metavar="PATH", type=str, nargs=2,
        help="paths to two corresponding mask images"
    )
    parser.add_argument(
        "--labels", metavar="LABEL", type=str, nargs=2,
        help="labels for the two series"
    )
    parser.add_argument(
        "--index", metavar="IND", type=int, default=0,
        help="volume index for 4d data"
    )
    parser.add_argument(
        "--index-offset", metavar="IND", type=int, default=0,
        help=(
            "Offset between the two image series. "
            "`index1 = index; index2 = index + offset"
        )
    )
    parser.add_argument(
        "--cut-coords", metavar="X,Y,Z", type=str, default="1.0, 0.0, 0.0",
        help='ortho cut coordinates (default: "1.0, 0.0, 0.0")'
    )
    parser.add_argument(
        "--vmax", metavar="VAL", type=float, default=None,
        help="plotting vmax"
    )
    parser.add_argument(
        "--colorbar", action="store_true",
        help="show colorbar"
    )

    args = parser.parse_args()
    main(args)
