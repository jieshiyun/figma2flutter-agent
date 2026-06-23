from __future__ import annotations

import copy
from typing import Any, Iterable

from agent.geometry import Deviation

"""Deterministic, geometry-driven IR repair.

Given the per-node deviations from `geometry.diff_rects`, nudge the offending
IR nodes back toward their Figma target — but only the corrections we can apply
without distorting content:

  - a node whose position (x/y) drifted and that carries an absolute
    `position`: shift the position by the negative of the drift.
  - a non-text node whose size (w/h) drifted and that carries an explicit
    `size`: shrink/grow the size by the negative of the drift.

Intrinsically-sized nodes (text, auto-layout frames with no explicit size) are
left untouched: forcing a text box would clip glyphs, and an auto-layout
frame's size follows its children. This keeps repair conservative — it fixes
genuine layout drift and is a no-op when the deterministic codegen is already
faithful (the preferred state; systematic gaps belong in codegen, not here).
"""

# Node types whose box is intrinsic to their content — never force their size.
_INTRINSIC_SIZE_TYPES = {"text"}


def patch_ir(
    ir: dict,
    deviations: Iterable[Deviation],
    tolerance: float = 1.0,
) -> tuple[dict, list[str]]:
    """Return a patched copy of `ir` plus human-readable notes per patch.

    The input IR is not mutated. Only deviations past `tolerance` on an
    actionable axis are applied; everything else is skipped.
    """
    patched = copy.deepcopy(ir)
    index = _index_by_id(patched)
    notes: list[str] = []
    for dev in deviations:
        node = index.get(dev.id)
        if node is None:
            continue
        note = _patch_node(node, dev, tolerance)
        if note:
            notes.append(note)
    return patched, notes


def _patch_node(node: dict, dev: Deviation, tolerance: float) -> str | None:
    changed: list[str] = []
    pos = node.get("position")
    if pos is not None:
        if "x" in dev.kinds and pos.get("x") is not None:
            pos["x"] = _round(pos["x"] - dev.dx)
            changed.append(f"x{-dev.dx:+.0f}")
        if "y" in dev.kinds and pos.get("y") is not None:
            pos["y"] = _round(pos["y"] - dev.dy)
            changed.append(f"y{-dev.dy:+.0f}")
    size = node.get("size")
    if size is not None and node.get("type") not in _INTRINSIC_SIZE_TYPES:
        if "w" in dev.kinds and size.get("width") is not None:
            size["width"] = _round(size["width"] - dev.dw)
            changed.append(f"w{-dev.dw:+.0f}")
        if "h" in dev.kinds and size.get("height") is not None:
            size["height"] = _round(size["height"] - dev.dh)
            changed.append(f"h{-dev.dh:+.0f}")
    if not changed:
        return None
    label = node.get("name") or dev.id
    return f"{label}: {', '.join(changed)}"


def _index_by_id(ir: dict) -> dict[str, dict]:
    """Map every id-bearing node in the IR (root + descendants) by its id."""
    out: dict[str, dict] = {}
    _walk(ir.get("root"), out)
    return out


def _walk(node: Any, out: dict[str, dict]) -> None:
    if not isinstance(node, dict):
        return
    nid = node.get("id")
    if nid is not None:
        out.setdefault(nid, node)
    for child in node.get("children") or []:
        _walk(child, out)


def _round(value: float) -> float:
    """Keep integers integral so codegen emits clean literals."""
    r = round(value, 3)
    return int(r) if float(r).is_integer() else r
