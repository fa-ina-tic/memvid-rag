# Claude Code Context

A Claude Code plugin providing local RAG (Retrieval-Augmented Generation) capabilities using memvid-sdk.

## Project Structure

```
.
├── .claude-plugin/
│   └── plugin.json       # Plugin metadata
├── commands/             # Slash command definitions
│   ├── create.md         # /memvid-rag:create - Create index file
│   ├── index.md          # /memvid-rag:index - Index documents
│   ├── search.md         # /memvid-rag:search - Search indexed documents
│   └── status.md         # /memvid-rag:status - Show system status
├── scripts/              # Python scripts for indexing and search
│   ├── index.py          # Document indexing with embeddings
│   └── search.py         # Semantic/hybrid search
└── skills/
    └── SKILL.md          # Main skill documentation
```

## Technology Stack

- **Python**: Runtime for memvid-sdk scripts
- **memvid-sdk**: Core library for document indexing and semantic search
- **Vector Embeddings**: Supports multiple providers (OpenAI, Cohere, Voyage AI, NVIDIA, local models)

## Key Commands

| Command | Description |
|---------|-------------|
| `/memvid-rag:create` | Initialize `knowledge.mv2` index file |
| `/memvid-rag:index <path>` | Index PDF documents with vector embeddings |
| `/memvid-rag:search <query>` | Semantic search across indexed documents |
| `/memvid-rag:status` | Display RAG system statistics |

## Development Notes

- Index file is stored as `knowledge.mv2` in the working directory
- Currently supports PDF files only
- Requires API key for cloud embedding providers (set via environment variable)
- Default embedding model: `embed-v4.0` (Cohere)

## Environment Variables

- `COHERE_API_KEY` - Cohere embeddings
- `OPENAI_API_KEY` - OpenAI embeddings
- `VOYAGE_API_KEY` - Voyage AI embeddings
- `NVIDIA_API_KEY` - NVIDIA embeddings
