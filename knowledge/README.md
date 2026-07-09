# precision-health-agents-kb

The persistent knowledge base for the precision-health-agents project. Follows the
[Karpathy LLM-wiki pattern](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f):
the LLM ingests sources and maintains an interlinked markdown wiki on top of
them, instead of re-deriving knowledge from raw sources on every query.

## Layout

```
precision-health-agents/kb/
├── raw/              # GITIGNORED (.gitkeep markers track structure)
│   ├── papers/
│   ├── notion/  slack/  web/  repos/  ...   # by provenance
├── notes/            # IN GIT — human drafts + ingest-queue.md
├── source/           # IN GIT — LLM-distilled .md, mirrors raw/ subtree
├── wiki/             # IN GIT — synthesis pages
│   ├── home.md
│   ├── index.md
│   ├── log.md        # append-only ops record
│   └── concepts/  findings/  business/  ...
├── tools/            # IN GIT — kb-specific lint scripts
├── kb-conventions.md # the operating contract
└── .claude/CLAUDE.md # routing rules for sessions started inside kb/
```

See [`kb-conventions.md`](kb-conventions.md) for the contract;
[`harness/docs/architecture.md`](../../harness/docs/architecture.md) for the
broader cb/kb/mb model.

## Search

Two qmd collections cover this kb:

| Collection | Indexes | Purpose |
|---|---|---|
| `precision-health-agents-kb` | `wiki/**/*.md` | Synthesis layer. Default first hit. |
| `precision-health-agents-kb-source` | `source/**/*.md` | Distilled summaries — cited evidence. |

Direct:
```bash
qmd query "<question>" -c precision-health-agents-kb        --top 5
qmd query "<question>" -c precision-health-agents-kb-source --top 5
```

Or use `/wiki-query` to run both in parallel.

## Common operations

```bash
/wiki-query <question>          # search the kb
/wiki-ingest <url-or-path>      # add a new source
/wiki-learn                      # promote conversation insights → wiki/findings/
/wiki-lint                       # health check — orphans, broken links, hash drift
```

## Conventions

- **`raw/` is gitignored.** Folder structure tracked via `.gitkeep`; file
  contents are local-only cache. Never `git add raw/`.
- **`source/` is regen-able.** Don't hand-edit; re-ingest if a distillation
  is wrong.
- **`notes/` is human-only.** Agents do not ghost-write personal drafts.
- **Heavy planning belongs in `mb/active/kb-<slug>.md`,** not here. kb is
  for content; mb is for workflow tracking.
- **Direct commits to main.** No branches or PRs by default. See
  `kb-conventions.md` for the rare exceptions.
