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
python ${CLAUDE_PLUGIN_ROOT}/scripts/index.py "Document Title" "Label" "file.pdf" --k=10 --mode=semantic
```

## Requirements

### Vector Embeddings (REQUIRED)
**This system REQUIRES vector embeddings for semantic search.** The indexing script will fail if embeddings cannot be created.

- **Embedding Model**: `embed-v4.0` from Cohere (default)
- **API Key**: `COHERE_API_KEY` environment variable **MUST be set**
- **Validation**: The script automatically verifies that vector embeddings were successfully created

### Why Vector Embeddings Are Required
Unlike lexical-only search (keyword matching), vector embeddings enable:
- **Semantic search**: Find documents by meaning, not just keywords
- **Context understanding**: Retrieve relevant information even with different wording
- **Better accuracy**: More precise results for complex queries

### Setting Up COHERE_API_KEY
Before indexing, set your Cohere API key:

**Windows (PowerShell)**:
```powershell
$env:COHERE_API_KEY="your-api-key-here"
```

**Windows (Command Prompt)**:
```cmd
set COHERE_API_KEY=your-api-key-here
```

**Linux/Mac**:
```bash
export COHERE_API_KEY="your-api-key-here"
```

### Error Handling
**NEW**: The indexing script now includes validation to ensure vector embeddings are created:

If vector embeddings fail, you will see an error like:
```
RuntimeError: Vector embeddings were not created!
vec_index_bytes: 8 (should be > 8).
This usually means:
  1. COHERE_API_KEY environment variable is not set
  2. The embedding model 'embed-v4.0' failed
  3. The embedding service is unavailable
Please set COHERE_API_KEY and try again.
```

**What Changed**: Previously, the script would silently fall back to lexical-only indexing if embeddings failed. Now it **fails fast** with a clear error message, ensuring you know immediately if vector embeddings aren't working.

## Response Format
On successful indexing with vector embeddings, you will see:
```
✓ Successfully indexed 'Document Title'
  - Frames added: 90
  - Vector index size: 245678 bytes (grew by 245670 bytes)
  - Embedding model: {'kind': 'cohere', 'model': 'embed-v4.0'}
```

- Confirmation that the document was indexed
- Number of frames (chunks) added
- Vector index growth (proves embeddings were created)
- Embedding model information
- Include timestamps for referenced information
