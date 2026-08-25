"""
files.py - Natural Language File & Folder Management Tools for JARVIS
"""
import os
import shutil
import glob
import logging
import datetime
from tools.base_tool import BaseTool, ToolResult
from tools.registry import tool_registry
from config.constants import PermissionLevel

try:
    from pypdf import PdfReader
    HAS_PYPDF = True
except ImportError:
    HAS_PYPDF = False

class ListFilesTool(BaseTool):
    name = "list_files"
    description = "Find or list files in a directory matching extension or search pattern."
    parameters_schema = {
        "type": "object",
        "properties": {
            "directory": {"type": "string", "description": "Folder path (default: Downloads or Documents)"},
            "extension": {"type": "string", "description": "File extension filter, e.g. .pdf"},
            "pattern": {"type": "string", "description": "Filename search pattern"}
        },
        "required": []
    }
    default_permission_level = PermissionLevel.SAFE

    def execute(self, directory: str = None, extension: str = None, pattern: str = None, **kwargs) -> ToolResult:
        dir_path = directory if directory else os.path.expanduser("~/Downloads")
        if not os.path.exists(dir_path):
            dir_path = os.path.expanduser("~")

        search_glob = os.path.join(dir_path, f"*{pattern or ''}*{extension or ''}")
        matches = glob.glob(search_glob)
        
        if not matches:
            return ToolResult(True, f"No matching files found in '{dir_path}'.")

        # Sort by modification time
        matches.sort(key=lambda x: os.path.getmtime(x), reverse=True)
        items = []
        for m in matches[:10]:
            basename = os.path.basename(m)
            size_mb = round(os.path.getsize(m) / (1024 * 1024), 2)
            mtime = datetime.datetime.fromtimestamp(os.path.getmtime(m)).strftime('%Y-%m-%d %H:%M')
            items.append(f"• {basename} ({size_mb} MB, Modified: {mtime})")

        out = "\n".join(items)
        return ToolResult(True, f"Found {len(matches)} files in '{dir_path}':\n{out}", data={"files": matches})

class OpenFileTool(BaseTool):
    name = "open_file"
    description = "Open file or folder in default system application."
    parameters_schema = {
        "type": "object",
        "properties": {
            "path": {"type": "string", "description": "File or directory path to open"}
        },
        "required": ["path"]
    }
    default_permission_level = PermissionLevel.SAFE

    def execute(self, path: str, **kwargs) -> ToolResult:
        expanded = os.path.expanduser(path)
        if not os.path.exists(expanded):
            # Try searching in Downloads
            dl_path = os.path.join(os.path.expanduser("~/Downloads"), path)
            if os.path.exists(dl_path):
                expanded = dl_path
            else:
                return ToolResult(False, "", f"File path '{path}' does not exist.")

        try:
            os.startfile(expanded)
            return ToolResult(True, f"Opened file '{os.path.basename(expanded)}'.")
        except Exception as e:
            return ToolResult(False, "", f"Failed to open '{path}': {e}")

class CreateFolderTool(BaseTool):
    name = "create_folder"
    description = "Create a new folder/directory."
    parameters_schema = {
        "type": "object",
        "properties": {
            "folder_name": {"type": "string", "description": "Folder name or full path"}
        },
        "required": ["folder_name"]
    }
    default_permission_level = PermissionLevel.SAFE

    def execute(self, folder_name: str, **kwargs) -> ToolResult:
        target = os.path.expanduser(folder_name)
        if not os.path.isabs(target):
            target = os.path.join(os.path.expanduser("~/Documents"), folder_name)

        try:
            os.makedirs(target, exist_ok=True)
            return ToolResult(True, f"Created folder '{target}'.")
        except Exception as e:
            return ToolResult(False, "", f"Failed to create folder: {e}")

class DeleteFileTool(BaseTool):
    name = "delete_file"
    description = "Delete specified file permanently (Requires User Confirmation!)."
    parameters_schema = {
        "type": "object",
        "properties": {
            "path": {"type": "string", "description": "Path of file to delete"}
        },
        "required": ["path"]
    }
    default_permission_level = PermissionLevel.CONFIRM

    def execute(self, path: str, **kwargs) -> ToolResult:
        expanded = os.path.expanduser(path)
        if not os.path.exists(expanded):
            return ToolResult(False, "", f"File '{path}' does not exist.")

        try:
            os.remove(expanded)
            return ToolResult(True, f"Deleted file '{os.path.basename(expanded)}'.")
        except Exception as e:
            return ToolResult(False, "", f"Failed to delete file: {e}")

class ReadPdfTool(BaseTool):
    name = "read_pdf"
    description = "Extract and read text content from a PDF document."
    parameters_schema = {
        "type": "object",
        "properties": {
            "path": {"type": "string", "description": "Path to PDF file"}
        },
        "required": ["path"]
    }
    default_permission_level = PermissionLevel.SAFE

    def execute(self, path: str, **kwargs) -> ToolResult:
        if not HAS_PYPDF:
            return ToolResult(False, "", "pypdf package is not installed.")

        expanded = os.path.expanduser(path)
        if not os.path.exists(expanded):
            return ToolResult(False, "", f"PDF file '{path}' not found.")

        try:
            reader = PdfReader(expanded)
            text_pages = []
            for i, page in enumerate(reader.pages[:5]): # First 5 pages
                txt = page.extract_text()
                if txt:
                    text_pages.append(f"--- Page {i+1} ---\n{txt.strip()}")

            summary = "\n\n".join(text_pages)
            return ToolResult(True, f"Read PDF '{os.path.basename(expanded)}' ({len(reader.pages)} total pages):\n\n{summary[:2000]}...")
        except Exception as e:
            return ToolResult(False, "", f"Failed to read PDF file: {e}")

tool_registry.register(ListFilesTool())
tool_registry.register(OpenFileTool())
tool_registry.register(CreateFolderTool())
tool_registry.register(DeleteFileTool())
tool_registry.register(ReadPdfTool())
