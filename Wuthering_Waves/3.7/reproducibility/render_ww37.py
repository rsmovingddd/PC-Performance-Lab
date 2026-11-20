#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Wuthering Waves v3.7.19 | Eight English Matplotlib charts.

Rebuild by running: python render_ww37.py
Requires matplotlib >= 3.6, no additional libraries.

Inputs (placed next to this script):
    v37_50runs.csv      -- 50 measured runs from five laptops
    v34_baseline.csv    -- 12 historical v3.4 device/scenario baselines

Outputs:
    01_... through 08_... .png, summary_v37.csv,
    comparison_v34_v37.csv.

Metric definitions:
- v3.7: arithmetic mean of each run's Average FPS and 1% low, separately.
  Three runs at Startorch Academy, four at Lahai-Roi, three at
  Whimpering Wastes. EVERY run (including the first) is included.
- Three-scene means: equal weight for each scene per device (not pooled
  frametimes; and NOT the grouped-bars figure 04, which shows each scene).
- v3.4/v3.7 comparison: all bars for each laptop/scene are plotted relative
  to THAT laptop/scene's v3.4 Average FPS. Thus v3.4 Avg = 100% of chart
  scale, and the 1% Low overlay preserves its actual relative length.
  Text labels for Low percentages use the corresponding v3.4 Low = 100%,
  independently of the displayed horizontal length scale.
- Testing conditions for v3.7: DX12, 2560x1440, Quality Priority preset,
  DLSS Quality, Frame Generation OFF, V-Sync OFF, BIOS virtualization OFF,
  NVIDIA driver 596.49; 3.7.19 Build 9391775 HD.
- v3.4 historical comparisons have not been fully standardized with v3.7
  for synchronization, warm-up, or the computation of historical 1% lows.
  The plotted gaps should not be treated as isolated engine optimizations.
