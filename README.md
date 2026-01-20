# Memvid RAG

Agent Skills for local RAG (Retrieval-Augmented Generation) using [memvid-sdk](https://github.com/memvid/memvid).

These skills follow the [Agent Skills](https://agent-skills.pages.dev/) specification so they can be used by any skills-compatible agent, including [Claude Code](https://docs.anthropic.com/en/docs/claude-code) and [Codex CLI](https://github.com/openai/codex).

## Installation

### Marketplace (Recommended)

Install via Claude Code plugin marketplace:

```
/plugin marketplace add fa-ina-tic/memvid-rag
/plugin install memvid-rag@memvid-rag-skills
```

### Claude Code (Manual)

Place the contents of this repository in a `/.claude` folder at your project root. See the [Claude Skills documentation](https://docs.anthropic.com/en/docs/claude-code/skills) for details.

### Codex CLI

Copy the `skills/` directory to `~/.codex/skills` following the [Agent Skills specification](https://agent-skills.pages.dev/).

## Requirements

- **Python 3.8+**
- **memvid-sdk**: Install with `pip install memvid-sdk`
- **API Key** (for cloud embeddings): Set one of the following environment variables:
  - `COHERE_API_KEY` - Cohere (default)
  - `OPENAI_API_KEY` - OpenAI
  - `VOYAGE_API_KEY` - Voyage AI
  - `NVIDIA_API_KEY` - NVIDIA

## Skills

This plugin enables semantic search over PDF documents:

| Command | Description |
|---------|-------------|
| `/memvid-rag:create` | Create a new `knowledge.mv2` index file |
| `/memvid-rag:index` | Index PDF documents with vector embeddings |
| `/memvid-rag:search` | Search indexed documents semantically |
| `/memvid-rag:status` | Show RAG system statistics |

## Usage

### 1. Create Index

Initialize a new knowledge base:

```
/memvid-rag:create
```

### 2. Index Documents

Add PDF documents to the knowledge base:

```
/memvid-rag:index ./documents/research-paper.pdf
```

### 3. Search

Query your indexed documents:

```
/memvid-rag:search What are the key findings?
/memvid-rag:search How does the algorithm work? --k=10 --mode=sem
```

### Search Options

- `--k=<number>` - Maximum results (default: 5)
- `--mode=<lex|sem|hybrid>` - Search mode (default: hybrid)
- `--snippet_chars=<number>` - Max characters per snippet (default: 240)
- `--min_relevancy=<float>` - Minimum relevancy threshold
- `--adaptive=<true|false>` - Enable adaptive result count

## Data Storage

All indexed data is stored locally in a `knowledge.mv2` file in your working directory.

## License

MIT
