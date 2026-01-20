---
description: Search from index
---

# search

Search documents from index file(*.mv2).

**Usage**: `/memvid-rag:search <question>`

Execute the search script with user's question:

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/search.py "$ARGUMENTS"
```

## Examples
- `/memvid-rag:search Why did we choose React?` - Search context about technology decisions
- `/memvid-rag:search What was the CORS solution?` - Recall specific solutions
- `/memvid-rag:search How did we fix the authentication bug?` - Get details about past fixes

you can pass arguments to modify search options:
- `/memvid-rag:search Why did we choose React? --k=5 --mode=sem` - Search context about technology decisions with top-k=5 documents in semantic search mode

## Response Format
- Provide documents based on stored memories
- Reference specific memories when applicable
- Include timestamps for referenced information
