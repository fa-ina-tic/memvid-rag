"""
RAG Core Library using Memvid
Handles all memvid operations with Claude embeddings and token-based chunking
"""

import os
import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime
import hashlib

# Memvid
try:
    from memvid import Mem
except ImportError:
    print("Warning: memvid-sdk not installed. Install with: uv pip install memvid-sdk")
    Mem = None

# Unstructured for document processing
try:
    from unstructured.partition.auto import partition
except ImportError:
    print("Warning: unstructured not installed. Install with: uv pip install unstructured")
    partition = None

# Tiktoken for token-based chunking
try:
    import tiktoken
except ImportError:
    print("Warning: tiktoken not installed. Install with: uv pip install tiktoken")
    tiktoken = None

# Anthropic for Claude embeddings
try:
    from anthropic import Anthropic
except ImportError:
    print("Warning: anthropic not installed. Install with: uv pip install anthropic")
    Anthropic = None


class RAGCore:
    """Core RAG functionality using Memvid with Claude embeddings and token-based chunking"""

    def __init__(
        self,
        db_path: str = "knowledge.mv2",
        max_tokens_per_chunk: int = 512,
        chunk_overlap_tokens: int = 50,
        tiktoken_encoding: str = "cl100k_base",
        embedding_provider: str = "claude",
        embedding_model: str = "claude-3-5-sonnet-20241022",
        max_file_size_mb: int = 50
    ):
        """
        Initialize RAG with memvid database path and configuration

        Args:
            db_path: Path to memvid database file
            max_tokens_per_chunk: Maximum tokens per chunk
            chunk_overlap_tokens: Number of overlapping tokens between chunks
            tiktoken_encoding: Tiktoken encoding to use (cl100k_base for Claude)
            embedding_provider: Embedding provider (claude, openai, etc.)
            embedding_model: Model to use for embeddings
            max_file_size_mb: Maximum file size to process
        """
        self.db_path = db_path
        self.mem = None
        self.max_tokens_per_chunk = max_tokens_per_chunk
        self.chunk_overlap_tokens = chunk_overlap_tokens
        self.tiktoken_encoding = tiktoken_encoding
        self.embedding_provider = embedding_provider
        self.embedding_model = embedding_model
        self.max_file_size_mb = max_file_size_mb

        # Initialize tokenizer
        if tiktoken is not None:
            try:
                self.tokenizer = tiktoken.get_encoding(tiktoken_encoding)
            except Exception as e:
                print(f"Warning: Failed to load tiktoken encoding {tiktoken_encoding}: {e}")
                self.tokenizer = None
        else:
            self.tokenizer = None

        # Initialize embedding client
        self.embedding_client = None
        if embedding_provider == "claude" and Anthropic is not None:
            api_key = os.environ.get("ANTHROPIC_API_KEY")
            if api_key:
                self.embedding_client = Anthropic(api_key=api_key)
            else:
                print("Warning: ANTHROPIC_API_KEY not set in environment")

    def initialize(self) -> bool:
        """Create or open existing .mv2 file"""
        if Mem is None:
            raise ImportError("memvid-sdk is not installed")

        try:
            # Check if database exists
            exists = os.path.exists(self.db_path)

            # Open or create the memory with embedding configuration
            if self.embedding_client:
                # Use custom embeddings
                self.mem = Mem(
                    self.db_path,
                    embedding_function=self._get_embedding
                )
            else:
                # Use default embeddings
                self.mem = Mem(self.db_path)

            if not exists:
                print(f"✓ Created new RAG database: {self.db_path}")
            else:
                print(f"✓ Opened existing RAG database: {self.db_path}")

            return True
        except Exception as e:
            print(f"✗ Failed to initialize RAG: {e}")
            return False

    def _get_embedding(self, text: str) -> List[float]:
        """
        Get embeddings for text using configured provider

        Note: This is a placeholder. Memvid v1.x may not support custom embeddings.
        This prepares the structure for when the feature is available.
        """
        if self.embedding_provider == "claude" and self.embedding_client:
            try:
                # Claude API doesn't have a direct embeddings endpoint yet
                # This is a placeholder for future implementation
                # For now, we'll rely on Memvid's default embeddings
                pass
            except Exception as e:
                print(f"Warning: Embedding generation failed: {e}")

        # Return empty list to use Memvid's default embeddings
        return []

    def index_file(self, file_path: str, metadata: Optional[Dict[str, Any]] = None) -> bool:
        """Index a single file into RAG memory using unstructured"""
        if self.mem is None:
            print("✗ RAG not initialized. Call initialize() first.")
            return False

        try:
            path = Path(file_path)

            if not path.exists():
                print(f"✗ File not found: {file_path}")
                return False

            # Get file stats
            stat = path.stat()
            file_size = stat.st_size
            file_type = path.suffix.lower()

            # Check file size
            max_size = self.max_file_size_mb * 1024 * 1024
            if file_size > max_size:
                print(f"✗ File too large: {file_path} ({file_size / 1024 / 1024:.2f} MB)")
                return False

            # Extract content using unstructured
            content = self._extract_content_unstructured(path)

            if not content:
                print(f"✗ Could not extract content from: {file_path}")
                return False

            # Create metadata
            meta = {
                "file_path": str(path.absolute()),
                "file_name": path.name,
                "file_type": file_type,
                "file_size": file_size,
                "indexed_at": datetime.now().isoformat(),
                "content_hash": hashlib.md5(content.encode()).hexdigest()
            }

            if metadata:
                meta.update(metadata)

            # Chunk the content using token-based chunking
            chunks = self._chunk_by_tokens(content)

            if not chunks:
                print(f"✗ No chunks created from: {file_path}")
                return False

            # Index each chunk
            for i, chunk in enumerate(chunks):
                chunk_meta = meta.copy()
                chunk_meta["chunk_id"] = i
                chunk_meta["total_chunks"] = len(chunks)

                # Add to memvid with metadata as labels
                self.mem.add(
                    text=chunk,
                    labels={
                        "file_path": meta["file_path"],
                        "file_type": file_type,
                        "chunk_id": str(i)
                    }
                )

            print(f"✓ Indexed: {path.name} ({len(chunks)} chunks)")
            return True

        except Exception as e:
            print(f"✗ Error indexing {file_path}: {e}")
            return False

    def index_directory(self, dir_path: str, patterns: List[str] = None) -> Dict[str, Any]:
        """Index all matching files in a directory"""
        if patterns is None:
            patterns = ["*.py", "*.md", "*.txt", "*.pdf", "*.docx", "*.html", "*.json"]

        path = Path(dir_path)
        if not path.exists():
            return {"success": False, "error": "Directory not found"}

        results = {
            "success": True,
            "indexed": 0,
            "failed": 0,
            "skipped": 0,
            "files": []
        }

        # Find all matching files
        files = []
        for pattern in patterns:
            files.extend(path.rglob(pattern))

        # Remove duplicates
        files = list(set(files))

        print(f"Found {len(files)} files to index...")

        for file in files:
            # Skip hidden files and directories
            if any(part.startswith('.') for part in file.parts):
                results["skipped"] += 1
                continue

            if self.index_file(str(file)):
                results["indexed"] += 1
                results["files"].append(str(file))
            else:
                results["failed"] += 1

        return results

    def query(self, question: str, k: int = 5, mode: str = "hybrid") -> List[Dict[str, Any]]:
        """Query RAG memory with semantic/hybrid search"""
        if self.mem is None:
            print("✗ RAG not initialized")
            return []

        try:
            # Perform search based on mode
            if mode == "sem" or mode == "semantic":
                results = self.mem.search(question, k=k)
            elif mode == "lex" or mode == "lexical":
                results = self.mem.search(question, k=k, mode="lexical")
            else:  # hybrid (default)
                results = self.mem.search(question, k=k, mode="hybrid")

            # Format results
            formatted = []
            for result in results:
                formatted.append({
                    "text": result.get("text", ""),
                    "score": result.get("score", 0.0),
                    "labels": result.get("labels", {}),
                    "metadata": result.get("metadata", {})
                })

            return formatted

        except Exception as e:
            print(f"✗ Query failed: {e}")
            return []

    def get_status(self) -> Dict[str, Any]:
        """Get RAG system status"""
        status = {
            "database": self.db_path,
            "initialized": self.mem is not None,
            "exists": os.path.exists(self.db_path),
            "config": {
                "max_tokens_per_chunk": self.max_tokens_per_chunk,
                "chunk_overlap_tokens": self.chunk_overlap_tokens,
                "embedding_provider": self.embedding_provider,
                "tiktoken_encoding": self.tiktoken_encoding
            }
        }

        if status["exists"]:
            stat = os.stat(self.db_path)
            status["size_bytes"] = stat.st_size
            status["size_mb"] = stat.st_size / 1024 / 1024
            status["modified"] = datetime.fromtimestamp(stat.st_mtime).isoformat()

        if self.mem is not None:
            try:
                # Try to get count of indexed items
                all_items = self.mem.search("", k=10000)
                status["indexed_chunks"] = len(all_items)
            except:
                status["indexed_chunks"] = "unknown"

        return status

    def clear(self) -> bool:
        """Clear RAG index by removing and recreating .mv2 file"""
        try:
            # Close existing connection
            if self.mem is not None:
                self.mem = None

            # Remove database file
            if os.path.exists(self.db_path):
                os.remove(self.db_path)
                print(f"✓ Removed old database: {self.db_path}")

            # Reinitialize
            return self.initialize()

        except Exception as e:
            print(f"✗ Failed to clear RAG: {e}")
            return False

    def list_indexed_files(self) -> List[str]:
        """List all indexed files"""
        if self.mem is None:
            return []

        try:
            # Query all items
            all_items = self.mem.search("", k=10000)

            # Extract unique file paths from labels
            files = set()
            for item in all_items:
                labels = item.get("labels", {})
                if "file_path" in labels:
                    files.add(labels["file_path"])

            return sorted(list(files))

        except Exception as e:
            print(f"✗ Failed to list files: {e}")
            return []

    def _extract_content_unstructured(self, path: Path) -> str:
        """
        Extract text content from various file types using unstructured

        Supports: PDF, DOCX, HTML, TXT, MD, JSON, CSV, XML, PPTX, XLSX, and more
        """
        if partition is None:
            # Fallback to simple text reading
            try:
                with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                    return f.read()
            except Exception as e:
                print(f"✗ Error reading {path}: {e}")
                return ""

        try:
            # Use unstructured to partition the document
            elements = partition(filename=str(path))

            # Extract text from all elements
            text_parts = []
            for element in elements:
                text_parts.append(str(element))

            content = "\n\n".join(text_parts)
            return content

        except Exception as e:
            print(f"✗ Error extracting content with unstructured from {path}: {e}")
            # Fallback to simple text reading
            try:
                with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                    return f.read()
            except:
                return ""

    def _chunk_by_tokens(self, content: str) -> List[str]:
        """
        Split content into chunks based on token count using tiktoken

        Args:
            content: Text content to chunk

        Returns:
            List of text chunks
        """
        if not self.tokenizer:
            # Fallback to character-based chunking
            return self._chunk_by_characters(content)

        try:
            # Encode the entire content
            tokens = self.tokenizer.encode(content)

            if len(tokens) <= self.max_tokens_per_chunk:
                return [content]

            chunks = []
            start = 0

            while start < len(tokens):
                # Define chunk end
                end = start + self.max_tokens_per_chunk

                # Extract chunk tokens
                chunk_tokens = tokens[start:end]

                # Decode back to text
                chunk_text = self.tokenizer.decode(chunk_tokens)

                # Try to break at sentence boundary for better coherence
                if end < len(tokens):
                    # Look for sentence endings in the last 20% of the chunk
                    boundary_start = int(len(chunk_text) * 0.8)
                    boundary_text = chunk_text[boundary_start:]

                    # Find last sentence ending
                    for separator in ['. ', '.\n', '! ', '!\n', '? ', '?\n']:
                        last_sep = boundary_text.rfind(separator)
                        if last_sep != -1:
                            actual_end = boundary_start + last_sep + len(separator)
                            chunk_text = chunk_text[:actual_end]
                            # Re-encode to get actual token count
                            chunk_tokens = self.tokenizer.encode(chunk_text)
                            break

                chunks.append(chunk_text.strip())

                # Move start position with overlap
                start = end - self.chunk_overlap_tokens

            return chunks

        except Exception as e:
            print(f"Warning: Token-based chunking failed: {e}. Falling back to character-based.")
            return self._chunk_by_characters(content)

    def _chunk_by_characters(self, content: str, chunk_size: int = 2000, overlap: int = 200) -> List[str]:
        """Fallback character-based chunking if tiktoken is not available"""
        if len(content) <= chunk_size:
            return [content]

        chunks = []
        start = 0

        while start < len(content):
            end = start + chunk_size
            chunk = content[start:end]

            # Try to break at sentence boundary
            if end < len(content):
                last_period = chunk.rfind('.')
                last_newline = chunk.rfind('\n')
                break_point = max(last_period, last_newline)

                if break_point > chunk_size * 0.5:
                    chunk = chunk[:break_point + 1]
                    end = start + break_point + 1

            chunks.append(chunk.strip())
            start = end - overlap

        return chunks


