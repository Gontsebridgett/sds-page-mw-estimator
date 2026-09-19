# SDS-PAGE — Protein Separation & Molecular Weight Estimator

A protocol write-up for SDS-PAGE (Sodium Dodecyl Sulfate–Polyacrylamide Gel
Electrophoresis), paired with a Python script that estimates the molecular weight
of unknown protein bands from their migration distance, using a standard curve
built from the protein ladder.

## Overview

SDS-PAGE separates proteins by molecular size. SDS denatures proteins and coats
them with a uniform negative charge proportional to mass, masking native charge.
Under an electric field, the polyacrylamide gel acts as a molecular sieve —
smaller proteins migrate further than larger ones. Comparing an unknown protein's
migration distance to a ladder of known molecular weights allows its size to be
estimated.

## Principle

- **Stacking gel** (low %) concentrates samples into a sharp starting band
- **Resolving gel** (higher %) performs the actual size-based separation
- Migration distance (or relative mobility, **Rf**) is linearly related to
  **log₁₀(molecular weight)** for the ladder standards — this relationship is
  used to build a standard curve for estimating unknown protein sizes

## Materials & Reagents

- Protein sample(s) + pre-stained molecular weight marker
- 30% acrylamide/bis-acrylamide, resolving & stacking buffers
- 10% SDS, 10% APS, TEMED
- Laemmli sample buffer (with reducing agent)
- Tris-glycine-SDS running buffer
- Coomassie Brilliant Blue stain / destain solution
- Vertical electrophoresis apparatus + power supply

## Method (Summary)

| Step | Action |
|---|---|
| 1 | Cast resolving gel, then stacking gel with comb |
| 2 | Denature samples in Laemmli buffer, 95–100°C, 5 min |
| 3 | Load samples + ladder into wells |
| 4 | Run at ~80V (stacking) → ~120–150V (resolving) |
| 5 | Stain with Coomassie Blue, 30–60 min |
| 6 | Destain until bands are clear |
| 7 | Image gel and measure migration distances |

## Result Interpretation

| Observation | Interpretation |
|---|---|
| Single sharp band | High sample purity |
| Multiple bands | Protein mixture or degradation |
| Smearing | Degradation, overloading, or incomplete denaturation |
| No bands | Insufficient protein, staining failure, or loading error |

## Analysis Script

`mw_estimator.py` takes migration distances measured from a gel image (ruler or
image-analysis measurement, in mm) for the ladder bands and an unknown sample,
fits a standard curve (`log10(MW)` vs. migration distance), and estimates the
molecular weight of the unknown band(s).

### Usage

```bash
pip install -r requirements.txt
python mw_estimator.py
```

### Sample output

```
Standard curve fit: log10(MW) = -0.0152 * distance + 2.392   (R² = 0.994)

Unknown_1: migration 38.5 mm  ->  Estimated MW: ~64.2 kDa
Unknown_2: migration 52.1 mm  ->  Estimated MW: ~39.9 kDa
```

## Repository Structure

```
sds-page-mw-estimator/
├── README.md
├── mw_estimator.py
├── requirements.txt
└── sample_data/
    └── migration_distances.csv
```

## Notes

Real molecular weight estimation from gel images typically uses image-analysis
software (e.g. ImageJ/Fiji) to measure migration distance precisely from a
scanned or photographed gel. This script demonstrates the underlying
calculation once those distances have been measured.
