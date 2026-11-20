# Wuthering Waves v3.7.19 — Five-Laptop Benchmark

**PC Performance Lab | Independent, non-sponsored benchmarking and technical investigation**

This study compares five laptops across three generations of NVIDIA Laptop GPUs using *Wuthering Waves* as a real-world workload. It investigates whole-system performance, run-to-run variation, and differences in frame presentation. It is not a game review or an isolated CPU/GPU benchmark.

The main dataset comprises **50 runs across five laptops and three scenarios**. The earlier V-Sync-On captures and historical version comparisons are supplementary datasets, not part of the main averages.

## 1. Results at a glance

| Laptop | CPU | Laptop GPU | Average FPS | 1% Low FPS |
|---|---|---|---:|---:|
| Legion 5 Pro / R9000P 2021 | Ryzen 7 5800H | RTX 3060 | 66.7 | 33.7 |
| Legion Pro 5 / R9000P 2023 | Ryzen 9 7945HX | RTX 4060 | 88.3 | 43.9 |
| Legion Pro 5 / R9000P 2025 | Ryzen 9 8945HX | RTX 5060 | 97.7 | 48.8 |
| ThinkBook 16p Gen 6 | Core Ultra 7 255HX | RTX 5060 | 100.5 | 52.0 |
| TUF Gaming A14 2025 | Ryzen AI 7 350 | RTX 5060 | 81.6 | 40.2 |

Each scenario is weighted equally in this table, regardless of run count or duration. All 50 runs are included. See `reproducibility/summary_v37.csv` for per-scene results.

### Key observations

- The three RTX 5060 laptops exhibit substantially different performance in this workload. Identical GPU model names do not guarantee identical whole-system performance.
- The RTX 4060 Legion outperforms the RTX 5060 TUF A14 in average FPS in all three measured scenarios. This does not establish that the RTX 4060 is intrinsically faster than the RTX 5060.
- The ThinkBook 16p leads the 2025 Legion in the three-scene mean, but its average-FPS advantage is only about 2.9%. The test does not isolate the CPU, GPU power budget, cooling, memory or presentation path as the cause.
- All five laptops show lower first-run 1% lows in Lahai-Roi than in each of their three subsequent runs. This is consistent with a warm-up effect; the responsible mechanism has not been isolated.

**Read the limitations in Sections 5–8 before generalizing these results.**

## 2. Test platforms and environment

| Device | Model identifier | Memory (as reported by CapFrameX) | Windows 11 |
|---|---|---|---|
| R9000P 2021 | 16ACH6H | 32 GB, 2 × 16 GB, 3200 MT/s | Pro, build 26200 |
| R9000P 2023 | 16ARX8 | 32 GB, 2 × 16 GB, 5200 MT/s | Pro, build 26200 |
| R9000P 2025 | 16ADR10 | 32 GB, 2 × 16 GB, 5200 MT/s | Pro, build 26200 |
| ThinkBook 16p 2025 | 16p G6 IAX | 32 GB, 2 × 16 GB, 5600 MT/s | Home, build 26200 |
| TUF A14 2025 | FA401KM | 32 GB, 4 × 8 GB, 7500 MT/s | Pro, build 26300 |

Memory topology is reproduced from the capture metadata; it should not be interpreted as the number of physically replaceable modules, particularly for soldered memory. Manufacturer model identifiers are provided for reference; regional configurations may differ.

The three R9000P laptops used Lenovo's Beast (Performance) mode; the ThinkBook 16p used High Performance. The more aggressive Lenovo Super mode was not used. The TUF A14's exact operating profile is not independently established in the archived capture metadata. The devices were not power-normalized, and factory performance modes are not equivalent across machines.

| Setting | Value |
|---|---|
| Game version | v3.7.19, Build 9391775 HD (test record) |
| Capture dates | 9–11 November 2026 (local dates in capture filenames) |
| API | DirectX 12 |
| Output resolution | 2560 × 1440 |
| Graphics preset | Quality Priority |
| Upscaling | DLSS Quality |
| Frame Generation | Off |
| In-game V-Sync | Off |
| In-game FPS limit | 120 FPS |
| NVIDIA driver | 596.49 |
| CapFrameX | 1.9.1.5 |
| BIOS virtualization | Disabled (test record) |
| Windows Game Mode / HAGS / Resizable BAR | Enabled / Enabled / Enabled |
| Display | Common external 1440p, 120 Hz monitor |

