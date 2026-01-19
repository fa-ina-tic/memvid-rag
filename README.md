# Current On Development.

# Memvid RAG Plugin for Claude Code

A powerful local file-based RAG (Retrieval-Augmented Generation) plugin for Claude Code that enables intelligent indexing and querying of your project documents using:
- **Memvid** for portable vector storage
- **Unstructured** for wide file format support
- **Tiktoken** for token-based chunking
- **Claude embeddings** (or other providers) for semantic search

## Overview

This plugin transforms Claude Code into a knowledge-enhanced assistant that can:
- **Index** diverse file formats (50+ types via unstructured)
- **Query** indexed content with semantic and hybrid search
- **Answer questions** about your codebase with proper citations
- **Auto-index** files as you work (via hooks)
- **Chunk intelligently** using token-based segmentation
- **Persist knowledge** in a single portable `.mv2` file

## Key Features

### Wide File Format Support (via Unstructured)
- ✅ **Documents**: PDF, DOCX, DOC, RTF, ODT
- ✅ **Spreadsheets**: XLSX, XLS, CSV
- ✅ **Presentations**: PPTX, PPT
- ✅ **Code**: `.py`, `.js`, `.ts`, `.java`, `.cpp`, etc.
- ✅ **Markup**: HTML, XML, Markdown
- ✅ **Data**: JSON, YAML, TOML
- ✅ **Plain text**: TXT, LOG, and more
- 🔜 **Images**: Structure prepared for CLIP embeddings (Memvid v2.0)
- 🔜 **Audio**: Structure prepared for Whisper embeddings (Memvid v2.0)

### Token-Based Chunking (via Tiktoken)
- **Precise control**: Chunk by token count, not characters
- **Optimized for LLMs**: Respects model token limits
- **Smart boundaries**: Breaks at sentence endings when possible
- **Configurable overlap**: Maintains context between chunks
- **Encoding support**: cl100k_base (Claude, GPT-4), p50k_base, etc.

### Intelligent Search
- **Semantic search**: Find conceptually similar content using embeddings
- **Lexical search**: Exact keyword matching with BM25
- **Hybrid search**: Combines both approaches (recommended)
- **Ranked results**: Relevance scores for all matches

### Automatic Indexing
- Files are automatically indexed when you read/write/edit them
- Debounced to avoid excessive indexing
- Silent background operation
- Configurable file patterns

### Portable Knowledge Base
- Single `.mv2` file stores all indexed data
- No external database required
- Crash-safe with WAL (Write-Ahead Logging)
- Version control friendly

## Installation

### 1. Install Dependencies

```bash
uv pip install memvid-sdk unstructured tiktoken anthropic
```

The dependencies are already listed in `pyproject.toml`:
```toml
dependencies = [
    "memvid-sdk>=0.1.0",
    "unstructured>=0.12.0",
    "tiktoken>=0.5.0",
    "anthropic>=0.18.0",
]
```

### 2. Optional: Set API Key for Claude Embeddings

```bash
export ANTHROPIC_API_KEY="your-api-key-here"
```

Note: Claude embeddings are prepared but may use Memvid's default embeddings until custom embedding support is fully available.

### 3. Plugin Structure

The plugin is located at `.claude/plugins/memvid-rag/` with the following structure:

```
.claude/plugins/memvid-rag/
├── .claude-plugin/
│   └── plugin.json          # Plugin manifest
├── lib/
│   └── rag_core.py          # Core RAG functionality
├── commands/
│   ├── index.md             # Index command
│   ├── query.md             # Query command
│   ├── status.md            # Status command
│   └── clear.md             # Clear command
├── hooks/
│   ├── hooks.json           # Hook configuration
│   ├── pre_tool_use.py      # Auto-indexing hook
│   └── session_start.py     # Initialization hook
└── skills/
    └── rag-query/
        └── SKILL.md         # RAG query skill
```

### 4. Verify Installation

Restart your Claude Code session and run:

```bash
/memvid-rag:status
```

You should see a status message indicating the plugin is ready.

## Quick Start

### 1. Index Your Project

```bash
# Index entire project with default patterns
/memvid-rag:index .

# Index specific directory
/memvid-rag:index ./src

# Index only Python files
/memvid-rag:index . --pattern "*.py"

# Index multiple file types
/memvid-rag:index . --pattern "*.py,*.md,*.js,*.pdf,*.docx"
```

