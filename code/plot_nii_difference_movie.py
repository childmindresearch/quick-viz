"""
Example usage:

python plot_nii_difference_movie.py \
    -o bold_diff_movie \
    --images /path/to/bold1.nii.gz /path/to/bold2.nii.gz \
    --masks /path/to/mask1.nii.gz /path/to/mask2.nii.gz \
    --labels bold1 bold2
"""

import argparse
import logging
import os
import pprint
import subprocess
from pathlib import Path

from matplotlib import pyplot as plt
import nibabel as nib
from nilearn import image as nilimg

from plot_nii_difference import plot_difference_triplet
from viz_utils import find_value_lims, apply_mask

plt.rcParams["figure.dpi"] = 150

logging.basicConfig(
    format="%(asctime)s %(levelname)-8s %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
)


def main(args: argparse.Namespace):
    logging.info("Args:\n%s", pprint.pformat(args.__dict__))
    outdir = Path(args.outdir)
    (outdir / "frames").mkdir(parents=True, exist_ok=True)

    logging.info("Loading images")
    imgs = [nib.load(path) for path in args.images]
    assert len(imgs) == 2, "only two images supported"
    assert imgs[0].ndim == imgs[1].ndim == 4, "both images should be 4d"
    assert len(args.labels) == 2, "two labels are required"
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

    # truncate to last volumes
    if img1.shape[3] != img2.shape[3]:
        ntpts1, ntpts2 = img1.shape[3], img2.shape[3]
        ntpts = min(ntpts1, ntpts2)
        logging.info("Truncating to %d time points", ntpts)
        img1 = nib.Nifti1Image(img1.dataobj[..., -ntpts:], img1.affine)
        img2 = nib.Nifti1Image(img2.dataobj[..., -ntpts:], img2.affine)
    else:
        ntpts = img1.shape[3]

    logging.info("Finding the vmax")
    _, vmax1 = find_value_lims(img1.get_fdata())
    _, vmax2 = find_value_lims(img2.get_fdata())
    vmax = max(vmax1, vmax2)

    cut_coords = tuple(float(val.strip()) for val in args.cut_coords.split(","))

    f, axs = plt.subplots(3, 1, figsize=(9, 9))

    for tpt in range(ntpts):
        logging.info("Plotting frame %d", tpt)
        fname = outdir / "frames" / f"{tpt:04d}.png"
        plot_difference_triplet(
            img1=nilimg.index_img(img1, tpt),
            img2=nilimg.index_img(img2, tpt),
            labels=args.labels,
            fig=f,
            axs=axs,
            index=tpt,
            cut_coords=cut_coords,
            vmax=vmax,
            colorbar=args.colorbar,
            fname=fname,
        )

    cmd = (
        "ffmpeg -y -framerate 2 -pattern_type glob -i '{frames}' "
        "-vf 'pad=ceil(iw/2)*2:ceil(ih/2)*2' "
        "-c:v libx264 -r 30 -pix_fmt yuv420p {out}"
    ).format(
        frames=str(outdir / "frames" / "*.png"),
        out=str(outdir / args.fname),
    )
    logging.info("Combining frames with ffmpeg\n\t%s", cmd)
    subprocess.call(cmd, shell=True)

    logging.info("Done")


if __name__ == "__main__":
    parser = argparse.ArgumentParser("plot_nii_difference_movie")
    parser.add_argument(
        "--outdir", "-o", metavar="PATH", required=True, type=str,
        help="path to output directory"
    )
    parser.add_argument(
        "--images", "-i", metavar="PATH", required=True, type=str, nargs=2,
        help="paths to two 4d image series"
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
        "--cut-coords", metavar="X,Y,Z", type=str, default="1.0, 0.0, 0.0",
        help='ortho cut coordinates (default: "1.0, 0.0, 0.0")'
    )
    parser.add_argument(
        "--colorbar", action="store_true",
        help="show colorbar"
    )
    parser.add_argument(
        "--fname", metavar="NAME", type=str, default="out.mp4",
        help='output video filename (default: "out.mp4")'
    )

    args = parser.parse_args()
    main(args)
