# FastF1 MCP Server - Configuration Guide

## Testing Your MCP Server

### Option 1: Using MCP Inspector (Recommended for Development)

The MCP Inspector allows you to test your server interactively:

```bash
# Activate your virtual environment first
source /home/sandeep/Desktop/f1_mcp/f1_env/bin/activate

# Run the MCP Inspector
npx @modelcontextprotocol/inspector /home/sandeep/Desktop/f1_mcp/f1_env/bin/python -m server
```

**Or use the mcp dev command:**
```bash
cd /home/sandeep/Desktop/f1_mcp/mcp_f1
/home/sandeep/Desktop/f1_mcp/f1_env/bin/python -m mcp dev
```

### Option 2: Claude Desktop Integration

To use your MCP server with Claude Desktop, add this configuration:

**Location:** `~/.config/Claude/claude_desktop_config.json` (Linux)

```json
{
  "mcpServers": {
    "fastf1": {
      "command": "/home/sandeep/Desktop/f1_mcp/f1_env/bin/python",
      "args": [
        "-m",
        "server"
      ],
      "cwd": "/home/sandeep/Desktop/f1_mcp/mcp_f1",
      "env": {
        "PYTHONPATH": "/home/sandeep/Desktop/f1_mcp/mcp_f1"
      }
    }
  }
}
```

### Option 3: VS Code Testing with Python Script

Create a simple test without MCP protocol overhead:

```bash
cd /home/sandeep/Desktop/f1_mcp
/home/sandeep/Desktop/f1_mcp/f1_env/bin/python test_server.py
```

## Server Commands

**Start the server (stdio mode):**
```bash
cd /home/sandeep/Desktop/f1_mcp/mcp_f1
/home/sandeep/Desktop/f1_mcp/f1_env/bin/python -m server
```

**Test the tool directly:**
```bash
python test_server.py
```

## Available MCP Tools

### compare_qualifying_laps

Compare top 3 qualifying drivers with telemetry visualization.

**Example request via Claude:**
```
Compare the top 3 qualifying laps from the 2024 Monaco Grand Prix
```

**Parameters:**
- `year`: 2024
- `race`: "Monaco"
- `session`: "Q" (default)

**Returns:**
- Driver names and lap times
- Path to PNG visualization with:
  - Speed comparison plot
  - Throttle/Brake dual y-axis plot
  - Detailed speed trace

## Troubleshooting

### Server not starting
- Ensure you're in the correct directory: `/home/sandeep/Desktop/f1_mcp/mcp_f1`
- Check Python environment: `/home/sandeep/Desktop/f1_mcp/f1_env/bin/python`
- Verify all dependencies installed: `pip list | grep -E "fastf1|mcp|matplotlib"`

### MCP Inspector not working
- Install Node.js if not available: `sudo apt install nodejs npm`
- Run: `npx @modelcontextprotocol/inspector --help`

### Telemetry data not loading
- Check internet connection (FastF1 downloads data from F1 API)
- Cache may be building first time (slower)
- Verify race name/year are correct

## Next Steps

1. Install MCP Inspector or Copilot MCP extension
2. Test with `python test_server.py` first
3. Use MCP Inspector for interactive testing
4. Configure Claude Desktop for production use
5. Add more tools to the server!
