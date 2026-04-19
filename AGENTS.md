## Rules
- Make the smallest correct change.
- Follow existing patterns in the touched files.
- Do not change unrelated code.

## Python
- Add type annotations to new public code.
- Use Google-style docstrings for public classes and functions.

### Statische Analyse und Formatierung -  Ablauf vor einem Commit

```bash
black src/ tests/ && ruff check src/ tests/ --fix && mypy src/ tests/
```

```cmd
python -m black src/ tests/
python -m ruff check src/ tests/ --fix
python -m mypy src/
```