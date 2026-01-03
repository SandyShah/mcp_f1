"""FastF1 MCP Server - Main Entry Point"""

from mcp.server.fastmcp import FastMCP
from .utils.cache import init_cache
from .tools.analysis import register_analysis_tools


# Initialize FastF1 cache
init_cache()

# Create MCP server instance
mcp = FastMCP("FastF1 MCP Server")

# Register all tools
register_analysis_tools(mcp)


def main():
    """Main entry point for the FastF1 MCP server"""
    print("Starting FastF1 MCP Server...")
    print("Available tools:")
    print("  - compare_qualifying_laps: Compare top 3 qualifying laps with telemetry")
    print("  - visualize_tyre_strategy: Create tyre strategy visualization for a race")
    print("\nServer ready!")
    mcp.run()


if __name__ == "__main__":
    main()
