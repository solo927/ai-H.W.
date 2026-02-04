"""
Day 12 Activity: String & Date Cleaning
Tasks:
1) Clean city strings (strip, lower, remove punctuation)
2) Map synonyms to canonical values
3) Parse mixed-format timestamps and localize to UTC
"""

import pandas as pd

# Load data (falls back to a demo dataset if missing)
try:
    df = pd.read_csv("data/day12_users.csv")
except FileNotFoundError:
    df = pd.DataFrame({
        "city": [" New York ", "NYC", "Los Angeles", "los angeles ", "San Fran", "S.F.", "Chicago"],
        "timestamp": [
            "2026-02-02 13:00",
            "02/02/2026 1:00 PM",
            "2026-02-02T13:00:00-05:00",
            "Feb 2, 2026 13:00 GMT+1",
            "2026/02/02 13:00",
            "2026-02-02 13:00:00Z",
            None,
        ],
    })

import re

def standardize_city(df, col="city", mapping=None):
    if mapping is None:
        mapping = {
            "nyc": "new york",
            "new york city": "new york",
            "new york": "new york",
            "la": "los angeles",
            "losangeles": "los angeles",
            "los angeles": "los angeles",
            "san fran": "san francisco",
            "sf": "san francisco",
            "s f": "san francisco",
            "s.f.": "san francisco",
        }
    s = df[col].astype(str).str.strip().str.lower().str.replace(r"[^\w\s]", "", regex=True)
    s = s.replace(mapping)
    df[col + "_std"] = s
    return df


def parse_and_localize(df, col="timestamp", default_tz="UTC"):
    parsed = pd.to_datetime(df[col], infer_datetime_format=True, errors="coerce")
    def to_utc(ts):
        if pd.isna(ts):
            return pd.NaT
        try:
            if getattr(ts, "tzinfo", None) is None:
                return ts.tz_localize(default_tz).tz_convert("UTC")
            else:
                return ts.tz_convert("UTC")
        except Exception:
            return pd.NaT
    parsed_utc = parsed.apply(to_utc)
    df[col + "_utc"] = parsed_utc
    return df

if __name__ == "__main__":
    print("Original:\n", df)
    df = standardize_city(df)
    df = parse_and_localize(df)
    print("\nCleaned columns:\n", df[["city", "city_std", "timestamp", "timestamp_utc"]])
