# FastF1 MCP Server

A Model Context Protocol (MCP) server for Formula 1 data analysis using FastF1. This server integrates with VS Code Copilot to provide telemetry analysis and qualifying lap comparisons.

## Features

- 🏎️ **Qualifying Lap Analysis**: Compare top 3 drivers' qualifying laps with detailed telemetry
- 📊 **Telemetry Visualization**: Speed, throttle, and brake application comparisons
- 🎯 **Top 10 Results**: Display qualifying results in a formatted table
- 🖼️ **VS Code Integration**: Visualizations automatically saved to workspace

## Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd f1_mcp
   ```

2. **Create and activate a Python virtual environment**
   ```bash
   python3 -m venv f1_env
   source f1_env/bin/activate  # On Windows: f1_env\Scripts\activate
   ```

3. **Install the MCP server**
   ```bash
   cd mcp_f1
   pip install -e .
   ```

## Usage

The MCP server is configured to work with VS Code Copilot. The configuration files in `.vscode/` directory use `${workspaceFolder}` variables for portability.

### Available Tools

#### `compare_qualifying_laps`
Analyzes qualifying sessions and generates telemetry comparisons.

**Parameters:**
- `year` (int): Season year (e.g., 2024)
- `race` (str): Race name or round number (e.g., 'Monaco', 'Japan', or '1')
- `session` (str, optional): Session type (default: 'Q' for qualifying)

**Example queries in VS Code Copilot:**
- "Fetch me qualifying results map for Japan GP 2025"
- "Show qualifying data for Monaco 2024"
- "Compare qualifying laps for Qatar GP 2024"

## Output

The tool generates:
1. **Top 10 qualifying times table** with driver names, teams, and lap times (mm:ss.ms format)
2. **Telemetry visualization** with 3 plots:
   - Speed comparison across top 3 drivers
   - Throttle application comparison
   - Brake application comparison

Visualizations are saved to `f1_visualizations/` directory in your workspace.

## Project Structure

```
f1_mcp/
├── .vscode/                 # VS Code configuration
│   ├── mcp.json            # MCP server configuration
│   └── settings.json       # Workspace settings
├── mcp_f1/                 # MCP server package
│   ├── server/             # Server implementation
│   │   ├── __init__.py
│   │   ├── __main__.py
│   │   ├── tools/          # MCP tools
│   │   │   ├── __init__.py
│   │   │   └── analysis.py # F1 analysis tools
│   │   └── utils/          # Utility functions
│   │       ├── __init__.py
│   │       └── cache.py    # FastF1 cache management
│   ├── pyproject.toml      # Package configuration
│   └── README.md
├── f1_visualizations/      # Generated plots (gitignored)
├── .gitignore
└── README.md               # This file
```

## Dependencies

- `fastf1` - F1 telemetry data access
- `fastmcp` - MCP framework
- `matplotlib` - Visualization
- `pandas` - Data manipulation
- `numpy` - Numerical computing

All dependencies are automatically installed when you run `pip install -e .` in the `mcp_f1/` directory.

## Configuration

The MCP server is configured in `.vscode/mcp.json` and `.vscode/settings.json`. These files use `${workspaceFolder}` variables to ensure portability across different machines and users.

## Contributing

Feel free to open issues or submit pull requests for improvements!

## License

MIT License
