#!/usr/bin/env python3
"""
HVAC/R Superheat & Subcooling practice calculator (stdlib only).

Uses compact embedded pressure-temperature (PT) saturation tables with
linear interpolation for common HVAC/R refrigerants. This is for
learning/practice only — real field work requires a manufacturer PT chart
or gauge set rated for the refrigerant in use.

Zeotropic blends (e.g. R-404A, R-407C, R-454B) use a single mid-range
approximate curve; real charts distinguish bubble/dew points (glide).
"""

from __future__ import annotations

import argparse
import sys
from typing import Dict, List, Tuple

# ---------------------------------------------------------------------------
# Compact saturation tables: (psig, Tsat °F)
# Approximate values for educational use. Documented as approximate.
# Real jobs need a PT chart / digital manifold for the exact refrigerant blend.
# ---------------------------------------------------------------------------

# R-410A (approx. bubble/dew mid-range; educational compact table)
R410A_TABLE: List[Tuple[float, float]] = [
    (50, -20),
    (70, -5),
    (80, 2),
    (90, 8),
    (100, 14),
    (110, 19),
    (118, 23),
    (125, 26),
    (130, 28),
    (140, 33),
    (150, 37),
    (160, 41),
    (170, 45),
    (180, 48),
    (190, 52),
    (200, 55),
    (210, 58),
    (220, 61),
    (230, 64),
    (240, 67),
    (250, 70),
    (260, 72),
    (270, 75),
    (280, 77),
    (290, 80),
    (300, 82),
    (320, 87),
    (340, 91),
    (360, 95),
    (380, 99),
    (400, 103),
    (420, 106),
    (440, 110),
    (460, 113),
    (480, 116),
    (500, 119),
]

# R-22 (approx.; educational compact table)
R22_TABLE: List[Tuple[float, float]] = [
    (20, -20),
    (30, -5),
    (35, 2),
    (40, 8),
    (45, 13),
    (49, 16),
    (55, 22),
    (60, 26),
    (65, 30),
    (70, 33),
    (75, 37),
    (80, 40),
    (85, 43),
    (90, 46),
    (95, 49),
    (100, 52),
    (105, 54),
    (110, 57),
    (120, 62),
    (130, 66),
    (140, 70),
    (150, 74),
    (160, 78),
    (170, 81),
    (180, 84),
    (190, 87),
    (200, 90),
    (210, 93),
    (220, 96),
    (230, 98),
    (240, 101),
    (250, 104),
    (260, 106),
    (270, 109),
    (280, 111),
    (300, 116),
]

# R-134a (approx.; educational compact table)
R134A_TABLE: List[Tuple[float, float]] = [
    (0, -15),
    (5, -5),
    (10, 5),
    (15, 12),
    (20, 19),
    (25, 26),
    (30, 32),
    (35, 37),
    (40, 42),
    (45, 47),
    (50, 52),
    (55, 56),
    (60, 60),
    (65, 64),
    (70, 68),
    (75, 72),
    (80, 75),
    (85, 79),
    (90, 82),
    (95, 85),
    (100, 88),
    (110, 94),
    (120, 100),
    (130, 105),
    (140, 110),
    (150, 115),
    (160, 119),
    (170, 124),
    (180, 128),
    (190, 132),
    (200, 136),
    (220, 143),
    (240, 150),
    (250, 153),
]

# R-404A (approx. mid-glide; educational compact table)
R404A_TABLE: List[Tuple[float, float]] = [
    (20, -28),
    (30, -16),
    (40, -7),
    (50, 1),
    (60, 8),
    (70, 14),
    (80, 20),
    (90, 25),
    (100, 30),
    (110, 35),
    (120, 39),
    (130, 43),
    (140, 47),
    (150, 51),
    (160, 54),
    (170, 58),
    (180, 61),
    (190, 64),
    (200, 67),
    (220, 73),
    (240, 78),
    (250, 81),
    (260, 83),
    (280, 88),
    (300, 93),
    (320, 97),
    (340, 102),
    (360, 106),
    (380, 110),
    (400, 114),
    (420, 118),
    (440, 121),
]