The game build, graphics settings, and BIOS configuration are based on test records; not every setting is independently embedded in the raw capture files. The capture metadata confirms the API, resolution, driver, capture-tool version and Windows features listed above.

### Display and capture chain

The benchmark uses an external HDMI display path through an AVerMedia GC553G2 capture card and its pass-through output. A separate recording system captures gameplay at 1080p60. This avoids running the video encoder on the benchmark laptop. It does not guarantee identical Windows presentation behavior or physical graphics routing on every device.

The FPS measurements are taken from CapFrameX on the test machine, **not** by counting frames in the 60 FPS video. Video is retained as supporting evidence of the gameplay route and test procedure.

## 3. Scenarios and sample counts

| Scenario | Workload | Runs per device |
|---|---|---:|
| Startorch Academy | Repeatable urban traversal route | 3 |
| Lahai-Roi | Motorcycle traversal route | 4 |
| Whimpering Wastes | Repeatable fixed-team combat route | 3 |
| **Total** | | **10** |

All five laptops followed this 3/4/3 run structure. The fourth scene from the preliminary testing campaign (玄方地界) was omitted from the final retest because weather and route conditions were difficult to standardize. In-game routes and combat events are repeatable procedures, not deterministic replay files.

The internal scene key in the input CSV is `Lahar-Roi`; the public charts use `Lahai-Roi`. Both refer to the same scenario.

## 4. Data and aggregation methodology

For each final run, the application-side `MsBetweenPresents` intervals in the CapFrameX JSON are used to calculate:

- **Average FPS:** 1000 divided by the arithmetic mean of positive frame intervals in milliseconds.
- **1% Low FPS:** 1000 divided by the arithmetic mean of the slowest 1% of those intervals (rounding the sample count up to a whole frame).

These are Present-based metrics, not a count of unique frames actually displayed. The 1% Low definition may differ from other tools' percentile or low-FPS implementations.

The arithmetic mean of run-level Average FPS and 1% Low is computed separately for each device/scenario. The overall summary then averages the three scenario means with equal weight. It is neither a pooled-frame calculation nor an equal-weight mean across all ten individual runs.

The primary results include **every run in the final 50-run dataset**, including the first run of each scene. The separate earlier synchronized dataset is not used in this calculation. Each final CSV record identifies its source JSON filename.

## 5. First-run behavior and sensitivity analysis

The Lahai-Roi first run shows consistently lower 1% lows across all five laptops:

| Device | Run 1 1% Low | Runs 2–4 mean 1% Low |
|---|---:|---:|
| R9000P 2021 | 27.18 | 32.53 |
| R9000P 2023 | 33.37 | 43.04 |
| R9000P 2025 | 40.66 | 43.56 |
| ThinkBook 16p | 43.47 | 49.73 |
| TUF A14 | 36.14 | 39.05 |

The PSO cache was not deliberately cleared for the retest. Therefore, the first run is not a controlled cold-cache measurement. Shader or script warm-up, asset streaming and other factors are plausible explanations, not independently established causes. The same consistent first-run pattern is not present in every scene.

To test whether run selection changes the overall comparison, three aggregation policies were examined. Each cell below shows Average FPS / 1% Low FPS, using equal scenario weighting under every policy.

| Device | All runs (n=50) | Omit Lahai-Roi run 1 (n=45) | Omit every scene's run 1 (n=35) |
|---|---:|---:|---:|
| R9000P 2021 | 66.70 / 33.65 | 66.84 / 34.10 | 66.68 / 34.19 |
| R9000P 2023 | 88.29 / 43.95 | 88.44 / 44.75 | 88.59 / 45.90 |
| R9000P 2025 | 97.74 / 48.76 | 97.69 / 49.00 | 97.92 / 49.92 |
| ThinkBook 16p | 100.55 / 51.99 | 100.73 / 52.51 | 100.19 / 52.40 |
| TUF A14 | 81.64 / 40.17 | 81.71 / 40.41 | 81.75 / 40.57 |