"""
from __future__ import annotations

import csv
import math
from collections import defaultdict
from pathlib import Path
from statistics import mean

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.ticker import MultipleLocator

ROOT = Path(__file__).resolve().parent
plt.rcParams.update({
    'font.family': 'DejaVu Sans',
    'font.sans-serif': ['DejaVu Sans', 'Liberation Sans'],
    'text.color': '#F0F5FC',
    'axes.labelcolor': '#BECDE0',
    'xtick.color': '#9BADBF',
    'ytick.color': '#F0F5FC',
    'font.size': 11,
    'figure.dpi': 100,
    'savefig.dpi': 200,
})

BG = '#080D16'
PANEL = '#101B2B'
WHITE = '#F1F5FA'
SECONDARY = '#BAC9D8'
MUTED = '#94A8BF'
GRID = '#2B3B51'
ACCENT = '#74C5E4'
GOLD = '#E7C989'

# The older CSV uses the internal key 'Lahar-Roi'. Public chart labels use
# the English name adopted in the user-approved Reddit post: 'Lahai-Roi'.
SCENES = ['Startorch Academy', 'Lahar-Roi', 'Whimpering Wastes']
SCENE_DISPLAY = {
    'Startorch Academy': 'STARTORCH ACADEMY',
    'Lahar-Roi': 'LAHAI-ROI',
    'Whimpering Wastes': 'WHIMPERING WASTES',
}
SCENE_NAME_CASE = {
    'Startorch Academy': 'Startorch Academy',
    'Lahar-Roi': 'Lahai-Roi',
    'Whimpering Wastes': 'Whimpering Wastes',
}
SCENE_COLORS = {
    'Startorch Academy': ('#50CAA0', '#277F64'),
    'Lahar-Roi': ('#62ACF4', '#2A609F'),
    'Whimpering Wastes': ('#F2AB70', '#985B35'),
}
DEVICES = [
    'R9000P 2021', 'R9000P 2023', 'R9000P 2025',
    'TUF A14 2025', 'ThinkBook 16p 2025'
]
DEVICE_LABELS = {
    'R9000P 2021': 'Legion 5 Pro 16ACH6H (R9000P 2021H)\nRyzen 7 5800H  |  RTX 3060 Laptop',
    'R9000P 2023': 'Legion Pro 5 16ARX8 (R9000P AXR8)\nRyzen 9 7945HX  |  RTX 4060 Laptop',
    'R9000P 2025': 'Legion Pro 5 16ADR10 (R9000P ADR10)\nRyzen 9 8945HX  |  RTX 5060 Laptop',
    'TUF A14 2025': 'ASUS TUF Gaming A14 (FA401KM)\nRyzen AI 7 350  |  RTX 5060 Laptop',
    'ThinkBook 16p 2025': 'ThinkBook 16p Gen 6 (16p G6 IAX)\nCore Ultra 7 255HX  |  RTX 5060 Laptop',
}


def read_csv(filename):
    with (ROOT / filename).open('r', encoding='utf-8-sig', newline='') as f:
        return list(csv.DictReader(f))


RUNS = read_csv('v37_50runs.csv')
BASELINES = read_csv('v34_baseline.csv')
assert len(RUNS) == 50, f'Expected 50 runs, got {len(RUNS)}'
assert len(BASELINES) == 12, f'Expected 12 baselines, got {len(BASELINES)}'

raw = defaultdict(lambda: {'avg': [], 'low': []})
for r in RUNS:
    pair = (r['device'], r['scene'])
    raw[pair]['avg'].append(float(r['average_fps']))
    raw[pair]['low'].append(float(r['low_1pct_fps']))

AGG = {k: {'avg': mean(v['avg']), 'low': mean(v['low']), 'n': len(v['avg'])}
       for k, v in raw.items()}
BASE = {(r['device'], r['scene']):
        {'avg': float(r['average_fps']), 'low': float(r['low_1pct_fps'])}
        for r in BASELINES}
for device in DEVICES:
    for scene in SCENES:
        assert AGG[device, scene]['n'] == (4 if scene == 'Lahar-Roi' else 3)
        if device != 'ThinkBook 16p 2025':
            assert (device, scene) in BASE


def three_scene_mean(device, metric, baseline=False):
    source = BASE if baseline else AGG
    return mean(source[device, sc][metric] for sc in SCENES)


def write_table(filename, records, fields):
    with (ROOT / filename).open('w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(records)


rows = []
for device in DEVICES:
    for scene in SCENES:
        d = AGG[device, scene]
        rows.append(dict(device=device, scene=SCENE_NAME_CASE[scene],
                         runs=d['n'], average_fps=f'{d["avg"]:.6f}',
                         low_1pct_fps=f'{d["low"]:.6f}'))
    rows.append(dict(device=device, scene='Three-scene equal-weight mean',
                     runs=10, average_fps=f'{three_scene_mean(device,"avg"):.6f}',
                     low_1pct_fps=f'{three_scene_mean(device,"low"):.6f}'))
write_table('summary_v37.csv', rows, list(rows[0]))

cmp_rows = []
for scene in SCENES + ['MEAN']:
    for device in DEVICES[:-1]:
        if scene == 'MEAN':
            b = {k: three_scene_mean(device, k, True) for k in ('avg', 'low')}
            v = {k: three_scene_mean(device, k) for k in ('avg', 'low')}
        else:
            b = BASE[device, scene]
            v = AGG[device, scene]
        cmp_rows.append(dict(device=device,
                             scene='Three-scene equal-weight mean' if scene == 'MEAN' else SCENE_NAME_CASE[scene],
                             avg34=f'{b["avg"]:.6f}', low34=f'{b["low"]:.6f}',
                             avg37=f'{v["avg"]:.6f}', low37=f'{v["low"]:.6f}',
                             avg_change_pct=f'{(v["avg"]/b["avg"]-1)*100:.3f}',
                             low_change_pct=f'{(v["low"]/b["low"]-1)*100:.3f}'))
write_table('comparison_v34_v37.csv', cmp_rows, list(cmp_rows[0]))


def make_canvas(number, section, title, detail, figsize=(16, 9.56)):
    fig = plt.figure(figsize=figsize, facecolor=BG)
    fig.text(.048, .955, 'WUTHERING WAVES   /   PC PERFORMANCE BENCHMARKS',
             color=ACCENT, fontsize=11, fontweight='bold')
    fig.text(.952, .955, f'{number:02d}  /  08', ha='right',
             color='#9AAFC6', fontsize=11.5, fontweight='bold')
    fig.text(.048, .895, section, color='#71CFAE', fontsize=11.5, fontweight='bold')
    fig.text(.048, .829, title, color=WHITE, fontsize=24, fontweight='bold')
    fig.text(.049, .781, detail, color=SECONDARY, fontsize=11.4)
    fig.add_artist(plt.Line2D([.048, .952], [.741, .741],
                               transform=fig.transFigure, color=GRID, lw=1.05))
    return fig


def make_axes(fig, rect, x_max, step=20, xlabel='Frame rate (FPS)'):
    ax = fig.add_axes(rect)
    ax.set_facecolor(PANEL)
    for sp in ax.spines.values():
        sp.set_visible(False)
    ax.set_xlim(0, x_max)
    ax.set_axisbelow(True)
    ax.grid(axis='x', lw=.72, color=GRID, alpha=.78)
    ax.xaxis.set_major_locator(MultipleLocator(step))
    ax.tick_params(axis='y', length=0, pad=16)
    ax.tick_params(axis='x', length=0, labelsize=10.5, pad=7)
    ax.set_xlabel(xlabel, fontsize=11.4, color=SECONDARY, labelpad=12)
    return ax


def put_device_labels(fig, ax, positions, devices, main_size=10.2, sub_size=9.2):
    """A separate, left-aligned label column eliminates the original huge
    empty left gutter created by right-aligned Matplotlib y tick labels.

    Using figure coordinates keeps the label positions synchronized with
    data-space bar centers, without shifting the data axes to the far right.
    """
    lo, hi = ax.get_ylim()
    bounds = ax.get_position()
    for y, dev in zip(positions, devices):
        fig_y = bounds.y0 + bounds.height * (y - lo) / (hi - lo)
        name, specs = DEVICE_LABELS[dev].split('\n', 1)
        fig.text(.051, fig_y + .012, name, ha='left', va='center',
                 fontsize=main_size, fontweight='semibold', color=WHITE)
        fig.text(.051, fig_y - .011, specs, ha='left', va='center',
                 fontsize=sub_size, color=SECONDARY)


def put_legend(fig, entries, xy, size=10.2, ncol=None):
    patches = [Patch(facecolor=color, label=label) for color, label in entries]
    fig.legend(handles=patches, loc='upper left', bbox_to_anchor=xy,
               frameon=False, ncol=ncol or len(entries), fontsize=size,
               labelcolor=SECONDARY, handlelength=1.6, handleheight=.85,
               columnspacing=2.2, borderaxespad=0)


def footer(fig, notes, rule_y=.185, first_y=.161, dy=.025, fontsize=9.5):
    fig.add_artist(plt.Line2D([.048, .952], [rule_y, rule_y],
                               transform=fig.transFigure, color=GRID, lw=.9))
    for i, note in enumerate(notes):
        fig.text(.049, first_y - i * dy, note, color=MUTED, fontsize=fontsize,
                 ha='left', va='top')


def draw_segment_bar(ax, y, average, low, light, dark, height=.53):
    ax.barh(y, low, color=dark, height=height, zorder=3)
    ax.barh(y, average - low, left=low, color=light, height=height, zorder=3)


def save_figure(fig, name):
    path = ROOT / name
    fig.savefig(path, dpi=200, facecolor=BG)
    plt.close(fig)
    return path


def scene_figure(scene, number):
    light, dark = SCENE_COLORS[scene]
    fig = make_canvas(number, '3.7.19  /  FIVE-LAPTOP COMPARISON',
                      SCENE_DISPLAY[scene],
                      'Build 9391775 HD   |   DX12 · 1440p · Quality Priority · DLSS Quality · FG Off · V-Sync Off')
    ax = make_axes(fig, [.278, .270, .662, .408], 120, 20)
    ys = [4-i for i in range(len(DEVICES))]
    for dev, y in zip(DEVICES, ys):
        avg = AGG[dev, scene]['avg']
        low = AGG[dev, scene]['low']
        draw_segment_bar(ax, y, avg, low, light, dark)
        ax.text(low-1.15, y, f'{low:.1f}', ha='right', va='center',
                fontsize=11.7, fontweight='bold', color=WHITE)
        ax.text(avg+1.7, y, f'{avg:.1f}', ha='left', va='center',
                fontsize=12.4, fontweight='bold', color=WHITE)
    ax.set_ylim(-.65, 4.7)
    ax.set_yticks(ys, [''] * len(ys))
    put_device_labels(fig, ax, ys, DEVICES)
    put_legend(fig, [(light, 'Average FPS (full bar)'),
                     (dark, '1% Low FPS (dark overlay)')], (.278, .707))
    footer(fig, [
        'Measurement: 3 runs at Startorch Academy / 4 at Lahai-Roi / 3 at Whimpering Wastes; all runs included.',
        'Settings: 2560 x 1440 · DLSS Quality · Frame Generation Off · V-Sync Off · BIOS virtualization Off.',
        'Metrics: each run measured with CapFrameX; bars show arithmetic means of run-level FPS and 1% lows.',
        'Hardware: manufacturer performance profiles, not necessarily maximum power; power limits differ by laptop.',
    ], fontsize=9.2)
    return save_figure(fig, f'{number:02d}_WW37_{SCENE_NAME_CASE[scene].replace(" ","_").replace("-","_")}.png')


def overview_figure():
    fig = make_canvas(4, '3.7.19  /  FIVE-LAPTOP COMPARISON',
                      'ALL THREE BENCHMARK SCENARIOS',
                      'Build 9391775 HD   |   Five laptops · 3 / 4 / 3 runs per scene   |   Measured FPS, not normalized',
                      figsize=(16, 10.0))
    ax = make_axes(fig, [.278, .239, .662, .440], 120, 20)
    centers = []
    for i, dev in enumerate(DEVICES):
        center = 4.45 - i*1.14
        centers.append(center)
        for j, sc in enumerate(SCENES):
            y = center + .29 - j*.29
            l, d = SCENE_COLORS[sc]
            avg = AGG[dev, sc]['avg']
            low = AGG[dev, sc]['low']
            draw_segment_bar(ax, y, avg, low, l, d, .242)
            ax.text(low-.95, y, f'{low:.1f}', ha='right', va='center',
                    fontsize=9.55, color=WHITE)
            ax.text(avg+1.6, y, f'{avg:.1f}', ha='left', va='center',
                    fontsize=10.2, fontweight='bold', color=WHITE)
        if i < len(DEVICES)-1:
            ax.axhline(center-.575, color=GRID, lw=.9, alpha=.85)
    ax.set_ylim(-.55, 5.18)
    ax.set_yticks(centers, [''] * len(centers))
    put_device_labels(fig, ax, centers, DEVICES, main_size=10.0, sub_size=9.0)
    put_legend(fig, [(SCENE_COLORS[sc][0], SCENE_NAME_CASE[sc]) for sc in SCENES],
               (.278, .709), size=9.7)
    footer(fig, [
        'Each scene is plotted separately: Average FPS = full bar; 1% Low = darker segment.',
        'Per-scene results are arithmetic means of all runs (Startorch 3; Lahai-Roi 4; Whimpering Wastes 3).',
        '3.7 settings: 2560 x 1440 · DX12 · DLSS Quality · FG Off · V-Sync Off · BIOS virtualization Off.',
        'Manufacturer performance presets used; different laptops have different combined CPU/GPU power budgets.',
    ], rule_y=.183, first_y=.159, dy=.025, fontsize=9.25)
    return save_figure(fig, '04_WW37_All_Three_Scenarios.png')


def comparison_figure(scene, number):
    is_mean = (scene == 'MEAN')
    suffix = 'THREE-SCENE EQUAL-WEIGHT MEAN' if is_mean else SCENE_DISPLAY[scene]
    fig = make_canvas(number, '3.4.17  vs  3.7.19  /  HISTORICAL COMPARISON',
                      'VERSION 3.4  vs  3.7   |   ' + suffix,
                      'Per laptop: v3.4 Average FPS = 100% on the horizontal scale   |   DX12 · DLSS Quality · FG Off')
    ax = make_axes(fig, [.278, .273, .662, .429], 145, 20,
                   'Relative FPS (% of that laptop\'s v3.4 Average FPS)')
    ax.axvline(100, color=GOLD, linestyle=(0, (5, 4)), lw=1.45, alpha=.85, zorder=2)
    ax.text(100.6, .985, '100% BASELINE', ha='left', va='top',
            fontsize=9.1, color=GOLD, transform=ax.get_xaxis_transform())
    centers = []
    for i, dev in enumerate(DEVICES[:-1]):
        b = {k: three_scene_mean(dev, k, True) if is_mean else BASE[dev, scene][k]
             for k in ('avg', 'low')}
        v = {k: three_scene_mean(dev, k) if is_mean else AGG[dev, scene][k]
             for k in ('avg', 'low')}
        center = 3.90 - i*1.13
        centers.append(center-.165)
        for ver, y in [('3.4', center), ('3.7', center-.33)]:
            avg = b['avg'] if ver=='3.4' else v['avg']
            low = b['low'] if ver=='3.4' else v['low']
            relative_avg = avg / b['avg'] * 100
            relative_low = low / b['avg'] * 100
            light, dark = (('#68B2F5', '#2D649F') if ver == '3.4'
                           else ('#53D1AA', '#277D65'))
            draw_segment_bar(ax, y, relative_avg, relative_low, light, dark, .276)
            if ver=='3.4':
                low_label = 'Low: 100%'
                avg_label = f'100%  ({b["avg"]:.1f} FPS)'
            else:
                low_delta = (v['low']/b['low'] - 1)*100
                avg_delta = (v['avg']/b['avg'] - 1)*100
                low_label = f'Low: {low_delta:+.1f}%'
                avg_label = f'{relative_avg:.1f}%  ({avg_delta:+.1f}%)'
            ax.text(relative_low - 1.20, y, low_label,
                    ha='right', va='center', fontsize=9.1,
                    fontweight='bold', color=WHITE)
            ax.text(relative_avg + 2.0, y, avg_label,
                    ha='left', va='center', fontsize=10.7,
                    fontweight='bold', color=WHITE)
            ax.text(2.05, y, ver, ha='left', va='center',
                    color='#C8E4FF' if ver == '3.4' else '#C8FAEA',
                    fontsize=9.2, fontweight='bold', zorder=4)
        if i < 3:
            ax.axhline(center-.66, color=GRID, lw=.8, alpha=.82)
    ax.set_ylim(-.02, 4.43)
    ax.set_yticks(centers, [''] * len(centers))
    put_device_labels(fig, ax, centers, DEVICES[:-1])
    put_legend(fig, [('#68B2F5', 'v3.4 reference'),
                     ('#53D1AA', 'v3.7.19 retest'),
                     ('#2D649F', 'Dark segment: 1% Low')],
               (.278, .722), size=10)
    footer(fig, [
        'Bar widths: v3.4 Average = 100%; both Average and Low segments are scaled by that same v3.4 Average.',
        'Labels: "Low: 100%" denotes the v3.4 Low reference; v3.7 Low % changes use v3.4 Low as their baseline.',
        'Versions: 3.4.17 Build 7789993  ->  3.7.19 Build 9391775 HD. New 3.7 tests: V-Sync Off; virtualization Off.',
        'CAUTION: Historical tests differ in V-Sync, cache warm-up, and potentially Low calculations; not isolated engine gains.',
    ], fontsize=9.0)
    if is_mean:
        name = '08_WW34_vs_WW37_Three_Scene_Mean.png'
    else:
        name = f'{number:02d}_WW34_vs_WW37_{SCENE_NAME_CASE[scene].replace(" ","_").replace("-","_")}.png'
    return save_figure(fig, name)


def main():
    all_paths = []
    for i, sc in enumerate(SCENES, 1):
        all_paths.append(scene_figure(sc, i))
    all_paths.append(overview_figure())
    for i, sc in enumerate(SCENES, 5):
        all_paths.append(comparison_figure(sc, i))
    all_paths.append(comparison_figure('MEAN', 8))
    for p in all_paths:
        print(p.name, f'{p.stat().st_size / 1024:.0f} KiB')

if __name__ == '__main__':
    main()
