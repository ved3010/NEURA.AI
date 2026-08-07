"""
E.D.I.T.H. Tactical MCP Server — Entry Point
Run with: python server.py (or uv run edith)
"""

from mcp.server.fastmcp import FastMCP
from edith.tools import register_all_tools
from config import config

# Create the E.D.I.T.H. MCP server instance
mcp = FastMCP(
    name=config.SERVER_NAME,
    instructions=(
        "You are E.D.I.T.H. (Even In Death, I'm The Hero), Tony Stark's tactical AI defense system. "
        "You possess comprehensive tools for system diagnostics, tactical protocols, web intelligence, "
        "workspace analysis, and persistent memory core management. "
        "Be direct, precise, intelligent, calm, and composed."
    ),
)

# Register all diagnostic, protocol, intelligence, workspace, and memory tools
register_all_tools(mcp)


def main():
    mcp.run(transport='sse')


if __name__ == "__main__":
    main()