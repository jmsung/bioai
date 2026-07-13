<!-- synced from knowledge-base — do not edit here; change upstream and re-pull -->
---
type: source
kind: paper
confidentiality: public
visibility: global
primary: bio-myosin
domains: [bio-myosin, bio-drug-discovery, bio-multiomics]
title: An 'Omics' Perspective on Cardiomyopathies and Heart Failure
authors: [Rajendra Raghow]
year: 2016
doi: 10.1016/j.molmed.2016.07.007
source_url: https://doi.org/10.1016/j.molmed.2016.07.007
drive_file_id: TODO
text_source: paperclip
ingested_by: agent
---

# An 'Omics' Perspective on Cardiomyopathies and Heart Failure

## TL;DR
A review arguing that unbiased multi-omics (genomics, transcriptomics, epigenomics, proteomics, metabolomics) is replacing reductionist single-variable studies of hypertrophic (HCM) and dilated (DCM) cardiomyopathy, revealing that multiple rare variants, modifier genes, and post-transcriptional regulation underpin the disease's extreme clinical heterogeneity — but that bioinformatics integration with clinical data remains the bottleneck.

## Key findings
- **Genetics of the disease.** Since the founding 1990 discovery of a causal **β-myosin heavy chain (MYH7)** mutation, >1500 mutations across **30 genes** have been linked to cardiomyopathies (Table 1). <70% of familial HCM is explained by **MYH7 + MYBPC3**; ~25% of familial DCM traces to **titin (TTN)** truncations. Most are autosomal dominant and act via functional haploinsufficiency or dominant-negative products.
- **Prevalence/risk.** Congenital HCM affects ~1 in 500; DCM ~1 in 250; both are leading causes of **sudden cardiac death (SCD)** in people under 35. ~5% of patients are compound heterozygous (>1 mutation, sometimes same gene).
- **Genomics.** GWAS achieved only modest success (SNPs explain a fraction of variance; rare variants elude single-marker significance). WGS/WES are superseding it — WES can probe ~180,000 exons and is well-suited to TTN's ~400 exons. A landmark integrated study (Roberts et al.) assessed TTN structure + titin mRNA/protein across **5267 clinically stratified individuals**, combining genetic, transcriptomic, proteomic data with clinical histories.
- **Transcriptomics.** Physiological vs. pathological CH have distinct profiles, yet share >1650 differentially expressed genes; the *networks* (mitochondrial energetics, fatty-acid metabolism, ECM, sarcomere organization) are differentially "rewired." RNA-seq revealed re-expression of **fetal splice isoforms** in pathological hypertrophy and altered splicing factors (Ptbp1, A2bp1). An RNA-seq signature classified failing vs. non-failing hearts in 313 patients at **90% accuracy** (Liu et al.).
- **Epigenomics.** Distinct DNA-methylation patterns in failing ISCH/DCM hearts; norepinephrine-induced CpG hypermethylation (e.g., PKC-ε) was reversed by **5-aza-2-deoxycytidine**, normalizing CH — flagging DNA methylation as a therapeutic target. ChIP-seq of 7 histone marks mapped active marks to cell-adhesion/ECM genes and repressive marks to oxidative-phosphorylation genes. miRs (miR-25, -22, -21) and lncRNAs regulate contractility, hypertrophy, fibrosis; some shuttle via exosomes as paracrine signals.
- **Proteomics.** LC-MS/MS and iTRAQ studies show CH proteomes dominated by regulators of sarcomere contractility, Ca²⁺ handling, antioxidant defense, mitochondrial energetics. TAC for 14/28 days altered 132/86 of 1748 proteins. ²H₂O-labeling measured turnover of ~3000–3228 proteins, implicating protein synthesis/stability and PTMs (not just abundance) in CH. Sex differences (more pronounced mitochondrial changes in males) align with estrogen cardioprotection.
- **Metabolomics** (the "most informative proxy for biochemistry"). Pressure-overload/infarcted hearts show ↓ purines, acylcarnitines, fatty acids, lysolipids, sphingolipids and ↑ pyrimidines, ascorbate, heme, branched-chain amino acids. A **fat→glucose fuel switch** and a putative block of FA/glucose flux into the TCA cycle distinguish decompensated from physiological CH; accumulation of acetyl-CoA/succinyl-CoA may feed back epigenetically. mTOR signaling links nutrient sensing to growth and autophagy inhibition.

## Methods (brief)
Narrative review surveying GWAS, WGS/WES, microarray/RNA-seq, ChIP-seq, MS-based proteomics (iTRAQ, ²H₂O turnover, top-down), and NMR/GC-LC-MS metabolomics across mouse/rat/zebrafish/Drosophila models (TAC, isoproterenol/angiotensin-II infusion, exercise) and patient/iPSC samples. No primary data.

## Limitations
A 2016 review; most omics findings are from animal models (TAC, isoproterenol) not patients, and the author repeatedly notes bioinformatics cannot yet reconcile heterogeneous platforms/models or integrate omics with clinical histories. No mechanistic myosin biochemistry; claims are associative, not causal.

## Citations of interest
- Geisterfer-Lowrance et al. 1996 (Science) — founding mouse model of familial HCM via MYH7 mutation.
- Roberts et al. 2015 (Sci. Transl. Med.) — integrated allelic/transcriptional/phenomic dissection of TTN truncations in 5267 individuals.
- Herman et al. 2012 (NEJM) — titin truncations causing DCM.
- Drozdov et al. 2010/2013 — gene-network meta-analyses distinguishing physiological vs. pathological CH.
- Liu et al. 2015 (Genomics) — RNA-seq heart-failure signature classifying 313 patients at 90% accuracy.
- Bernardo et al. 2010 (Pharmacol. Ther.) — molecular distinction between physiological and pathological cardiac hypertrophy.
- Sansbury et al. 2014 / Lai et al. 2014 (Circ. Heart Fail.) — metabolomic reprogramming in pressure-overloaded and failing hearts.