# R-407C (approx. mid-glide; educational compact table)
R407C_TABLE: List[Tuple[float, float]] = [
    (30, -10),
    (40, 0),
    (50, 9),
    (60, 17),
    (70, 24),
    (80, 30),
    (90, 36),
    (100, 41),
    (110, 46),
    (120, 50),
    (130, 55),
    (140, 59),
    (150, 63),
    (160, 66),
    (170, 70),
    (180, 73),
    (190, 76),
    (200, 79),
    (220, 85),
    (240, 91),
    (250, 93),
    (260, 96),
    (280, 101),
    (300, 105),
    (320, 110),
    (340, 114),
    (360, 118),
    (380, 122),
    (400, 126),
    (420, 129),
]

# R-32 (approx.; educational compact table)
R32_TABLE: List[Tuple[float, float]] = [
    (50, -16),
    (70, -1),
    (80, 5),
    (90, 11),
    (100, 16),
    (110, 21),
    (120, 26),
    (130, 30),
    (140, 34),
    (150, 38),
    (160, 42),
    (170, 45),
    (180, 49),
    (190, 52),
    (200, 55),
    (210, 58),
    (220, 61),
    (230, 64),
    (240, 67),
    (250, 69),
    (260, 72),
    (280, 77),
    (300, 81),
    (320, 86),
    (340, 90),
    (360, 94),
    (380, 98),
    (400, 101),
    (420, 105),
    (440, 108),
    (460, 112),
    (480, 115),
    (500, 118),
]

# R-454B (approx. mid-glide; educational compact table — R-410A-class A2L)
R454B_TABLE: List[Tuple[float, float]] = [
    (50, -18),
    (70, -3),
    (80, 4),
    (90, 10),
    (100, 16),
    (110, 21),
    (120, 26),
    (130, 30),
    (140, 34),
    (150, 38),
    (160, 42),
    (170, 46),
    (180, 49),
    (190, 53),
    (200, 56),
    (210, 59),
    (220, 62),
    (230, 65),
    (240, 68),
    (250, 70),
    (260, 73),
    (280, 78),
    (300, 82),
    (320, 87),
    (340, 91),
    (360, 95),
    (380, 99),
    (400, 103),
    (420, 106),
    (440, 110),
    (460, 113),
    (480, 116),
    (500, 119),
]

TABLES: Dict[str, List[Tuple[float, float]]] = {
    "R-410A": R410A_TABLE,
    "R-22": R22_TABLE,
    "R-134a": R134A_TABLE,
    "R-404A": R404A_TABLE,
    "R-407C": R407C_TABLE,
    "R-32": R32_TABLE,
    "R-454B": R454B_TABLE,
}

SUPPORTED = ", ".join(TABLES.keys())

ALIASES = {
    "R410A": "R-410A",
    "R-410A": "R-410A",
    "410A": "R-410A",
    "R22": "R-22",
    "R-22": "R-22",
    "22": "R-22",
    "R134A": "R-134a",
    "R-134A": "R-134a",
    "R-134a": "R-134a",
    "134A": "R-134a",
    "R404A": "R-404A",
    "R-404A": "R-404A",
    "404A": "R-404A",
    "R407C": "R-407C",
    "R-407C": "R-407C",
    "407C": "R-407C",
    "R32": "R-32",
    "R-32": "R-32",
    "32": "R-32",
    "R454B": "R-454B",
    "R-454B": "R-454B",
    "454B": "R-454B",
}


