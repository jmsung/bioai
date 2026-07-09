"""Process ST001906 metabolomics data into a curated diabetes metabolomics dataset.

Downloads plasma metabolomics data from Metabolomics Workbench (study ST001906),
normalizes intensities, and computes pathway-level metabolite scores.

Source: Metabolomics Workbench ST001906 (GC-MS/MS, 61 fasting plasma samples)
- 30 control, 31 diabetes (Type 2)
- 78 named metabolites (amino acids, lipids, carbohydrates, organic acids)

Metabolite pathway panels based on diabetes metabolomics literature:
1. Amino acid metabolism (branched-chain + aromatic)
2. Carbohydrate / glucose metabolism
3. Lipid / fatty acid metabolism
4. TCA cycle / energy metabolism
5. Ketone body metabolism
"""

from __future__ import annotations

import urllib.request
from pathlib import Path

import numpy as np
import pandas as pd

DATA_DIR = Path(__file__).parent.parent / "data" / "metabolomics"
RAW_DIR = DATA_DIR / "raw"
RAW_PATH = RAW_DIR / "ST001906_raw.txt"
OUTPUT_PATH = RAW_DIR / "diabetes_metabolomics.csv"

API_URL = "https://www.metabolomicsworkbench.org/rest/study/analysis_id/AN003103/datatable"

# ---------------------------------------------------------------------------
# Diabetes-relevant metabolite pathway panels
# ---------------------------------------------------------------------------
PATHWAY_METABOLITES: dict[str, list[str]] = {
    "amino_acid": [
        "Alanine", "Glycine", "Leucine", "Isoleucine", "Valine",
        "Phenylalanine", "Tyrosine", "Tryptophan", "Lysine", "Histidine",
        "Methionine", "Proline", "Serine", "Threonine", "Glutamine",
        "Glutamate", "Asparagine", "Aspartate", "Arginine", "Ornithine",
        "Cysteine", "Cystine", "Hydroxyproline",
    ],
    "carbohydrate": [
        "Glucose", "Fructose", "Galactose", "Mannose", "Allose",
        "Arabinose", "Xylulose", "Gluconate", "Glucuronate",
        "1,5-Anhydroglucitol", "Inositol", "Mannitol", "Erythritol",
        "N-Acetylglucosamine",
    ],
    "lipid": [
        "Cholesterol", "Oleate", "Palmitate", "Stearate", "Linoleate",
        "Palmitoleate", "Myristate", "Laureate", "Heptadecanoate",
        "Pentadecanoate", "Elaidiate", "alpha-Tocopherol",
    ],
    "tca_energy": [
        "Citrate", "Succinate", "Malate", "Pyruvate", "Lactate",
        "Glycerate", "Glycolate", "Phosphate", "Gluconate",
    ],
    "ketone_oxidative": [
        "3-Hydroxybutyrate", "2-Hydroxybutyrate", "2-Aminobutyrate",
        "3-Aminoisobutyrate", "Ketoisoleucine", "Ketovaline",
        "Urate", "Creatinine",
    ],
}


def download_raw_data() -> None:
    """Download ST001906 data table from Metabolomics Workbench REST API."""
    if RAW_PATH.exists():
        print(f"Raw data already exists at {RAW_PATH}")
        return

    RAW_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Downloading ST001906 from {API_URL}...")
    urllib.request.urlretrieve(API_URL, RAW_PATH)
    print(f"Saved to {RAW_PATH}")


def load_raw_data() -> pd.DataFrame:
    """Load the raw tab-separated data table."""
    df = pd.read_csv(RAW_PATH, sep="\t")
    # Clean class labels: "Diagnosis:Control" -> "control", "Diagnosis:Diabetes" -> "diabetes"
    df["Class"] = df["Class"].str.replace("Diagnosis:", "").str.lower()
    df = df.rename(columns={"Samples": "sample_id", "Class": "condition"})
    return df


def build_curated_dataset() -> None:
    """Build the final curated metabolomics CSV."""
    download_raw_data()

    print("Step 1: Loading raw data...")
    df = load_raw_data()
    metabolite_cols = [c for c in df.columns if c not in ("sample_id", "condition")]
    print(f"  {len(df)} samples × {len(metabolite_cols)} metabolites")
    print(f"  Groups: {dict(df['condition'].value_counts())}")

    print("\nStep 2: Adding numeric labels...")
    df.insert(1, "condition_numeric", df["condition"].map({"control": 0, "diabetes": 1}))

    print("\nStep 3: Computing pathway scores (mean z-score)...")
    # Z-score each metabolite across all samples
    zscore_df = df[metabolite_cols].apply(lambda x: (x - x.mean()) / x.std())

    pathway_cols = []
    for pathway, metabolites in PATHWAY_METABOLITES.items():
        matched = [m for m in metabolites if m in zscore_df.columns]
        if matched:
            col_name = f"pathway_{pathway}"
            df[col_name] = zscore_df[matched].mean(axis=1)
            pathway_cols.append(col_name)
            print(f"  {pathway}: {len(matched)}/{len(metabolites)} metabolites matched")

    print(f"\nStep 4: Saving to {OUTPUT_PATH}...")
    # Reorder: metadata, pathway scores, metabolites
    meta_cols = ["sample_id", "condition", "condition_numeric"]
    metabolite_cols_sorted = sorted(metabolite_cols)
    df = df[meta_cols + sorted(pathway_cols) + metabolite_cols_sorted]

    df.to_csv(OUTPUT_PATH, index=False)
    print(f"Shape: {df.shape} (samples × features)")

    print("\nPathway score summary (mean by group):")
    print(df.groupby("condition")[pathway_cols].mean().round(3).to_string())

    # Quick sanity check: glucose should be higher in diabetes
    if "Glucose" in df.columns:
        ctrl_glucose = df[df["condition"] == "control"]["Glucose"].mean()
        diab_glucose = df[df["condition"] == "diabetes"]["Glucose"].mean()
        ratio = diab_glucose / ctrl_glucose
        print(f"\nGlucose sanity check: diabetes/control ratio = {ratio:.2f}")


if __name__ == "__main__":
    build_curated_dataset()
