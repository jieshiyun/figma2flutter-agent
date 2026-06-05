from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path

import numpy as np
from PIL import Image

# SSIM stabilizing constants for 8-bit images (Wang et al. 2004).
_L = 255.0
_C1 = (0.01 * _L) ** 2
_C2 = (0.03 * _L) ** 2
_WINDOW = 7

# Composite-score weights: structure (SSIM) dominates, raw pixel error fills in.
_W_SSIM = 0.6
_W_PIXEL = 0.4


@dataclass(frozen=True)
class VisualReport:
    """Result of comparing a reference image to a Flutter screenshot.

    visual_score is a 0..100 composite; ssim is 0..1 (1 == identical
    structure); pixel_mae is 0..1 mean absolute per-channel error.
    size_ratio is (candidate_w / reference_w, candidate_h / reference_h)
    before the candidate is resized to match for the pixel metrics.
    """

    reference_size: tuple[int, int]
    candidate_size: tuple[int, int]
    size_ratio: tuple[float, float]
    pixel_mae: float
    ssim: float
    visual_score: float

    def to_dict(self) -> dict:
        d = asdict(self)
        # JSON has no tuples; keep them as lists.
        for k in ("reference_size", "candidate_size", "size_ratio"):
            d[k] = list(d[k])
        return d


def load_image(path: str | Path) -> Image.Image:
    """Load an image as RGB (drops alpha by compositing on white)."""
    img = Image.open(path)
    if img.mode in ("RGBA", "LA", "P"):
        img = img.convert("RGBA")
        bg = Image.new("RGBA", img.size, (255, 255, 255, 255))
        img = Image.alpha_composite(bg, img)
    return img.convert("RGB")


def _to_array(img: Image.Image) -> np.ndarray:
    return np.asarray(img, dtype=np.float64)


def _window_mean(x: np.ndarray, w: int) -> np.ndarray:
    """Mean over a (w x w) sliding window via an integral image (numpy only)."""
    pad = w // 2
    xp = np.pad(x, pad, mode="edge")
    s = np.cumsum(np.cumsum(xp, axis=0), axis=1)
    s = np.pad(s, ((1, 0), (1, 0)), mode="constant")
    h, wd = x.shape
    total = s[w : w + h, w : w + wd] - s[0:h, w : w + wd] - s[w : w + h, 0:wd] + s[0:h, 0:wd]
    return total / (w * w)


def ssim(ref_gray: np.ndarray, cand_gray: np.ndarray, window: int = _WINDOW) -> float:
    """Mean structural similarity over a sliding window. Inputs same shape."""
    x, y = ref_gray, cand_gray
    mu_x = _window_mean(x, window)
    mu_y = _window_mean(y, window)
    mu_x2, mu_y2, mu_xy = mu_x * mu_x, mu_y * mu_y, mu_x * mu_y
    sigma_x2 = _window_mean(x * x, window) - mu_x2
    sigma_y2 = _window_mean(y * y, window) - mu_y2
    sigma_xy = _window_mean(x * y, window) - mu_xy
    num = (2 * mu_xy + _C1) * (2 * sigma_xy + _C2)
    den = (mu_x2 + mu_y2 + _C1) * (sigma_x2 + sigma_y2 + _C2)
    return float(np.clip((num / den).mean(), -1.0, 1.0))


def _gray(arr: np.ndarray) -> np.ndarray:
    return arr @ np.array([0.299, 0.587, 0.114])


def compare(reference_path: str | Path, candidate_path: str | Path) -> VisualReport:
    """Compare a reference image against a candidate screenshot.

    The candidate is resized to the reference's dimensions before the pixel
    and SSIM metrics are computed, so they measure layout/appearance rather
    than scale. The raw size difference is reported separately.
    """
    ref = load_image(reference_path)
    cand = load_image(candidate_path)
    ref_w, ref_h = ref.size
    cand_w, cand_h = cand.size

    if (cand_w, cand_h) != (ref_w, ref_h):
        cand = cand.resize((ref_w, ref_h), Image.LANCZOS)

    ref_arr = _to_array(ref)
    cand_arr = _to_array(cand)

    pixel_mae = float(np.abs(ref_arr - cand_arr).mean() / _L)
    score_ssim = ssim(_gray(ref_arr), _gray(cand_arr))
    visual = 100.0 * (_W_SSIM * max(0.0, score_ssim) + _W_PIXEL * (1.0 - pixel_mae))

    return VisualReport(
        reference_size=(ref_w, ref_h),
        candidate_size=(cand_w, cand_h),
        size_ratio=(cand_w / ref_w, cand_h / ref_h),
        pixel_mae=round(pixel_mae, 6),
        ssim=round(score_ssim, 6),
        visual_score=round(visual, 2),
    )
