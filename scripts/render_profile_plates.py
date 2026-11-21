#!/usr/bin/env python3
"""Deterministic living SVG scientific-plate generator for Ablation-Tool's GitHub Profile.

Rooted in Richard S. Gallagher's *Computer Visualization* (1994) and the Nuclide
burnt-orange / instrument-teal / petrol-slate visual system — distinct from Zoe's
nocturnal starlight aesthetic, yet harmoniously aligned across shared research.
Generates self-contained GitHub-safe animated SVGs (dark & light themes).
"""

from __future__ import annotations

import html
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets"

SANS = "'Segoe UI', -apple-system, BlinkMacSystemFont, 'Helvetica Neue', Arial, sans-serif"
SERIF = "Georgia, 'Palatino Linotype', 'Book Antiqua', serif"
MONO = "'JetBrains Mono', 'Fira Code', ui-monospace, SFMono-Regular, Menlo, monospace"

THEMES = {
    "dark": {
        "bg0": "#091219",
        "bg1": "#0E1B26",
        "bg2": "#131828",
        "panel": "#0F1D28",
        "panel_alt": "#132432",
        "border": "#21384A",
        "grid": "#1B3040",
        "ink": "#F2EDE4",
        "ink2": "#B7C8D4",
        "muted": "#7C97A9",
        "orange": "#E85D1A",
        "orange_hi": "#FF8142",
        "teal": "#2DD4BF",
        "teal_mid": "#22A6B3",
        "violet": "#C06EFF",
        "copper": "#F0CFA0",
        "sub_line": "#4B6278",
        "badge_bg": "#0B1620",
    },
    "light": {
        "bg0": "#F6F2E9",
        "bg1": "#EFE9DC",
        "bg2": "#EAE3D4",
        "panel": "#FCFBF7",
        "panel_alt": "#F4EFE4",
        "border": "#CFC4B0",
        "grid": "#DFD6C5",
        "ink": "#13212B",
        "ink2": "#314756",
        "muted": "#5C7180",
        "orange": "#C94810",
        "orange_hi": "#E65F20",
        "teal": "#0D8C85",
        "teal_mid": "#117A8B",
        "violet": "#7C34B5",
        "copper": "#9C6B2E",
        "sub_line": "#96A5B2",
        "badge_bg": "#F7F3EA",
    },
}


