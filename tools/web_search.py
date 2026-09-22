import os

from tavily import TavilyClient

client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))


def web_search(query: str) -> str:
    try:
        response = client.search(query=query, max_results=3)
        results = response.get("results", [])

        if not results:
            return "No relevant web results found."

        formatted = []
        for r in results:
            formatted.append(f"{r.get('title', 'Untitled')}\n{r.get('content', '')}")

        return "\n\n---\n\n".join(formatted)

    except Exception as e:
        return f"Web search error: {e}"
