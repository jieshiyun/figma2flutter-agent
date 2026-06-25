# Changelog

All notable changes to this project are documented here. See
[CLAUDE.md](CLAUDE.md) for the detailed step-by-step development log.

## [0.2.0] - 2026-06-24

### Added
- **LLM layout inference** (`--llm`): re-flows absolutely-positioned (Stack)
  frames into idiomatic `Row`/`Column` from their child geometry. Per-frame,
  validated, and non-fatal (unclear frames stay a `Stack`). Live-verified.
- **Per-child counter-axis fill** (`layoutAlign`): only children that opt in are
  stretched to fill width, so hug-content text is no longer over-stretched.
- **Demo gallery**: the Flutter app now showcases Login, Shop (product grid),
  Settings, Profile, and Simple screens; inputs under `examples/`.
- **Evaluation metrics** (`python -m agent.metrics`): aggregates compile/repair
  success, visual fidelity, generated LOC, and component-reuse ratio across
  saved runs.
- **Docs**: `ARCHITECTURE.md` design rationale, before/after and demo
  screenshots, and a CI badge in the README.
- **CI**: GitHub Actions runs the test suite on Python 3.10–3.12.

### Fixed
- Dart string escaping: `$` is now escaped, so text like a price (`$199`) no
  longer breaks generation via string interpolation.
- Auto-layout frames hug their main axis instead of being pinned to the Figma
  box size, eliminating `RenderFlex` overflow when rendered content differs.

### Changed
- `--llm` repurposed from the deferred experimental whole-plan planner to the
  targeted Stack→flow inference above; the old `plan_with_llm` was removed.

### Validated
- End-to-end on two live Figma nodes (profile + feed): `flutter analyze` clean,
  visual scores 87 / 90, per-node geometry within ~1px of the source layout.

## [0.1.0] - 2026-06-22

Initial release: deterministic Figma JSON → Design IR → Component Plan →
Flutter pipeline with `flutter analyze` validation, LLM-based code repair
(`--repair`, DeepSeek), visual and geometry fidelity diffs, design tokens,
real bundled fonts, and image/icon download from the Figma API.
