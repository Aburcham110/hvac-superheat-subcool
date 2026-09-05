# HVAC/R Superheat & Subcooling Practice CLI

Small Python (stdlib-only) practice tool to calculate **superheat** and/or **subcooling** for **R-410A** or **R-22**.

Saturation temperatures come from a **compact embedded PT table** with linear interpolation. This is for learning only — **real field work needs a manufacturer PT chart or a refrigerant-rated digital manifold**.

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

## Notes

- Guidance lines are labeled **`[APPROXIMATE guidance]`** — they are rough rules of thumb, not manufacturer specs.
- Table coverage is limited; pressures outside the embedded range will error with a clear message.
- Prefer stdlib only — no `requirements.txt` needed.
