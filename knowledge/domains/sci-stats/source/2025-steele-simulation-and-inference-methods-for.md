<!-- synced from knowledge-base — do not edit here; change upstream and re-pull -->
---
type: source
kind: paper
confidentiality: public
visibility: global
primary: sci-stats
domains: [sci-stats, bio-multiomics]
title: Simulation and inference methods for non-Markovian stochastic biochemical reaction networks
authors: [Thomas P. Steele, David J. Warne]
year: 2025
doi: 10.48550/arxiv.2512.02478
source_url: https://doi.org/10.48550/arxiv.2512.02478
drive_file_id: TODO
text_source: paperclip
ingested_by: agent
---

# Simulation and inference methods for non-Markovian stochastic biochemical reaction networks

## TL;DR
A general framework for exact and approximate stochastic simulation of non-Markovian (delay-bearing, history-dependent) biochemical reaction networks, plus a coupling scheme that lets multifidelity Bayesian inference run on such systems — yielding ~2 orders-of-magnitude efficiency gains on a delayed-autoinhibition gene-regulation model.

## Key findings
- **Problem.** Standard stochastic chemical kinetics (Gillespie direct, next-reaction, τ-leaping) assume Markovian dynamics with instantaneous, memoryless reaction events. Processes like transcription/translation have non-negligible durations → **delay reactions** whose completion propensity depends on internal clock time *and* system state, making the process non-Markovian. Prior art (Boguñá et al. 2014; Anderson 2007) handled exact simulation but had **no approximate scheme and no coupling**, blocking multilevel/multifidelity acceleration.
- **Contribution 1 — non-Markovian Next Reaction Method (nM-NRM, Algorithm 3).** Exact simulator generalizing Anderson's modified NRM to random delays depending on both time and state, via the Kurtz random-time-change representation. Matches the generality of the Boguñá Gillespie method but, unlike it, admits a natural discretization and coupling. Delay bookkeeping uses per-channel sets `D_j` tracking initiated-but-uncompleted reactions (|D_j| = ongoing-reaction copy number).
- **Contribution 2 — non-Markovian τ-leaping (nM-TLM, Algorithm 4).** First approximate scheme for these systems; freezes state over `[t, t+τ)`, fires Poisson-distributed reaction counts, groups delay initiations with shared initiation time. Empirical convergence matches first-order theory: **weak error O(τ)**, **strong error O(τ^1/2)** (Fig. 3, estimated from n = 120,000 sims at T = 300).
- **Contribution 3 — exact coupling (Algorithm 5 / C-nM-NRM, B.1).** Generates an exact nM-NRM path *positively correlated* to an nM-TLM path by reusing common unit-rate Poisson clocks (completing the Poisson process via uniform event-time placement, then disassembling delay groups into unit-copy channels). Coupling visibly collapses variance between paired paths (Fig. 2) and improves the low-fidelity simulator's ROC as a predictor of the high-fidelity accept/reject (lower false-positive/false-negative, higher true-positive; Appendix A, Fig. A.1).
- **Inference result.** On the gene-regulation-with-delayed-autoinhibition model, multifidelity ABC (Prescott–Baker) using nM-TLM as low-fidelity + coupled nM-NRM corrections inferred θ = [β*_m, β_p, α] from synthetic data (ε = 460). Estimator variance scaled as Var ∝ O(cost⁻¹) as expected. **τ = 0.68 gave <10× speedup; τ = 2.31 gave ~100× (two orders of magnitude)** efficiency improvement (Fig. 5) — the first extension of multifidelity inference to non-Markovian systems.

## Methods (brief)
Derives the inter-event survival function as an inhomogeneous-Poisson hazard depending on internal time, extending the Kurtz representation (Eq. 11) with delay-initiation and delay-completion terms. Test model: 4-reaction network (delayed mRNA transcription with Hill-function autoinhibition and Weibull-shaped, resource-limited completion; instantaneous translation and two degradations). Inference via ABC rejection vs. multifidelity ABC with adaptive continuation-probability tuning (1,000 warm-up samples).

## Limitations
Demonstrated on a single low-dimensional gene-regulation model with synthetic (not experimental) data and uniform priors; only ABC was implemented (BSL/NLE/NPE discussed but untested). Automatic tuning of the τ step size remains an open problem — the speedup depends strongly on τ, and too-large τ degrades the low-fidelity predictor.

## Citations of interest
- Boguñá et al. 2014 (Phys. Rev. E 90:042108) — non-Markovian Gillespie algorithm; the exact baseline this work generalizes and makes discretizable.
- Anderson 2007 (J. Chem. Phys. 127) — modified next reaction method for time-dependent propensities and delays; direct ancestor of nM-NRM.
- Gillespie 2001 (J. Chem. Phys. 115:1716) — τ-leaping; basis of the nM-TLM approximation.
- Prescott & Baker 2020 (SIAM/ASA JUQ 8:114) — multifidelity ABC; the inference scheme accelerated here.
- Anderson & Higham 2012 (Multiscale Model. Simul. 10:146) — coupled MLMC for continuous-time Markov chains; coupling template extended to the non-Markovian case.
- Warne et al. 2019 (J. R. Soc. Interface 16:20180943) — review of stochastic biochemical simulation/inference; framing reference.
