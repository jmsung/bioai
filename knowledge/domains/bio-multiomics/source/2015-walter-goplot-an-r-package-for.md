<!-- synced from knowledge-base — do not edit here; change upstream and re-pull -->
---
type: source
kind: paper
confidentiality: public
visibility: global
primary: bio-multiomics
domains: [bio-multiomics]
title: "GOplot: an R package for visually combining expression data with functional analysis"
authors: [Wencke Walter, Fátima Sánchez-Cabo, Mercedes Ricote]
year: 2015
doi: 10.1093/bioinformatics/btv300
source_url: https://doi.org/10.1093/bioinformatics/btv300
drive_file_id: TODO
text_source: paperclip
ingested_by: agent
---

# GOplot: an R package for visually combining expression data with functional analysis

## TL;DR
GOplot is an R package (built on ggplot2) that fuses gene/protein/metabolite expression data with the output of any gene-ontology enrichment analysis, producing layered, publication-quality plots that preserve both the statistical significance of enriched terms and the per-molecule expression direction in a single view.

## Key findings
- **Problem addressed:** existing enrichment-visualization tools (REVIGO, ggbio, RCircos) display either functional-analysis results *or* expression data, but none combine them in a way that "guarantees the preservation of the power of both analyses." GOplot fills that integration gap.
- **Two input datasets required:** (1) a list of selected molecules with expression levels (e.g. logFC), and (2) the results of a functional/enrichment analysis (e.g. GO terms with adjusted P-values).
- **Two preprocessing functions:**
  - `circle_dat()` — merges expression and enrichment data into the canonical input object for most plotting functions.
  - `chord_dat()` — generates a binary molecule-to-term assignment matrix used by `GOChord()`.
- **Plotting functions span general → specific (deductive reasoning path):**
  - `GOBar()` / `GOBubble()` — comparative overview charts encoding **enrichment significance (−log10 adjusted P-value)** and the term **z-score**; bubble circles are area-proportional to the number of molecules per category; bars sortable by z-score or P-value.
  - `GOCircle()` — inner ring bar plot (height = significance, color = z-score) with an outer ring of scatterplots showing per-gene logFC within each term (Fig. 1a).
  - `GOChord()` — ribbon diagram linking genes to their assigned terms, with blue-to-red logFC coding beside each gene (Fig. 1b).
  - `GOCluster()` — circular dendrogram of clustered expression profiles; inner ring shows color-coded logFC across up to three conditions, outer ring the assigned functional terms (Fig. 1c).
  - `GOVenn()` — Venn diagram that reports not just overlap counts but the **expression pattern** of shared elements (commonly upregulated, commonly downregulated, or contraregulated); also deployed as an interactive **shiny** web app.
- **Usability claim:** insightful integrated plots in only a few lines of code, lowering the barrier to communicating omics findings.
- **Availability:** distributed via CRAN (`GOplot`); shiny Venn app and a worked manual with sample figures are publicly hosted.

## Methods (brief)
The package is implemented on top of ggplot2 (the grammar-of-graphics system), exploiting its multilayered plotting to assemble pre-specified composite charts. It ships a sample endothelial-cell dataset (`EC`, derived from GEO accession GSE47067): expression data were normalized, differentially expressed genes identified, and a gene-annotation enrichment analysis run with the DAVID tool (adjusted P < 0.05). Figure 1 was generated from this dataset via `circle_dat()`, `chord_dat()`, and the plotting calls.

## Limitations
An Applications Note describing a visualization wrapper, not a new analytical method: GOplot consumes (and is only as good as) upstream enrichment results from external tools like DAVID, and does not itself perform statistical testing. `GOCluster` is limited to displaying up to three expression conditions.

## Citations of interest
- Huang et al. (2009), *Nat. Protoc.* — DAVID bioinformatics resources for gene-list enrichment analysis (the enrichment engine feeding GOplot's example).
- Wickham (2009), *ggplot2* — the grammar-of-graphics framework GOplot is built upon.
- Supek et al. (2011), *PLoS ONE* — REVIGO, a prior GO-term summarization/visualization tool.
- Yin et al. (2012), *Genome Biol.* — ggbio, extending the grammar of graphics to genomic data.
- Zhang et al. (2013), *BMC Bioinformatics* — RCircos for Circos-style 2D track plots.
