<!-- synced from knowledge-base — do not edit here; change upstream and re-pull -->
---
type: source
kind: paper
confidentiality: public
visibility: global
primary: bio-multiomics
domains: [bio-multiomics]
title: "GAM: a web-service for integrated transcriptional and metabolic network analysis"
authors: [Alexey A. Sergushichev, Alexander A. Loboda, Abhishek K. Jha, Emma E. Vincent, Edward M. Driggers, Russell G. Jones, Edward J. Pearce, Maxim N. Artyomov]
year: 2016
doi: 10.1093/nar/gkw266
source_url: https://doi.org/10.1093/nar/gkw266
drive_file_id: TODO
text_source: paperclip
ingested_by: agent
---

# GAM: a web-service for integrated transcriptional and metabolic network analysis

## TL;DR
GAM ("genes and metabolites") is a web-service that integrates steady-state metabolomic and transcriptional differential-expression data on a KEGG-derived metabolic network and returns the *most regulated connected subnetwork* between two conditions by solving a maximum-weight connected subgraph (MWCS) problem.

## Key findings
- Addresses a gap: while flux-balance (FBA/IOMA) and pathway-enrichment (MetaboAnalyst, iPEAP) tools exist, accessible **network-based** integration of mammalian *steady-state* metabolomics + transcriptomics that can discover novel subnetworks (vs. nearest-neighbor tools like MetScape) was lacking.
- Pre-assembled metabolic networks for **human, mouse, Arabidopsis, yeast**, built from the KEGG REACTION + RPAIR + ENZYME databases; other KEGG organisms addable on request.
- Input is differential-expression (DE) tables for genes and/or metabolites (ID, pval, log2FC) — directly accepts raw **limma** and **DESeq2** output; gene IDs via RefSeq/Entrez/symbol, metabolites via HMDB/KEGG IDs.
- Pipeline (Figure 1): (i) restrict network to reactions with expressed enzymes; (ii) map reaction network to a simple graph; (iii) score nodes/edges; (iv) solve MWCS for the most-regulated module; (v) post-process.
- **Scoring** adopted from Dittrich et al. (2008): DE P-values fit to a β-uniform mixture (signal = B(a,1), noise = uniform); score is the log-likelihood ratio of being in the signal component, normalized to an FDR threshold — so low-P nodes get positive scores, high-P get negative. Separate FDR thresholds for metabolites vs. enzymes let users bias toward metabolic or transcriptional signal. A reaction inherits the *smallest* P-value among its catalyzing genes (any one enzyme changing implies possible flux change).
- Two graph mappings: a **flow-centric** view (metabolites = nodes, reactions = edges, using only "main" RPAIR interconversions) preferred when metabolomic data are present, and a **gene-centric** view (metabolites and reactions both nodes) preferred for transcription-only data; reactions sharing an enzyme are collapsed to cut redundancy.
- Three MWCS formulations defined — **simple** (SMWCS, node-weighted, optimum is a tree), **generalized** (GMWCS, node+edge weights, may contain cycles), **acyclic** (AMWCS) — served by three solvers: **heinz**, **heinz2** (El-Kebir & Klau), and the authors' own **gmwcs** (ILP reduction solved with CPLEX). Defaults: heinz2/gmwcs with a 30 s limit for interactivity; optional heinz run to provable optimality within 4 min.
- "Autogenerate FDRs" yields a starting module of ~100–150 reactions; a one-click button runs both steps. Output visualizes online with links to KEGG entries and downloads as PDF, XLSX, or Cytoscape XGMML.
- **Case study 1** (mouse M1 LPS+IFNγ vs. M0 macrophages): integrated analysis highlighted TCA-cycle and glycolysis changes at the metabolic level and urea cycle / fatty-acid synthesis at the transcriptional level — only joint integration gave the complete picture.
- **Case study 2** (MCF10A mammary cells, 2-deoxyglucose vs. control, GSE59228, transcription-only): recovered upregulation of the glutathione redox locus and glutaminolysis — known signatures of glucose starvation — demonstrating utility even without metabolomics.

## Methods (brief)
Networks built from KEGG REACTION/RPAIR/ENZYME with ubiquitous and anomeric metabolites collapsed/excluded to avoid connectivity bias (Supplementary Tables S1–S3). Implemented as R packages (GAM, GAM.db, GAM.networks) plus an R Shiny web front-end; source on GitHub (ctlab/GAM, ctlab/shinygam, ctlab/gmwcs-solver). MWCS solved via integer linear programming with CPLEX and a problem-splitting heuristic.

## Limitations
A discovery/hypothesis-generation tool, not validation; modules are statistically regulated subnetworks, not proven causal flux changes. Restricted to KEGG-supported organisms and metabolites with database IDs; results depend on user-set FDR thresholds and the 30 s solver time limit yields good *suboptimal* (not always provably optimal) solutions. Steady-state data cannot resolve true flux directionality.

## Citations of interest
- Dittrich et al. 2008 (*Bioinformatics* 24:i223) — the MWCS exact-solver and β-uniform scoring scheme GAM adopts from PPI-network analysis.
- El-Kebir & Klau 2014 (arXiv:1409.5308) — heinz2 SMWCS solver.
- Jha et al. 2015 (*Immunity* 42:419) — macrophage-polarization metabolic-module study supplying the M0/M1 case-study data.
- Vincent et al. 2015 (*Mol. Cell* 60:195) — PEPCK metabolic-adaptation study; prior network-integration application.
- Kanehisa 2000 (*NAR* 28:27) — KEGG database underlying the reaction networks.
- Beisser et al. 2012 (*Bioinformatics* 28:1887) — robustness of MWCS functional modules to noise.