The overall ranking is unchanged under each policy for both metrics. Average FPS changes by less than 0.4% for each laptop relative to the primary result. This is a robustness check against these particular sample-selection choices, not proof of statistical significance or freedom from systematic bias.

The alternative policies are post-hoc analyses. They do not replace the main 50-run dataset or its eight existing charts. Future studies may use a predefined warm-up run followed by a fixed number of measured runs, with the warm-up captures retained separately.

## 6. R9000P 2025: Windows presentation-path limitation

This is an important qualification for interpreting the five-device comparison.

| Capture field | R9000P 2025 (10 runs) | Other four laptops (40 runs) |
|---|---|---|
| CapFrameX presentation label | Windowed or Borderless | Fullscreen Optimized or Borderless |
| PresentMode | 4 — Composed: Flip | Predominantly 3 — Hardware: Independent Flip |
| SyncInterval | 0 | 0 |
| AllowsTearing | 0 | Predominantly 1 |

The R9000P 2023 also contains limited mixed-mode/tearing-flag transitions. The labels do not establish exclusive fullscreen status, physical GPU wiring, or MUX/Optimus state by themselves.

The R9000P 2025 exhibits a much stronger refresh-period pattern in `MsBetweenDisplayChange` than might be inferred from its application-side frame intervals. In all ten final captures, approximately 99.6–99.9% of positive display-change intervals lie within ±0.25 ms of integer multiples of the 120 Hz refresh period (8.33 ms). This is a descriptive observation, not a measurement of dropped-frame percentage or a correction factor for FPS.

`MsBetweenPresents` measures the cadence of application Present calls, whereas `MsBetweenDisplayChange` tracks display changes. Composed presentation can affect display timing, and can also affect application throughput via the presentation pipeline. Thus even Present-based measurements are not guaranteed to represent identical rendering conditions. A direct interpretation of these scores as equivalent displayed smoothness, latency, or uncapped GPU throughput would be inappropriate.

Separate troubleshooting involving **Frame Generation enabled** found different behavior on hybrid internal-panel output, dGPU-direct internal-panel output and external displays. Window-mode changes could also alter the symptom. These observations are not part of the Frame-Generation-Off benchmark, and do not establish that both phenomena share one root cause. The exact driver/Windows/game interaction and any quantitative penalty remain unresolved. A controlled same-device A/B comparison would be required to isolate them.

## 7. Preliminary v3.7 test campaign (V-Sync On)

An earlier campaign recorded 288 JSON captures: eight hardware configurations × four scenarios × three game entries × three runs. It included the five laptops, a ThinkBook 14+ with an RTX 5060 over OCuLink, and Ryzen 9 9950X3D CCD1 desktop configurations with RTX 4060 and RTX 5060.

All 288 captures were recorded with `SyncInterval=1` and `AllowsTearing=0`. Many showed strong refresh-linked timing patterns, including 8.33/16.67/25 ms intervals at 120 Hz. Display-side quantization alone is expected under synchronization and does not establish a game defect. Strong application-side quantization and session-dependent behavior nevertheless motivated the later retest with V-Sync disabled.

The original synchronized measurements are retained for exploratory analysis. They must not be pooled with the final 50 runs or converted into V-Sync-Off results by deleting refresh-quantized frames. Differences between the campaigns can also reflect build and procedure changes.

## 8. Historical comparison and limitations

The four historical comparison charts use v3.4.17, Build 7789993, as a reference for four of the laptops. No matching v3.4 baseline is available for the ThinkBook 16p. Versions 3.5 and 3.6 are not included in the current eight-chart package.

Historical records were not fully standardized for synchronization, cache warm-up, or low-FPS calculation. **The observed differences must not be attributed exclusively to game-side optimization.**

For versions 3.4, 3.5 and 3.6, the original CapFrameX capture files were not consistently archived. The original gameplay recordings were retained, including the benchmark results displayed at the end of the recorded tests. Historical figures can therefore be checked against those recordings where available, but their original frame-level statistics cannot always be recalculated. The historical CSV is a reference table, not reconstructed raw frame-time evidence. Screenshots and a recording index may be added separately as the historical archive is organized.

Other important limitations:

- **Whole-system comparison:** differences in CPU, GPU power limits, cooling, memory, firmware and Windows builds are confounding factors. No universal GPU ranking or isolated CPU performance conclusion is intended.
- **Display topology:** only the common external HDMI test setup is represented in the main results; internal display performance may differ.
- **120 FPS cap / Frame Generation off:** results approaching the cap cannot establish uncapped performance. Generated-frame performance is outside the scope of this study.
- **Small sample sizes and live gameplay:** three or four runs per scene cannot characterize the complete range of performance. Closely spaced scores should not be interpreted as statistically established superiority.
- **Settings and build provenance:** some settings depend on the recorded test procedure rather than raw metadata. The archived data cannot independently establish every environmental condition.

## 9. Charts, data and reproducibility

The following layout is used for the publication package (release assets and supplementary reports may be added separately):

```text
Wuthering-Waves/3.7/
├── README.md
├── charts/
├── laptop_retest_(final_adopted)/
├── original_main_test_5_laptops/
└── reproducibility/
    ├── v37_50runs.csv
    ├── v34_baseline.csv
    ├── summary_v37.csv
    ├── comparison_v34_v37.csv
    └── render_ww37.py
```

| File | Purpose |
|---|---|
| `v37_50runs.csv` | 50 run-level measurements with source JSON filenames and presentation metadata |
| `v34_baseline.csv` | 12 historical reference records (4 devices × 3 scenes) |
| `summary_v37.csv` | 15 device/scenario means and 5 equal-weight overall summaries |
| `comparison_v34_v37.csv` | 12 device/scenario comparisons and 4 overall historical comparisons |
| `render_ww37.py` | Generates the eight English performance charts and both derived CSVs |

Run from the `reproducibility/` directory, with both input CSVs next to the script:

```bash
python -m pip install "matplotlib>=3.6"
python render_ww37.py
```

The script reproduces the published charts from the curated run-level inputs; it does not parse the original JSON or reconstruct the historical records. Its outputs are written next to the script. The charts use the full bar for Average FPS and the dark segment for 1% Low (not stacked independent metrics). In historical charts, widths are normalized to that device/scenario's v3.4 Average FPS, whereas percentage labels for 1% Low refer to the corresponding v3.4 1% Low.

### Figure index

The eight published English figures (filenames from the plotting script) are:

| Figure | Description |
|---|---|
| `01_WW37_Startorch_Academy.png` | Startorch Academy — five-laptop comparison |
| `02_WW37_Lahai_Roi.png` | Lahai-Roi — five-laptop comparison |
| `03_WW37_Whimpering_Wastes.png` | Whimpering Wastes — five-laptop comparison |
| `04_WW37_All_Three_Scenarios.png` | All three scenarios, shown separately |
| `05_WW34_vs_WW37_Startorch_Academy.png` | Historical comparison — Startorch Academy |
| `06_WW34_vs_WW37_Lahai_Roi.png` | Historical comparison — Lahai-Roi |
| `07_WW34_vs_WW37_Whimpering_Wastes.png` | Historical comparison — Whimpering Wastes |
| `08_WW34_vs_WW37_Three_Scene_Mean.png` | Historical comparison — equal-weight mean |

### Raw captures and video evidence

The original final retest archive (`3.7_retest_laptops.zip`) contains 50 JSON captures and 57 CSV exports. The extra CSV exports are not extra benchmark runs. The earlier 288-capture archive (`dddd.zip`) is a separate synchronized dataset. The original recording archive is retained separately due to its size.

GitHub Releases is the intended distribution channel for downloadable raw-data packages; availability depends on which assets have been published. 

The full video captures can be downloaded via Baidu Netdisk: <https://pan.baidu.com/s/1I6ptqzPOwPs8rd4LQFpqyA?pwd=fx5e>

A separate technical report (`REPORT.md`) is planned for deeper analysis of variability, warm-up behavior, presentation paths and historical comparisons. This README provides the study overview, data provenance and principal caveats without claiming that the underlying mechanisms have already been resolved.

## 10. Reuse and feedback

See the repository-level license information for the applicable terms. Original analysis and code should be distinguished from third-party software, game imagery and trademarks. Please identify the game build, test settings and source when citing the results. Reuse does not imply endorsement by PC Performance Lab.

Methodological feedback, reproducibility checks and suggestions for future technical investigations are welcome.