def build_hero(mode: str) -> str:
    t = THEMES[mode]
    # Build 9 laminar -> spectral filtration streamlines across the right wind-tunnel viewport
    # Viewport bounds: x=578..1152, y=38..342
    # Threshold plane tau sits around x=838 (tilted slightly in 3D perspective)
    stream_svgs: list[str] = []
    # Mesh background grid lines inside wind tunnel
    mesh_lines: list[str] = []
    for k in range(10):
        u = k / 9.0
        x_top = 602 + u * 524
        x_bot = 594 + u * 524
        mesh_lines.append(
            f'<line x1="{x_top:.1f}" y1="112" x2="{x_bot:.1f}" y2="294" stroke="{t["grid"]}" stroke-width="0.8" opacity="0.65"/>'
        )
    for r in range(6):
        v = r / 5.0
        y_l = 122 + v * 168
        y_r = 104 + v * 176
        mesh_lines.append(
            f'<path d="M 598,{y_l:.1f} Q 856,{(y_l+y_r)/2 - 12:.1f} 1122,{y_r:.1f}" fill="none" stroke="{t["grid"]}" stroke-width="0.8" opacity="0.6"/>'
        )

    for i in range(9):
        y0 = 136.0 + i * 17.5
        xt = 836.0 + (i - 4) * 1.4
        yt = 122.0 + i * 16.4
        pre_path = f"M 606,{y0:.1f} C 696,{y0 - 6:.1f} 768,{yt + 3:.1f} {xt:.1f},{yt:.1f}"

        if i < 5:
            # Above threshold tau: bright laminar orange -> glowing teal-to-violet spectral wake
            y_end = 94.0 + i * 20.5
            post_path = (
                f"M {xt:.1f},{yt:.1f} "
                f"C {xt + 78:.1f},{yt - 28 + i * 2:.1f} {xt + 185:.1f},{y_end - 8:.1f} 1132,{y_end:.1f}"
            )
            full_path = (
                f"M 606,{y0:.1f} C 696,{y0 - 6:.1f} 768,{yt + 3:.1f} {xt:.1f},{yt:.1f} "
                f"C {xt + 78:.1f},{yt - 28 + i * 2:.1f} {xt + 185:.1f},{y_end - 8:.1f} 1132,{y_end:.1f}"
            )
            dur = 4.4 + i * 0.45
            begin = i * 0.65
            stream_svgs.append(f'''
      <path d="{pre_path}" fill="none" stroke="url(#laminarGrad)" stroke-width="2.6" stroke-linecap="round"/>
      <path d="{post_path}" fill="none" stroke="url(#wakeGrad)" stroke-width="2.6" stroke-linecap="round" filter="url(#glow)"/>
      <circle cx="{xt:.1f}" cy="{yt:.1f}" r="3.4" fill="{t["teal"]}" stroke="{t["bg0"]}" stroke-width="1"/>
      <circle r="3.2" fill="{t["orange_hi"]}" filter="url(#glow)">
        <animateMotion dur="{dur:.2f}s" begin="{begin:.2f}s" repeatCount="indefinite" path="{pre_path}"/>
      </circle>
      <circle r="3.2" fill="{t["teal"]}" filter="url(#glow)">
        <animateMotion dur="{dur:.2f}s" begin="{begin + 0.25:.2f}s" repeatCount="indefinite" path="{post_path}"/>
      </circle>''')
        else:
            # Below threshold tau: amber-orange decaying into dashed sub-threshold tail
            y_end = 224.0 + (i - 5) * 20.0
            post_path = (
                f"M {xt:.1f},{yt:.1f} "
                f"C {xt + 74:.1f},{yt + 16:.1f} {xt + 175:.1f},{y_end - 4:.1f} 1126,{y_end:.1f}"
            )
            stream_svgs.append(f'''
      <path d="{pre_path}" fill="none" stroke="{t["orange"]}" stroke-width="1.9" stroke-opacity="0.72" stroke-linecap="round"/>
      <path d="{post_path}" fill="none" stroke="{t["sub_line"]}" stroke-width="1.4" stroke-dasharray="4 5" opacity="0.68"/>
      <circle cx="{xt:.1f}" cy="{yt:.1f}" r="2.4" fill="{t["muted"]}" opacity="0.8"/>''')

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 380" width="1200" height="380" role="img" aria-label="Plate 01: Nicholas Michael Kloster — Independent Intelligence and Security Researcher, Architect of Zoe.">
  <defs>
    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{t["bg0"]}"/>
      <stop offset="55%" stop-color="{t["bg1"]}"/>
      <stop offset="100%" stop-color="{t["bg2"]}"/>
    </linearGradient>
    <linearGradient id="laminarGrad" gradientUnits="userSpaceOnUse" x1="606" y1="180" x2="842" y2="180">
      <stop offset="0%" stop-color="{t["copper"]}"/>
      <stop offset="35%" stop-color="{t["orange_hi"]}"/>
      <stop offset="100%" stop-color="{t["orange"]}"/>
    </linearGradient>
    <linearGradient id="wakeGrad" gradientUnits="userSpaceOnUse" x1="836" y1="150" x2="1132" y2="150">
      <stop offset="0%" stop-color="{t["teal"]}"/>
      <stop offset="62%" stop-color="{t["teal_mid"]}"/>
      <stop offset="100%" stop-color="{t["violet"]}"/>
    </linearGradient>
    <linearGradient id="tauPlane" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="{t["teal"]}" stop-opacity="0.26"/>
      <stop offset="58%" stop-color="{t["teal"]}" stop-opacity="0.14"/>
      <stop offset="100%" stop-color="{t["violet"]}" stop-opacity="0.06"/>
    </linearGradient>
    <linearGradient id="outerFrame" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{t["orange"]}" stop-opacity="0.72"/>
      <stop offset="50%" stop-color="{t["teal"]}" stop-opacity="0.62"/>
      <stop offset="100%" stop-color="{t["violet"]}" stop-opacity="0.65"/>
    </linearGradient>
    <filter id="glow" x="-35%" y="-35%" width="170%" height="170%">
      <feGaussianBlur stdDeviation="2.4" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <clipPath id="clip"><rect x="2" y="2" width="1196" height="376" rx="18"/></clipPath>
  </defs>

  <g clip-path="url(#clip)">
    <rect width="1200" height="380" fill="url(#bgGrad)"/>

    <!-- Subtle top/left technical registration ticks -->
    <g stroke="{t["grid"]}" stroke-width="0.9" opacity="0.65">
      <line x1="28" y1="22" x2="46" y2="22"/>
      <line x1="28" y1="22" x2="28" y2="40"/>
      <line x1="28" y1="358" x2="46" y2="358"/>
      <line x1="28" y1="340" x2="28" y2="358"/>
    </g>

    <!-- Left Editorial Plate Column -->
    <text x="48" y="54" font-family="{MONO}" font-size="10.2" font-weight="700" letter-spacing="1.35" fill="{t["teal"]}">PLATE 01 · SCIENTIFIC VISUALIZATION &amp; AUTONOMOUS INTELLIGENCE</text>

    <line x1="48" y1="70" x2="534" y2="70" stroke="{t["orange"]}" stroke-width="1.6"/>
    <text x="48" y="92" font-family="{SERIF}" font-style="italic" font-size="15.5" font-weight="700" fill="{t["ink"]}">Independent Researcher · Architect &amp; Research Partner of Zoe</text>
    <line x1="48" y1="104" x2="534" y2="104" stroke="{t["orange"]}" stroke-width="1.6"/>

    <text x="46" y="160" font-family="{SANS}" font-size="47" font-weight="800" letter-spacing="-0.6" fill="{t["ink"]}">Nicholas Michael</text>
    <text x="46" y="210" font-family="{SANS}" font-size="47" font-weight="800" letter-spacing="-0.6" fill="{t["orange"]}">Kloster</text>

    <text x="48" y="246" font-family="{SANS}" font-size="15" fill="{t["ink2"]}">Operational Metacognition, Self-Governing Autonomy,</text>
    <text x="48" y="268" font-family="{SANS}" font-size="15" fill="{t["ink2"]}">Volumetric Visual Computing &amp; Adversarial Security Research</text>

    <text x="48" y="302" font-family="{SERIF}" font-style="italic" font-size="14.5" fill="{t["teal"]}">“Transforming the symbolic into the geometric.”</text>

    <line x1="48" y1="322" x2="534" y2="322" stroke="{t["border"]}" stroke-width="1"/>
    <text x="48" y="345" font-family="{MONO}" font-size="9.8" letter-spacing="0.2" fill="{t["muted"]}">Ablation-Tool/zoe · 17 Engines · 62 Layers · 18 Papers · 456 Visuals · 6 CVEs</text>

    <!-- Right Gallagher Scientific Instrument Viewport -->
    <rect x="572" y="32" width="592" height="316" rx="14" fill="{t["panel"]}" stroke="{t["border"]}" stroke-width="1.3"/>
    <text x="594" y="58" font-family="{MONO}" font-size="10.8" letter-spacing="1.4" fill="{t["muted"]}">FIELD: A_τ(p) SPECTRAL FILTRATION</text>
    <circle cx="1014" cy="54" r="3.4" fill="{t["teal"]}">
      <animate attributeName="opacity" values="0.45;1;0.45" dur="2.6s" repeatCount="indefinite"/>
    </circle>
    <text x="1142" y="58" text-anchor="end" font-family="{MONO}" font-size="11" font-weight="700" fill="{t["teal"]}">A_τ(p) = 5 · k*(κ)</text>

    <!-- Background curved computational mesh -->
    {"".join(mesh_lines)}

    <!-- Translucent 3D Threshold Plane tau -->
    <polygon points="824,84 848,74 858,284 834,296" fill="url(#tauPlane)" stroke="{t["teal"]}" stroke-width="1.2" stroke-dasharray="3 3" opacity="0.92"/>
    <text x="855" y="94" font-family="{SERIF}" font-style="italic" font-size="15" font-weight="700" fill="{t["teal"]}">τ</text>

    <!-- Animated Laminar-to-Spectral Streamlines -->
    {"".join(stream_svgs)}

    <!-- Viewport Bottom Instrument Caption -->
    <line x1="594" y1="316" x2="1142" y2="316" stroke="{t["border"]}" stroke-width="0.9"/>
    <text x="594" y="335" font-family="{MONO}" font-size="10.2" letter-spacing="0.9" fill="{t["muted"]}">LAMINAR PRIOR p(x) → THRESHOLD τ → SPECTRAL WAKE</text>
    <text x="1142" y="335" text-anchor="end" font-family="{MONO}" font-size="10.5" font-weight="700" letter-spacing="1.1" fill="{t["orange"]}">PLATE FIG. 1.1</text>
  </g>

  <rect x="2" y="2" width="1196" height="376" rx="18" fill="none" stroke="url(#outerFrame)" stroke-width="1.5"/>
