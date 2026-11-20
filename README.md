# PC Performance Lab

Independent benchmarking, in-depth analysis, and technical exploration of 
PC hardware and systems.

Independent, non-sponsored personal research project focused on understanding 
how PC hardware and systems behave in real-world applications.

This repository publishes reproducible, real-game benchmark
observations: tested hardware, game builds, settings, capture methods,
raw frame-time data, derived results, and the limitations that affect
interpretation.

Rather than simply reporting benchmark scores, this project aims to investigate 
the factors behind measured performance, explain unexpected behavior, and 
explore the capabilities and limitations of different hardware and software 
configurations.

Areas of interest include, but are not limited to:

- Gaming and application performance
- CPU, GPU, memory, and system bottlenecks
- BIOS, firmware, and system-level configuration
- Power management and thermal behavior
- Drivers and software optimization
- Hardware feature unlocking and configuration modifications
- Performance anomalies and their underlying mechanisms
- Benchmark methodology and data analysis

The project emphasizes transparent testing procedures, reproducible results, 
evidence-based analysis, and explicit documentation of known limitations.

All testing is conducted independently, without manufacturer sponsorship 
or provided review samples.

## What you will find here

- **Game-specific benchmark reports** — each report documents the game
  build, test scenes, graphics settings, hardware, sample counts, and
  known limitations.
- **Raw captures** — original CapFrameX JSON/CSV exports where
  available.
- **Processed data** — per-run tables, summaries, and comparison
  datasets derived from raw captures.
- **Charts and scripts** — rendered figures and, where practical, the
  scripts and source tables used to generate them.

The current public-facing benchmark series includes a five-laptop
comparison for *Wuthering Waves* v3.7. The wider exploratory dataset for
that version also contains additional laptop and desktop configurations;
it is kept separate from the five-laptop retest.

## Repository layout

The exact folders may expand as more games and versions are added. The
intended structure is like:

``` text
PC-Gaming-Benchmarks/
├── README.md
└── Wuthering-Waves/
    └── 3.7/
        ├── README.md
        ├── charts/
        ├── data/
        │   ├── final-five-laptop-retest/
        │   └── exploratory-vsync-on/
        └── scripts/
```

## Testing principles

1.  **Keep the raw data.** Original captures are retained separately
    from processed tables and charts.
2.  **Document the conditions.** A result is meaningful only with its
    game build, graphics settings, driver, hardware configuration, and
    capture method.
3.  **Do not silently discard inconvenient runs.** Exclusions, retries,
    and aggregation rules should be stated explicitly.
4.  **Separate different test conditions.** Results collected with
    different V-Sync states, frame-generation settings, caps, display
    paths, or warm-up procedures should not be pooled as if they were
    one experiment.
5.  **Prefer repeatable in-game routes.** Real gameplay scenes are
    useful, but route variation, weather, combat events, and other
    uncontrolled factors must be acknowledged.
6.  **Treat cross-device results as observations, not universal
    guarantees.** Laptop power limits, cooling, memory configuration,
    firmware, and display presentation paths can differ substantially.

## How to read the results

- **Average FPS** describes the measured frame-production rate for the
  stated test run and conditions.
- **1% Low** is reported using the method documented in the
  corresponding game report. It should not be assumed to match every
  benchmark tool’s internal implementation exactly.
- **Per-scene results** should be preferred when workloads differ. A
  multi-scene average is meaningful only when its weighting method is
  stated.
- **Version-to-version comparisons** are historical comparisons, not
  automatically controlled experiments. A game update may coincide with
  changes in drivers, caches, synchronization, or test procedure.

## Hardware and test requests

The test matrix is maintained as a personal project and changes over
time. Suggestions for additional devices, scenes, or technical follow-up
tests are welcome. Requests are best-effort: they depend on hardware
availability, reproducibility, and time, and are not guaranteed to be
completed.

## Important limitations

A benchmark result applies to the specific device, game build, settings,
and test path documented in its report. It should not be treated as a
guaranteed result for every laptop with the same GPU name. In
particular:

- Laptop GPU power limits and CPU/GPU sharing policies are not
  necessarily equal.
- Manufacturer performance modes are not directly equivalent across
  brands or models.
- Windows presentation mode and the physical display-output route can
  affect displayed frame pacing independently of the game’s own
  frame-production timing.
- FPS caps can limit the maximum observable result.
- Game updates can change rendering workloads, shaders, caches, and
  performance.

Please read the game-specific README before drawing conclusions from a
chart.

## Reuse and attribution

If you refer to these results, please link to the repository and
identify the game version, device, and test conditions. Raw data and
charts are provided for technical reference; do not assume that
third-party game assets, logos, or other copyrighted material are
licensed for redistribution.

## Licensing

Different types of material in this repository are licensed separately:

- **Source code and scripts:** [MIT License](https://opensource.org/licenses/MIT).
- **Original benchmark data, charts, reports, and documentation:** [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/), to the extent that I hold the relevant rights.
- **Original hardware photographs:** All rights reserved, unless otherwise specified.
- **Game footage, screenshots, trademarks, and third-party assets:** Not covered by the above licenses. Their respective rights remain with their copyright holders.

Reuse of these materials does not imply my endorsement of any product, publication, or organization.

