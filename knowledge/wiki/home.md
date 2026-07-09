---
type: front-door
author: human
---

# precision-health-agents — kb

A living knowledge base for the precision-health-agents project. Persistent memory; the
agent's context across sessions; your library across tasks.

## Where to start

- **Got a question?** Use `/wiki-query <question>` (or just ask in plain English
  — the agent routes domain questions through qmd automatically). Hit `index.md`
  to browse the catalog.
- **Adding a paper or doc?** `/wiki-ingest <url-or-path>` — one approval gate
  covers the batch.
- **Planning a multi-step kb effort?** Don't put the plan here — create
  `mb/active/kb-<slug>.md` instead. kb is for content; mb is for workflow tracking.

## Layers

- `wiki/` — synthesis pages (you are here). Hand- or agent-curated.
- `source/` — distilled markdown, one file per ingested artifact. The cited
  ground truth.
- `notes/` — drafts, jots, structural sketches. Human-only; agents do not
  ghost-write here.
- `raw/` — full-text originals (gitignored, local cache). Re-fetchable from
  `source_url` in the matching `source/` frontmatter.

See [`../kb-conventions.md`](../kb-conventions.md) for the full contract.

## Recent activity

See [`log.md`](log.md) for chronological ingests, lint passes, and synthesis events.