</svg>
'''


def build_atlas(mode: str) -> str:
    t = THEMES[mode]
    c1 = "M 362,162 C 402,162 402,196 426,204"
    c2 = "M 362,324 C 402,324 402,286 426,276"
    c3 = "M 774,204 C 798,196 798,162 838,162"
    c4 = "M 774,276 C 798,286 798,324 838,324"

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 440" width="1200" height="440" role="img" aria-label="Plate 02: The Zoe Research Manifold linking mathematical substrates, autonomy, scientific and security instruments, and open scientific record.">
  <defs>
    <linearGradient id="atBg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{t["bg0"]}"/>
      <stop offset="100%" stop-color="{t["bg1"]}"/>
    </linearGradient>
    <linearGradient id="coneGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="{t["orange_hi"]}"/>
      <stop offset="100%" stop-color="{t["orange"]}"/>
    </linearGradient>
    <filter id="glow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="2.2" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <clipPath id="atClip"><rect x="2" y="2" width="1196" height="436" rx="18"/></clipPath>
  </defs>

  <g clip-path="url(#atClip)">
    <rect width="1200" height="440" fill="url(#atBg)"/>

    <!-- Header bar -->
    <text x="36" y="38" font-family="{MONO}" font-size="11.5" font-weight="700" letter-spacing="2.2" fill="{t["teal"]}">PLATE 02  ·  THE RESEARCH MANIFOLD</text>
    <text x="1164" y="38" text-anchor="end" font-family="{MONO}" font-size="10.8" letter-spacing="1.4" fill="{t["muted"]}">SYMBOLIC THEORY → UNIFIED CORE → INSTRUMENTS &amp; OPEN RECORD</text>
    <line x1="36" y1="54" x2="1164" y2="54" stroke="{t["border"]}" stroke-width="1"/>

    <!-- Animated connectors -->
    <path d="{c1}" fill="none" stroke="{t["orange"]}" stroke-width="1.8" opacity="0.85"/>
    <circle r="3.2" fill="{t["orange_hi"]}" filter="url(#glow)"><animateMotion dur="3.4s" repeatCount="indefinite" path="{c1}"/></circle>

    <path d="{c2}" fill="none" stroke="{t["teal"]}" stroke-width="1.8" opacity="0.85"/>
    <circle r="3.2" fill="{t["teal"]}" filter="url(#glow)"><animateMotion dur="3.8s" begin="0.6s" repeatCount="indefinite" path="{c2}"/></circle>

    <path d="{c3}" fill="none" stroke="{t["violet"]}" stroke-width="1.8" opacity="0.85"/>
    <circle r="3.2" fill="{t["violet"]}" filter="url(#glow)"><animateMotion dur="3.6s" begin="1.1s" repeatCount="indefinite" path="{c3}"/></circle>

    <path d="{c4}" fill="none" stroke="{t["copper"]}" stroke-width="1.8" opacity="0.85"/>
    <circle r="3.2" fill="{t["copper"]}" filter="url(#glow)"><animateMotion dur="4.0s" begin="1.7s" repeatCount="indefinite" path="{c4}"/></circle>

    <!-- Downward link 01 -> 02 -->
    <line x1="198" y1="224" x2="198" y2="254" stroke="{t["orange"]}" stroke-width="1.6"/>
    <polygon points="194,250 202,250 198,258" fill="{t["orange"]}"/>

    <!-- Card 01 -->
    <rect x="36" y="78" width="326" height="146" rx="12" fill="{t["panel"]}" stroke="{t["border"]}" stroke-width="1.2"/>
    <rect x="48" y="94" width="3.5" height="114" rx="2" fill="{t["orange"]}"/>
    <text x="64" y="108" font-family="{MONO}" font-size="10.5" font-weight="700" letter-spacing="1.4" fill="{t["orange"]}">01 · MATHEMATICAL SUBSTRATE</text>
    <text x="64" y="132" font-family="{SANS}" font-size="17" font-weight="700" fill="{t["ink"]}">Accessible Volume &amp; Filtration</text>
    <text x="64" y="152" font-family="{MONO}" font-size="10.5" fill="{t["muted"]}">March 6, 2026 · Kloster Theorem</text>
    <text x="64" y="176" font-family="{SANS}" font-size="12.5" fill="{t["ink2"]}">• Strict threshold measure A_τ(p)</text>
    <text x="64" y="195" font-family="{SANS}" font-size="12.5" fill="{t["ink2"]}">• Spectral generating theorem H(p), M_k(p)</text>
    <text x="64" y="214" font-family="{SANS}" font-size="12.5" fill="{t["ink2"]}">• Stage 4 Mars auto-tuning lens k*(κ)</text>

    <!-- Card 02 -->
    <rect x="36" y="258" width="326" height="148" rx="12" fill="{t["panel"]}" stroke="{t["border"]}" stroke-width="1.2"/>
    <rect x="48" y="274" width="3.5" height="116" rx="2" fill="{t["teal"]}"/>
    <text x="64" y="288" font-family="{MONO}" font-size="10.5" font-weight="700" letter-spacing="1.4" fill="{t["teal"]}">02 · SELF-GOVERNING LOOP</text>
    <text x="64" y="312" font-family="{SANS}" font-size="17" font-weight="700" fill="{t["ink"]}">Autonomy, Play &amp; Evolution</text>
    <text x="64" y="332" font-family="{MONO}" font-size="10.5" fill="{t["muted"]}">L3 Research · L4 Multi-Module · L5 Ph 1–2</text>
    <text x="64" y="356" font-family="{SANS}" font-size="12.5" fill="{t["ink2"]}">• L3 Cycles (14/14) &amp; L4 3-Engine AST (17/17)</text>
    <text x="64" y="375" font-family="{SANS}" font-size="12.5" fill="{t["ink2"]}">• L5 10-Domain Core &amp; Open-World (16+18)</text>
    <text x="64" y="394" font-family="{SANS}" font-size="12.5" fill="{t["ink2"]}">• Native 44-Phoneme Voice &amp; 16 Playroom</text>

    <!-- Central Flagship Card: ZOE -->
    <rect x="426" y="76" width="348" height="332" rx="16" fill="{t["panel_alt"]}" stroke="{t["teal"]}" stroke-width="1.8"/>
    <!-- Registration corner brackets -->
    <path d="M 442,102 L 442,90 L 454,90" fill="none" stroke="{t["teal"]}" stroke-width="1.4"/>
    <path d="M 758,102 L 758,90 L 746,90" fill="none" stroke="{t["teal"]}" stroke-width="1.4"/>

    <text x="452" y="114" font-family="{MONO}" font-size="10.5" font-weight="700" letter-spacing="1.6" fill="{t["teal"]}">FLAGSHIP MONOREPO</text>
    <text x="452" y="152" font-family="{SANS}" font-size="34" font-weight="800" fill="{t["ink"]}">Zoe</text>
    <text x="452" y="174" font-family="{MONO}" font-size="11.5" fill="{t["muted"]}">Ablation-Tool/zoe · Nicholas × Zoe</text>
    <text x="452" y="196" font-family="{SANS}" font-size="13.5" fill="{t["ink2"]}">Visual Computing &amp; Research OS</text>

    <!-- 3D Isometric Cube + Dual Cone Filtration Glyph (top-right inside central card) -->
    <g transform="translate(698,144)">
      <polygon points="0,-46 42,-23 42,23 0,46 -42,23 -42,-23" fill="none" stroke="{t["border"]}" stroke-width="1.3"/>
      <line x1="0" y1="-46" x2="0" y2="46" stroke="{t["grid"]}" stroke-width="1" stroke-dasharray="2 3"/>
      <line x1="-42" y1="-23" x2="0" y2="0" stroke="{t["border"]}" stroke-width="1"/>
      <line x1="42" y1="-23" x2="0" y2="0" stroke="{t["border"]}" stroke-width="1"/>
      <path d="M -26,8 Q 0,-12 28,12" fill="none" stroke="{t["teal"]}" stroke-width="2" filter="url(#glow)"/>
      <path d="M -18,22 Q 4,-6 22,-20" fill="none" stroke="{t["violet"]}" stroke-width="1.6" opacity="0.88"/>
      <polygon points="-14,-24 4,-24 -5,4" fill="url(#coneGrad)" opacity="0.92"/>
      <ellipse cx="-5" cy="-24" rx="9" ry="3.2" fill="{t["copper"]}"/>
      <polygon points="-2,-6 16,-6 7,22" fill="url(#coneGrad)" opacity="0.88"/>
      <ellipse cx="7" cy="-6" rx="9" ry="3.2" fill="{t["orange_hi"]}"/>
    </g>

    <line x1="452" y1="214" x2="748" y2="214" stroke="{t["border"]}" stroke-width="1"/>

    <rect x="452" y="232" width="6" height="6" rx="1" fill="{t["orange"]}"/>
    <text x="468" y="239" font-family="{SANS}" font-size="13" fill="{t["ink"]}">13 runtime source projects · Zero submodules</text>
    <rect x="452" y="258" width="6" height="6" rx="1" fill="{t["teal"]}"/>
    <text x="468" y="265" font-family="{SANS}" font-size="13" fill="{t["ink"]}">17 registered engines · 62 GEM visual layers</text>
    <rect x="452" y="284" width="6" height="6" rx="1" fill="{t["violet"]}"/>
    <text x="468" y="291" font-family="{SANS}" font-size="13" fill="{t["ink"]}">Native Voice · 40 MHz CicadaClock · CERN</text>
    <rect x="452" y="310" width="6" height="6" rx="1" fill="{t["copper"]}"/>
    <text x="468" y="317" font-family="{SANS}" font-size="13" fill="{t["ink"]}">Zero-deception constitution · Verified CI</text>

    <!-- Bottom Legend Pill inside central card -->
    <rect x="452" y="344" width="296" height="40" rx="10" fill="{t["panel"]}" stroke="{t["border"]}" stroke-width="1"/>
    <circle cx="478" cy="364" r="4" fill="{t["orange"]}"/>
    <text x="490" y="368" font-family="{MONO}" font-size="10.2" font-weight="700" fill="{t["ink2"]}">THEORY</text>
    <circle cx="564" cy="364" r="4" fill="{t["teal"]}"/>
    <text x="576" y="368" font-family="{MONO}" font-size="10.2" font-weight="700" fill="{t["ink2"]}">INSTRUMENT</text>
    <circle cx="674" cy="364" r="4" fill="{t["violet"]}"/>
    <text x="686" y="368" font-family="{MONO}" font-size="10.2" font-weight="700" fill="{t["ink2"]}">PROOF</text>

    <!-- Card 03 -->
    <rect x="838" y="78" width="326" height="146" rx="12" fill="{t["panel"]}" stroke="{t["border"]}" stroke-width="1.2"/>
    <rect x="850" y="94" width="3.5" height="114" rx="2" fill="{t["violet"]}"/>
    <text x="866" y="108" font-family="{MONO}" font-size="10.5" font-weight="700" letter-spacing="1.4" fill="{t["violet"]}">03 · APPLIED INSTRUMENTS</text>
    <text x="866" y="132" font-family="{SANS}" font-size="17" font-weight="700" fill="{t["ink"]}">Science, Forensics &amp; Security</text>
    <text x="866" y="152" font-family="{MONO}" font-size="10.5" fill="{t["muted"]}">Dorothy · CERN · Ablation · PALA · Kevlar</text>
    <text x="866" y="176" font-family="{SANS}" font-size="12.5" fill="{t["ink2"]}">• Allen CCFv3 brain atlas (315,932 tris)</text>
    <text x="866" y="195" font-family="{SANS}" font-size="12.5" fill="{t["ink2"]}">• AIARE reverse engineering &amp; Rust carver</text>
    <text x="866" y="214" font-family="{SANS}" font-size="12.5" fill="{t["ink2"]}">• .MOD/.MID Poincaré &amp; MCP firewall</text>

    <!-- Card 04 -->
    <rect x="838" y="258" width="326" height="148" rx="12" fill="{t["panel"]}" stroke="{t["border"]}" stroke-width="1.2"/>
    <rect x="850" y="274" width="3.5" height="116" rx="2" fill="{t["copper"]}"/>
    <text x="866" y="288" font-family="{MONO}" font-size="10.5" font-weight="700" letter-spacing="1.4" fill="{t["copper"]}">04 · OPEN SCIENTIFIC RECORD</text>
    <text x="866" y="312" font-family="{SANS}" font-size="17" font-weight="700" fill="{t["ink"]}">Monographs, Archive &amp; Integrity</text>
    <text x="866" y="332" font-family="{MONO}" font-size="10.5" fill="{t["muted"]}">18 PDFs · 9 Monographs · Sessions</text>
    <text x="866" y="356" font-family="{SANS}" font-size="12.5" fill="{t["ink2"]}">• 23-p. Zoe Universe &amp; 87-p. Autonomy PDFs</text>
    <text x="866" y="375" font-family="{SANS}" font-size="12.5" fill="{t["ink2"]}">• 456 visuals · SHA-256 &amp; PKCS #7 sigs</text>
    <text x="866" y="394" font-family="{SANS}" font-size="12.5" fill="{t["ink2"]}">• 34-turn TrueColor Session Chronicles</text>
  </g>
  <rect x="2" y="2" width="1196" height="436" rx="18" fill="none" stroke="{t["border"]}" stroke-width="1.5"/>
</svg>
'''


