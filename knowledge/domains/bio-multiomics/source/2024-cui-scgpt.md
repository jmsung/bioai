<!-- synced from knowledge-base — do not edit here; change upstream and re-pull -->
---
type: source
kind: paper
confidentiality: public
visibility: global
primary: bio-multiomics
domains: [bio-multiomics]
title: "scGPT: toward building a foundation model for single-cell multi-omics using generative AI"
authors: [Haotian Cui, Chloe Wang, Hassaan Maan, Kuan Pang, Fengning Luo, Nan Duan, Bo Wang]
year: 2024
doi: 10.1038/s41592-024-02201-0
source_url: https://www.nature.com/articles/s41592-024-02201-0
drive_file_id: TODO
text_source: paperclip
ingested_by: agent
---

# scGPT: toward building a foundation model for single-cell multi-omics using generative AI

## TL;DR
scGPT is a generative-pretrained transformer trained on >33M human cells that learns joint gene and cell embeddings; fine-tuned, it sets state-of-the-art on cell-type annotation, perturbation-response prediction, batch correction, multi-omic integration and gene-network inference, exhibiting an LLM-style data-scaling effect.

## Key findings
- **Pretraining scale & architecture.** 33M normal human cells from CELLxGENE (51 organs/tissues, 441 studies); 12 transformer blocks, 8 heads, embedding dim 512, max input 1,200 non-zero genes. Genes are tokenized like words; expression is value-binned per cell into B relative bins to neutralize cross-batch scale differences.
- **Novel generative attention mask.** Because genes are non-sequential, the authors invented an attention mask that allows attention only between "known" genes and the query gene, predicting unknown-gene expression iteratively (top 1/K most-confident genes promoted to "known" each of K steps). Supports both "gene-prompt" and "cell-prompt" generation — one of the first autoregressive schemes for non-sequential data.
- **Cell-type annotation.** Beat transformer baselines TOSICA and scBERT on accuracy, precision, recall and macro-F1 across human pancreas, multiple sclerosis (~0.85 accuracy on held-out MS query) and tumor-infiltrating myeloid datasets; high precision (>0.8) for most types except rare ones (<50 cells in reference).
- **Perturbation prediction (Perturb-seq).** On Adamson (87 1-gene), Replogle (1,823 1-gene) and Norman (131 2-gene + 105 1-gene) datasets, scGPT beat GEARS and linear regression on Pearson_delta by 5–20% margins. **Reverse perturbation**: fine-tuned on 39/210 (18%) combos, it retrieved the correct source perturbation on average 91.4% within top-1 (relevant) and 65.7% correct within top-8 — vs ~105.5 random tryouts needed.
- **Integration.** Multi-batch scRNA-seq (PBMC 10k AvgBIO 0.821, 5–10% over scVI/Seurat/Harmony) and multi-omic (10x Multiome RNA+ATAC; BMMC RNA+protein, +9% AvgBIO over Seurat v4; ASAP mosaic RNA/ATAC/protein over scMoMaT). Modality/batch tokens are concatenated post-transformer to drive batch correction.
- **Gene networks.** Zero-shot gene embeddings recovered HLA class I vs II clusters and CD3/CD79/CD8 functional groups. Gene programs from scGPT yielded substantially more Reactome pathway hits than coexpression (15 shared + 22 unique, 14 immune-related). Attention maps validated against ChIP-Atlas: 20/20 (DDIT3) and 19/20 (BHLHE40) top-influenced genes were known TF targets.
- **Scaling law.** Fine-tuned performance rose monotonically with pretraining data (30k→33M cells), mirroring NLG scaling laws. Context-matched pretraining helped (blood model beat brain model on COVID-19 by 8% at similar size), but whole-human was the versatile default.

## Methods (brief)
Self-supervised generative pretraining with a masked-attention transformer (FlashAttention) over value-binned expression; gene-expression-prediction MSE loss. Fine-tuning objectives: GEP, GEP-for-cell-modeling (GEPC), elastic cell similarity (ECS), domain-adaptation reverse backprop (DAR) and cross-entropy cell-type classification. Implemented in PyTorch/Scanpy; metrics via scib.

## Limitations
Pretraining does not inherently remove batch effects, so zero-shot performance degrades on data with strong technical variation. Evaluation is hard given absent biological ground truth and variable data quality. Several benchmark datasets were subsampled (e.g., COVID-19 to 20k cells); rare cell types remain poorly annotated.

## Citations of interest
- Theodoris et al. 2023 (Geneformer) — prior transformer trained on expression-ranked genes for network biology; scGPT's closest precedent.
- Yang et al. 2022 (scBERT) & Chen et al. 2023 (TOSICA) — transformer annotation baselines scGPT outperforms.
- Roohani et al. 2023 (GEARS) — perturbation-prediction baseline.
- Vaswani et al. 2017 (Attention is all you need) & Dao et al. 2022 (FlashAttention) — core architecture and efficient attention.
- Kaplan et al. 2020 (scaling laws) — the NLG result scGPT's data-scaling effect mirrors.
- Cao & Gao 2022 (scGLUE), Zhang et al. 2023 (scMoMaT) — multi-omic integration baselines.
