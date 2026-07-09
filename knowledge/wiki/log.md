---
type: ops-log
author: agent
---

# Log

Append-only chronological record of kb activity — ingests, lint passes,
synthesis events, contract changes. Each entry starts with `## [YYYY-MM-DD]`
so the log is parseable with simple shell tools:

```bash
grep '^## \[' wiki/log.md | tail -10
```

Format:

```
## [YYYY-MM-DD] <event-type> | <one-line summary>
- <detail line>
- <detail line>
```

Event types: `ingest`, `synth`, `lint`, `contract`, `setup`, `note`.

---

## [2026-05-09] setup | kb scaffolded from harness/templates/kb/

- Layout created: raw/ (gitignored), notes/, source/, wiki/, tools/.
- Front-door files: `wiki/home.md`, `wiki/index.md`, `wiki/log.md`.
- Operating contract: `kb-conventions.md`.
- Routing rules for sessions inside kb/: `.claude/CLAUDE.md`.