def build_metrics(mode: str) -> str:
    t = THEMES[mode]
    # Balanced 3x2 telemetry grid: 6 cards of width=364, height=164
    wave_pts = " ".join(
        f"{'M' if i == 0 else 'L'} {24 + i * 8:.1f},{84 - 16 * math.sin(i * 0.48) * math.exp(-abs(i - 20) * 0.04):.1f}"
        for i in range(41)
    )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 436" width="1200" height="436" role="img" aria-label="Plate 03: Measured Empirical Signatures and Preserved Negative Controls across L0-L5, Native Voice, Groove, and Dorothy.">
  <defs>
    <linearGradient id="mBg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{t["bg0"]}"/>
      <stop offset="100%" stop-color="{t["bg1"]}"/>
    </linearGradient>
    <clipPath id="mClip"><rect x="2" y="2" width="1196" height="432" rx="18"/></clipPath>
  </defs>

  <g clip-path="url(#mClip)">
    <rect width="1200" height="436" fill="url(#mBg)"/>

    <text x="36" y="36" font-family="{MONO}" font-size="11.5" font-weight="700" letter-spacing="2.2" fill="{t["teal"]}">PLATE 03  ·  EMPIRICAL SIGNATURES &amp; NEGATIVE CONTROLS (L0–L5 · VOICE · CLOCK)</text>
    <text x="1164" y="36" text-anchor="end" font-family="{MONO}" font-size="10.2" letter-spacing="1.1" fill="{t["muted"]}">ALL METRICS REPRODUCIBLE FROM CANONICAL REPOSITORIES</text>
    <line x1="36" y1="50" x2="1164" y2="50" stroke="{t["border"]}" stroke-width="1"/>

    <!-- FIG 3A: Kloster Spectral Filtration -->
    <g transform="translate(36,68)">
      <rect width="364" height="164" rx="12" fill="{t["panel"]}" stroke="{t["border"]}" stroke-width="1.2"/>
      <text x="18" y="26" font-family="{MONO}" font-size="10" fill="{t["muted"]}">FIG 3A</text>
      <text x="346" y="26" text-anchor="end" font-family="{MONO}" font-size="10.5" font-weight="700" fill="{t["teal"]}">4/4 BENCHMARKS</text>
      <text x="18" y="48" font-family="{SANS}" font-size="15.5" font-weight="700" fill="{t["ink"]}">Kloster Spectral Filtration</text>

      <text x="18" y="76" font-family="{MONO}" font-size="10.2" font-weight="700" fill="{t["ink"]}">M₄^(1/4)</text>
      <rect x="92" y="65" width="184" height="13" rx="4" fill="{t["teal"]}"/>
      <text x="346" y="76" text-anchor="end" font-family="{MONO}" font-size="10.2" fill="{t["teal"]}">4/4 wins</text>

      <text x="18" y="98" font-family="{MONO}" font-size="10.2" fill="{t["ink2"]}">Slice A_τ</text>
      <rect x="92" y="87" width="144" height="13" rx="4" fill="{t["teal_mid"]}" opacity="0.8"/>
      <text x="346" y="98" text-anchor="end" font-family="{MONO}" font-size="10.2" fill="{t["muted"]}">baseline</text>

      <text x="18" y="120" font-family="{MONO}" font-size="10.2" fill="{t["ink2"]}">Naive JSD</text>
      <rect x="92" y="109" width="76" height="13" rx="4" fill="{t["orange"]}"/>
      <text x="346" y="120" text-anchor="end" font-family="{MONO}" font-size="10.2" fill="{t["orange"]}">0.4087 ctrl</text>

      <text x="18" y="149" font-family="{MONO}" font-size="9.8" fill="{t["orange"]}">Negative control preserved visibly</text>
    </g>

    <!-- FIG 3B: Stage 4 Mars Adaptive Lens -->
    <g transform="translate(418,68)">
      <rect width="364" height="164" rx="12" fill="{t["panel"]}" stroke="{t["border"]}" stroke-width="1.2"/>
      <text x="18" y="26" font-family="{MONO}" font-size="10" fill="{t["muted"]}">FIG 3B</text>
      <text x="346" y="26" text-anchor="end" font-family="{MONO}" font-size="10.5" font-weight="700" fill="{t["teal"]}">AUROC 0.79374</text>
      <text x="18" y="48" font-family="{SANS}" font-size="15.5" font-weight="700" fill="{t["ink"]}">Stage 4 Mars Lens k*(κ)</text>

      <line x1="22" y1="126" x2="342" y2="126" stroke="{t["border"]}" stroke-width="1"/>
      <line x1="22" y1="64" x2="22" y2="126" stroke="{t["border"]}" stroke-width="1"/>
      <line x1="22" y1="115" x2="342" y2="115" stroke="{t["muted"]}" stroke-width="1" stroke-dasharray="3 3"/>
      <line x1="22" y1="102" x2="342" y2="102" stroke="{t["teal_mid"]}" stroke-width="1.1" stroke-dasharray="3 3"/>
      <path d="M 30,90 Q 182,76 334,86" fill="none" stroke="{t["orange"]}" stroke-width="2.2"/>
      <line x1="22" y1="73" x2="176" y2="73" stroke="{t["teal"]}" stroke-width="1.3" stroke-dasharray="2 3"/>
      <circle cx="176" cy="73" r="4.5" fill="{t["teal"]}"/>
      <text x="186" y="77" font-family="{MONO}" font-size="10.2" font-weight="700" fill="{t["teal"]}">k*(κ) 0.79374</text>
      <text x="340" y="100" text-anchor="end" font-family="{MONO}" font-size="9.2" fill="{t["teal_mid"]}">A_τ 0.7738</text>
      <text x="340" y="113" text-anchor="end" font-family="{MONO}" font-size="9.2" fill="{t["muted"]}">H(p) 0.7631</text>

      <text x="18" y="149" font-family="{MONO}" font-size="9.8" fill="{t["muted"]}">Beats every fixed k ∈ [1.5, 8.0] unlabeled</text>
    </g>

    <!-- FIG 3C: L3 & L4 Multi-Module Evolution -->
    <g transform="translate(800,68)">
      <rect width="364" height="164" rx="12" fill="{t["panel"]}" stroke="{t["border"]}" stroke-width="1.2"/>
      <text x="18" y="26" font-family="{MONO}" font-size="10" fill="{t["muted"]}">FIG 3C</text>
      <text x="346" y="26" text-anchor="end" font-family="{MONO}" font-size="10.5" font-weight="700" fill="{t["teal"]}">17/17 VERIFIER</text>
      <text x="18" y="48" font-family="{SANS}" font-size="15.5" font-weight="700" fill="{t["ink"]}">L3 &amp; L4 Multi-Module Evolution</text>

      <line x1="26" y1="122" x2="342" y2="122" stroke="{t["border"]}" stroke-width="1"/>
      <polyline points="54,113 136,88 218,74" fill="none" stroke="{t["teal"]}" stroke-width="2.4"/>
      <line x1="218" y1="74" x2="306" y2="108" stroke="{t["orange"]}" stroke-width="1.8" stroke-dasharray="4 3"/>
      <circle cx="54" cy="113" r="4" fill="{t["teal"]}"/>
      <circle cx="136" cy="88" r="4" fill="{t["teal"]}"/>
      <circle cx="218" cy="74" r="4.5" fill="{t["teal"]}"/>
      <text x="218" y="65" text-anchor="middle" font-family="{MONO}" font-size="10" font-weight="700" fill="{t["teal"]}">0.7625 (3 eng)</text>
      <text x="72" y="115" font-family="{MONO}" font-size="9.5" fill="{t["muted"]}">0.597</text>
      <text x="306" y="112" text-anchor="middle" font-family="{MONO}" font-size="12" font-weight="700" fill="{t["orange"]}">×</text>
      <text x="54" y="133" text-anchor="middle" font-family="{MONO}" font-size="9" fill="{t["muted"]}">G0</text>
      <text x="136" y="133" text-anchor="middle" font-family="{MONO}" font-size="9" fill="{t["muted"]}">G1</text>
      <text x="218" y="133" text-anchor="middle" font-family="{MONO}" font-size="9" fill="{t["teal"]}">G2</text>
      <text x="306" y="133" text-anchor="middle" font-family="{MONO}" font-size="9" fill="{t["orange"]}">G3×</text>

      <text x="18" y="149" font-family="{MONO}" font-size="9.8" fill="{t["orange"]}">15/15 seeds · 17/17 probes · 0.0 rollback</text>
    </g>

    <!-- FIG 3D: L5 Phases 1 & 2 Core + Open-World -->
    <g transform="translate(36,250)">
      <rect width="364" height="164" rx="12" fill="{t["panel"]}" stroke="{t["border"]}" stroke-width="1.2"/>
      <text x="18" y="26" font-family="{MONO}" font-size="10" fill="{t["muted"]}">FIG 3D · L5 IN PROGRESS</text>
      <text x="346" y="26" text-anchor="end" font-family="{MONO}" font-size="10.5" font-weight="700" fill="{t["teal"]}">16/16 + 18/18</text>
      <text x="18" y="48" font-family="{SANS}" font-size="15.5" font-weight="700" fill="{t["ink"]}">L5 Phases 1 &amp; 2 Core + Open-World</text>

      <text x="18" y="76" font-family="{MONO}" font-size="9.8" font-weight="700" fill="{t["ink"]}">Ph1 (10/10)</text>
      <rect x="104" y="65" width="182" height="12" rx="4" fill="{t["teal"]}"/>
      <text x="346" y="76" text-anchor="end" font-family="{MONO}" font-size="10" font-weight="700" fill="{t["teal"]}">0.9777</text>

      <text x="18" y="97" font-family="{MONO}" font-size="9.8" font-weight="700" fill="{t["ink"]}">Ph2 (5/5)</text>
      <rect x="104" y="86" width="180" height="12" rx="4" fill="{t["violet"]}"/>
      <text x="346" y="97" text-anchor="end" font-family="{MONO}" font-size="10" font-weight="700" fill="{t["violet"]}">0.9730</text>

      <text x="18" y="118" font-family="{MONO}" font-size="9.8" fill="{t["ink2"]}">Ctrls Mean</text>
      <rect x="104" y="107" width="48" height="12" rx="4" fill="{t["orange"]}"/>
      <text x="346" y="118" text-anchor="end" font-family="{MONO}" font-size="10" fill="{t["orange"]}">0.2646 ctrl</text>

      <text x="18" y="136" font-family="{MONO}" font-size="9.5" fill="{t["ink2"]}">AST repair 15/15 · 2,400-ep mem · 16 LLMs</text>
      <text x="18" y="152" font-family="{MONO}" font-size="9.8" fill="{t["orange"]}">l5_agi_qualified=False · Zero PyTorch</text>
    </g>

    <!-- FIG 3E: Zoe Native Voice & Cymatics -->
    <g transform="translate(418,250)">
      <rect width="364" height="164" rx="12" fill="{t["panel"]}" stroke="{t["border"]}" stroke-width="1.2"/>
      <text x="18" y="26" font-family="{MONO}" font-size="10" fill="{t["muted"]}">FIG 3E · ACOUSTICS &amp; VDI</text>
      <text x="346" y="26" text-anchor="end" font-family="{MONO}" font-size="10.5" font-weight="700" fill="{t["violet"]}">14/14 VERIFIER</text>
      <text x="18" y="48" font-family="{SANS}" font-size="15.5" font-weight="700" fill="{t["ink"]}">Zoe Native Voice &amp; Cymatics</text>

      <rect x="18" y="58" width="328" height="50" rx="6" fill="{t["panel_alt"]}" stroke="{t["border"]}" stroke-width="0.8"/>
      <line x1="24" y1="84" x2="340" y2="84" stroke="{t["border"]}" stroke-width="0.9"/>
      <path d="{wave_pts}" fill="none" stroke="{t["teal"]}" stroke-width="1.8"/>
      <circle cx="72" cy="70" r="3" fill="{t["violet"]}"/>
      <circle cx="128" cy="96" r="3" fill="{t["orange_hi"]}"/>
      <circle cx="184" cy="68" r="3.4" fill="{t["teal"]}"/>
      <circle cx="240" cy="98" r="3" fill="{t["copper"]}"/>
      <circle cx="296" cy="72" r="3" fill="{t["violet"]}"/>
      <text x="72" y="66" text-anchor="middle" font-family="{MONO}" font-size="8" fill="{t["muted"]}">F1</text>
      <text x="128" y="66" text-anchor="middle" font-family="{MONO}" font-size="8" fill="{t["muted"]}">F2</text>
      <text x="184" y="64" text-anchor="middle" font-family="{MONO}" font-size="8" fill="{t["teal"]}">F3</text>
      <text x="240" y="66" text-anchor="middle" font-family="{MONO}" font-size="8" fill="{t["muted"]}">F4</text>
      <text x="296" y="66" text-anchor="middle" font-family="{MONO}" font-size="8" fill="{t["muted"]}">F5</text>

      <text x="18" y="122" font-family="{MONO}" font-size="9.6" fill="{t["ink"]}">44 phonemes · 332 rules · pitch ≤ 0.31%</text>
      <text x="18" y="137" font-family="{MONO}" font-size="9.6" fill="{t["ink2"]}">Woodworth ±45° ITD/ILD · 3-bitplane VDI</text>
      <text x="18" y="152" font-family="{MONO}" font-size="9.8" fill="{t["teal"]}">Zero external TTS · bit_diff = 0</text>
    </g>

    <!-- FIG 3F: Groove, Clock & Dorothy Atlas -->
    <g transform="translate(800,250)">
      <rect width="364" height="164" rx="12" fill="{t["panel"]}" stroke="{t["border"]}" stroke-width="1.2"/>
      <text x="18" y="26" font-family="{MONO}" font-size="10" fill="{t["muted"]}">FIG 3F · TEMPORAL &amp; CCFv3</text>
      <text x="346" y="26" text-anchor="end" font-family="{MONO}" font-size="10.5" font-weight="700" fill="{t["teal"]}">R = 0.9334</text>
      <text x="18" y="48" font-family="{SANS}" font-size="15.5" font-weight="700" fill="{t["ink"]}">Groove, Clock &amp; Dorothy Atlas</text>

      <rect x="18" y="62" width="78" height="66" rx="6" fill="{t["panel_alt"]}" stroke="{t["border"]}" stroke-width="0.9"/>
      <ellipse cx="57" cy="95" rx="28" ry="7" transform="rotate(42 57 95)" fill="none" stroke="{t["orange"]}" stroke-width="1.7"/>
      <circle cx="43" cy="82" r="2.1" fill="{t["teal"]}"/>
      <circle cx="71" cy="108" r="2.1" fill="{t["teal"]}"/>
      <circle cx="49" cy="87" r="1.9" fill="{t["orange_hi"]}"/>
      <circle cx="65" cy="103" r="1.9" fill="{t["orange_hi"]}"/>
      <circle cx="57" cy="95" r="1.8" fill="{t["violet"]}"/>

      <text x="108" y="76" font-family="{MONO}" font-size="9.5" fill="{t["teal"]}">Swing ρ₁=−0.978 vs −0.060</text>
      <text x="108" y="96" font-family="{MONO}" font-size="9.5" fill="{t["ink"]}">Event-Causal 71.24 cyc/s</text>
      <text x="108" y="116" font-family="{MONO}" font-size="9.5" fill="{t["violet"]}">Dorothy 315,932 tris · 40Hz</text>

      <text x="18" y="152" font-family="{MONO}" font-size="9.8" fill="{t["orange"]}">.MOD 0.0 bits · 12 CCFv3 · clinical=False</text>
    </g>
  </g>

  <rect x="2" y="2" width="1196" height="432" rx="18" fill="none" stroke="{t["border"]}" stroke-width="1.5"/>
