<!-- synced from knowledge-base — do not edit here; change upstream and re-pull -->
---
type: source
kind: paper
confidentiality: public
visibility: global
primary: bio-multiomics
domains: [bio-multiomics, bio-clinical]
title: "Dynamics of huntingtin protein interactions in the striatum identifies candidate modifiers of Huntington disease"
authors: [Todd M. Greco, Christopher Secker, Eduardo Silva Ramos, Joel D. Federspiel, Jeh-Ping Liu, Alma M. Perez, Ismael Al-Ramahi, Jeffrey P. Cantle, Jeffrey B. Carroll, Juan Botas, Scott O. Zeitlin, Erich E. Wanker, Ileana M. Cristea]
year: 2022
doi: 10.1016/j.cels.2022.01.005
source_url: https://doi.org/10.1016/j.cels.2022.01.005
drive_file_id: TODO
text_source: paperclip
ingested_by: agent
---

# Dynamics of huntingtin protein interactions in the striatum identifies candidate modifiers of Huntington disease

## TL;DR
Quantitative IP-MS of FLAG-tagged huntingtin from the striatum of Q140 vs Q20 knockin HD mice maps polyglutamine-dependent changes in both the **abundance** and **relative stability** of huntingtin (Htt) protein interactions, and cross-validation in human cells (LuTHy two-hybrid) and a Drosophila motor assay pinpoints synaptic (SNARE, glutamate receptor) and lysosomal (V-ATPase) interactors as candidate genetic disease modifiers.

## Key findings
- **Dual-readout IP-MS workflow.** Parallel label-free (specificity + level via SAINT/MS1) and ¹³C₆-lysine metabolic-labeling (relative stability via isotope ratio, "stability ratio" SR) arms were applied to FLAG-Htt isolated from striatal tissue at 2 and 10 months (early vs late pathogenesis). FLAG-Htt was >95% soluble, IP efficiency ~70%, and Htt/Hap40 enriched >1,000-fold.
- **278 candidate Htt PPIs** passed SAINT >0.80 in ≥1 condition; **72 were previously unannotated** HTT interactors. PolyQ-dependence (|log2 FC| ≥1, p ≤0.05) gave **123 differential PPIs at 2 months** (113 increased / 10 decreased) and **139 at 10 months (all increased)**.
- **PolyQ expansion predominantly *increases* Htt interactions.** Hierarchical clustering (Fig 2A) gave 9 clusters; clusters 1–2 peaked early (synaptic transmission/signal transduction — SNAREs Nsf, Snap25, Syn1/2; WNT/Giα signaling), clusters 5–7 rose late (synapse morphogenesis, actin regulation). Largest single increase: vesicle-fusing ATPase **Nsf (>50-fold)**.
- **Stability is a distinct, mostly early axis.** SR measured for 201/278 PPIs. Stable+specific PPIs rose polyQ-dependently from 72→106 at 2 months. Most level changes were *not* accompanied by stability changes (Class 1); among stability changes, increases dominated (35 vs 8). Hap40 stayed maximally stable (SR=1), polyQ-independent.
- **Actin-cytoskeleton complexes are selectively stabilized at 2 months**: Arp2/3 subunits (Actr2/3/3b, Arpc1a/3), CAPZ heterodimer, plus myosins (Myl6, Myh9/10/14, Myo5a). β-catenin (Ctnnb1) was a stabilized first-neighbor interactor at both ages.
- **Validation.** 39 hotspot PPIs tested by LuTHy in human HEK293 cells against HTTQ145; **22/39 validated** (BRET and/or LuC), with >50% congruence supporting many direct interactions. **10 genes tested in Drosophila HD models were all genetic modifiers** of mHTT-induced motor decline (armadillo/CTNNB1 dosage-sensitive); CNTN1, ATP6V1D, ATP6V0D1 were novel modifiers. V-ATPase V1 vs V0 subunit knockdowns had opposing effects.
- Differential PPIs were largely **not** explained by transcriptome/proteome changes (vs Langfelder 2016 data), implicating direct biochemical interactome remodeling.

## Methods (brief)
Anti-FLAG immunoaffinity purification from Htt3xFlagQ20/+ and Htt3xFlagQ140/+ knockin mouse striata, analyzed by nLC-MS/MS (Orbitrap Velos). Specificity scored by SAINT (spectral counts); abundance by MS1 label-free; stability by 1:1 spike-in of ¹³C₆-lysine whole-brain reference and light/(light+heavy) isotope ratios. Orthogonal validation: LuTHy dual-readout (BRET + luciferase co-IP) two-hybrid in HEK293; Drosophila startle-induced negative-geotaxis motor performance assay with neuronal mHTT expression.

## Limitations
Striatal IP-MS used n=3 (pooled striata); stability arm relied on whole-brain (not striatal) ¹³C reference due to tissue yield, and 10-month endogenous signal was lower (reduced reproducibility). Triton-soluble Htt only — insoluble aggregate-associated interactions are excluded. Genetic-modifier validation was in Drosophila, not mammalian neurons.

## Citations of interest
- Shirasaki et al. 2012, *Neuron* — network organization of the huntingtin proteomic interactome in mammalian brain (prior BACHD interactome benchmark).
- Kaltenbach et al. 2007, *PLoS Genet* — HTT-interacting proteins as genetic modifiers of neurodegeneration.
- Joshi et al. 2013, *Mol Syst Biol* — original label-free + metabolic-labeling IP-MS stability workflow (HDAC interactome) adapted here.
- Trepte et al. 2018, *Mol Syst Biol* — LuTHy double-readout two-hybrid method used for human-cell validation.
- Guo et al. 2018, *Nature* — cryo-EM structure of huntingtin (HAP40 as direct HEAT-domain binder).
- Choi et al. 2011, *Nat Methods* — SAINT probabilistic scoring of affinity-purification MS data.
- Langfelder et al. 2016, *Nat Neurosci* — CAG-length-dependent transcriptome/proteome networks (used to exclude expression-driven artifacts).
