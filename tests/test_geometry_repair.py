from agent import geometry_repair
from agent.geometry import Deviation


def _dev(id, kinds, dx=0, dy=0, dw=0, dh=0):
    return Deviation(
        id=id, name=None, kinds=tuple(kinds),
        target=(0, 0, 0, 0), actual=(0, 0, 0, 0),
        dx=dx, dy=dy, dw=dw, dh=dh, max_abs=max(abs(dx), abs(dy), abs(dw), abs(dh)),
    )


def _ir(children):
    return {"version": "0.1", "root": {"id": "root", "type": "screen",
            "layout": {"direction": "stack"}, "children": children}}


def test_position_drift_is_nudged_back():
    ir = _ir([{"id": "a", "type": "rectangle", "position": {"x": 16, "y": 32},
               "size": {"width": 10, "height": 10}}])
    out, notes = geometry_repair.patch_ir(ir, [_dev("a", ("x", "y"), dx=4, dy=-3)])
    node = out["root"]["children"][0]
    assert node["position"] == {"x": 12, "y": 35}  # 16-4, 32-(-3)
    assert len(notes) == 1


def test_size_drift_on_container_is_corrected():
    ir = _ir([{"id": "a", "type": "rectangle", "size": {"width": 100, "height": 50}}])
    out, _ = geometry_repair.patch_ir(ir, [_dev("a", ("w", "h"), dw=6, dh=-2)])
    assert out["root"]["children"][0]["size"] == {"width": 94, "height": 52}


def test_text_size_is_never_forced():
    ir = _ir([{"id": "t", "type": "text", "text": "Hi", "size": {"width": 80, "height": 20}}])
    out, notes = geometry_repair.patch_ir(ir, [_dev("t", ("w",), dw=4)])
    assert out["root"]["children"][0]["size"] == {"width": 80, "height": 20}
    assert notes == []  # intrinsic text is skipped


def test_input_ir_is_not_mutated():
    ir = _ir([{"id": "a", "type": "rectangle", "position": {"x": 10, "y": 10},
               "size": {"width": 5, "height": 5}}])
    geometry_repair.patch_ir(ir, [_dev("a", ("x",), dx=2)])
    assert ir["root"]["children"][0]["position"] == {"x": 10, "y": 10}


def test_only_listed_axes_are_patched():
    ir = _ir([{"id": "a", "type": "rectangle", "position": {"x": 10, "y": 10},
               "size": {"width": 5, "height": 5}}])
    out, _ = geometry_repair.patch_ir(ir, [_dev("a", ("x",), dx=2, dy=9, dw=9, dh=9)])
    node = out["root"]["children"][0]
    assert node["position"] == {"x": 8, "y": 10}      # only x moved
    assert node["size"] == {"width": 5, "height": 5}  # w/h untouched (not in kinds)


def test_unknown_id_is_ignored():
    ir = _ir([{"id": "a", "type": "rectangle", "size": {"width": 5, "height": 5}}])
    out, notes = geometry_repair.patch_ir(ir, [_dev("ghost", ("w",), dw=3)])
    assert notes == []
    assert out["root"]["children"][0]["size"] == {"width": 5, "height": 5}


def test_node_without_position_or_size_is_skipped():
    ir = _ir([{"id": "a", "type": "frame", "layout": {"direction": "vertical"}, "children": []}])
    out, notes = geometry_repair.patch_ir(ir, [_dev("a", ("x", "w"), dx=3, dw=3)])
    assert notes == []
