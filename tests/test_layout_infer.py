from __future__ import annotations

import json
from typing import Any

import pytest

from agent import codegen, layout_infer, planner


class FakeLLM:
    """Returns queued responses (one per call), or a single fixed response."""

    def __init__(self, *responses: str) -> None:
        self.responses = list(responses)
        self.calls: list[str] = []

    def complete(self, prompt: str) -> str:
        self.calls.append(prompt)
        return self.responses.pop(0) if len(self.responses) > 1 else self.responses[0]


class ExplodingLLM:
    def complete(self, prompt: str) -> str:
        raise NotImplementedError("no LLM client configured")


def _stack_frame(children: list[dict], **extra: Any) -> dict:
    node = {
        "id": "f",
        "type": "frame",
        "size": {"width": 300, "height": 200},
        "layout": {"direction": "stack"},
        "children": children,
    }
    node.update(extra)
    return node


def _ir(frame: dict) -> dict:
    return {
        "version": "0.1",
        "root": {
            "id": "s",
            "type": "screen",
            "layout": {"direction": "vertical"},
            "children": [frame],
        },
    }


def _two_children() -> list[dict]:
    return [
        {"id": "a", "type": "text", "text": "A", "position": {"x": 0, "y": 0}, "size": {"width": 100, "height": 20}},
        {"id": "b", "type": "text", "text": "B", "position": {"x": 0, "y": 40}, "size": {"width": 100, "height": 20}},
    ]


# ---------------------------------------------------------------------------
# Successful inference
# ---------------------------------------------------------------------------


def test_vertical_inference_reflows_and_drops_positions() -> None:
    ir = _ir(_stack_frame(_two_children()))
    resp = json.dumps(
        {"direction": "vertical", "order": ["a", "b"], "spacing": 20,
         "padding": {"top": 8, "right": 8, "bottom": 8, "left": 8}, "alignment": "start"}
    )
    out, notes = layout_infer.infer_flow_layouts(ir, FakeLLM(resp))
    frame = out["root"]["children"][0]
    assert frame["layout"] == {
        "direction": "vertical", "spacing": 20,
        "padding": {"top": 8, "right": 8, "bottom": 8, "left": 8}, "alignment": "start",
    }
    assert [c["id"] for c in frame["children"]] == ["a", "b"]
    assert all("position" not in c for c in frame["children"])
    assert any("stack -> vertical" in n for n in notes)


def test_inference_respects_returned_order() -> None:
    ir = _ir(_stack_frame(_two_children()))
    resp = json.dumps({"direction": "horizontal", "order": ["b", "a"]})
    out, _ = layout_infer.infer_flow_layouts(ir, FakeLLM(resp))
    frame = out["root"]["children"][0]
    assert frame["layout"]["direction"] == "horizontal"
    assert [c["id"] for c in frame["children"]] == ["b", "a"]


def test_input_ir_is_not_mutated() -> None:
    ir = _ir(_stack_frame(_two_children()))
    layout_infer.infer_flow_layouts(ir, FakeLLM(json.dumps({"direction": "vertical", "order": ["a", "b"]})))
    assert ir["root"]["children"][0]["layout"] == {"direction": "stack"}


# ---------------------------------------------------------------------------
# Rejected / kept-as-stack cases
# ---------------------------------------------------------------------------


def test_stack_response_keeps_stack() -> None:
    ir = _ir(_stack_frame(_two_children()))
    out, notes = layout_infer.infer_flow_layouts(ir, FakeLLM(json.dumps({"direction": "stack"})))
    assert out["root"]["children"][0]["layout"] == {"direction": "stack"}
    assert any("kept stack" in n for n in notes)


def test_order_not_a_permutation_is_rejected() -> None:
    ir = _ir(_stack_frame(_two_children()))
    # 'c' is not a child; order drops 'b' -> reject, keep stack
    out, _ = layout_infer.infer_flow_layouts(ir, FakeLLM(json.dumps({"direction": "vertical", "order": ["a", "c"]})))
    assert out["root"]["children"][0]["layout"] == {"direction": "stack"}


def test_invalid_json_keeps_stack_non_fatal() -> None:
    ir = _ir(_stack_frame(_two_children()))
    out, notes = layout_infer.infer_flow_layouts(ir, FakeLLM("not json"))
    assert out["root"]["children"][0]["layout"] == {"direction": "stack"}
    assert any("skipped" in n for n in notes)


def test_no_client_key_keeps_stack_non_fatal() -> None:
    ir = _ir(_stack_frame(_two_children()))
    out, notes = layout_infer.infer_flow_layouts(ir, ExplodingLLM())
    assert out["root"]["children"][0]["layout"] == {"direction": "stack"}
    assert any("skipped" in n for n in notes)


def test_single_child_frame_is_not_queried() -> None:
    one = [{"id": "a", "type": "text", "text": "A", "position": {"x": 0, "y": 0}}]
    client = FakeLLM(json.dumps({"direction": "vertical", "order": ["a"]}))
    layout_infer.infer_flow_layouts(_ir(_stack_frame(one)), client)
    assert client.calls == []


def test_bad_padding_is_dropped_but_flow_kept() -> None:
    ir = _ir(_stack_frame(_two_children()))
    resp = json.dumps({"direction": "vertical", "order": ["a", "b"], "padding": {"top": "x"}})
    out, _ = layout_infer.infer_flow_layouts(ir, FakeLLM(resp))
    layout = out["root"]["children"][0]["layout"]
    assert layout["direction"] == "vertical"
    assert "padding" not in layout


# ---------------------------------------------------------------------------
# End-to-end: inferred Column reaches codegen
# ---------------------------------------------------------------------------


def test_inferred_column_emits_column_not_stack() -> None:
    ir = _ir(_stack_frame(_two_children(), name="Panel"))
    resp = json.dumps({"direction": "vertical", "order": ["a", "b"], "spacing": 20})
    out, _ = layout_infer.infer_flow_layouts(ir, FakeLLM(resp))
    dart = codegen.generate(planner.plan(out))
    assert "Column(" in dart
    assert "Positioned(" not in dart


def test_prompt_includes_geometry() -> None:
    client = FakeLLM(json.dumps({"direction": "stack"}))
    layout_infer.infer_flow_layouts(_ir(_stack_frame(_two_children())), client)
    prompt = client.calls[0]
    assert "x=0" in prompt and "y=40" in prompt
    assert "vertical" in prompt
