from __future__ import annotations

from pathlib import Path

import numpy as np
from PIL import Image

from agent import visual


def _write(path: Path, arr: np.ndarray) -> Path:
    Image.fromarray(arr.astype("uint8")).save(path)
    return path


def _noise(w: int, h: int, seed: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    return rng.integers(0, 256, size=(h, w, 3), dtype=np.uint8).astype("uint8")


def test_identical_images_score_100(tmp_path: Path) -> None:
    img = _write(tmp_path / "a.png", _noise(40, 60, 1))
    report = visual.compare(img, img)
    assert report.visual_score == 100.0
    assert report.ssim == 1.0
    assert report.pixel_mae == 0.0
    assert report.size_ratio == (1.0, 1.0)


def test_opposite_images_score_low(tmp_path: Path) -> None:
    white = _write(tmp_path / "w.png", np.full((30, 30, 3), 255))
    black = _write(tmp_path / "b.png", np.zeros((30, 30, 3)))
    report = visual.compare(white, black)
    assert report.pixel_mae == 1.0
    assert report.visual_score < 30.0


def test_similar_beats_dissimilar(tmp_path: Path) -> None:
    base = _noise(50, 50, 7)
    ref = _write(tmp_path / "ref.png", base)
    # Slight perturbation stays far closer than independent noise.
    near = _write(tmp_path / "near.png", np.clip(base.astype(int) + 8, 0, 255))
    far = _write(tmp_path / "far.png", _noise(50, 50, 99))
    near_report = visual.compare(ref, near)
    far_report = visual.compare(ref, far)
    assert near_report.visual_score > far_report.visual_score
    assert near_report.ssim > far_report.ssim


def test_size_ratio_reported_and_candidate_resized(tmp_path: Path) -> None:
    ref = _write(tmp_path / "ref.png", _noise(100, 200, 3))
    cand = _write(tmp_path / "cand.png", _noise(50, 50, 3))
    report = visual.compare(ref, cand)
    assert report.reference_size == (100, 200)
    assert report.candidate_size == (50, 50)
    assert report.size_ratio == (0.5, 0.25)


def test_to_dict_is_json_friendly(tmp_path: Path) -> None:
    img = _write(tmp_path / "a.png", _noise(10, 10, 2))
    d = visual.compare(img, img).to_dict()
    assert d["reference_size"] == [10, 10]
    assert d["size_ratio"] == [1.0, 1.0]
    assert isinstance(d["visual_score"], float)


def test_rgba_flattened_on_white(tmp_path: Path) -> None:
    # A fully transparent RGBA image should compare as white.
    rgba = Image.new("RGBA", (20, 20), (0, 0, 0, 0))
    rgba_path = tmp_path / "t.png"
    rgba.save(rgba_path)
    white = _write(tmp_path / "white.png", np.full((20, 20, 3), 255))
    report = visual.compare(white, rgba_path)
    assert report.pixel_mae == 0.0