### 2. Query Your Knowledge Base

```bash
# Basic query with hybrid search
/memvid-rag:query "How does authentication work?"

# Semantic search for concepts
/memvid-rag:query "error handling patterns" --mode sem

# Get more results
/memvid-rag:query "database queries" --k 10
```

### 3. Use the RAG Skill

```bash
# Ask questions and get contextual answers
/memvid-rag:ask "What does main.py do?"

# Claude will automatically retrieve relevant context
/memvid-rag:ask "Where are the API endpoints defined?"
```

## Commands Reference

### `/memvid-rag:index`
Index files or directories into the RAG memory.

**Syntax:**
```bash
/memvid-rag:index <path> [--pattern "*.py,*.md"]
```

**Examples:**
```bash
/memvid-rag:index main.py                      # Index single file
/memvid-rag:index .                             # Index entire project
/memvid-rag:index ./docs --pattern "*.md,*.pdf" # Index docs only
```

**Features:**
- Supports 50+ file formats via unstructured
- Token-based chunking (512 tokens per chunk, 50 token overlap)
- Automatic metadata tracking
- File size limit: 50MB (configurable)

---

### `/memvid-rag:query`
Search indexed content with semantic/lexical/hybrid search.

**Syntax:**
```bash
/memvid-rag:query <question> [--k 5] [--mode sem|lex|hybrid]
```

**Examples:**
```bash
/memvid-rag:query "authentication implementation"
/memvid-rag:query "def process_data" --mode lex --k 10
```

**Search Modes:**
- `sem` (semantic): Conceptual similarity using embeddings
- `lex` (lexical): Exact keyword matching with BM25
- `hybrid`: Combines both (default, recommended)

---

### `/memvid-rag:status`
Show RAG system status and configuration.

**Syntax:**
```bash
/memvid-rag:status
```

**Output:**
- Database file size and location
- Number of indexed chunks
- Configuration (token limits, encoding, provider)
- List of indexed files

---

### `/memvid-rag:clear`
Clear the RAG index (delete and recreate .mv2 file).

**Syntax:**
```bash
/memvid-rag:clear [--confirm]
```

**Warning:** This permanently deletes all indexed content!

---

### `/memvid-rag:ask`
Intelligent RAG-powered Q&A skill.

**Syntax:**
```bash
/memvid-rag:ask <question>
```

**Features:**
- Automatically retrieves relevant context
- Synthesizes information across multiple sources
- Provides citations with file paths
- Handles complex questions

## Architecture

### Token-Based Chunking Flow

```
Document → Unstructured Parser → Raw Text → Tiktoken Encoder
                                                    ↓
                                             Token Array
                                                    ↓
                          ┌─────────────────────────┴─────────────────────────┐
                          ↓                                                   ↓
                   Chunk 1 (512 tokens)                            Chunk 2 (512 tokens)
                   with 50 token overlap                           with 50 token overlap
                          ↓                                                   ↓
                   Tiktoken Decoder                               Tiktoken Decoder
                          ↓                                                   ↓
                      Text Chunk                                        Text Chunk
                          ↓                                                   ↓
                   Memvid Storage ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ←
```

### Data Flow

```
User Files → Unstructured → Text Extraction → Tiktoken Chunking
                                                      ↓
                                               Memvid .mv2 Index
                                                      ↓
                                        Query Skill/Command → Claude Context
```

### Component Integration

```
┌──────────────────┐
│  Unstructured    │  Handles 50+ file formats
│  (Document       │  Extracts text, tables, structure
│   Processing)    │
└────────┬─────────┘
         │
         ↓
┌──────────────────┐
│   Tiktoken       │  Token-based chunking
│  (Chunking)      │  512 tokens/chunk, 50 overlap
└────────┬─────────┘
         │
         ↓
┌──────────────────┐
│    Memvid        │  Vector storage & search
│  (Storage &      │  Hybrid search (semantic + lexical)
│   Search)        │
└────────┬─────────┘
         │
         ↓
┌──────────────────┐
│  Claude API      │  Embeddings (future)
│  (Embeddings)    │  Currently using Memvid defaults
└──────────────────┘
```

## Configuration

### Default Settings

Located in `.claude/plugins/memvid-rag/.claude-plugin/plugin.json`:

