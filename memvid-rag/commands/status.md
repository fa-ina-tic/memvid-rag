---
description: Show the current status of the RAG system
---

# status

Show the current status of the RAG system.

## Python Script

```python
import os
from memvid_sdk import use

with use("basic", "knowledge.mv2", mode="open", read_only=True) as mv:
    stats = mv.stats()
    for k, v in stats.items():
        print(f"{k} : {v}")
```
