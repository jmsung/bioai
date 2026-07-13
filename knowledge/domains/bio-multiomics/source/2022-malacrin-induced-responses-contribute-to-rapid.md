<!-- synced from knowledge-base — do not edit here; change upstream and re-pull -->
---
type: source
kind: paper
confidentiality: public
visibility: global
primary: bio-multiomics
domains: [bio-multiomics]
title: Induced responses contribute to rapid plant adaptation to herbivory
authors: [Antonino Malacrinò, Laura Böttner, Sara Nouere, Meret Huber, Martin Schäfer, Shuqing Xu]
year: 2022
doi: 10.1101/2022.11.24.517793
source_url: https://doi.org/10.1101/2022.11.24.517793
drive_file_id: TODO
text_source: paperclip
ingested_by: agent
---

# Induced responses contribute to rapid plant adaptation to herbivory

## TL;DR
Using >30 generations of outdoor experimental evolution of the duckweed *Spirodela polyrhiza* under snail (*Lymnaea stagnalis*) herbivory, the authors show that herbivory rapidly raises plant resistance through three jointly acting mechanisms — shifted genotype frequencies, herbivory-induced phenotypic plasticity, and altered plant microbiota — providing direct multigenerational evidence that induced responses are adaptive.

## Key findings
- **Rapid morphological/growth shifts under herbivory.** Across two growing seasons, herbivory populations had lower surface area per frond (χ²=75.83; df=1; p<0.0001) and higher dry weight per frond (χ²=12.95; p=0.0003) than controls. Morphological changes appeared within ~4 weeks and persisted past ~30 asexual generations, implying robustness to abiotic variation.
- **Slower growth post-herbivory.** Plants previously exposed to herbivory grew more slowly in frond number (χ²=36.72; p<0.0001), biomass (χ²=706.37; p<0.0001), and area (χ²=26794; p<0.0001) over a 2-week assay.
- **Increased resistance (adaptive plasticity).** Snails consumed fewer fronds (χ²=35.74; p<0.0001), less biomass (χ²=449.61; p<0.0001), and less surface area (χ²=730.22; p<0.0001) from herbivory-evolved populations. Herbivory also consistently induced higher production of the putative defensive metabolite **tyramine** across both seasons.
- **Genotype-frequency evolution.** From a 25%-each four-genotype start (Sp21, Sp56, Sp58, Sp65), herbivory shifted Sp21 and Sp65 in opposite directions by week 12: Sp21 fell (control 33.9±2.4% vs herbivory 24.5±1.8%, p=0.0004) while Sp65 rose (control 19.3±1.6% vs herbivory 27.1±2.1%, p=0.0006); Sp56/Sp58 unchanged. Intrinsic genotype growth/resistance differences (driven mainly by susceptible Sp56) did **not** explain the Sp21/Sp65 shifts.
- **Plasticity × evolution interaction.** In factorially-assembled synthetic populations, genotype-frequency change alone did not alter resistance in non-induced plants (p=0.914) but did increase resistance in herbivory-induced plants (plasticity×evolution χ²=4.47; df=1; p=0.034; induced p=0.006) — selection acted on induced resistance traits.
- **Microbiota contribution is genotype-specific.** Herbivory-induced microbiota (plants protected from direct feeding by fine nets) raised resistance only in Sp65 (χ²=3.78; p=0.05), not the other genotypes. Bacterial community structure shifted significantly in Sp65 (F1,12=1.58; p=0.01) but not Sp21 (p=0.06); eukaryotic communities were unchanged in both.

## Methods (brief)
Replicated outdoor experimental evolution across 10 ponds, each split into paired herbivory/control cages (12 snails added over 3 weeks). Growth and 24 h herbivory resistance assays quantified consumed fronds/biomass/area. Genotype frequencies were estimated by pool-seq (Illumina NovaSeq, mapped with Bowtie2; HAFpipe over 68 diagnostic loci, <1.9% misassignment), with non-mapping reads profiled via Kraken2/Bracken for microbiota. 16S/18S amplicon metagenomics (DADA2, SILVA/PR2, PERMANOVA) characterized genotype-specific communities; targeted metabolomics tracked defensive metabolites; linear mixed-effects models (lme4) with FDR correction throughout.

## Limitations
Single plant–herbivore model system (clonal duckweed, four genotypes, one snail species); three of ten populations collapsed in season 2. Microbiota resistance effect rests on a single genotype (Sp65) at borderline significance (p=0.05); the causal bacterial taxa and the mechanistic basis of resistance (specific metabolites vs cell-wall thickening) remain unidentified. Preprint, not peer-reviewed.

## Citations of interest
- Agrawal et al. 2012, *Science* 338:113 — insect herbivores drive real-time ecological/evolutionary change in plant populations.
- Karban & Myers 1989, *Annu. Rev. Ecol. Syst.* 20:331 — the long-standing hypothesis that induced plant responses are adaptive.
- Xu et al. 2019, *Nat. Commun.* 10:1243 — low genetic variation and mutation rate in giant duckweed (basis for the model system).
- Wang et al. 2014, *Nat. Commun.* 5:3311 — *Spirodela polyrhiza* reference genome.
- Tilk et al. 2019, *G3* 9:4159 — HAFpipe, accurate allele frequencies from ultra-low-coverage pool-seq.
- Baldwin 1998, *PNAS* 95:8113 — jasmonate-induced defenses are costly but benefit plants under attack.
