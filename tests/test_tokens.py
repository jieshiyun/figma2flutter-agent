from __future__ import annotations

from typing import Any

from agent import codegen
from agent.tokens import Tokens, _sanitize_ident


def _screen(children: list[dict]) -> dict:
    return {
        "version": "0.1",
        "root": {
            "id": "s",
            "name": "TokenScreen",
            "type": "screen",
            "layout": {"direction": "vertical", "spacing": 16},
            "children": children,
        },
    }


def _gen(children: list[dict]) -> str:
    from agent import planner

    return codegen.generate(planner.plan(_screen(children)))


def test_repeated_color_defined_once_referenced_many() -> None:
    dart = _gen(
        [
            {"id": "a", "type": "text", "text": "A", "color": "#111111"},
            {"id": "b", "type": "text", "text": "B", "color": "#111111"},
        ]
    )
    assert dart.count("static const Color c111111 =") == 1
    assert dart.count("AppColors.c111111") == 2


def test_spacing_token_shared_across_padding_and_gap() -> None:
    dart = _gen([{"id": "t", "type": "text", "text": "Hi"}])
    # the screen's spacing: 16 becomes a token
    assert "static const double s16 = 16;" in dart
    assert "spacing: AppSpacing.s16" in dart


def test_typography_token_with_per_use_color_via_copywith() -> None:
    dart = _gen(
        [
            {
                "id": "t",
                "type": "text",
                "text": "Hi",
                "fontSize": 24,
                "fontWeight": 700,
                "color": "#0A84FF",
            }
        ]
    )
    assert (
        "static const TextStyle s24w700 = "
        "TextStyle(fontSize: 24, fontWeight: FontWeight.w700);" in dart
    )
    assert "AppTextStyles.s24w700.copyWith(color: AppColors.c0a84ff)" in dart


def test_sizes_and_radii_stay_literal_not_spacing_tokens() -> None:
    dart = _gen(
        [
            {
                "id": "r",
                "type": "rectangle",
                "fill": "#FFFFFF",
                "cornerRadius": 8,
                "size": {"width": 100, "height": 40},
            }
        ]
    )
    assert "width: 100" in dart
    assert "BorderRadius.circular(8)" in dart
    # 100/40/8 are dimensions, not gaps -> no spacing tokens for them
    assert "AppSpacing.s100" not in dart
    assert "AppSpacing.s8" not in dart


def test_no_tokens_means_no_theme_classes() -> None:
    dart = codegen.generate(
        {
            "version": "0.1",
            "rootComponent": "Bare",
            "components": [
                {
                    "name": "Bare",
                    "root": {
                        "id": "s",
                        "type": "screen",
                        "layout": {"direction": "vertical"},
                        "children": [{"id": "t", "type": "text", "text": "Hi"}],
                    },
                }
            ],
        }
    )
    assert "abstract final class App" not in dart


def test_color_helper_is_literal_when_no_active_registry() -> None:
    # Called directly (outside generate) the helper stays a plain literal.
    assert codegen._color("#FFFFFF") == "Color(0xFFFFFFFF)"


# ---------------------------------------------------------------------------
# Route B: semantic color names from published Figma Styles
# ---------------------------------------------------------------------------


def test_sanitize_ident_camel_cases_style_name() -> None:
    assert _sanitize_ident("Green/Primary") == "greenPrimary"
    assert _sanitize_ident("Gray/03") == "gray03"
    assert _sanitize_ident("Carbon Neutral/300") == "carbonNeutral300"
    assert _sanitize_ident("White") == "white"
    assert _sanitize_ident("300") == ""  # leading digit -> unusable
    assert _sanitize_ident("!!!") == ""


def test_tokens_prefers_semantic_name_else_value_derived() -> None:
    t = Tokens({"#5DB075": "Green/Primary"})
    assert t.color("#5DB075") == "AppColors.greenPrimary"
    assert t.color("#123456") == "AppColors.c123456"  # no style -> fallback
    # stable: same hex always interns to the same name
    assert t.color("#5DB075") == "AppColors.greenPrimary"
    assert t.colors == {"greenPrimary": "#5DB075", "c123456": "#123456"}


def test_tokens_disambiguates_name_collision() -> None:
    t = Tokens({"#111111": "Brand", "#222222": "Brand"})
    assert t.color("#111111") == "AppColors.brand"
    assert t.color("#222222") == "AppColors.brand2"


def test_codegen_uses_semantic_color_names_from_plan_tokens() -> None:
    from agent import planner

    ir = _screen([{"id": "t", "type": "text", "text": "Hi", "color": "#5DB075"}])
    ir["tokens"] = {"colors": {"#5DB075": "Green/Primary"}}
    dart = codegen.generate(planner.plan(ir))
    assert "static const Color greenPrimary = Color(0xFF5DB075);" in dart
    assert "AppColors.greenPrimary" in dart
