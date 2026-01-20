---
description: Index files or directories into the RAG memory system using Memvid
---

# index
Index file or directory.
We currently supports .pdf files only
Before indexing documents, check if index file(`knowledge.mv2`) exist.
if not, create index before put documents

**Usage**: `/memvid-rag:index <document_title> <document_label> <file_path>`

Execute the index script with user's question.
You first have to inspect the pdf file and get title and label to run:

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/index.py "$ARGUMENTS"
```

## Requirements
We currently uses semantic search for multimodality.
Default embedding model would be `embed-v4.0` from cohere(Requires `COHERE_API_KEY` be setted).

## Response Format
- Provide which file has indexed and how many documents has been added
- Include timestamps for referenced information
