# Figma Flutter Codegen

## Project Goal

Convert a Figma mobile screen into maintainable, readable Flutter UI code through
a **deterministic** pipeline, with optional LLM assistance only where it clearly
beats rules (layout inference, `flutter analyze` repair).

What it handles today:
- **Input:** a Figma node JSON file, a saved `/nodes` response, or a live Figma node URL.
- **Output:** one runnable, `dart format`-clean Flutter screen with deduplicated reusable components and value-/style-derived design tokens.
- **Elements:** frame, text, rectangle, image, ellipse, line, vector (icon rasterization + rounded-rect heuristic), button-like frame, component / instance.
- **Layout:** vertical / horizontal auto-layout (padding, spacing, alignment, per-child `layoutAlign` fill) plus an absolute-positioning fallback (`Stack` / `Positioned`).
- **Validation:** `flutter analyze`, plus optional visual (screenshot diff) and geometry (per-node rect) fidelity checks.

## Architecture

```text
Figma JSON / Figma URL
→ Design IR
→ optional layout inference (LLM)
→ Component Plan
→ deterministic Flutter codegen (+ design tokens)
→ flutter analyze validation
→ optional LLM repair
→ visual / geometry validation
→ run artifacts
```

Core pipeline modules (`agent/`):

- `figma_client` — fetch a node, images, and styles via the Figma REST API.
- `ir_parser` — convert raw Figma JSON into the Design IR.
- `layout_infer` — optional LLM pass: relabel a `Stack` frame as a `Row`/`Column` from child geometry (`--llm`).
- `planner` — Design IR → Component Plan; dedupe structurally-identical components.
- `codegen` — generate Dart/Flutter from the plan.
- `validator` — run `flutter analyze`; run `dart format` on output.
- `repair` — LLM patches the generated file from analyze errors (`--repair`).

Supporting modules:

- `tokens` — intern style literals into `AppColors` / `AppSpacing` / `AppTextStyles`.
- `images` — download image fills + rasterize icon vectors, wire `pubspec.yaml` assets.
- `llm` — LLM client (DeepSeek provider + offline stub).
- `visual` — screenshot diff: SSIM / pixel-MAE → `visual_score`.
- `screenshot` — build & run the golden / rect-dump Flutter tests that capture renders.
- `geometry` — per-node rect diff against Figma's `absoluteBoundingBox`.
- `geometry_repair` — deterministic position/size nudges from geometry deltas.
- `run_logger` — persist run artifacts under `runs/` (`--save-run`).
- `metrics` — aggregate headline metrics across saved runs.

## Current Scope

- Flutter only — not React Native.
- Mobile portrait.
- Static UI — no interaction or app logic.
- Not a full Figma compiler — diagonal vectors, boolean ops, and complex effects are skipped gracefully (non-fatal warnings).
- Deterministic codegen first; LLM is opt-in and used only for layout inference (`--llm`) and analyze repair (`--repair`), both offline-tested with a fake client.

Prefer simple files, clear boundaries, and testable functions.

## Tech Stack

- Python pipeline (stdlib; Pillow + numpy for visual/geometry validation).
- Flutter / Dart output (Inter font bundled for faithful text metrics).
- JSON Schema for the Design IR and Component Plan (`schemas/`).
- Optional DeepSeek LLM via `DEEPSEEK_API_KEY` — the deterministic path needs no key.
- CLI entry point (`python -m agent.cli` / `figma2flutter`); `make` targets for one-command demo/eval.

## Repository Structure

```text
figma-flutter-codegen/
├── agent/                 # pipeline modules (see Architecture)
│   ├── cli.py
│   ├── figma_client.py
│   ├── ir_parser.py
│   ├── layout_infer.py
│   ├── planner.py
│   ├── codegen.py
│   ├── tokens.py
│   ├── images.py
│   ├── validator.py
│   ├── repair.py
│   ├── llm.py
│   ├── visual.py
│   ├── screenshot.py
│   ├── geometry.py
│   ├── geometry_repair.py
│   ├── run_logger.py
│   └── metrics.py
├── schemas/               # design_ir + component_plan JSON schemas
├── examples/              # sample Figma JSON, IR, and a committed benchmark fixture
├── flutter_app/           # Flutter gallery app (target for generated code)
├── tests/                 # pytest suite (network and Flutter mocked)
├── docs/                  # CHANGELOG (build log) + evaluation benchmark
├── .github/workflows/     # CI: Python tests + Flutter generate/analyze/smoke
├── Makefile               # make demo / make eval / make test
└── README.md
```

## Coding Rules

- Keep functions small.
- Add type hints.
- Add unit tests for parser and codegen (and any new module).
- Do not hide errors.
- Do not call external APIs in tests.
- Keep generated Flutter code readable (it is passed through `dart format`).
- Prefer deterministic code generation before adding LLM generation.

## Development Order

The project was built incrementally, **deterministic-first** (rule-based codegen
before any LLM). The full numbered build log — every step with its rationale,
per-phase test counts, real-node visual/geometry scores, model/token
confirmations, full bug investigations, per-version visual-score movements, and
the features that were *prototyped then removed* — lives in
[docs/CHANGELOG.md](docs/CHANGELOG.md).

The intended build order was: repo structure → Design IR schema → sample Figma
JSON → parser → rule-based codegen → CLI → Flutter shell → `flutter analyze`
validator → planner/Component Plan → repair loop. Everything after that
(real Figma source, node coverage, design tokens, visual/geometry validation,
real LLM provider, fidelity fixes, evaluation, CI, one-command demo) is logged
in the changelog.

## Definition of Done

A change is done when:

- relevant Python tests pass (`pytest` / `make test`), and no test calls external APIs;
- generated Dart is `dart format`-clean and `flutter analyze` passes for the demo app;
- the golden smoke test renders every screen without throwing (`make demo`);
- visual / geometry outputs are refreshed when fidelity logic changes (`make eval`);
- CLI behavior and this file / the README are updated when they change.

The canonical end-to-end command must always work:

```bash
python -m agent.cli --input examples/figma_sample.json --output flutter_app/lib/generated_screen.dart
flutter analyze        # in flutter_app/
```
