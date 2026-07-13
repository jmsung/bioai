<!-- synced from knowledge-base — do not edit here; change upstream and re-pull -->
---
type: source
kind: paper
confidentiality: public
visibility: global
primary: bio-myosin
domains: [bio-myosin, bio-clinical]
title: "Adaptation and validation of the ACMG/AMP variant classification framework for MYH7-associated inherited cardiomyopathies: recommendations by ClinGen's Inherited Cardiomyopathy Expert Panel"
authors: [Melissa A. Kelly, Colleen Caleshu, Ana Morales, Jillian Buchan, Zena Wolf, Steven M. Harrison, Stuart Cook, Mitchell W. Dillon, John Garcia, Eden Haverfield, Jan D.H. Jongbloed, Daniela Macaya, Arjun Manrai, Kate Orland, Gabriele Richard, Katherine Spoonamore, Matthew Thomas, Kate Thomson, Lisa M. Vincent, Roddy Walsh, Hugh Watkins, Nicola Whiffin, Jodie Ingles, J. Peter van Tintelen, Christopher Semsarian, James S. Ware, Ray Hershberger, Birgit Funke]
year: 2018
doi: 10.1038/gim.2017.218
drive_file_id: TODO
text_source: paperclip
ingested_by: agent
---

# Adaptation and validation of the ACMG/AMP variant classification framework for MYH7-associated inherited cardiomyopathies

**Authors:** Melissa A. Kelly, Colleen Caleshu, Ana Morales, … James S. Ware, Ray Hershberger, Birgit Funke; for ClinGen's Inherited Cardiomyopathy Expert Panel (CMP-EP)
**Year:** 2018
**Venue:** Genetics in Medicine 20(3):351 (advance online 4 Jan 2018)

## Abstract

ClinGen's Inherited Cardiomyopathy Expert Panel adapted the general-purpose 2015 ACMG/AMP sequence-variant classification framework for *MYH7* (β-cardiac myosin heavy chain), chosen as a pilot gene because it is the second most common inherited cause of HCM and third most common of DCM. The panel produced disease- and gene-specific rule specifications, validated them by double-review of 60 pilot *MYH7* variants, submitted the resulting classifications to ClinVar at 3-star (expert-panel-reviewed) status, and intends the framework as a template extensible to other cardiomyopathy genes.

## Key contributions

- Gene-specific derivative of the ACMG/AMP framework for *MYH7*-associated HCM/DCM/RCM (collectively 1 in 200–500 individuals).
- Of the original 28 rules: **9 deemed not applicable, 12 disease/gene-specific adjustments, 5 strength modifications**.
- Quantitative, previously-vague thresholds made explicit (allele frequency, segregation, proband counts, functional-data acceptability).
- Demonstrated that sharing unpublished internal-lab case data reclassified 20% (12/60) of pilot variants — a data-sharing argument.

## Methods

Core task team (Partners LMM, Stanford, Ohio State) revised the framework; draft rules applied to 60 *MYH7* variants (representative spectrum, including 10 initial + discrepant ClinVar assertions) via structured double review (one clinical + one lab expert each), with conflicts escalated to the full CMP-EP. Data curated Aug–Sep 2015; reference transcript NM_000257.3. ExAC cohorts used as proxy controls; filtering allele frequency (95% Poisson correction) applied.

## Key results

- **Allele-frequency rules:** BA1 (standalone benign) set to filtering AF ≥0.1% (vs default 5%, ~2 orders of magnitude conservative); BS1 ≥0.02%; PM2 (rare) at <0.004%. Derived from prevalence 1/200, penetrance 30%, gene contribution 10.6%, max pathogenic-variant contribution 2%.
- **Segregation (PP1 tiers):** ≥3 meioses (supporting, LOD 0.9), ≥5 (moderate, LOD 1.5), ≥7 meioses (strong, LOD 2.1); single-family requirement waived for this well-established gene.
- **Proband counts (PS4 tiers):** ≥2 (supporting), ≥6 (moderate), ≥15 probands (strong), using ExAC as quasi-case-control.
- **Functional data (PS3):** only a mammalian variant-specific **knock-in** model qualifies as strong; transgenic/knockout/zebrafish and typical in-vitro myosin assays deemed insufficient (low PPV).
- **Protein domain (PM1):** head-domain hotspot aa 181–937 (constraint z=6.54, clustering p<3e-15) weighted moderate; PP2 retired to avoid double-counting.
- **PVS1 removed** (LOF not an established *MYH7* mechanism); assigned PVS1_Moderate for LOF variants.
- Inter-expert concordance rose to **93%** after data-error correction (vs 20% with the unadapted framework, 90% with institutional criteria).

## Limitations / open questions

- Proband cohorts skew Caucasian; BS1 caution flagged for less-characterized populations.
- Thresholds assume autosomal-dominant, single-variant disease paradigm (misses compound-het / oligogenic cases).
- Framework is a "stepping stone" — expected to need iterative refinement and extension to other sarcomere genes.
