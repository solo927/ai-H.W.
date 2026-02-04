"""
Day 11 Activity: Outlier Strategies
Tasks:
1) Load numeric data with outliers
2) Implement percentile capping (winsorization)
3) Implement removal strategy
4) Compare summary stats before/after
"""

import os
import pandas as pd
import numpy as np

# Load data (prefer local CSVs if present)
p1 = os.path.join(os.path.dirname(__file__), "data", "day11_income.csv")
p2 = os.path.join(os.path.dirname(__file__), "day11_income.csv")
if os.path.exists(p1):
    df = pd.read_csv(p1)
elif os.path.exists(p2):
    df = pd.read_csv(p2)
else:
    rng = np.random.default_rng(0)
    incomes = np.concatenate([rng.normal(50000, 10000, size=200), [500000, 600000]])
    df = pd.DataFrame({"income": incomes})

def winsorize_series(s, lower_q, upper_q):
    lower = s.quantile(lower_q)
    upper = s.quantile(upper_q)
    return s.clip(lower=lower, upper=upper)

def remove_upper_tail(s, upper_q):
    upper = s.quantile(upper_q)
    return s[s <= upper]

def compare_stats(orig, winsor, removed):
    print("--- Summary statistics ---")
    print("Original:\n", orig.describe())
    print("\nWinsorized:\n", winsor.describe())
    print("\nRemoved upper tail:\n", removed.describe())

if __name__ == "__main__":
    s = df["income"]
    wins = winsorize_series(s, 0.05, 0.95)
    removed = remove_upper_tail(s, 0.95)
    compare_stats(s, wins, removed)
    print("\nWinsorized top values:\n", wins.sort_values(ascending=False).head())
    print("\nRemoved tail max:", removed.max())