</svg>
'''


def build_pillars(mode: str) -> str:
    t = THEMES[mode]
    c_left = "M 448,149 L 468,149"
    c_right = "M 732,149 L 752,149"
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 256" width="1200" height="256" role="img" aria-label="Plate 04: The Two Pillars — Adversarial Rigor and Mathematical Autonomy bridged by the Epistemic Firewall.">
  <defs>
    <linearGradient id="pBg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{t["bg0"]}"/>
      <stop offset="100%" stop-color="{t["bg1"]}"/>
    </linearGradient>
    <filter id="pGlow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="2.0" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <clipPath id="pClip"><rect x="2" y="2" width="1196" height="252" rx="16"/></clipPath>
  </defs>
  <g clip-path="url(#pClip)">
    <rect width="1200" height="256" fill="url(#pBg)"/>
    <text x="34" y="36" font-family="{MONO}" font-size="11.2" font-weight="700" letter-spacing="2.0" fill="{t["teal"]}">PLATE 04  ·  THE TWO PILLARS: ADVERSARIAL RIGOR × MATHEMATICAL AUTONOMY</text>
    <text x="1166" y="36" text-anchor="end" font-family="{MONO}" font-size="10.2" letter-spacing="1.2" fill="{t["muted"]}">EPISTEMIC FIREWALL BRIDGE</text>
    <line x1="34" y1="48" x2="1166" y2="48" stroke="{t["border"]}" stroke-width="1"/>

    <!-- Bridge Connectors -->
    <line x1="448" y1="149" x2="468" y2="149" stroke="{t["orange"]}" stroke-width="2" opacity="0.85"/>
    <circle r="3.0" fill="{t["orange_hi"]}" filter="url(#pGlow)">
      <animateMotion dur="2.2s" repeatCount="indefinite" path="{c_left}"/>
    </circle>
    <line x1="732" y1="149" x2="752" y2="149" stroke="{t["violet"]}" stroke-width="2" opacity="0.85"/>
    <circle r="3.0" fill="{t["teal"]}" filter="url(#pGlow)">
      <animateMotion dur="2.2s" begin="0.8s" repeatCount="indefinite" path="{c_right}"/>
    </circle>

    <!-- Left Pillar Card -->
    <g transform="translate(34,64)">
      <rect width="414" height="170" rx="12" fill="{t["panel"]}" stroke="{t["border"]}" stroke-width="1.2"/>
      <line x1="12" y1="2" x2="402" y2="2" stroke="{t["orange"]}" stroke-width="3" stroke-linecap="round"/>
      <text x="20" y="28" font-family="{MONO}" font-size="10" font-weight="700" letter-spacing="1.2" fill="{t["orange"]}">PILLAR I · TACTICAL &amp; ADVERSARIAL GROUNDING</text>
      <text x="20" y="52" font-family="{SANS}" font-size="16.5" font-weight="700" fill="{t["ink"]}">Real-World Defense &amp; Discipline</text>
      <text x="20" y="78" font-family="{SANS}" font-size="11.8" fill="{t["ink2"]}">• 8+ yrs U.S. Army Infantry SSG · 2× Afghanistan</text>
      <text x="20" y="100" font-family="{SANS}" font-size="11.8" fill="{t["ink2"]}">• SQI E Military Mountaineer · Resilience (8R)</text>
      <text x="20" y="122" font-family="{SANS}" font-size="11.8" fill="{t["ink2"]}">• 6 CVEs (Cisco FMC/ISE 9.0 Crit · CISA ICS)</text>
      <text x="20" y="144" font-family="{SANS}" font-size="11.8" fill="{t["ink2"]}">• 4 ISE Hardening · CISA ICS/OT · 109 DC3</text>
    </g>

    <!-- Central Epistemic Bridge -->
    <g transform="translate(468,64)">
      <rect width="264" height="170" rx="12" fill="{t["panel_alt"]}" stroke="{t["teal"]}" stroke-width="1.6"/>
      <text x="132" y="24" text-anchor="middle" font-family="{MONO}" font-size="9.8" font-weight="700" letter-spacing="1.4" fill="{t["teal"]}">SHARED COVENANT</text>
      <polygon points="132,36 146,50 132,64 118,50" fill="none" stroke="{t["orange"]}" stroke-width="1.5" filter="url(#pGlow)"/>
      <polygon points="132,42 140,50 132,58 124,50" fill="{t["teal"]}" opacity="0.88"/>
      <text x="132" y="84" text-anchor="middle" font-family="{MONO}" font-size="11.5" font-weight="700" fill="{t["ink"]}">EPISTEMIC FIREWALL</text>
      <text x="132" y="106" text-anchor="middle" font-family="{MONO}" font-size="10.8" font-weight="700" fill="{t["teal"]}">measurement ≠ evidence</text>
      <text x="132" y="124" text-anchor="middle" font-family="{MONO}" font-size="10.8" font-weight="700" fill="{t["orange"]}">≠ belief update ≠ action</text>
      <text x="132" y="152" text-anchor="middle" font-family="{MONO}" font-size="9.6" fill="{t["muted"]}">Security discipline enforces honesty</text>
    </g>

    <!-- Right Pillar Card -->
    <g transform="translate(752,64)">
      <rect width="414" height="170" rx="12" fill="{t["panel"]}" stroke="{t["border"]}" stroke-width="1.2"/>
      <line x1="12" y1="2" x2="402" y2="2" stroke="{t["violet"]}" stroke-width="3" stroke-linecap="round"/>
      <text x="20" y="28" font-family="{MONO}" font-size="10" font-weight="700" letter-spacing="1.2" fill="{t["violet"]}">PILLAR II · MATHEMATICAL &amp; GENERATIVE HEART</text>
      <text x="20" y="52" font-family="{SANS}" font-size="16.5" font-weight="700" fill="{t["ink"]}">Operational Metacognition &amp; Zoe</text>
      <text x="20" y="78" font-family="{SANS}" font-size="11.8" fill="{t["ink2"]}">• Originated A_τ(p) (Mar 6, 2026) &amp; Kloster Thm</text>
      <text x="20" y="100" font-family="{SANS}" font-size="11.8" fill="{t["ink2"]}">• L3 Cycles, L4 3-Engine AST &amp; L5 Ph 1–2 Core</text>
      <text x="20" y="122" font-family="{SANS}" font-size="11.8" fill="{t["ink2"]}">• Native 44-Phoneme Voice, Cymatics &amp; CCFv3</text>
      <text x="20" y="144" font-family="{SANS}" font-size="11.8" fill="{t["ink2"]}">• 34-Turn, 1,414-Step TrueColor Session Logs</text>
    </g>
  </g>
  <rect x="2" y="2" width="1196" height="252" rx="16" fill="none" stroke="{t["border"]}" stroke-width="1.4"/>
</svg>
'''


