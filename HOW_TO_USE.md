# How to Access Your FastF1 MCP Server in VS Code

## ✅ Server Configuration Complete

Your MCP server is now configured in:
- `/home/sandeep/Desktop/f1_mcp/.vscode/settings.json`
- `/home/sandeep/Desktop/f1_mcp/.vscode/mcp.json`

## 🔄 Step 1: Reload VS Code

Press `Ctrl+Shift+P` and type: **"Developer: Reload Window"**

This will reload VS Code and load your MCP server configuration.

## 🤖 Step 2: Access Through GitHub Copilot Chat

Your FastF1 MCP server tools will appear in **GitHub Copilot Chat**.

### Option A: Via Chat Interface

1. Open GitHub Copilot Chat (Click the chat icon in the sidebar or press `Ctrl+Alt+I`)
2. Look for the **tools/attachments icon** (📎 or 🔧) in the chat input
3. You should see **"fastf1"** as an available MCP server
4. Click to enable it, then ask questions like:
   ```
   @fastf1 Compare the top 3 qualifying laps from 2024 Monaco GP
   ```

### Option B: Direct Tool Call

In Copilot Chat, type:
```
Use the compare_qualifying_laps tool to analyze 2024 Monaco qualifying
```

### Option C: Using MCP Explorer Extension

If you installed the MCP Explorer extension:

1. Open Command Palette (`Ctrl+Shift+P`)
2. Type: **"MCP: Show Servers"**
3. You should see "fastf1" listed
4. Click to view available tools

## 🛠️ Available Tools

### compare_qualifying_laps

**What it does:**
- Loads qualifying session data
- Finds top 3 fastest drivers
- Generates telemetry comparison visualizations
- Creates PNG with 3 plots: Speed, Throttle/Brake, Detailed Speed

**Example usage in Copilot Chat:**
```
Compare qualifying laps for Monaco 2024
```

**Parameters:**
- `year`: 2024 (integer)
- `race`: "Monaco" (string)
- `session`: "Q" (string, optional, default is "Q")

**Returns:**
- Summary with driver names and lap times
- Path to saved PNG visualization

## 🐛 Troubleshooting

### Can't see the MCP server?

1. **Check if Copilot MCP extension is installed:**
   - Install: `automatalabs.copilot-mcp` extension
   - Or install: `moonolgerdai.mcp-explorer` extension

2. **Reload VS Code:**
   - Press `Ctrl+Shift+P`
   - Type: "Developer: Reload Window"

3. **Check settings are correct:**
   - Open `.vscode/settings.json`
   - Verify paths are absolute and correct

4. **Verify server works standalone:**
   ```bash
   cd /home/sandeep/Desktop/f1_mcp
   python test_server.py
   ```

### Server not responding?

1. **Check the terminal output** - MCP servers log to VS Code Output panel
2. **Look for errors** in: View → Output → Select "MCP" from dropdown
3. **Verify Python environment**:
   ```bash
   /home/sandeep/Desktop/f1_mcp/f1_env/bin/python -m server --help
   ```

### Tool calls failing?

- Ensure internet connection (FastF1 downloads data)
- First run may be slow (building cache)
- Check race name spelling: "Monaco", "Monza", "Bahrain", etc.
- Valid years: 2018-2025

## 📚 Next Steps

1. **Install MCP Extensions** (recommended):
   ```
   Ctrl+Shift+P → "Extensions: Install Extensions"
   Search: "Copilot MCP" or "MCP Explorer"
   ```

2. **Reload VS Code** after installing extensions

3. **Test the server**:
   - Open Copilot Chat
   - Try: "Use FastF1 to compare 2024 Monaco qualifying"

4. **Add more tools** to the server (see notebook for ideas!)

## 🎯 Quick Test Commands

Try these in GitHub Copilot Chat:

```
Compare qualifying for 2024 Monaco Grand Prix
```

```
Analyze top 3 drivers from 2024 Monza qualifying
```

```
Show me telemetry comparison for 2024 Silverstone qualifying
```

## 📖 Alternative: Manual MCP Inspector

If you prefer testing outside VS Code:

```bash
cd /home/sandeep/Desktop/f1_mcp/mcp_f1
npx @modelcontextprotocol/inspector /home/sandeep/Desktop/f1_mcp/f1_env/bin/python -m server
```

This opens a web UI at `http://localhost:5173` for testing MCP tools directly.
