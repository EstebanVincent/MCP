import os
from typing import Literal

from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.models import (
    QueryType,
    VectorizedQuery,
)
from openai import AzureOpenAI

from mcp.server.fastmcp import FastMCP

# Create an MCP server with authentication
mcp = FastMCP(
    "Chanel Knowledge",
    host="0.0.0.0",
    port=8005,
)


def embed_query(query):
    with AzureOpenAI(
        api_key=os.getenv("AZURE_OPENAI_KEY"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    ) as openai_client:
        response = openai_client.embeddings.create(
            input=query, model="text-embedding-3-large"
        )
    return response.data[0].embedding


@mcp.tool()
def search_official_documents(
    search_index: Literal["esvi-mcp-official", "esvi-mcp-deepresearch"],
    query: str,
    k: int = 5,
) -> dict:
    """
    Connect to an AI Search index and perform hybrid semantic search with query to return k results
    Use esvi-mcp-official first, then esvi-mcp-deepresearch if answer not found
    """
    vector_query = embed_query(query)
    vector_query_obj = VectorizedQuery(
        vector=vector_query,
        k_nearest_neighbors=k,
        fields="embedding",
        weight=0.7,
    )
    with SearchClient(
        endpoint=os.getenv("AZURE_SEARCH_SERVICE_ENDPOINT"),
        index_name=search_index,
        credential=AzureKeyCredential(os.getenv("AZURE_SEARCH_ADMIN_KEY")),
    ) as search_client:
        search_results = search_client.search(
            search_text=query,
            vector_queries=[vector_query_obj],
            query_type=QueryType.SEMANTIC,
            semantic_configuration_name="my-semantic-config",
            top=k,
        )

    results = list(search_results)
    clean_results = []
    for r in results:
        clean_r = {
            "filename": r["filename"],
            "content": r["content"],
            "score": r["@search.reranker_score"],
            "caption": None,
        }
        clean_results.append(clean_r)
    return clean_results


if __name__ == "__main__":
    # streamable-http not yet supported by vscode, change in url /sse to /mcp
    # mcp.run(transport="streamable-http")
    mcp.run(transport="stdio")
