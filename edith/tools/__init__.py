"""
E.D.I.T.H. MCP Tool Suite Package
Registers all diagnostic, protocol, intelligence, workspace, and memory tools with FastMCP.
"""

from .diagnostics import register_diagnostic_tools
from .protocols import register_protocol_tools
from .intelligence import register_intelligence_tools
from .workspace import register_workspace_tools


def register_all_tools(mcp):
    """Register all E.D.I.T.H. MCP tools with FastMCP instance."""
    register_diagnostic_tools(mcp)
    register_protocol_tools(mcp)
    register_intelligence_tools(mcp)
    register_workspace_tools(mcp)