```json
{
  "config": {
    "rag_file": "knowledge.mv2",
    "auto_index": true,
    "max_file_size_mb": 50,
    "max_tokens_per_chunk": 512,
    "chunk_overlap_tokens": 50,
    "embedding_provider": "claude",
    "embedding_model": "claude-3-5-sonnet-20241022",
    "tiktoken_encoding": "cl100k_base"
  }
}
```

### Customization Options

You can modify settings in `rag_core.py`:

```python
rag = RAGCore(
    db_path="knowledge.mv2",
    max_tokens_per_chunk=512,        # Adjust for your needs
    chunk_overlap_tokens=50,          # More overlap = better context
    tiktoken_encoding="cl100k_base",  # Claude/GPT-4 encoding
    embedding_provider="claude",      # Future: openai, cohere, etc.
    max_file_size_mb=50               # Larger files allowed
)
```

### Tiktoken Encodings

- `cl100k_base`: Claude, GPT-4, GPT-3.5-turbo (recommended)
- `p50k_base`: GPT-3 (Davinci, Curie)
- `r50k_base`: GPT-3 (Ada, Babbage)

## Use Cases

### 1. Multi-Format Documentation Search
```bash
# Index diverse documentation
/memvid-rag:index ./docs --pattern "*.pdf,*.docx,*.html,*.md"

# Query across all formats
/memvid-rag:ask "How do I configure authentication?"
```

### 2. Codebase Understanding
```bash
# Index entire codebase
/memvid-rag:index . --pattern "*.py,*.js,*.java"

# Ask architectural questions
/memvid-rag:ask "What are the main components?"
/memvid-rag:ask "How is error handling implemented?"
```

### 3. Research Paper Analysis
```bash
# Index research papers
/memvid-rag:index ./papers --pattern "*.pdf"

# Query specific topics
/memvid-rag:query "transformer architecture improvements" --k 10
```

### 4. Meeting Notes & Presentations
```bash
# Index meeting artifacts
/memvid-rag:index ./meetings --pattern "*.pptx,*.docx,*.txt"

# Find decisions and action items
/memvid-rag:query "action items from Q4 planning"
```

## Technical Details

### Token-Based Chunking Algorithm

1. **Encoding**: Text → Tokens using tiktoken
2. **Segmentation**: Split into chunks of max_tokens_per_chunk
3. **Overlap**: Last chunk_overlap_tokens carried forward
4. **Boundary Detection**: Break at sentence endings when possible
5. **Decoding**: Tokens → Text for storage

**Benefits:**
- Precise token control for LLM context windows
- Better than character-based chunking
- Respects semantic boundaries
- Optimized for embedding models

### Unstructured Processing

**Supported Elements:**
- Text blocks
- Tables (converted to text)
- Lists
- Headers
- Metadata

**Extraction Strategy:**
1. Automatic format detection
2. Element-wise parsing
3. Text aggregation
4. Metadata preservation

### Fallback Mechanisms

- **No Tiktoken**: Falls back to character-based chunking (2000 chars)
- **No Unstructured**: Falls back to simple text reading
- **No API Key**: Uses Memvid's default embeddings

## Performance Tips

1. **Optimize Chunk Size**:
   - Code: 256-512 tokens
   - Documentation: 512-1024 tokens
   - Books/Papers: 768-1536 tokens

2. **Use Appropriate Overlap**:
   - Short chunks: 25-50 tokens overlap
   - Long chunks: 50-100 tokens overlap

3. **Selective Indexing**:
   ```bash
   /memvid-rag:index ./src --pattern "*.py,*.js"  # Only code
   ```

4. **Hybrid Search for Best Results**:
   ```bash
   /memvid-rag:query "your question" --mode hybrid
   ```

## Troubleshooting

### Installation Issues

**Unstructured not installing:**
```bash
# Unstructured has many optional dependencies
# Install with specific formats
uv pip install "unstructured[pdf,docx]"
```

**Tiktoken encoding error:**
```python
# Use a different encoding
tiktoken_encoding="p50k_base"  # Instead of cl100k_base
```

### Runtime Issues

**Large files failing:**
- Increase `max_file_size_mb` in config
- Or split files manually

**Chunking too granular:**
- Increase `max_tokens_per_chunk` (e.g., 1024)
- Reduce `chunk_overlap_tokens`

**Poor search results:**
- Try different search modes (`--mode sem`, `--mode lex`)
- Increase result count (`--k 20`)
- Re-index with better chunk sizes

## Advanced Configuration

