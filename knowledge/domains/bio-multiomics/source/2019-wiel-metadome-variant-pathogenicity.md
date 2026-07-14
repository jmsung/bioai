<!-- synced from knowledge-base — do not edit here; change upstream and re-pull -->
---
type: source
kind: paper
confidentiality: public
visibility: global
primary: bio-multiomics
domains: [bio-multiomics, bio-clinical]
title: "MetaDome: Pathogenicity analysis of genetic variants through aggregation of homologous human protein domains"
authors: [Laurens Wiel, Coos Baakman, Daan Gilissen, Joris A. Veltman, Gerrit Vriend, Christian Gilissen]
year: 2019
doi: 10.1002/humu.23798
source_url: https://doi.org/10.1002/humu.23798
drive_file_id: 1Naco4j-vBHIrIaw6qmnaBuqLWhLmvDLF
text_source: pdf
ingested_by: claude-opus-4-8
---
# MetaDome: Pathogenicity analysis of genetic variants through aggregation of homologous human protein domains

**Authors:** Laurens Wiel, Coos Baakman, Daan Gilissen, Joris A. Veltman, Gerrit Vriend, Christian Gilissen (Radboud University Medical Center, Nijmegen)  ·  **Year:** 2019  ·  **Venue:** Human Mutation 40(8):1030–1038

## One-line
MetaDome is a free web server that interprets variants of unknown significance by aggregating human population and pathogenic variation across *homologous* Pfam protein domains ("meta-domains"), producing an amino-acid-resolution genetic-tolerance profile so a residue's constraint can be read even when its own gene is sparsely sampled.

## Key claim
Transferring variation information between homologous positions — a classic bioinformatics idea (MSA/BLAST) — works *within the human genome* at the Pfam-domain level: equivalent positions across paralogous domains share tolerance behavior, so pooling variation across all copies of a domain sharpens per-position pathogenicity signal. ~71–72% of disease-causing missense variants (HGMD/ClinVar) fall in regions translating to a Pfam domain, and pathogenic missense variants at equivalent domain positions tend to co-occur with an *absence* of population variation at those positions (and vice versa). MetaDome operationalizes this into an interactive tool for non-bioinformaticians.

## Method
Map population variation (gnomAD) and pathogenic mutations (ClinVar; earlier version used ExAC + HGMD) onto Pfam protein domains across the human proteome, then aggregate homologous domain occurrences into meta-domains to compute per-position genetic-tolerance / intolerance scores at single-amino-acid resolution. Serve as a web app: gene-wide tolerance landscapes plus schematic protein views, letting a user drop in a variant of interest and see meta-domain variation at the corresponding position. Engineering: open-source (github.com/cmbi/metadome), Dockerized (Flask + PostgreSQL + Celery/Redis/RabbitMQ), D3/JQuery visualizations; live at stuart.radboudumc.nl/metadome.

## Result
- Updated data coverage: **56,319 human transcripts, 71,419 Pfam protein domains, 12,164,292 genetic variants (gnomAD), 34,076 pathogenic mutations (ClinVar).**
- Delivers amino-acid-resolution intolerance profiles gene-wide, and per-position meta-domain evidence (presence/absence of homologous population vs pathogenic variation) to support VUS interpretation.
- Worked example demonstrates added value for interpreting a variant of unknown significance beyond single-gene population-frequency lookups.
- Complements/extends intolerance methods like RVIS/subRVIS by borrowing strength across domain homologs rather than treating each gene in isolation.

## Limitations / open questions
- Coverage is bounded by Pfam annotation — variants outside any Pfam domain (~28–29% of pathogenic missense) get no meta-domain signal.
- Aggregation assumes homologous positions share functional constraint; paralog-specific sites can be mispredicted.
- It surfaces evidence (tolerance context), not a calibrated pathogenicity classifier — interpretation is left to the user.

## Key terms
MetaDome, meta-domains, genetic tolerance / intolerance, variant of unknown significance (VUS), Pfam protein domains, domain homology, gnomAD, ClinVar, HGMD, ExAC, RVIS/subRVIS, missense pathogenicity, multiple sequence alignment, web server