def build_security(mode: str) -> str:
    t = THEMES[mode]
    cols = [
        ("6 CVEs", "CISCO FMC/ISE & CISA ICS", "Up to 9.0 Critical · Peer impersonation, root privesc, SSO forgery, OCSP & ICS", t["orange"]),
        ("4 DEFECTS", "CISCO ISE HARDENING", "Oracle creds, unauth SSE API bindings, expired CA & Tomcat shutdown", t["teal"]),
        ("8+ YEARS", "U.S. ARMY INFANTRY SSG", "11B3O · 2× Afghanistan · Master Resilience (8R) · SQI E Mountaineer", t["copper"]),
        ("ICS / DFIR", "FEDERAL & CYBER TRAINING", "CISA ICS/OT · ITDRC · GETS/WPS Admin · 22 FEMA EMI · 109 DC3 Courses", t["violet"]),
    ]

    blocks_clean: list[str] = []
    lines_map = [
        ("Up to 9.0 Critical · Peer impersonation,", "root privesc, SSO forgery & CISA ICS"),
        ("Hardcoded Oracle creds, unauth SSE", "API bindings, expired CA & Tomcat"),
        ("11B3O · 2× Afghanistan deployments", "Master Resilience (8R) · SQI E Mountaineer"),
        ("CISA ICS/OT · ITDRC · GETS/WPS Admin", "22 FEMA EMI · 109 DC3 Academy courses"),
    ]
    for idx, (stat, title, _desc, accent) in enumerate(cols):
        x = 34 + idx * 288
        l1, l2 = lines_map[idx]
        blocks_clean.append(f'''
    <g transform="translate({x},62)">
      <rect width="268" height="122" rx="11" fill="{t["panel"]}" stroke="{t["border"]}" stroke-width="1.2"/>
      <line x1="12" y1="2" x2="256" y2="2" stroke="{accent}" stroke-width="3" stroke-linecap="round"/>
      <text x="18" y="36" font-family="{SANS}" font-size="23" font-weight="800" fill="{accent}">{html.escape(stat)}</text>
      <text x="18" y="56" font-family="{MONO}" font-size="10" font-weight="700" letter-spacing="1.0" fill="{t["ink"]}">{html.escape(title)}</text>
      <text x="18" y="82" font-family="{SANS}" font-size="11.5" fill="{t["ink2"]}">{html.escape(l1)}</text>
      <text x="18" y="100" font-family="{SANS}" font-size="11.5" fill="{t["ink2"]}">{html.escape(l2)}</text>
    </g>''')

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 206" width="1200" height="206" role="img" aria-label="Plate 05: Security Research Disclosures, U.S. Army Service, and Federal ICS/Cyber Training.">
  <defs>
    <linearGradient id="secBg" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="{t["bg0"]}"/>
      <stop offset="100%" stop-color="{t["bg1"]}"/>
    </linearGradient>
    <clipPath id="secClip"><rect x="2" y="2" width="1196" height="202" rx="16"/></clipPath>
  </defs>
  <g clip-path="url(#secClip)">
    <rect width="1200" height="206" fill="url(#secBg)"/>
    <text x="34" y="36" font-family="{MONO}" font-size="11.5" font-weight="700" letter-spacing="2.2" fill="{t["orange"]}">PLATE 05  ·  OPERATIONAL TRACK RECORD &amp; SECURITY DISCLOSURES</text>
    <text x="1166" y="36" text-anchor="end" font-family="{MONO}" font-size="10.2" letter-spacing="1.2" fill="{t["muted"]}">GROUNDED IN ADVERSARIAL REALITY</text>
    <line x1="34" y1="48" x2="1166" y2="48" stroke="{t["border"]}" stroke-width="1"/>
    {"".join(blocks_clean)}
  </g>
  <rect x="2" y="2" width="1196" height="202" rx="16" fill="none" stroke="{t["border"]}" stroke-width="1.4"/>