# Convenience functions for command-line usage
def initialize_rag(db_path: str = "knowledge.mv2") -> RAGCore:
    """Initialize and return RAG core instance"""
    rag = RAGCore(db_path)
    rag.initialize()
    return rag


def index_file(db_path: str, file_path: str) -> bool:
    """Index a single file"""
    rag = RAGCore(db_path)
    if rag.initialize():
        return rag.index_file(file_path)
    return False


def index_directory(db_path: str, dir_path: str, patterns: List[str] = None) -> Dict[str, Any]:
    """Index a directory"""
    rag = RAGCore(db_path)
    if rag.initialize():
        return rag.index_directory(dir_path, patterns)
    return {"success": False, "error": "Failed to initialize"}


def query_rag(db_path: str, question: str, k: int = 5, mode: str = "hybrid") -> List[Dict[str, Any]]:
    """Query the RAG system"""
    rag = RAGCore(db_path)
    if rag.initialize():
        return rag.query(question, k, mode)
    return []


def get_status(db_path: str = "knowledge.mv2") -> Dict[str, Any]:
    """Get RAG status"""
    rag = RAGCore(db_path)
    rag.initialize()
    return rag.get_status()


def clear_rag(db_path: str = "knowledge.mv2") -> bool:
    """Clear RAG database"""
    rag = RAGCore(db_path)
    return rag.clear()


def list_files(db_path: str = "knowledge.mv2") -> List[str]:
    """List indexed files"""
    rag = RAGCore(db_path)
    if rag.initialize():
        return rag.list_indexed_files()
    return []
