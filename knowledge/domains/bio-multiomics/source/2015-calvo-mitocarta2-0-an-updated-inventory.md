<!-- synced from knowledge-base — do not edit here; change upstream and re-pull -->
---
type: source
kind: paper
confidentiality: public
visibility: global
primary: bio-multiomics
domains: [bio-multiomics]
title: "MitoCarta2.0: an updated inventory of mammalian mitochondrial proteins"
authors: [Sarah E. Calvo, Karl R. Clauser, Vamsi K. Mootha]
year: 2016
doi: 10.1093/nar/gkv1003
source_url: https://doi.org/10.1093/nar/gkv1003
drive_file_id: TODO
text_source: paperclip
ingested_by: agent
---

# MitoCarta2.0: an updated inventory of mammalian mitochondrial proteins

## TL;DR
MitoCarta2.0 is a curated inventory of 1158 human and 1158 mouse genes encoding proteins with strong evidence of mitochondrial localization, built by naïve-Bayes integration of seven genome-scale datasets against a hand-curated training set. It updates the 2008 MitoCarta1.0, adding ~240 (human) and ~191 (mouse) genes through better gene models, literature curation, and homology mapping.

## Key findings
- **Human MitoCarta2.0 = 1158 genes** (918 retained from MitoCarta1.0 + 240 new); **mouse = 1158 genes** (967 retained + 191 new). 79% (human) / 83% (mouse) overlap with v1.0 (Figure 3).
- Built as the union of a **training set (T_mito): 960 human / 961 mouse definite mitochondrial genes** plus all Maestro naïve-Bayes predictions at **FDR ≤ 5%** (198 human predictions).
- T_mito is the union of (i) literature curation, (ii) presence in **APEX-labeling matrix or IMS proteomes** in HEK 293T cells, and (iii) confirmed GFP-tagging/microscopy localization. The training set grew **60%** over v1.0; 15 v1.0 genes were dropped on re-curation.
- **Seven data sources** integrated, each weighted by accuracy: MS/MS abundance across 14 mouse tissues, *S. cerevisiae* homology, coexpression (now 91 tissues, +50%), Pfam protein domain, TargetP N-terminal targeting signal, *Rickettsia prowazekii* ancestry, and PGC-1α-induction.
- Each feature scored as a **LogOdds = log2[P(F_b|T_mito)/P(F_b|T_non-mito)]**; summed under conditional-independence assumption into a per-gene Maestro score (Figure 2A–C).
- **Integration vastly outperforms any single method**: at the 5% FDR threshold the naïve-Bayes classifier reaches **80% sensitivity, 99.6% specificity** (10-fold CV: 79%/99.7%) — far above any individual data source (Figure 2D).
- Data-source improvements: MS/MS reprocessing (reversed faulty lock-mass calibration) yielded **75% more spectra and 10% more unique peptides**; jackHMMER added distant yeast/Rickettsia homologs with separate ortholog/homolog scoring for higher specificity.
- New-vs-dropped examples: **ECHDC1** entered v2.0 via improved MS/MS + newly annotated yeast homolog + coexpression (Figure 2B); **NFXL1** dropped because a corrected full-length RefSeq protein has only a low-confidence targeting signal (Figure 2C).
- Of 240 new human genes: **100 in APEX matrix/IMS proteomes, 36 other literature, 104 computational** (FDR≤5%). Of 94 retired human genes, 9 were pseudogenes.
- 96% of human/mouse entries are reciprocal top hits; species-specific genes (e.g., human ATAD3B, mouse Csl) and threshold-edge cases (human BOLA3, LDHB) differ between inventories.

## Methods (brief)
Human/mouse RefSeq release 63 proteins mapped to NCBI Gene loci. Seven complementary localization features computed (largely mouse-derived, mapped to human orthologs by reciprocal BlastP). Maestro naïve-Bayes classifier weights each feature by LogOdds against T_mito / T_non-mito training sets; FDR computed with prior O = 1500/21000. APEX proximity labeling (matrix + IMS) supplied high-specificity proteomic training data.

## Limitations
The inventory is static (no continuous literature updates), mitochondrial-centric (does not flag additional or condition-dependent localizations), gene- rather than isoform-based, and biased toward double-membrane-interior proteins — so it is less accurate for the **outer mitochondrial membrane**, which needs additional experimental data.

## Citations of interest
- Pagliarini et al. 2008, *Cell* — original MitoCarta1.0 compendium and complex I disease biology.
- Calvo et al. 2006, *Nat. Genet.* — the Maestro naïve-Bayes integrative-genomics framework reused here.
- Rhee et al. 2013, *Science* & Hung et al. 2014, *Mol. Cell* — APEX spatially-restricted proximity labeling of mitochondrial matrix and IMS proteomes.
- Emanuelsson et al. 2000, *J. Mol. Biol.* — TargetP N-terminal targeting-signal predictor.
- Andersson et al. 1998, *Nature* — *Rickettsia prowazekii* genome / endosymbiotic origin of mitochondria, basis of the ancestry feature.