def sat_temp_f(refrigerant: str, pressure_psig: float) -> float:
    """Linearly interpolate saturation temperature (°F) from the compact table."""
    table = TABLES[refrigerant]
    if pressure_psig < table[0][0] or pressure_psig > table[-1][0]:
        lo, hi = table[0][0], table[-1][0]
        raise ValueError(
            f"Pressure {pressure_psig} psig outside table range "
            f"({lo:.0f}–{hi:.0f} psig) for {refrigerant}."
        )

    for i in range(len(table) - 1):
        p0, t0 = table[i]
        p1, t1 = table[i + 1]
        if p0 <= pressure_psig <= p1:
            if p1 == p0:
                return t0
            frac = (pressure_psig - p0) / (p1 - p0)
            return t0 + frac * (t1 - t0)

    return table[-1][1]


def superheat_f(suction_psig: float, suction_temp_f: float, refrigerant: str) -> float:
    """Superheat = actual suction line temp − sat temp at suction pressure."""
    tsat = sat_temp_f(refrigerant, suction_psig)
    return suction_temp_f - tsat


def subcooling_f(liquid_psig: float, liquid_temp_f: float, refrigerant: str) -> float:
    """Subcooling = sat temp at liquid pressure − actual liquid line temp."""
    tsat = sat_temp_f(refrigerant, liquid_psig)
    return tsat - liquid_temp_f


def guidance_superheat(sh: float) -> str:
    """Approximate, rule-of-thumb guidance — clearly labeled."""
    if sh < 5:
        note = "Very low — risk of liquid floodback (approx. rule of thumb)."
    elif sh <= 20:
        note = "Often in a common target band for many fixed-orifice systems (approx.)."
    elif sh <= 30:
        note = "Somewhat high — may indicate undercharge or airflow issue (approx.)."
    else:
        note = "High — check charge, metering device, and airflow (approx.)."
    return f"[APPROXIMATE guidance] Superheat {sh:.1f}°F: {note}"


def guidance_subcooling(sc: float) -> str:
    """Approximate, rule-of-thumb guidance — clearly labeled."""
    if sc < 5:
        note = "Low — possible undercharge or restriction (approx. rule of thumb)."
    elif sc <= 15:
        note = "Often in a common target band for many TXV systems (approx.)."
    elif sc <= 20:
        note = "Somewhat high — may indicate overcharge (approx.)."
    else:
        note = "High — check for overcharge or non-condensables (approx.)."
    return f"[APPROXIMATE guidance] Subcooling {sc:.1f}°F: {note}"


def normalize_refrigerant(name: str) -> str:
    key = name.strip().upper().replace(" ", "").replace("_", "-")
    if key not in ALIASES:
        raise ValueError(
            f"Unsupported refrigerant '{name}'. Use one of: {SUPPORTED}."
        )
    return ALIASES[key]


def prompt_float(label: str) -> float:
    while True:
        raw = input(f"{label}: ").strip()
        try:
            return float(raw)
        except ValueError:
            print("Please enter a number.")


def interactive() -> None:
    print("HVAC/R Superheat & Subcooling practice calculator")
    print("(Embedded approx. PT tables — real jobs need a PT chart.)")
    print(f"Supported: {SUPPORTED}\n")

    mode = input("Mode (superheat|subcooling|both) [both]: ").strip().lower() or "both"
    if mode not in ("superheat", "subcooling", "both"):
        print("Invalid mode.", file=sys.stderr)
        sys.exit(1)

    ref_raw = input(f"Refrigerant [{list(TABLES.keys())[0]}]: ").strip() or "R-410A"
    refrigerant = normalize_refrigerant(ref_raw)

    suction_psig = suction_temp = liquid_psig = liquid_temp = None
    if mode in ("superheat", "both"):
        suction_psig = prompt_float("Suction pressure (psig)")
        suction_temp = prompt_float("Suction line temperature (°F)")
    if mode in ("subcooling", "both"):
        liquid_psig = prompt_float("Liquid pressure (psig)")
        liquid_temp = prompt_float("Liquid line temperature (°F)")

    print_results(mode, refrigerant, suction_psig, suction_temp, liquid_psig, liquid_temp)


