<!-- synced from knowledge-base — do not edit here; change upstream and re-pull -->
---
type: source
kind: paper
confidentiality: public
visibility: global
primary: bio-multiomics
domains: [bio-multiomics]
title: A multimodal conversational agent for DNA, RNA and protein tasks
authors: [Bernardo P. de Almeida, Guillaume Richard, Hugo Dalla-Torre, Christopher Blum, Lorenz Hexemer, Priyanka Pandey, Stefan Laurent, Chandana Rajesh, Marie Lopez, Alexandre Laterre, Maren Lang, Uğur Şahin, Karim Beguir, Thomas Pierrot]
year: 2025
doi: 10.1038/s42256-025-01047-1
source_url: https://doi.org/10.1038/s42256-025-01047-1
drive_file_id: TODO
text_source: paperclip
ingested_by: agent
---

# A multimodal conversational agent for DNA, RNA and protein tasks

## TL;DR
ChatNT couples a pretrained DNA foundation model (Nucleotide Transformer v2, 500M) to a frozen English LLM (Vicuna-7B) via a question-aware Perceiver projection, yielding a single conversational agent that solves dozens of DNA/RNA/protein prediction tasks in plain English — setting a new state of the art on the Nucleotide Transformer benchmark while matching task-specialized models.

## Key findings
- **Unified multitask model.** One model solves all 18 Nucleotide Transformer benchmark tasks at once at **MCC 0.77**, vs 0.69 for the previous SOTA NT v2 (500M) — an 8-point gain — instead of 18 separately fine-tuned experts.
- **Question-aware projection is the key trick.** A standard Perceiver resampler (Flamingo-style gated cross-attention) gives a fixed embedding set regardless of the question, creating an information bottleneck across diverse tasks. Adding cross-attention between the learnable queries and the English question raised average MCC from **0.71 → 0.77**. K=64 resampled embeddings was the sweet spot (K=1 or 4 too weak to steer the frozen decoder).
- **Architecture.** Three modular parts — DNA encoder (backprop'd, not frozen, to push supervised signal into the encoder), projection (trained from scratch), and a **frozen** English decoder (preserves conversational ability, prevents degradation). DNA tokens = 6-mers; sequences padded to 2,048 tokens (~12 kb).
- **Curated 27-task instructions dataset** beyond the benchmark: 21 DNA, 3 RNA, 3 protein tasks across human/mouse/fly/plants/yeast — 605M DNA tokens (3.6 Gbp) + 273M English tokens, ~1,000 Q–A pairs/task. RNA/protein tasks predicted from the corresponding CDS, not RNA/AA sequences.
- **Matches specialists.** On RNA/protein regression, PCC 0.62–0.91; **beat** APARENT2 on proximal polyadenylation (0.91 vs 0.90) and ESM2 on protein meltome (0.89 vs 0.85). Lagged Saluki on RNA degradation (PCC 0.62/0.63 vs 0.74/0.71) and DeepSTARR on Drosophila enhancer activity. Regression generally weaker than classification.
- **Regression as digit generation.** Scalars emitted as digit tokens under cross-entropy loss; autoregression imposes a hierarchical (most-significant-digit-first) decomposition, giving results comparable to MSE without needing a structured numeric output.
- **Calibrated confidence.** A perplexity-based classifier scores positive vs negative answer templates, converts to logits/probabilities, and is calibrated with a Platt model — recovering classifier-like uncertainty without changing the agent's text output (post-hoc, not yet integrated).
- **Interpretability.** Gradient⊙input attribution back through decoder→projection→encoder recovered known motifs — splice-donor **GT**, splice-acceptor **AG**, and the promoter **TATA** box — from the single unified model, showing biologically coherent features.

## Methods (brief)
End-to-end multimodal instruction tuning in JAX/Haiku: DNA encoder + Perceiver projection trained, English decoder frozen. Adam (lr 3e-5), batch 256 samples (65,536 tokens), uniform task sampling, 2B tokens (7.8M samples) on 8×H100 over 4 days. Tasks framed as text(+DNA)-to-text with positional tags (`@myseq.fna`) to interleave multiple sequences; train/test split on both sequences and question phrasings to test English generalization.

## Limitations
Encoder caps context at ~12 kb (2,048 tokens); regression underperforms classification and trails specialists (Saluki, DeepSTARR, AgroNT on plant enhancers); confidence calibration is post-hoc for binary tasks only; no mechanism yet to flag out-of-distribution queries or covered task/cell-type scope; proof-of-concept with no tool-calling or true agentic autonomy despite the "agent" framing.

## Citations of interest
- Dalla-Torre et al., *Nature Methods* 2025 — Nucleotide Transformer, the DNA encoder and benchmark backbone.
- Alayrac et al., NeurIPS 2022 — Flamingo Perceiver resampler, the projection architecture adapted here.
- Lin et al., *Science* 2023 — ESM2, protein-task baseline (fluorescence, stability, meltome).
- Linder et al., *Genome Biol.* 2022 — APARENT2, polyadenylation baseline (beaten by ChatNT).
- Agarwal & Kelley, *Genome Biol.* 2022 — Saluki, RNA-degradation baseline (beats ChatNT).
- de Almeida et al., *Nat. Genet.* 2022 — DeepSTARR, enhancer-activity baseline.
- Schick et al., NeurIPS 2023 — Toolformer, cited for future tool-augmented extensions.
