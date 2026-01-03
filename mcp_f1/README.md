# FastF1 MCP Server

A Model Context Protocol (MCP) server that provides access to Formula 1 data and telemetry using the FastF1 library.

## Features

- **Qualifying Analysis**: Compare top 3 drivers' qualifying laps with telemetry visualization
- **Speed Maps**: Detailed speed comparison across all drivers
- **Throttle & Brake Analysis**: Combined throttle and brake telemetry on dual y-axis plots

## Installation

```bash
# Install in development mode
pip install -e .
```

## Usage

```bash
# Run the MCP server
fastf1-mcp-server
```

## Tools

### compare_qualifying_laps

Analyzes and compares the top 3 fastest qualifying laps with detailed telemetry visualization.

**Parameters:**
- `year` (int): Season year (e.g., 2024)
- `race` (str): Race name or round number (e.g., 'Monaco', 'Monza', or '1')
- `session` (str, optional): Session type (default: 'Q' for qualifying)

**Returns:**
- Summary of top 3 lap times with driver and team information
- Path to generated visualization PNG file with 3 plots:
  1. Speed comparison (all 3 drivers)
  2. Throttle/Brake combined (dual y-axis)
  3. Speed comparison with telemetry overlay

## Requirements

- Python 3.8+
- FastF1 >= 3.0.0
- Matplotlib >= 3.5.0
- NumPy >= 1.21.0
- MCP SDK >= 0.1.0
