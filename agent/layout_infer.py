from __future__ import annotations

import copy
import json
from typing import Any

from agent.llm import LLMClient, strip_code_fence

"""LLM layout inference: recover flow (Row/Column) from absolute positioning.

Figma frames *without* auto-layout are lowered by the parser to
`layout.direction = "stack"`, and codegen emits `Stack` + `Positioned`. That is
faithful but not idiomatic — a vertically-stacked card is really a `Column`.
The deterministic pipeline can't recover that intent (the geometry is all it
has), which is exactly the judgment an LLM is good at.

This pass walks the IR and, for each `stack` frame, asks the LLM to read the
children's rectangles and decide whether they form a single vertical column or
horizontal row (with spacing / padding / alignment), or are genuinely free-form
(keep the stack). It is **opt-in** (`--llm`) and **safe**: every inference is
validated (the returned order must be a permutation of the existing children,
directions/alignments must be in range) and applied per-frame, so a bad or
missing response simply leaves that frame as a Stack. Each frame is one small
request, so large pages never hit a single-request token ceiling.
"""

_DIRECTIONS = ("vertical", "horizontal")
_ALIGNMENTS = ("start", "center", "end", "stretch")
_JUSTIFY = ("start", "center", "end", "spaceBetween")
_PAD_KEYS = ("top", "right", "bottom", "left")


def infer_flow_layouts(ir: dict, client: LLMClient) -> tuple[dict, list[str]]:
    """Return a patched copy of the IR with stack frames re-flowed where the
    LLM infers a clear Row/Column, plus a per-frame note list. Input untouched."""
    patched = copy.deepcopy(ir)
    notes: list[str] = []
    root = patched.get("root")
    if isinstance(root, dict):
        _infer_node(root, client, notes)
    return patched, notes


def _infer_node(node: dict, client: LLMClient, notes: list[str]) -> None:
    if node.get("type") in ("frame", "screen") and _is_stack(node):
        _try_infer_frame(node, client, notes)
    for child in node.get("children") or []:
        if isinstance(child, dict):
            _infer_node(child, client, notes)


def _is_stack(node: dict) -> bool:
    return (node.get("layout") or {}).get("direction") == "stack"


def _try_infer_frame(node: dict, client: LLMClient, notes: list[str]) -> None:
    children = node.get("children") or []
    if len(children) < 2:
        return  # nothing to arrange
    nid = node.get("id")
    try:
        raw = strip_code_fence(client.complete(build_flow_prompt(node))).strip()
        data = json.loads(raw)
    except (NotImplementedError, ValueError, json.JSONDecodeError) as exc:
        notes.append(f"frame {nid!r}: inference skipped ({exc})")
        return
    if _apply_inference(node, data):
        notes.append(f"frame {nid!r}: stack -> {node['layout']['direction']}")
    else:
        notes.append(f"frame {nid!r}: kept stack")


_PROMPT_TEMPLATE = """\
You convert absolutely-positioned Figma nodes into a Flutter auto-layout.

The container is {w}x{h} px. Its children below carry (x, y) top-left corners
relative to the container and (w, h) sizes:

{children}

Decide whether the children form ONE clean flow:
- a vertical column (stacked top-to-bottom, non-overlapping), or
- a horizontal row (left-to-right, non-overlapping).

If so, return ONLY this JSON (no commentary, no code fence):
{{"direction": "vertical" | "horizontal",
  "order": [child ids in flow order],
  "spacing": <typical gap in px>,
  "padding": {{"top": n, "right": n, "bottom": n, "left": n}},
  "alignment": "start" | "center" | "end" | "stretch",
  "justify": "start" | "center" | "end" | "spaceBetween"}}

`order` must list every child id exactly once. `alignment` is the cross-axis
placement, `justify` the main-axis distribution. If the children overlap or are
free-form (e.g. text on top of a background), return {{"direction": "stack"}}.
"""


def build_flow_prompt(node: dict) -> str:
    """Build the inference prompt from a stack frame's children geometry."""
    size = node.get("size") or {}
    lines = []
    for c in node.get("children") or []:
        pos = c.get("position") or {}
        csz = c.get("size") or {}
        lines.append(
            f"- id={c.get('id')!r} type={c.get('type')} "
            f"x={pos.get('x', '?')} y={pos.get('y', '?')} "
            f"w={csz.get('width', '?')} h={csz.get('height', '?')}"
        )
    return _PROMPT_TEMPLATE.format(
        w=size.get("width", "?"),
        h=size.get("height", "?"),
        children="\n".join(lines),
    )


def _apply_inference(node: dict, data: Any) -> bool:
    """Validate an inference and, if sound, re-flow the frame in place.

    Returns True when applied; False leaves the frame as a Stack (the response
    said "stack", or was malformed / not a permutation of the children)."""
    if not isinstance(data, dict):
        return False
    direction = data.get("direction")
    if direction not in _DIRECTIONS:
        return False
    children = node.get("children") or []
    ids = [str(c.get("id")) for c in children]
    order = data.get("order")
    if not isinstance(order, list) or sorted(map(str, order)) != sorted(ids):
        return False
    by_id = {str(c.get("id")): c for c in children}
    new_children = [by_id[str(i)] for i in order]
    for c in new_children:
        c.pop("position", None)  # flow positions the children now

    layout: dict[str, Any] = {"direction": direction}
    spacing = data.get("spacing")
    if isinstance(spacing, (int, float)) and not isinstance(spacing, bool) and spacing >= 0:
        layout["spacing"] = spacing
    padding = _valid_padding(data.get("padding"))
    if padding is not None:
        layout["padding"] = padding
    if data.get("alignment") in _ALIGNMENTS:
        layout["alignment"] = data["alignment"]
    if data.get("justify") in _JUSTIFY:
        layout["justify"] = data["justify"]

    node["layout"] = layout
    node["children"] = new_children
    return True


def _valid_padding(pad: Any) -> dict | None:
    if not isinstance(pad, dict):
        return None
    out: dict[str, float] = {}
    for k in _PAD_KEYS:
        v = pad.get(k, 0)
        if not isinstance(v, (int, float)) or isinstance(v, bool):
            return None
        out[k] = v
    if not any(out.values()):
        return None
    return out
