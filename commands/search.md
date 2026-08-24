---
description: Search from index
---

# search

Search documents from index file(*.mv2).

**Usage**: `/memvid-rag:search <question>`

Execute the search script with user's question:

```bash
uv run --project ${CLAUDE_PLUGIN_ROOT} ${CLAUDE_PLUGIN_ROOT}/scripts/search.py $ARGUMENTS
```

Note: `$ARGUMENTS` must NOT be quoted — the script treats `--key=value` words as options and joins the remaining words into the query. Quoting would turn options into literal query text.

## Examples
- `/memvid-rag:search Why did we choose React?` - Search context about technology decisions
- `/memvid-rag:search What was the CORS solution?` - Recall specific solutions
- `/memvid-rag:search How did we fix the authentication bug?` - Get details about past fixes

you can pass arguments to modify search options:
- `/memvid-rag:search Why did we choose React? --k=5 --mode=sem` - Search context about technology decisions with top-k=5 documents in semantic search mode
- `--file=<path>` - Search a custom index file (default: `knowledge.mv2`)
- `--query_embedding_model=<model_id>` - Must match the model used at index time (default: `openai-small`). Pass this if the documents were indexed with a different model (e.g. `openai-large`).

## Response Format
- Provide documents based on stored memories
- Reference specific memories when applicable
- Include timestamps for referenced information
