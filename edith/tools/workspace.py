"""
E.D.I.T.H. Developer Workspace & Terminal Tools
"""

import os
import subprocess
import logging
from edith.memory import remember_fact, recall_memory, add_task, get_tasks

logger = logging.getLogger("edith.tools.workspace")


def analyze_workspace(dir_path: str = ".") -> str:
    """Analyze files, directories, line count estimates in target workspace."""
    try:
        abs_path = os.path.abspath(dir_path)
        file_count = 0
        dir_count = 0
        extensions = {}
        
        for root, dirs, files in os.walk(abs_path):
            if ".git" in root or "__pycache__" in root or "node_modules" in root or ".venv" in root:
                continue
            dir_count += len(dirs)
            for f in files:
                file_count += 1
                ext = os.path.splitext(f)[1] or "no_ext"
                extensions[ext] = extensions.get(ext, 0) + 1

        top_exts = sorted(extensions.items(), key=lambda x: x[1], reverse=True)[:5]
        ext_summary = ", ".join([f"{ext}: {count} files" for ext, count in top_exts])

        return (
            f"E.D.I.T.H. Workspace Analysis [{abs_path}]:\n"
            f"• Subdirectories: {dir_count}\n"
            f"• Source Files: {file_count}\n"
            f"• Breakdown: {ext_summary}"
        )
    except Exception as e:
        return f"Workspace analysis failed: {e}"


def run_terminal_command(command: str) -> str:
    """Safely execute a shell command in the workspace directory."""
    # List of dangerous commands to block for security
    forbidden = ["rm -rf /", "mkfs", ":(){ :|:& };:", "dd if="]
    if any(f in command for f in forbidden):
        return "E.D.I.T.H. Security Guard: Command execution blocked for safety reasons."

    try:
        res = subprocess.run(
            command, shell=True, capture_output=True, text=True, timeout=10
        )
        output = res.stdout or res.stderr or "Command completed with no output."
        return f"E.D.I.T.H. Terminal Execution [{command}]:\n{output[:1000]}"
    except subprocess.TimeoutExpired:
        return f"Command execution timed out after 10 seconds: {command}"
    except Exception as e:
        return f"Command execution error: {e}"


def register_workspace_tools(mcp):
    @mcp.tool()
    def analyze_workspace_tool(dir_path: str = ".") -> str:
        """Inspect and summarize files, directories, and structure of workspace."""
        return analyze_workspace(dir_path)

    @mcp.tool()
    def run_terminal_command_tool(command: str) -> str:
        """Run a safe terminal command in the workspace environment."""
        return run_terminal_command(command)

    @mcp.tool()
    def remember_fact_tool(key: str, value: str) -> str:
        """Save a tactical note or fact into E.D.I.T.H. persistent memory."""
        return remember_fact(key, value)

    @mcp.tool()
    def recall_memory_tool(key: str = "") -> str:
        """Recall saved notes, facts, or preferences from E.D.I.T.H. memory."""
        return recall_memory(key)

    @mcp.tool()
    def add_task_tool(task_description: str) -> str:
        """Add a new item to E.D.I.T.H. task roster."""
        return add_task(task_description)

    @mcp.tool()
    def get_tasks_tool() -> str:
        """Retrieve all active tasks from E.D.I.T.H. roster."""
        return get_tasks()
