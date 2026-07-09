# kb conventions

The architectural contract for this kb. The bigger picture (cb/kb/mb buckets,
visibility, archetypes, git mechanics) lives at
[`harness/docs/architecture.md`](../../docs/architecture.md). This file is the
project-facing summary of *kb-specific* operating rules.

## Layout (4 layers)

```
precision-health-agents/kb/
  raw/      # GITIGNORED — full-text originals (PDF/HTML/etc.). Local cache.
  notes/    # IN GIT — human-only drafts (jots, structural sketches)
            #          + lightweight ingest-queue.md
  source/   # IN GIT — LLM-distilled .md per raw artifact (regen-able)
  wiki/     # IN GIT — synthesized, hand-curated pages (the usable output)
    home.md       # narrative front door
    index.md      # catalog (agent-maintained)
    log.md        # append-only ops record
    ...
  tools/    # IN GIT — kb-specific lint scripts (template-owned, synced from harness)
```

`raw/` and `source/` are organized by **provenance** (papers, notion, slack,
web, repos, talks, docs, agent_runs), not topic. Topic routing happens in
`wiki/`. Mirror the project's source-of-truth folder structure (e.g., shared
Drive layout) so files dropped at the source land in the matching local folder.

## Layer ownership

| Layer | Who writes | Regen-able | Notes |
|---|---|---|---|
| `raw/` | `/wiki-ingest` only, with explicit per-artifact approval | yes (re-fetch from `source_url`) | Never `git add`. Folder structure tracked via `.gitkeep`. |
| `notes/` | **human only** | no | Agent does not ghost-write personal drafts. |
| `source/` | `/wiki-ingest` only | yes (re-distill from `raw/`) | Don't hand-edit; fix the distillation template or re-ingest. |
| `wiki/` | human or `/wiki-learn` | no | The cited synthesis layer. |
| `wiki/log.md` | both, append-only | no | Every ingest / promotion / lint records an entry. |

## Operating rules

1. **Human gates ingest.** `/wiki-ingest` never writes `raw/` or `source/`
   without explicit per-artifact approval. Bulk mode: one approval covers
   the batch; the gate is never skipped.
2. **`source/` is regen-able.** If a distillation is wrong, fix the
   distillation template or the underlying `raw/`, then re-ingest. Don't
   patch `source/` in place.
3. **`notes/` is human-only.** Agents do not write personal drafts.
   Promotion to `wiki/` is manual or via `/wiki-learn`.
4. **`wiki/log.md` is append-only.** Every ingest, promotion, and lint pass
   records an entry. Format:
   ```
   ## [YYYY-MM-DD] <event-type> | <one-line summary>
   - <detail>
   ```
   Event types: `ingest`, `synth`, `lint`, `contract`, `setup`, `note`.
5. **For repos: README only, never clone.** Code is not kb-relevant; only
   the README's narrative goes in `source/`.
6. **Search defaults to this kb.** Web search is opt-in via explicit phrasing
   ("search the web", "look online"). See `.claude/CLAUDE.md` for the routing.

## qmd collections

Two qmd collections cover this kb:

| Collection | Indexes | Purpose |
|---|---|---|
| `precision-health-agents-kb` | `wiki/**/*.md` | Synthesis layer. Default first hit. |
| `precision-health-agents-kb-source` | `source/**/*.md` | Distilled summaries — cited evidence. |

Direct CLI:

```bash
qmd query "<question>" -c precision-health-agents-kb        --top 5
qmd query "<question>" -c precision-health-agents-kb-source --top 5
```

Or use `/wiki-query` to run both in parallel and merge.

## Workflow

- **Direct commits to main.** kb stays on main of its git (umbrella when
  `kb: private`; kb-git when `kb: shared`). No branches, no PRs by default.
- **Multi-step planning lives in mb.** A plan with goals/todos/progress
  ("ingest 5 papers → distill each → synthesize a findings page") goes to
  `mb/active/kb-<slug>.md`, not here. The lightweight `notes/ingest-queue.md`
  is for one-line artifact references; richer planning is workflow tracking.
- **Exceptions** where you might want a branch+PR (rare): bulk reorg of
  `wiki/`, experimental structural changes, team-contributor PRs on a
  shared kb-git. Default = direct to main.

## Frontmatter conventions

- **No `created:` / `updated:`** — git tracks that.
- For ingested artifacts (`source/<type>/<slug>.md`): `title`, `author`,
  `source_url`, `retrieved`, `distilled_at`, `distilled_from_hash`.
- For wiki pages: `type` (front-door, catalog, ops-log, synthesis, etc.),
  `author` (human / agent / both).

## Filename conventions

Lowercase-kebab. By artifact type:
- `papers` → `<year>-<firstAuthor>-<slug>`
- `programs` → `<YYYY-MM-DD>-<slug>`
- `slides` → `<YYYY-MM-DD>-<speaker-or-author>-<slug>`
- `notion` / `slack` → `<YYYY-MM-DD>-<thread-or-channel>-<slug>`
- `web` / `blog` → `<YYYY-MM-DD>-<author-or-domain>-<slug>`
- `gist` → `<author>-<slug>`
- `repos` → `<owner>-<repo>` (README only, no clone)
