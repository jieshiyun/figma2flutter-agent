from __future__ import annotations

import json
from typing import Any

from agent.codegen import _class_name

PLAN_VERSION = "0.1"


def plan(ir: dict) -> dict:
    """Deterministically turn Design IR v0.1 into a Component Plan v0.1.

    Every frame that carries a `name` is lifted into its own component, and
    its original position is replaced by a component reference node. Unnamed
    frames stay inline. The root screen becomes `rootComponent`. The result
    is what codegen renders into one StatelessWidget per component.

    Pure and deterministic: no IO, stable ordering (root first, then
    extracted components in depth-first order of appearance).
    """
    if ir.get("version") != "0.1":
        raise ValueError(f"unsupported IR version: {ir.get('version')!r}")
    root = ir.get("root")
    if not isinstance(root, dict) or root.get("type") != "screen":
        got = root.get("type") if isinstance(root, dict) else root
        raise ValueError(f"root must be a screen, got {got!r}")

    components: list[dict] = []
    taken: set[str] = set()

    def claim(raw_name: str | None, fallback: str) -> str:
        base = _class_name(raw_name) if raw_name else fallback
        name = base
        n = 2
        while name in taken:
            name = f"{base}{n}"
            n += 1
        taken.add(name)
        return name

    def extract(node: dict) -> dict:
        """Return a copy of a container node with named-frame children
        replaced by component references; recurse into all frames."""
        new_children: list[dict] = []
        for child in node.get("children", []):
            if child.get("type") == "frame" and child.get("name"):
                comp_name = claim(child.get("name"), "Component")
                components.append({"name": comp_name, "root": extract(child)})
                ref: dict = {"type": "component", "ref": comp_name}
                # Preserve absolute position so a Stack parent can place the
                # referenced component with a Positioned wrapper, and the
                # counter-axis fill flag so a flex parent still stretches it.
                if "position" in child:
                    ref["position"] = child["position"]
                if "layoutAlign" in child:
                    ref["layoutAlign"] = child["layoutAlign"]
                new_children.append(ref)
            elif child.get("type") == "frame":
                new_children.append(extract(child))
            else:
                new_children.append(child)
        out = dict(node)
        out["children"] = new_children
        return out

    root_name = claim(root.get("name"), "GeneratedScreen")
    root_component = {"name": root_name, "root": extract(root)}
    components.insert(0, root_component)
    components = _dedupe(components, root_name)
    out: dict[str, Any] = {
        "version": PLAN_VERSION,
        "rootComponent": root_name,
        "components": components,
    }
    # Carry design tokens (e.g. semantic color names) through to codegen.
    if ir.get("tokens"):
        out["tokens"] = ir["tokens"]
    return out


def _dedupe(components: list[dict], root_name: str) -> list[dict]:
    """Merge structurally-identical components into one reusable widget.

    Figma instances of the same component produce identical subtrees (they
    differ only by id/position). Collapsing them removes duplicate classes
    like Card2/Card3 and rewrites every reference to the canonical name.
    Runs to a fixed point so nested duplicates collapse too.
    """
    while True:
        seen: dict[str, str] = {}
        alias: dict[str, str] = {}
        for comp in components:
            key = _struct_key(comp["root"])
            if key in seen and comp["name"] != root_name:
                alias[comp["name"]] = seen[key]
            else:
                seen.setdefault(key, comp["name"])
        if not alias:
            return components
        components = [c for c in components if c["name"] not in alias]
        for comp in components:
            _rewrite_refs(comp["root"], alias)


def _struct_key(node: dict) -> str:
    """Canonical signature of a node ignoring identity/placement fields."""
    return json.dumps(_canonical(node), sort_keys=True)


def _canonical(node: dict) -> dict:
    out: dict[str, Any] = {}
    for k, v in node.items():
        if k in ("id", "position"):
            continue
        out[k] = [_canonical(c) for c in v] if k == "children" else v
    return out


def _rewrite_refs(node: dict, alias: dict[str, str]) -> None:
    for child in node.get("children", []):
        if child.get("type") == "component":
            if child.get("ref") in alias:
                child["ref"] = alias[child["ref"]]
        else:
            _rewrite_refs(child, alias)
