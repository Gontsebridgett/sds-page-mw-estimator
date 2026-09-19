"""
mw_estimator.py

Estimates the molecular weight of unknown protein bands on an SDS-PAGE gel
by fitting a standard curve (log10(MW) vs. migration distance) from ladder
bands of known molecular weight, then applying it to unknown bands.
"""

import csv
import math
from pathlib import Path

DATA_PATH = Path(__file__).parent / "sample_data" / "migration_distances.csv"


def load_data(path: Path):
    ladder, unknowns = [], []
    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["type"] == "ladder":
                ladder.append((float(row["migration_mm"]), float(row["known_mw_kda"])))
            else:
                unknowns.append((row["band_id"], float(row["migration_mm"])))
    return ladder, unknowns


def linear_regression(x_vals, y_vals):
    """Simple least-squares fit: y = m*x + b. Returns (m, b, r_squared)."""
    n = len(x_vals)
    mean_x = sum(x_vals) / n
    mean_y = sum(y_vals) / n

    ss_xy = sum((x - mean_x) * (y - mean_y) for x, y in zip(x_vals, y_vals))
    ss_xx = sum((x - mean_x) ** 2 for x in x_vals)
    m = ss_xy / ss_xx
    b = mean_y - m * mean_x

    ss_tot = sum((y - mean_y) ** 2 for y in y_vals)
    ss_res = sum((y - (m * x + b)) ** 2 for x, y in zip(x_vals, y_vals))
    r_squared = 1 - (ss_res / ss_tot) if ss_tot else 1.0

    return m, b, r_squared


def main():
    ladder, unknowns = load_data(DATA_PATH)

    distances = [d for d, _ in ladder]
    log_mw = [math.log10(mw) for _, mw in ladder]

    m, b, r_squared = linear_regression(distances, log_mw)
    print(f"Standard curve fit: log10(MW) = {m:.4f} * distance + {b:.3f}   (R\u00b2 = {r_squared:.3f})\n")

    for band_id, distance in unknowns:
        estimated_mw = 10 ** (m * distance + b)
        print(f"{band_id}: migration {distance} mm  ->  Estimated MW: ~{estimated_mw:.1f} kDa")


if __name__ == "__main__":
    main()
