"""
browser.py - Brave & Chrome Browser Automation Tools for JARVIS
"""
import time
import webbrowser
import logging
import urllib.parse
from typing import Optional
from tools.base_tool import BaseTool, ToolResult
from tools.registry import tool_registry
from automation.windows import WindowsAutomation, app_registry
from config.constants import PermissionLevel

try:
    import requests
    from bs4 import BeautifulSoup
    HAS_SCRAPER = True
except ImportError:
    HAS_SCRAPER = False

class OpenUrlTool(BaseTool):
    name = "open_url"
    description = "Open web URL or search link in default browser (Brave/Chrome)."
    parameters_schema = {
        "type": "object",
        "properties": {
            "url": {"type": "string", "description": "URL or search web address to open"}
        },
        "required": ["url"]
    }
    default_permission_level = PermissionLevel.SAFE

    def execute(self, url: str, **kwargs) -> ToolResult:
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "https://" + url

        brave_path = app_registry.find_app_path("brave")
        if brave_path:
            WindowsAutomation.launch_app(f'"{brave_path}" "{url}"')
            return ToolResult(True, f"Opened URL in Brave: {url}")

        webbrowser.open(url)
        return ToolResult(True, f"Opened URL in default browser: {url}")

class SearchWebTool(BaseTool):
    name = "search_web"
    description = "Search Google/Brave for given query and return top results or open in browser."
    parameters_schema = {
        "type": "object",
        "properties": {
            "query": {"type": "string", "description": "Search topic query"}
        },
        "required": ["query"]
    }
    default_permission_level = PermissionLevel.SAFE

    def execute(self, query: str, **kwargs) -> ToolResult:
        encoded = urllib.parse.quote(query)
        search_url = f"https://www.google.com/search?q={encoded}"

        # Fetch top organic snippets if scraper available
        snippets = []
        if HAS_SCRAPER:
            try:
                headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
                resp = requests.get(f"https://html.duckduckgo.com/html/?q={encoded}", headers=headers, timeout=5)
                if resp.status_code == 200:
                    soup = BeautifulSoup(resp.text, "html.parser")
                    results = soup.find_all("a", class_="result__snippet")
                    for r in results[:4]:
                        snippets.append(r.text.strip())
            except Exception as e:
                logging.warning(f"[SearchWebTool] Scraping snippet error: {e}")

        # Open search page in Brave/Browser
        brave_path = app_registry.find_app_path("brave")
        if brave_path:
            WindowsAutomation.launch_app(f'"{brave_path}" "{search_url}"')
        else:
            webbrowser.open(search_url)

        if snippets:
            summary = "\n".join(f"- {s}" for s in snippets)
            return ToolResult(True, f"Searched for '{query}'. Key results:\n{summary}")

        return ToolResult(True, f"Opened search for '{query}' in browser.")

class ReadWebpageTool(BaseTool):
    name = "read_webpage"
    description = "Extract and read textual content from web page URL."
    parameters_schema = {
        "type": "object",
        "properties": {
            "url": {"type": "string", "description": "Webpage URL to scrape"}
        },
        "required": ["url"]
    }
    default_permission_level = PermissionLevel.SAFE

    def execute(self, url: str, **kwargs) -> ToolResult:
        if not HAS_SCRAPER:
            return ToolResult(False, "", "BeautifulSoup / requests not available for page reading.")

        if not url.startswith("http://") and not url.startswith("https://"):
            url = "https://" + url

        try:
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
            resp = requests.get(url, headers=headers, timeout=8)
            if resp.status_code != 200:
                return ToolResult(False, "", f"HTTP error {resp.status_code} loading page.")

            soup = BeautifulSoup(resp.text, "html.parser")
            # Remove scripts & styles
            for elem in soup(["script", "style", "nav", "footer"]):
                elem.extract()
            text = soup.get_text(separator="\n").strip()
            # Clean empty lines
            lines = [line.strip() for line in text.splitlines() if line.strip()]
            clean_text = "\n".join(lines[:100]) # First 100 lines
            return ToolResult(True, f"Read text from {url}:\n\n{clean_text[:1500]}...")
        except Exception as e:
            return ToolResult(False, "", f"Failed to read webpage: {e}")

# Register Browser tools
tool_registry.register(OpenUrlTool())
tool_registry.register(SearchWebTool())
tool_registry.register(ReadWebpageTool())
