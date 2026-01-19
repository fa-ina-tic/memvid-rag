---
description: Search from index
---

# search

Search documents from index file(*.mv2).
Clear

## Python Script
```python
import os
from memvid_sdk import use

with use("basic", "knowledge.mv2", mode="auto", read_only=False) as mv:
    mv.ask(
        title="Contract Summary",
        label="legal",
        text=""
    )
```