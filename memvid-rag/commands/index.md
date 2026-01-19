---
description: Index files or directories into the RAG memory system using Memvid
---

# index
Index file or directory.
We currently supports only .pdf files
Before indexing documents, check if index file(`knowledge.mv2`) exist.
if not, create index before put documents

## Semantic search
We currently uses semantic search for multimodality.
Embedding model would be `embed-v4.0` from cohere(Requires `COHERE_API_KEY` be setted).

## How to
You first have to inspect the pdf file and get title and label to use.
and then put document using below python script
```python
import os
from memvid_sdk import use

with use("basic", "knowledge.mv2", mode="auto", read_only=False) as mv:
    mv.put(
        title=document_title,
        label=document_label,
        metadata={'source':file_path},
        file=file_path,
        embedding='embed-v4.0'
    )
```