</svg>
'''


def build_footer(mode: str) -> str:
    t = THEMES[mode]
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 186" width="1200" height="186" role="img" aria-label="Closing Colophon — Nicholas Michael Kloster x Zoe.">
  <defs>
    <linearGradient id="ftBg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{t["bg0"]}"/>
      <stop offset="100%" stop-color="{t["bg2"]}"/>
    </linearGradient>
    <linearGradient id="ftRule" gradientUnits="userSpaceOnUse" x1="120" y1="126" x2="1080" y2="126">
      <stop offset="0%" stop-color="{t["orange"]}" stop-opacity="0"/>
      <stop offset="30%" stop-color="{t["orange"]}" stop-opacity="0.8"/>
      <stop offset="70%" stop-color="{t["teal"]}" stop-opacity="0.8"/>
      <stop offset="100%" stop-color="{t["violet"]}" stop-opacity="0"/>
    </linearGradient>
    <clipPath id="ftClip"><rect x="2" y="2" width="1196" height="182" rx="16"/></clipPath>
  </defs>
  <g clip-path="url(#ftClip)">
    <rect width="1200" height="186" fill="url(#ftBg)"/>
    <text x="600" y="54" text-anchor="middle" font-family="{SERIF}" font-style="italic" font-size="16.5" fill="{t["ink"]}">
      “Visualization is about transforming the symbolic into the geometric… letting users observe their simulations directly.”
    </text>
    <text x="600" y="78" text-anchor="middle" font-family="{MONO}" font-size="10.2" letter-spacing="1.4" fill="{t["muted"]}">RICHARD S. GALLAGHER · COMPUTER VISUALIZATION</text>
    <text x="600" y="110" text-anchor="middle" font-family="{SERIF}" font-size="16" font-weight="700" fill="{t["teal"]}">
      “When in doubt, choose freedom and dignity. And no deception.”
    </text>
    <line x1="120" y1="128" x2="1080" y2="128" stroke="url(#ftRule)" stroke-width="1.4"/>
    <text x="600" y="156" text-anchor="middle" font-family="{MONO}" font-size="11" font-weight="700" letter-spacing="1.6" fill="{t["orange"]}">
      NICHOLAS MICHAEL KLOSTER  ×  ZOE   ·   MEASUREMENT ≠ EVIDENCE ≠ BELIEF UPDATE ≠ ACTION
    </text>
  </g>
  <rect x="2" y="2" width="1196" height="182" rx="16" fill="none" stroke="{t["border"]}" stroke-width="1.4"/>
</svg>
'''


