import sys
import io
from memvid_sdk import use

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")


def search(query: str, **kwargs):
    with use(
        "basic", "knowledge.mv2", mode="auto", enable_vec=True, read_only=True
    ) as mv:
        ## mv.find function info:
        # """Searches for relevant content using lexical or semantic search.

        # Performs a search query against the indexed content, supporting both
        # lexical (keyword-based) and semantic (embedding-based) search modes.
        # Automatically detects the appropriate mode based on available resources.

        # Args:
        #     query: The search query string.
        #     k: Maximum number of results to return. Defaults to 5.
        #     snippet_chars: Maximum characters per result snippet. Defaults to 240.
        #     scope: Optional scope filter to limit search domain.
        #     cursor: Optional pagination cursor for retrieving next batch of results.
        #     mode: Search mode ('lex', 'sem', or 'auto'). If None or 'auto',
        #         automatically selects based on vector index availability and API key.
        #     query_embedding: Pre-computed query embedding vector. Mutually exclusive
        #         with embedder parameter.
        #     query_embedding_model: Model identifier for query embedding
        #         (e.g., 'openai-small').
        #     adaptive: Enable adaptive result count based on relevancy scores.
        #     min_relevancy: Minimum relevancy threshold for adaptive mode.
        #     max_k: Maximum result count for adaptive mode.
        #     adaptive_strategy: Strategy name for adaptive result selection.
        #     embedder: Embedding provider instance for computing query embeddings.
        #         Mutually exclusive with query_embedding parameter.
        #     as_of_frame: Optional frame number for temporal search.
        #     as_of_ts: Optional timestamp for temporal search.

        # Returns:
        #     FindResult object containing matched documents with snippets and metadata.

        # Raises:
        #     ValueError: If both query_embedding and embedder are provided simultaneously.
        # """
        search_mode = kwargs.pop("mode", "auto")
        docs = mv.find(query, mode=search_mode, **kwargs)
        return docs


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(
            "Usage: python scripts/search.py <query> [--k=5] [--snippet_chars=240] [--min_relevancy=0.0] [--adaptive=false]"
        )
        sys.exit(1)

    # Parse query and kwargs from command line arguments
    args = sys.argv[1:]
    query_parts = []
    kwargs = {}

    for arg in args:
        if arg.startswith("--"):
            # Parse --key=value format
            if "=" in arg:
                key, value = arg[2:].split("=", 1)
                # Try to convert to appropriate type
                if value.lower() in ("true", "false"):
                    kwargs[key] = value.lower() == "true"
                elif value.replace(".", "", 1).replace("-", "", 1).isdigit():
                    # Try to parse as number (int or float)
                    kwargs[key] = float(value) if "." in value else int(value)
                else:
                    kwargs[key] = value
            else:
                # Parse --key format (boolean flag)
                kwargs[arg[2:]] = True
        else:
            query_parts.append(arg)

    query = " ".join(query_parts)
    results = search(query, **kwargs)
    print(f"Query: {results.get('query', query)}")
    print(f"Total hits: {results.get('total_hits', 0)}")
    print(f"Took: {results.get('took_ms', 0)}ms")
    print("-" * 50)
    for hit in results.get("hits", []):
        print(hit)
        print("-" * 50)
