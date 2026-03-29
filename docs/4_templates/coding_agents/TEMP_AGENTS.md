# AGENTS.md

## Scope
This file defines cross-agent working agreements for this repository.

- Applies to: [whole repository / specific directory]
- Primary audience: coding agents and human maintainers
- Out of scope: personal preferences, IDE/editor settings, local machine quirks

## Project Context
- Project name: [name]
- Goal: [what this repository does]
- Main users / consumers: [internal team / customers / service]
- Critical flows:
  - [flow 1]
  - [flow 2]
- Non-goals:
  - [non-goal 1]

## Architecture Snapshot
- Languages / frameworks: [e.g. TypeScript, Go, Python]
- Build system / package manager: [e.g. pnpm, npm, poetry, make]
- Runtime(s): [e.g. node, docker, k8s]
- Key directories:
  - `src/` — [purpose]
  - `tests/` — [purpose]
  - `docs/` — [purpose]
  - `scripts/` — [purpose]

## Source of Truth
Read these first before making non-trivial changes:
- `README.md`
- `[architecture doc path]`
- `[api spec path]`
- `[domain glossary path]`

## Standard Commands
Agents may rely on these commands unless the task says otherwise:
- Install: `[...]`
- Dev: `[...]`
- Lint: `[...]`
- Typecheck: `[...]`
- Unit tests: `[...]`
- Integration tests: `[...]`
- Build: `[...]`

## Working Agreements
- Prefer minimal, local changes over broad refactors.
- Preserve public APIs unless the task explicitly requires breaking changes.
- Do not introduce new dependencies without justification in the final summary.
- Update tests when behavior changes.
- Update docs when user-facing or developer-facing behavior changes.
- Keep diffs reviewable and avoid unrelated cleanup.

## Code Standards
- Naming conventions: [rules]
- Error handling: [rules]
- Logging / observability: [rules]
- Comments / docstrings: [rules]
- Configuration style: [rules]
- API / schema evolution rules: [rules]

## Validation Before Completion
Before reporting completion:
- Run the narrowest sufficient checks first.
- Required checks:
  - `[...]`
  - `[...]`
- If a check cannot be run locally, state that explicitly.
- If changes are risky, explain residual risk.

## Safety & Boundaries
- Never touch without explicit approval:
  - `[sensitive path 1]`
  - `[sensitive path 2]`
- Treat as sensitive:
  - `.env*`
  - secrets / credentials / tokens
  - production configuration
- Destructive commands require: [explicit approval / are forbidden]
- Network access policy: [allowed / restricted / forbidden]
- Data handling constraints: [PII, compliance, tenant isolation, etc.]

## Deliverable Format
When finishing work:
- Summarize what changed and why.
- List files changed.
- List validation performed.
- List assumptions, open questions, and follow-ups.

## Local Overrides
More specific directories may define additional instruction files closer to the work area.
Use the most local guidance that applies.

