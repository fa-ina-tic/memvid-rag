---
description: Create Index to Use
---

# create
Create `knowledge.mv2` file if it does not exist.

```bash
uv run --project ${CLAUDE_PLUGIN_ROOT} ${CLAUDE_PLUGIN_ROOT}/scripts/create.py
```

Optionally specify a custom filename:
```bash
uv run --project ${CLAUDE_PLUGIN_ROOT} ${CLAUDE_PLUGIN_ROOT}/scripts/create.py "custom_name.mv2"
```
