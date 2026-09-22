"""
Custom MCP server for the AI Research Assistant.

This exposes the document knowledge base as an MCP tool, so any
MCP-compatible client (like Claude Desktop) can search the uploaded
documents directly.

Run locally with:
    python mcp_server/server.py

Then connect it in Claude Desktop's config (claude_desktop_config.json):
{
  "mcpServers": {
    "doc-search": {
      "command": "python",
      "args": ["/absolute/path/to/mcp_server/server.py"]
    }
  }
}
"""

import sys
import os

# Allow importing rag.py from the project root
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mcp.server.fastmcp import FastMCP
from rag import retrieve, add_document

mcp = FastMCP("DocSearch")


@mcp.tool()
def search_my_documents(query: str) -> str:
    """
    Search the user's uploaded documents for information relevant
    to the given query. Returns the most relevant chunks of text.
    """
    return retrieve(query)


@mcp.tool()
def upload_document(file_path: str) -> str:
    """
    Add a PDF document (given a local file path) to the knowledge
    base so it can be searched later.
    """
    chunks = add_document(file_path, os.path.basename(file_path))
    return f"Added {chunks} chunks from {file_path} to the knowledge base."


if __name__ == "__main__":
    mcp.run()
