# HVAC/R Superheat & Subcooling Practice CLI

Small Python (stdlib-only) practice tool to calculate **superheat** and/or **subcooling** for common HVAC/R refrigerants:

**R-410A · R-22 · R-134a · R-404A · R-407C · R-32 · R-454B**

Saturation temperatures come from a **compact embedded PT table** with linear interpolation. This is for learning only — **real field work needs a manufacturer PT chart or a refrigerant-rated digital manifold**.

Zeotropic blends (**R-404A**, **R-407C**, **R-454B**) use an **approximate mid-glide** curve (not separate bubble/dew points). Treat all guidance as practice-only.

## Formulas

- **Superheat (°F)** = suction line temp − saturation temp at suction pressure  
- **Subcooling (°F)** = saturation temp at liquid pressure − liquid line temp  

## Requirements

- Python 3.9+ (uses only the standard library)

## How to run

```bash
cd hvac-superheat-subcool
python3 hvac_calc.py --help
```

### Example (both superheat and subcooling, R-410A)

```bash
python3 hvac_calc.py \
  --mode both \
  --refrigerant R-410A \
  --suction-psig 118 \
  --suction-temp 55 \
  --liquid-psig 400 \
  --liquid-temp 95
```

### Interactive mode

```bash
python3 hvac_calc.py -i
# or just: python3 hvac_calc.py
```

### Superheat only (R-22)

```bash
python3 hvac_calc.py \
  --mode superheat \
  -r R-22 \
  --suction-psig 70 \
  --suction-temp 50
```

### Other refrigerants

```bash
python3 hvac_calc.py --mode superheat -r R-134a --suction-psig 35 --suction-temp 50
python3 hvac_calc.py --mode both -r R-404A --suction-psig 70 --suction-temp 30 --liquid-psig 250 --liquid-temp 90
python3 hvac_calc.py --mode superheat -r R-407C --suction-psig 70 --suction-temp 45
python3 hvac_calc.py --mode both -r R-32 --suction-psig 120 --suction-temp 55 --liquid-psig 400 --liquid-temp 95
python3 hvac_calc.py --mode both -r R-454B --suction-psig 118 --suction-temp 55 --liquid-psig 400 --liquid-temp 95
```

## Notes

- Guidance lines are labeled **`[APPROXIMATE guidance]`** — they are rough rules of thumb, not manufacturer specs, and do not replace OEM charge charts.
- Table coverage is limited; pressures outside the embedded range will error with a clear message.
- Prefer stdlib only — no `requirements.txt` needed.