def print_results(
    mode: str,
    refrigerant: str,
    suction_psig: float | None,
    suction_temp: float | None,
    liquid_psig: float | None,
    liquid_temp: float | None,
) -> None:
    print()
    print(f"Refrigerant: {refrigerant}")
    print("Note: Saturation temps from compact educational PT table (interpolated).")
    print("      Zeotropic blends use an approximate mid-glide curve (not bubble/dew).")
    print("      Real jobs need a manufacturer PT chart / rated manifold.\n")

    if mode in ("superheat", "both"):
        assert suction_psig is not None and suction_temp is not None
        tsat = sat_temp_f(refrigerant, suction_psig)
        sh = superheat_f(suction_psig, suction_temp, refrigerant)
        print("--- Superheat ---")
        print(f"  Suction pressure:     {suction_psig:.1f} psig")
        print(f"  Saturation temp:      {tsat:.1f} °F  (from table)")
        print(f"  Suction line temp:    {suction_temp:.1f} °F")
        print(f"  Superheat:            {sh:.1f} °F")
        print(f"  {guidance_superheat(sh)}")
        print()

    if mode in ("subcooling", "both"):
        assert liquid_psig is not None and liquid_temp is not None
        tsat = sat_temp_f(refrigerant, liquid_psig)
        sc = subcooling_f(liquid_psig, liquid_temp, refrigerant)
        print("--- Subcooling ---")
        print(f"  Liquid pressure:      {liquid_psig:.1f} psig")
        print(f"  Saturation temp:      {tsat:.1f} °F  (from table)")
        print(f"  Liquid line temp:     {liquid_temp:.1f} °F")
        print(f"  Subcooling:           {sc:.1f} °F")
        print(f"  {guidance_subcooling(sc)}")
        print()


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description=(
            "Practice CLI for HVAC/R superheat and subcooling using "
            f"compact educational PT tables ({SUPPORTED})."
        )
    )
    p.add_argument(
        "--mode",
        choices=["superheat", "subcooling", "both"],
        default="both",
        help="What to calculate (default: both)",
    )
    p.add_argument(
        "--refrigerant",
        "-r",
        default="R-410A",
        help=f"One of: {SUPPORTED} (default: R-410A)",
    )
    p.add_argument("--suction-psig", type=float, help="Suction / low-side pressure (psig)")
    p.add_argument("--suction-temp", type=float, help="Suction line temperature (°F)")
    p.add_argument("--liquid-psig", type=float, help="Liquid / high-side pressure (psig)")
    p.add_argument("--liquid-temp", type=float, help="Liquid line temperature (°F)")
    p.add_argument(
        "--interactive",
        "-i",
        action="store_true",
        help="Prompt for inputs instead of using flags",
    )
    return p


def main(argv: List[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.interactive or (
        args.suction_psig is None
        and args.suction_temp is None
        and args.liquid_psig is None
        and args.liquid_temp is None
        and len(sys.argv) == 1
    ):
        if args.interactive or len(sys.argv) == 1:
            interactive()
            return 0

    try:
        refrigerant = normalize_refrigerant(args.refrigerant)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    mode = args.mode
    suction_psig = args.suction_psig
    suction_temp = args.suction_temp
    liquid_psig = args.liquid_psig
    liquid_temp = args.liquid_temp

    if mode in ("superheat", "both"):
        if suction_psig is None or suction_temp is None:
            print(
                "Error: --suction-psig and --suction-temp required for superheat.",
                file=sys.stderr,
            )
            return 1
    if mode in ("subcooling", "both"):
        if liquid_psig is None or liquid_temp is None:
            print(
                "Error: --liquid-psig and --liquid-temp required for subcooling.",
                file=sys.stderr,
            )
            return 1

    try:
        print_results(mode, refrigerant, suction_psig, suction_temp, liquid_psig, liquid_temp)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
