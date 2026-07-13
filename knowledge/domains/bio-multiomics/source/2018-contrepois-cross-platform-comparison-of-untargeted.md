<!-- synced from knowledge-base — do not edit here; change upstream and re-pull -->
---
type: source
kind: paper
confidentiality: public
visibility: global
primary: bio-multiomics
domains: [bio-multiomics]
title: Cross-Platform Comparison of Untargeted and Targeted Lipidomics Approaches on Aging Mouse Plasma
authors: [Kévin Contrepois, Salah Mahmoudi, Baljit K. Ubhi, Katharina Papsdorf, Daniel Hornburg, Anne Brunet, Michael Snyder]
year: 2018
doi: 10.1038/s41598-018-35807-4
source_url: https://doi.org/10.1038/s41598-018-35807-4
drive_file_id: TODO
text_source: paperclip
ingested_by: agent
---

# Cross-Platform Comparison of Untargeted and Targeted Lipidomics Approaches on Aging Mouse Plasma

## TL;DR
A head-to-head benchmark of untargeted RPLC-MS against the targeted Lipidyzer (SCIEX) platform shows both profile >300 lipids across 11 classes in mouse plasma with comparable precision/accuracy and well-correlated quantification (median r=0.71 on endogenous lipids, 0.99 on internal-standard dilutions); applied to aging, both identify triacylglycerols (TAG) as the lipid class most sensitive to age.

## Key findings
- **Coverage is similar but complementary.** LC-MS detected 337 lipids, Lipidyzer 342, both across 11 classes. After converting LC-MS TAG/SM annotations to match Lipidyzer's level of information (337→554 annotations), 196 species overlapped (35% of untargeted, 57% of targeted). Combined, the platforms reach **700 lipid molecular species** in mouse plasma.
- **Complementarity by class.** Lipidyzer uniquely detected free fatty acids (FFA) and many cholesterol esters (CE); LC-MS uniquely detected many phosphatidylcholines (PC), especially ether-linked PC (plasmalogens), and phosphatidylinositols (PI). Neither covered acylcarnitines, oxylipins, FAHFA, bile acids, PS, PG, or PA.
- **Annotation differences.** LC-MS resolves all three fatty acids in a TAG (e.g. TAG(16:0/18:1/18:2)); Lipidyzer reports one FA plus total carbons/unsaturation (TAG52:3-FA16:0), overestimating TAG count. SM: LC-MS gives total carbons (SM(d38:1)), Lipidyzer assumes an 18:1 sphinganine backbone and reports the other FA.
- **Precision.** Intra-day median CV 3.1% (LC-MS) / 4.7% (Lipidyzer); inter-day 10.6% / 5.0%; technical repeatability (triplicate pool) 6.9% / 4.7% (Fig 1D). Comparable to or better than the 5.5–10% reported across 9 LC-MS platforms.
- **Accuracy.** Median 6.9% (LC-MS) vs 13.0% (Lipidyzer) (Fig 1E). Lipidyzer signal plateaued at high concentrations for TAG, DAG, CE, CER; dropping the top calibration point made accuracies comparable.
- **Aging signal.** Comparing young (4 mo, n=10) vs old (25 mo, n=10) male C57BL/6 mice: modest global decline in total lipids (P=0.01 LC-MS, P=0.07 Lipidyzer), driven by reduced TAG (P=0.02 / P=0.03). LC-MS also saw decreased DAG (P=0.02) and CER (P=0.03); Lipidyzer did not (coverage difference).
- ~Half of detected lipids changed with age (170 LC-MS / 172 Lipidyzer, FDR<0.05); most decreased, only 2–3% increased. **TAG was the most age-susceptible class: 78% of individual TAG species deregulated** across both platforms (Fig 2F), nearly all decreasing. TAG made up 45% (LC-MS) and 84% (Lipidyzer) of significantly deregulated lipids.

## Methods (brief)
Lipids extracted from 30 µl plasma by biphasic chloroform/methanol. Untargeted: Accucore C18 RPLC on a Q Exactive Plus (62-min run, pos+neg modes); features extracted with XCMS/CAMERA, identified via LipidSearch with manual MS/MS validation. Targeted: Lipidyzer (5500 QTRAP + SelexION differential mobility spectrometry, flow-injection MRM, 21-min run), quantified against 54 deuterated internal standards covering 10 classes. Two-tailed Welch's t-test with q-value/FDR correction.

## Limitations
Small N (10 vs 10), male C57BL/6 only, single overnight-fasted timepoint, plasma only. Lipidyzer internal standards are validated for human plasma/serum, so quantification in mouse (or other tissues) is approximate; the platform plateaus at high concentrations for several neutral-lipid classes. TAG nomenclature mismatch forced exclusion of TAG from the inter-platform correlation analysis.

## Citations of interest
- Quehenberger et al. 2010 (J Lipid Res) — LIPIDMAPS human plasma lipidome diversity, the comparator for class abundance.
- Bowden et al. 2017 (J Lipid Res) — NIST interlaboratory lipidomics harmonization exercise (SRM 1950); benchmark for overlap statistics.
- Cajka, Smilowitz & Fiehn 2017 (Anal Chem) — validation of quantitative untargeted lipidomics across nine LC-MS platforms; CV benchmark.
- Lintonen et al. 2014 (Anal Chem) — differential mobility spectrometry-driven shotgun lipidomics, the basis for Lipidyzer class separation.
- Houtkooper et al. 2011 (Sci Rep) — metabolic footprint of aging in mice, prior aging-lipid context.
