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
python ${CLAUDE_PLUGIN_ROOT}/scripts/index.py "Document Title" "Label" "file.pdf" --embedding_model=embed-v4.0
```

## Requirements

### Vector Embeddings (REQUIRED)
**This system REQUIRES vector embeddings for semantic search.** The indexing script will fail if embeddings cannot be created.

### Supported Embedding Models

#### Built-in Local Model (No API Key Required)
| Model | Dimensions | Notes |
|-------|------------|-------|
| BGE-small-en-v1.5 | 384 | Default model |

#### Local ONNX Models (No API Key Required)
| Model | Dimensions | Size |
|-------|------------|------|
| BGE-small-en-v1.5 | 384 | ~120MB |
| BGE-base-en-v1.5 | 768 | ~420MB |
| Nomic-embed-text-v1.5 | 768 | ~530MB |
| GTE-large | 1024 | ~1.3GB |

#### OpenAI
| Model | Dimensions | API Key |
|-------|------------|---------|
| text-embedding-3-small | 1536 | `OPENAI_API_KEY` |
| text-embedding-3-large | 3072 | `OPENAI_API_KEY` |
| text-embedding-ada-002 | 1536 | `OPENAI_API_KEY` (legacy) |

#### Cohere
| Model | Dimensions | API Key |
|-------|------------|---------|
| embed-english-v3.0 | 1024 | `COHERE_API_KEY` |
| embed-multilingual-v3.0 | 1024 | `COHERE_API_KEY` |
| embed-english-light-v3.0 | 384 | `COHERE_API_KEY` |
| embed-multilingual-light-v3.0 | 384 | `COHERE_API_KEY` |

#### Voyage AI
| Model | Dimensions | API Key |
|-------|------------|---------|
| voyage-3 | 1024 | `VOYAGE_API_KEY` |
| voyage-3-lite | 512 | `VOYAGE_API_KEY` |
| voyage-code-3 | 1024 | `VOYAGE_API_KEY` |

#### NVIDIA
| Model | API Key |
|-------|---------|
| nvidia/nv-embed-v1 | `NVIDIA_API_KEY` |

#### HuggingFace (Local, Python only)
| Model | API Key |
|-------|---------|
| Any sentence-transformers model (e.g., `all-MiniLM-L6-v2`) | None required |

### Why Vector Embeddings Are Required
Unlike lexical-only search (keyword matching), vector embeddings enable:
- **Semantic search**: Find documents by meaning, not just keywords
- **Context understanding**: Retrieve relevant information even with different wording
- **Better accuracy**: More precise results for complex queries

### Setting Up API Keys
Before indexing, set your API key for the embedding provider you choose:

**Windows (PowerShell)**:
```powershell
$env:COHERE_API_KEY="your-api-key-here"
$env:OPENAI_API_KEY="your-api-key-here"
$env:VOYAGE_API_KEY="your-api-key-here"
$env:NVIDIA_API_KEY="your-api-key-here"
```

**Windows (Command Prompt)**:
```cmd
set COHERE_API_KEY=your-api-key-here
set OPENAI_API_KEY=your-api-key-here
set VOYAGE_API_KEY=your-api-key-here
set NVIDIA_API_KEY=your-api-key-here
```

**Linux/Mac**:
```bash
export COHERE_API_KEY="your-api-key-here"
export OPENAI_API_KEY="your-api-key-here"
export VOYAGE_API_KEY="your-api-key-here"
export NVIDIA_API_KEY="your-api-key-here"
```
