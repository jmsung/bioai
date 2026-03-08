# Metabolomics Dataset — ST001906

Fasting plasma metabolomics for Type 2 diabetes classification.

## Source

- **Study**: ST001906 (Metabolomics Workbench)
- **Platform**: GC-MS/MS (Shimadzu TQ8040)
- **Sample type**: Fasting blood plasma
- **Subjects**: 61 (30 control, 31 T2D)

## Files

| File | Description |
|------|-------------|
| `raw/ST001906_raw.txt` | Raw tab-separated data from REST API |
| `raw/diabetes_metabolomics.csv` | Processed CSV with pathway scores |

## Schema (diabetes_metabolomics.csv)

- `sample_id` — Sample identifier (C01–C30 control, P01B–P33B diabetes)
- `condition` — "control" or "diabetes"
- `condition_numeric` — 0 (control) or 1 (diabetes)
- `pathway_amino_acid` — Mean z-score of 23 amino acid metabolites
- `pathway_carbohydrate` — Mean z-score of 14 carbohydrate metabolites
- `pathway_lipid` — Mean z-score of 12 lipid/fatty acid metabolites
- `pathway_tca_energy` — Mean z-score of 9 TCA cycle / energy metabolites
- `pathway_ketone_oxidative` — Mean z-score of 8 ketone body / oxidative metabolites
- 78 individual metabolite intensity columns

## Metabolite Pathways

| Pathway | Count | Key Metabolites |
|---------|-------|-----------------|
| Amino acid | 23 | BCAA (Leu/Ile/Val), aromatic (Phe/Tyr/Trp), Glu, Gly |
| Carbohydrate | 14 | Glucose, Fructose, Mannose, 1,5-Anhydroglucitol, Inositol |
| Lipid | 12 | Cholesterol, Oleate, Palmitate, Stearate, Linoleate |
| TCA/Energy | 9 | Citrate, Pyruvate, Lactate, Succinate, Malate |
| Ketone/Oxidative | 8 | 3-Hydroxybutyrate, 2-Hydroxybutyrate, Urate, Creatinine |

## Processing

```bash
uv run python scripts/process_metabolomics.py
```