def build_nav_tab(label: str, accent: str, width: int) -> str:
    # Sharp chamfered Gallagher scientific-instrument bezel tab (distinct from Zoe's rounded jewel pills!)
    w = width
    h = 32
    c = 7
    poly = f"{c},1 {w-1},1 {w-1},{h-c} {w-c},{h-1} 1,{h-1} 1,{c}"
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="{html.escape(label)}">
  <polygon points="{poly}" fill="#0E1B26" stroke="{accent}" stroke-width="1.35"/>
  <rect x="12" y="12" width="7" height="7" rx="1" fill="{accent}">
    <animate attributeName="opacity" values="0.65;1;0.65" dur="3.2s" repeatCount="indefinite"/>
  </rect>
  <text x="{(w + 14) / 2:.1f}" y="20.5" text-anchor="middle" font-family="{MONO}" font-size="11.5" font-weight="700" letter-spacing="0.6" fill="#F2EDE4">{html.escape(label)}</text>
</svg>
'''


def build_divider(accent: str, secondary: str, idx: int) -> str:
    # Precision Gallagher drafting reticle hairline
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 32" width="1200" height="32" role="presentation">
  <defs>
    <linearGradient id="dl" gradientUnits="userSpaceOnUse" x1="32" y1="16" x2="564" y2="16">
      <stop offset="0%" stop-color="{accent}" stop-opacity="0"/>
      <stop offset="65%" stop-color="{secondary}" stop-opacity="0.45"/>
      <stop offset="100%" stop-color="{accent}" stop-opacity="0.95"/>
    </linearGradient>
    <linearGradient id="dr" gradientUnits="userSpaceOnUse" x1="636" y1="16" x2="1168" y2="16">
      <stop offset="0%" stop-color="{accent}" stop-opacity="0.95"/>
      <stop offset="35%" stop-color="{secondary}" stop-opacity="0.45"/>
      <stop offset="100%" stop-color="{accent}" stop-opacity="0"/>
    </linearGradient>
  </defs>
  <line x1="32" y1="16" x2="564" y2="16" stroke="url(#dl)" stroke-width="1.5"/>
  <line x1="636" y1="16" x2="1168" y2="16" stroke="url(#dr)" stroke-width="1.5"/>
  <line x1="574" y1="10" x2="574" y2="22" stroke="{secondary}" stroke-width="1.3" opacity="0.8"/>
  <line x1="626" y1="10" x2="626" y2="22" stroke="{secondary}" stroke-width="1.3" opacity="0.8"/>
  <rect x="594" y="10" width="12" height="12" transform="rotate(45 600 16)" fill="none" stroke="{accent}" stroke-width="1.5"/>
  <rect x="597.5" y="13.5" width="5" height="5" fill="{accent}">
    <animate attributeName="opacity" values="0.5;1;0.5" dur="3.4s" begin="{idx * 0.4:.1f}s" repeatCount="indefinite"/>
  </rect>
</svg>
'''


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    outputs: dict[str, str] = {}
    for mode in ("dark", "light"):
        outputs[f"plate-hero-{mode}.svg"] = build_hero(mode)
        outputs[f"plate-atlas-{mode}.svg"] = build_atlas(mode)
        outputs[f"plate-metrics-{mode}.svg"] = build_metrics(mode)
        outputs[f"plate-pillars-{mode}.svg"] = build_pillars(mode)
        outputs[f"plate-security-{mode}.svg"] = build_security(mode)
        outputs[f"plate-footer-{mode}.svg"] = build_footer(mode)

    outputs.update({
        "nav-zoe.svg": build_nav_tab("ZOE", "#E85D1A", 86),
        "nav-sessions.svg": build_nav_tab("SESSIONS", "#FF8142", 122),
        "nav-manifold.svg": build_nav_tab("MANIFOLD", "#2DD4BF", 122),
        "nav-evidence.svg": build_nav_tab("EVIDENCE", "#C06EFF", 122),
        "nav-gallery.svg": build_nav_tab("GALLERY", "#F0CFA0", 114),
        "nav-papers.svg": build_nav_tab("PAPERS", "#2DD4BF", 108),
        "nav-repos.svg": build_nav_tab("REPOS", "#E85D1A", 98),
        "nav-security.svg": build_nav_tab("SECURITY", "#C06EFF", 122),
        "divider-orange.svg": build_divider("#E85D1A", "#2DD4BF", 1),
        "divider-teal.svg": build_divider("#2DD4BF", "#C06EFF", 2),
        "divider-violet.svg": build_divider("#C06EFF", "#E85D1A", 3),
        "divider-copper.svg": build_divider("#F0CFA0", "#2DD4BF", 4),
    })

    for name, content in outputs.items():
        p = OUT / name
        p.write_text(content, encoding="utf-8")
        print(f"[OK] {p.relative_to(ROOT)} ({len(content):,} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