### Custom Embedding Providers

Future support for:
```python
# OpenAI embeddings
embedding_provider="openai"
embedding_model="text-embedding-3-large"

# Cohere embeddings
embedding_provider="cohere"
embedding_model="embed-english-v3.0"
```

### Custom File Patterns

Edit hooks configuration:
```json
{
  "config": {
    "index_patterns": ["*.py", "*.rs", "*.go", "*.pdf", "*.docx"]
  }
}
```

## Comparison with Other Approaches

### vs. Character-Based Chunking
✅ More precise control
✅ Better for LLM compatibility
✅ Respects token limits
❌ Requires tiktoken dependency

### vs. PyPDF2/PyMuPDF
✅ Supports 50+ formats (not just PDF)
✅ Better table extraction
✅ Unified API for all formats
❌ Larger dependency footprint

### vs. Simple Text Splitting
✅ Token-aware boundaries
✅ Configurable overlap
✅ Semantic boundary detection
❌ More computational overhead

## Future Enhancements

- [ ] Custom Claude embeddings (when API available)
- [ ] Image indexing with CLIP (Memvid v2.0)
- [ ] Audio transcription and indexing (Memvid v2.0)
- [ ] Incremental updates (detect changed files)
- [ ] Multi-language support
- [ ] Graph-based relationships
- [ ] Advanced metadata filtering

## Dependencies

- **memvid-sdk** (>=0.1.0): Core RAG functionality
- **unstructured** (>=0.12.0): Multi-format document processing
- **tiktoken** (>=0.5.0): Token-based chunking
- **anthropic** (>=0.18.0): Claude API client (for future embeddings)

## References

- [Memvid Documentation](https://docs.memvid.com)
- [Memvid GitHub](https://github.com/memvid/memvid)
- [Unstructured Documentation](https://unstructured-io.github.io/unstructured/)
- [Tiktoken GitHub](https://github.com/openai/tiktoken)
- [Claude Code Documentation](https://code.claude.com/docs)

## License

This is a sample project for demonstration purposes.

---

## Example Session

```bash
# Install dependencies
$ uv pip install memvid-sdk unstructured tiktoken anthropic

# Start indexing
$ /memvid-rag:index .
Found 32 files to index...
✓ Indexed: main.py (4 chunks)
✓ Indexed: README.md (12 chunks)
✓ Indexed: docs/api.pdf (25 chunks)
✓ Indexed: presentation.pptx (18 chunks)
...
==================================================
Indexing Summary:
  ✓ Indexed: 32 files
  ✗ Failed: 0 files
  ⊘ Skipped: 8 files
==================================================

# Check status
$ /memvid-rag:status
======================================================================
Memvid RAG Status
======================================================================

Database: knowledge.mv2
  Location: /project/knowledge.mv2
  Exists: Yes
  Size: 5.23 MB
  Last Modified: 2026-01-19T14:30:45

Initialized: Yes
Indexed Chunks: 487

Configuration:
  Max Tokens/Chunk: 512
  Chunk Overlap: 50 tokens
  Encoding: cl100k_base
  Embedding Provider: claude

Indexed Files (32):
  1. ./main.py
  2. ./README.md
  3. ./docs/api.pdf
  4. ./docs/presentation.pptx
  ...

======================================================================

# Ask a question
$ /memvid-rag:ask "How does the application handle errors?"

Searching for: "How does the application handle errors?"

======================================================================
Retrieved Context:
======================================================================

Source 1 (relevance: 0.892):
  File: ./lib/error_handler.py
  Chunk: 0

  class ErrorHandler:
      """Centralized error handling for the application.

      Uses a decorator pattern to catch and log errors,
      with support for custom error types and retry logic."""
      ...

----------------------------------------------------------------------
Source 2 (relevance: 0.845):
  File: ./docs/architecture.pdf
  Chunk: 12

  Error Handling Architecture

  The application uses a multi-tiered error handling approach:
  1. Try-catch blocks at the controller level
  2. Global exception middleware
  3. Centralized error logging service
  ...

======================================================================

Based on the retrieved context, the application uses a centralized
error handling system implemented in ./lib/error_handler.py. The
architecture follows a multi-tiered approach with try-catch blocks,
middleware, and logging services as documented in ./docs/architecture.pdf.

[Full synthesized answer with citations...]
```

---

**Enhanced RAG with wide format support and token-based chunking! 🚀**
