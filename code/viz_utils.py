from typing import Tuple

import numpy as np
import nibabel as nib
from nilearn import image as nilimg


def apply_mask(img: nib.Nifti1Image, mask: nib.Nifti1Image) -> nib.Nifti1Image:
    assert img.ndim in {3, 4} and mask.ndim == 3
    mask = nilimg.resample_to_img(mask, img, interpolation="nearest")
    mask = (mask.get_fdata() > 0).astype(img.get_data_dtype())
    if img.ndim == 4:
        mask = mask[..., None]
    img = nib.Nifti1Image(img.dataobj * mask, img.affine)
    return img


def find_value_lims(
    img: np.ndarray, quantile: float = 0.01, masked: bool = True
) -> Tuple[float, float]:
    if img.ndim == 4:
        midpoint = img.shape[3] // 2
        img = img[..., midpoint]
    img = np.asarray(img)
    if masked:
        mask = (img != 0.0) & ~np.isnan(img)
        img = img[mask]
    low, high = np.quantile(img, [quantile, 1-quantile])
    return low, high