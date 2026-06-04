from __future__ import annotations

import re
from typing import Any

"""Deterministic design-token registry (token routes A + B).

Each distinct literal value is interned once and referenced many times.
Spacing and typography names are always value-derived (route A); color names
prefer a semantic name when the parser resolved one from a published Figma
fill Style (route B — e.g. `Green/Primary` -> `AppColors.greenPrimary`) and
fall back to the value-derived `c<hex>` otherwise. Two designs with the same
inputs produce identical token tables, and any Figma file maps cleanly.

Identifier names stay lowerCamelCase-safe (lowercase hex, `p` for the decimal
point, camelCased style names) so the generated constants pass `flutter_lints`'
constant_identifier_names.
"""


class Tokens:
    """Interns literal style values into named, deduplicated constants."""

    def __init__(self, color_names: dict[str, str] | None = None) -> None:
        self.colors: dict[str, str] = {}  # name -> raw hex
        self.spacings: dict[str, Any] = {}  # name -> raw number
        self.text_styles: dict[str, tuple[Any, Any]] = {}  # name -> (size, weight)
        # hex -> semantic Style name resolved by the parser (route B).
        self._color_names = color_names or {}
        # hex -> assigned const name, so a colour always interns to one name.
        self._color_ref: dict[str, str] = {}

    def color(self, hex_str: str) -> str:
        name = self._color_ref.get(hex_str)
        if name is None:
            name = self._assign_color_name(hex_str)
            self._color_ref[hex_str] = name
            self.colors[name] = hex_str
        return f"AppColors.{name}"

    def _assign_color_name(self, hex_str: str) -> str:
        base = _sanitize_ident(self._color_names.get(hex_str, ""))
        if not base:
            base = "c" + hex_str.lstrip("#").lower()
        name, i = base, 2
        while name in self.colors:  # different hex already holds this name
            name, i = f"{base}{i}", i + 1
        return name

    def spacing(self, value: Any) -> str:
        name = "s" + _ident_num(value)
        self.spacings[name] = value
        return f"AppSpacing.{name}"

    def text_style(self, size: Any, weight: Any) -> str:
        name = ""
        if size is not None:
            name += "s" + _ident_num(size)
        if weight is not None:
            name += "w" + str(int(weight))
        self.text_styles[name] = (size, weight)
        return f"AppTextStyles.{name}"


def _sanitize_ident(raw: str) -> str:
    """camelCase a Figma Style name into a Dart identifier ("" if unusable).

    "Green/Primary" -> "greenPrimary", "Gray/03" -> "gray03". Returns "" when
    the name is empty or would start with a digit, so the caller falls back to
    a value-derived name.
    """
    parts = [p for p in re.split(r"[^0-9A-Za-z]+", raw) if p]
    if not parts:
        return ""
    out = parts[0][0].lower() + parts[0][1:]
    for p in parts[1:]:
        out += p[0].upper() + p[1:]
    if not out or out[0].isdigit():
        return ""
    return out


def _ident_num(v: Any) -> str:
    """Render a number as an identifier-safe fragment (12.5 -> '12p5')."""
    if isinstance(v, bool):
        raise TypeError("expected number, got bool")
    if isinstance(v, float) and v.is_integer():
        v = int(v)
    s = repr(v) if isinstance(v, float) else str(v)
    return s.replace("-", "n").replace(".", "p")
