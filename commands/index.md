---
description: Index files or directories into the RAG memory system using Memvid
---

# index
Index file or directory.
We currently supports .pdf files only
Before indexing documents, check if index file(`knowledge.mv2`) exist.
if not, create index before put documents

**Usage**: `/memvid-rag:index <user_query>`

## Workflow

**IMPORTANT**: Before indexing, you MUST follow these steps:

### Step 1: Inspect PDF Content
First, use the Read tool to inspect the PDF file and understand its content:
- Read text data from the PDF file to extract key information
- Identify the document's title, main topic, and subject area
- Understand what the document is about

### Step 2: Determine Indexing Parameters
Based on the PDF content inspection, determine:
- `document_title`: A descriptive title for the document (e.g., "Agentic RAG Survey", "Machine Learning Guide")
- `document_label`: A category or label for classification (e.g., "AI Research", "Technical Documentation", "Survey Paper")
- `file_path`: The absolute path to the PDF file

### Step 3: Execute Indexing Script
Run the index script with the parameters determined from Step 2:

**Example**:
```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/index.py "Document Title" "Label" "file.pdf"
```

with optional parameters:
```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/index.py "Document Title" "Label" "file.pdf" --embedding_model=openai-large
```

## Requirements

### Vector Embeddings (REQUIRED)
**This system REQUIRES vector embeddings for semantic search.** The indexing script will fail if embeddings cannot be created.

### Supported Embedding Models

#### OpenAI (Default)
| Model ID | OpenAI Model | Dimensions | API Key |
|----------|-------------|------------|---------|
| `openai-small` | text-embedding-3-small | 1536 | `OPENAI_API_KEY` |
| `openai-large` | text-embedding-3-large | 3072 | `OPENAI_API_KEY` |
| `openai-ada` | text-embedding-ada-002 | 1536 | `OPENAI_API_KEY` (legacy) |

The default model is `openai-small`. To use a different model, pass `--embedding_model=<model_id>`.

### Why Vector Embeddings Are Required
Unlike lexical-only search (keyword matching), vector embeddings enable:
- **Semantic search**: Find documents by meaning, not just keywords
- **Context understanding**: Retrieve relevant information even with different wording
- **Better accuracy**: More precise results for complex queries

### Setting Up API Key
Before indexing, set the `OPENAI_API_KEY` environment variable:

**Windows (PowerShell)**:
```powershell
$env:OPENAI_API_KEY="your-api-key-here"
```

**Windows (Command Prompt)**:
```cmd
set OPENAI_API_KEY=your-api-key-here
```

**Linux/Mac**:
```bash
export OPENAI_API_KEY="your-api-key-here"
```
