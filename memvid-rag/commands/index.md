---
description: Index files or directories into the RAG memory system using Memvid
---

# index

Index file or directory. Use .venv if it exist on project directory
It is currently under development, so you have to run below python script only.
DO NOT RUN ANTHING EXECPT BELOW PYTHON SCRIPT!

## Python Script
```python
import os
from memvid_sdk import use

with use("basic", "knowledge.mv2", mode="auto", read_only=False) as mv:
    mv.put(
        title="Contract Summary",
        label="legal",
        text="Key terms: 2-year agreement, auto-renewal clause."
    )
```
