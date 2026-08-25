"""
web_search.py - Factual Research Engine for General Knowledge & Current Events
"""
import urllib.parse
import logging
from tools.base_tool import BaseTool, ToolResult
from tools.registry import tool_registry
from config.constants import PermissionLevel

try:
    import requests
    from bs4 import BeautifulSoup
    HAS_SCRAPER = True
except ImportError:
    HAS_SCRAPER = False

class FactualSearchTool(BaseTool):
    name = "research_query"
    description = "Research general knowledge or factual query on the web."
    parameters_schema = {
        "type": "object",
        "properties": {
            "query": {"type": "string", "description": "Factual question or research query"}
        },
        "required": ["query"]
    }
    default_permission_level = PermissionLevel.SAFE

    def execute(self, query: str, **kwargs) -> ToolResult:
        if not HAS_SCRAPER:
            return ToolResult(False, "", "Web scraper missing.")

        encoded = urllib.parse.quote(query)
        url = f"https://html.duckduckgo.com/html/?q={encoded}"
        try:
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
            resp = requests.get(url, headers=headers, timeout=6)
            if resp.status_code == 200:
                soup = BeautifulSoup(resp.text, "html.parser")
                results = soup.find_all("a", class_="result__snippet")
                findings = [r.text.strip() for r in results[:5] if r.text.strip()]
                if findings:
                    summary = "\n".join(f"• {f}" for f in findings)
                    return ToolResult(True, f"Web Research results for '{query}':\n{summary}")
            return ToolResult(False, "", "No clear web search results found.")
        except Exception as e:
            return ToolResult(False, "", f"Research failed: {e}")

tool_registry.register(FactualSearchTool())
