@AGENTS.md

<!--
Maintainer note:
Keep this file short. Put stable topic-specific Claude guidance into .claude/rules/.
Put repeatable workflows into .claude/skills/.
Use hooks/settings for enforcement, not prose here.
-->


## Claude Code Entry Points
Use these files as first references for repository context:
- Project overview: @README.md
- Architecture: @[docs/architecture.md]
- Commands / scripts: @[package.json]
- Additional reference: @[docs/developer-guide.md]

## Claude-Specific Operating Model

### Plan Mode
Use plan-first behavior for:
- changes spanning more than [N] files
- schema / migration / infra changes
- security-sensitive work
- refactors with unclear blast radius

For small, low-risk edits, proceed directly with implementation.

### Permission Expectations
- Preferred mode: [Ask permissions / Auto accept edits]
- Never use bypass-permissions unless inside: [sandbox / CI container / VM]
- Ask before running:
  - destructive shell commands
  - data migrations
  - deployment commands
  - anything that touches production credentials or infrastructure

### Verification Strategy
After edits:
1. Run the narrowest useful check first.
2. Then run broader checks only if needed.
3. If verification is skipped, say why.

Preferred order:
- targeted test: `[...]`
- typecheck/lint: `[...]`
- broader suite/build: `[...]`

## Claude-Specific Structure

### Rules
Persistent Claude-specific guidance belongs in `.claude/rules/`.

Suggested rule files:
- `.claude/rules/testing.md`
- `.claude/rules/api-design.md`
- `.claude/rules/security.md`

Use path-scoped rules for areas such as:
- `src/api/**`
- `infra/**`
- `migrations/**`

### Skills
Use `.claude/skills/*/SKILL.md` for repeatable workflows that should load on demand.

Suggested skills:
- release-prep
- incident-triage
- code-review
- migration-checklist

### Hooks
Automated guardrails belong in hooks, not in prose.
Examples:
- block destructive commands
- run formatter / lint checks
- notify on risky file edits

### Subagents
Use specialized subagents only where they reduce context load or improve reliability.

Suggested subagents:
- reviewer — reviews diffs for bugs and regressions
- tester — runs and interprets validation steps
- migration-specialist — handles schema/data migrations

## Repo-Specific Claude Reminders
- High-risk paths:
  - `[path]`
  - `[path]`
- Generated files:
  - `[path]`
- Slow tests / expensive commands:
  - `[command]`
- Files that should usually be read before editing:
  - `@[path]`
  - `@[path]`

## Noise Control
Avoid spending time in these paths unless the task explicitly requires it:
- `[dist/]`
- `[vendor/]`
- `[coverage/]`
- `[generated/]`

## Human Maintainer Notes
<!--
Use HTML comments for maintainer-only notes.
Example:
- why a rule exists
- when to delete a temporary workaround
- link to an internal discussion
-->