<!-- synced from knowledge-base — do not edit here; change upstream and re-pull -->
---
type: source
kind: paper
confidentiality: public
visibility: global
primary: bio-multiomics
domains: [bio-multiomics]
title: "Tabular Foundation Models Are Competitive Cellular Perturbation Predictors Across Biological Scales"
authors: [Giovanni Palla, Alexander Hillsley, Yang-Joon Kim, Loic A. Royer]
year: 2026
doi: 10.64898/2026.06.28.735106
source_url: https://www.biorxiv.org/content/10.64898/2026.06.28.735106v2
drive_file_id: TODO
text_source: paperclip
ingested_by: agent
---

# Tabular Foundation Models Are Competitive Cellular Perturbation Predictors Across Biological Scales

**Authors:** Giovanni Palla (now Lila Sciences), Alexander Hillsley, Yang-Joon Kim, Loic A. Royer (Chan Zuckerberg Biohub, San Francisco)
**Year:** 2026 (bioRxiv preprint, v2, posted 2026-06-28)
**Venue:** bioRxiv · DOI 10.64898/2026.06.28.735106

## Abstract

General-purpose **Tabular Foundation Models (TFMs)** — TabPFN and TabICL, Prior-Fitted Networks pretrained only on synthetic data — are benchmarked against domain-specific single-cell architectures (PRESAGE, scGPT, scLAMBDA, STACK, Prophet) for predicting cellular responses to genetic/chemical perturbations. Across four settings spanning three biological scales, TFMs match or outperform every specialized baseline despite having **no biology-specific pretraining**, arguing that strong posterior-predictive regression and good featurization matter more than hand-crafted biological inductive biases.

## Key contributions

- Frames perturbation prediction as a unified tabular regression problem (estimating conditional mean response µ(c,p)), making general PFNs natural candidates.
- Shows synthetic-data-pretrained TFMs are competitive-to-superior vs. bespoke single-cell foundation models across cell / pseudobulk / embryo scales.
- Simple recipe: PCA-decompose the output space → zero-shot tabular regression, one principal component at a time, on a frozen TabPFN/TabICL backbone.
- Code: github.com/royerlab/tfm-perturbation.

## Methods

Four evaluation settings: (1) **cell-level** cross-cell-type prediction (OpenProblems 2k-HVG, with an optimal-transport cell-matching adaptation step); (2) **pseudobulk** perturbation prediction on five Perturb-seq cell-line datasets (PRESAGE protocol, 5-fold CV); (3) genome-wide **CRISPR screen** in primary human CD4+ T cells (within-donor, 2 donors × 5 folds); (4) **embryo-level** cell-type composition forecasting in the zscape zebrafish developmental atlas (~2.7M cells, 28 perturbations, 5 timepoints, strict timepoint holdout). Ranked by mean-rank Borda aggregation across metrics/datasets/folds; CatBoost included as a strong tabular baseline; Bootstrap serves as an oracle upper bound.

## Key results

- **A PFN backbone ranks #1 on every task** (TabICL on cell-level & pseudobulk; TabPFN on zebrafish).
- Cell-level: TabICL(OT) leads Pearson-δ (0.570) and perturbation discrimination (0.795); TFMs beat STACK despite not training on the data. OT matching > kNN (+0.07–0.11 Pearson-δ).
- Pseudobulk: TabICL/TabPFN consistently best across 5 datasets; scGPT near the Mean baseline, scLAMBDA intermediate.
- CD4+ T-cell genome-wide: **TabPFN the only model positively correlated with truth** (cosine +0.108 top-20 DE); all others ≈ Mean baseline. Absolute metrics modest — genome-wide primary-cell knockouts give near-null pseudobulk signal (93% of logFC within ±0.1).
- Zebrafish: TabPFN best (Spearman 0.808, R²=0.704), CatBoost close (0.662), Prophet R²=0.651.
- Ablations: what matters is the **in-context inference step**, not a reusable per-perturbation encoding; output basis must cover high-variance target directions (NMF beats PCA by +0.117; bottom-PCs collapse). Diversity-aware support selection (farthest-point sampling) recovers near-full-context signal from ~25% of training perturbations.

## Limitations / open questions

- In-vivo / primary-cell perturbation systems (CD4+ T cells) have weak signal and high cell/sample variability; models ignoring this underperform — calls for variability-aware predictors.
- Large gap to the Bootstrap oracle remains (learned models 0.22–0.58 cosine vs 0.97–0.99), so absolute predictive power is still limited.
