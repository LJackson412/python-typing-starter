## Rules
- Make the smallest correct change.
- Follow existing patterns in the touched files.
- Do not change unrelated code.

## Python
- Code must pass `mypy --strict`.
- Use `ruff` for linting.
- Use `black` for formatting.
- Add type annotations to new public code.
- Use Google-style docstrings for public classes and functions.

## Verification
Before finishing, run:

```bash
ruff check .
black --check .
mypy --strict .
```