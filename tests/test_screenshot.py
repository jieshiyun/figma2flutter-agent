from __future__ import annotations

from agent import screenshot


def test_build_golden_test_embeds_class_size_and_paths() -> None:
    src = screenshot.build_golden_test("ProfilePosts", 375, 812)
    assert "import 'package:flutter_app/generated_screen.dart';" in src
    assert "const Size(375, 812)" in src
    assert "home: ProfilePosts()" in src
    assert "find.byType(ProfilePosts)" in src
    assert "matchesGoldenFile('visual_golden/actual.png')" in src
    # Network images can't load under flutter_test; capture must not fail.
    assert "while (tester.takeException() != null)" in src


def test_build_golden_test_respects_custom_screen_file() -> None:
    src = screenshot.build_golden_test("Home", 320, 640, screen_file="screen.dart")
    assert "import 'package:flutter_app/screen.dart';" in src
    assert "const Size(320, 640)" in src

def test_build_rect_dump_test_embeds_class_size_and_output() -> None:
    src = screenshot.build_rect_dump_test("ProfilePosts", 375, 812)
    assert "import 'package:flutter_app/generated_screen.dart';" in src
    assert "const Size(375, 812)" in src
    assert "home: ProfilePosts()" in src
    assert "find.byType(KeyedSubtree)" in src
    assert "putIfAbsent" in src  # first occurrence wins for deduped components
    assert "test/visual_rects/rects.json" in src
    # Network images can't load under flutter_test; capture must not fail.
    assert "while (tester.takeException() != null)" in src


def test_build_rect_dump_test_respects_custom_screen_file() -> None:
    src = screenshot.build_rect_dump_test("Home", 320, 640, screen_file="screen_keyed.dart")
    assert "import 'package:flutter_app/screen_keyed.dart';" in src

def test_rect_dump_test_loads_fonts_when_given() -> None:
    src = screenshot.build_rect_dump_test(
        "Home", 375, 812, fonts=[("Inter", "fonts/Inter.ttf")]
    )
    assert "FontLoader('Inter')" in src
    assert "rootBundle.load('fonts/Inter.ttf')" in src


def test_rect_dump_test_without_fonts_has_no_loader() -> None:
    src = screenshot.build_rect_dump_test("Home", 375, 812)
    assert "FontLoader(" not in src


def test_discover_fonts_lists_ttf_by_stem(tmp_path) -> None:
    (tmp_path / "fonts").mkdir()
    (tmp_path / "fonts" / "Inter.ttf").write_bytes(b"x")
    (tmp_path / "fonts" / "Roboto.otf").write_bytes(b"x")
    (tmp_path / "fonts" / "notes.txt").write_text("ignore")
    assert screenshot.discover_fonts(tmp_path) == [
        ("Inter", "fonts/Inter.ttf"),
        ("Roboto", "fonts/Roboto.otf"),
    ]


def test_discover_fonts_empty_when_no_dir(tmp_path) -> None:
    assert screenshot.discover_fonts(tmp_path) == []
