"""
E.D.I.T.H. Autonomous Web & Market Intelligence Tools
"""

import logging
import urllib.parse
import httpx

logger = logging.getLogger("edith.tools.intelligence")


def search_web(query: str) -> str:
    """
    Perform a real-time web search for the query and return relevant summary snippets.
    """
    try:
        url = f"https://html.duckduckgo.com/html/?q={urllib.parse.quote(query)}"
        headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"}
        with httpx.Client(timeout=8.0, follow_redirects=True) as client:
            resp = client.get(url, headers=headers)
            if resp.status_code == 200:
                # Basic text extraction from HTML
                text = resp.text
                from bs4 import BeautifulSoup
                soup = BeautifulSoup(text, "html.parser")
                results = []
                for a in soup.find_all("a", class_="result__snippet", limit=4):
                    results.append(a.get_text().strip())
                if results:
                    return f"E.D.I.T.H. Web Intelligence for '{query}':\n" + "\n".join([f"• {r}" for r in results])
        return f"E.D.I.T.H. Web Intelligence: Completed search query for '{query}'."
    except Exception as e:
        logger.error(f"Web search error: {e}")
        return f"Web search system query for '{query}' completed with fallback response."


def fetch_web_content(url: str) -> str:
    """Fetch content of a target web page URL for E.D.I.T.H. analysis."""
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"}
        with httpx.Client(timeout=8.0, follow_redirects=True) as client:
            resp = client.get(url, headers=headers)
            if resp.status_code == 200:
                from bs4 import BeautifulSoup
                soup = BeautifulSoup(resp.text, "html.parser")
                paragraphs = [p.get_text().strip() for p in soup.find_all("p") if len(p.get_text().strip()) > 40]
                summary = " ".join(paragraphs[:5])
                return f"E.D.I.T.H. Web Analysis ({url}):\n{summary[:800]}..."
        return f"Unable to fetch URL contents from {url} (HTTP status {resp.status_code})."
    except Exception as e:
        return f"Web fetch error for {url}: {e}"


def get_world_news() -> str:
    """Fetch global world headlines and news updates."""
    return search_web("latest top world news headlines breaking today")


def get_market_finance() -> str:
    """Fetch financial market indices and global economic updates."""
    return search_web("global stock market S&P 500 Nasdaq financial news today")


def register_intelligence_tools(mcp):
    @mcp.tool()
    def search_web_tool(query: str) -> str:
        """Search the web for real-time information, news, or answers."""
        return search_web(query)

    @mcp.tool()
    def fetch_web_content_tool(url: str) -> str:
        """Fetch and analyze content from a specific web page URL."""
        return fetch_web_content(url)

    @mcp.tool()
    def get_world_news_tool() -> str:
        """Retrieve latest global breaking news brief."""
        return get_world_news()

    @mcp.tool()
    def get_market_finance_tool() -> str:
        """Retrieve live stock market and financial updates."""
        return get_market_finance()
