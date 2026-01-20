# memvid-rag

A simple local RAG (Retrieval-Augmented Generation) plugin for Claude Code, built on [memvid-sdk](https://github.com/Olow304/memvid-sdk).

## Overview

memvid-rag enables semantic search capabilities for your local documents directly within Claude Code. Index PDF files into a local knowledge base and perform natural language queries to retrieve relevant information.

## Features

- **Local Storage**: All data stored in a single `knowledge.mv2` file
- **Hybrid Search**: Combines lexical and semantic search for better results
- **PDF Support**: Index PDF documents with automatic text extraction
- **Vector Embeddings**: Semantic search powered by Cohere embeddings

## Requirements

- Python 3.8+
- memvid-sdk: `pip install memvid-sdk`
- Cohere API Key (for vector embeddings)

## Setup

1. Install dependencies:
   ```bash
   pip install memvid-sdk
   ```

2. Set your Cohere API key:
   ```bash
   # Linux/Mac
   export COHERE_API_KEY="your-api-key-here"

   # Windows PowerShell
   $env:COHERE_API_KEY="your-api-key-here"

   # Windows CMD
   set COHERE_API_KEY=your-api-key-here
   ```

## Usage

### Commands

| Command | Description |
|---------|-------------|
| `/memvid-rag:create` | Create a new index file |
| `/memvid-rag:index <path>` | Index a PDF file |
| `/memvid-rag:search <query>` | Search indexed documents |
| `/memvid-rag:status` | Show system status |

### Examples

```bash
# Create index (if not exists)
/memvid-rag:create

# Index a PDF document
/memvid-rag:index ./documents/research-paper.pdf

# Search your knowledge base
/memvid-rag:search What are the key findings?

# Search with options
/memvid-rag:search How does it work? --k=10 --mode=sem
```

### Search Options

| Option | Description | Default |
|--------|-------------|---------|
| `--k` | Maximum results to return | 5 |
| `--mode` | Search mode: `lex`, `sem`, `hybrid` | hybrid |
| `--snippet_chars` | Max characters per snippet | 240 |
| `--min_relevancy` | Minimum relevancy threshold | 0.0 |
| `--adaptive` | Enable adaptive result count | false |

## Project Structure

```
memvid-rag/
├── .claude-plugin/
│   └── plugin.json       # Plugin metadata
├── commands/
│   ├── create.md         # Create index command
│   ├── index.md          # Index documents command
│   ├── search.md         # Search command
│   └── status.md         # Status command
├── scripts/
│   ├── index.py          # Indexing script
│   └── search.py         # Search script
└── skills/
    └── SKILL.md          # Skill documentation
```

## How It Works

1. **Indexing**: PDF documents are processed, text is extracted, and vector embeddings are generated using Cohere's `embed-v4.0` model
2. **Storage**: Documents are stored in a compressed `knowledge.mv2` file with lexical, vector, and time indexes
3. **Search**: Queries use hybrid search combining keyword matching (lexical) and semantic similarity (vector) for optimal results

## License

MIT

## Author

Soomin Lee ([@fa-ina-tic](https://github.com/fa-ina-tic))
