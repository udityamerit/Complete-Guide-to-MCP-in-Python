
# MCP Server Setup using UV

## What is UV?

[uv](https://docs.astral.sh/uv/) is a fast Python package and project manager written in Rust.

It is used to:

- Create and manage Python projects
- Install dependencies
- Manage virtual environments
- Run Python applications efficiently
- Replace tools like `pip`, `venv`, and `poetry` with a much faster alternative

UV helps developers set up projects quickly and manage dependencies in a clean and organized way.

---

# Setting Up an MCP Server

## Step 1: Install UV and Initialize the Project

First, install `uv` on your system.

Then initialize your project using:

```bash
uv init
```

This command initializes the current folder as a Python project.

---

## Step 2: Install MCP Dependency

Install the MCP dependency using:

```bash
uv add mcp[cli]
```

This installs the MCP package along with its CLI tools.

---

## Step 3: Create Your MCP Server

Create a Python file for your MCP server, for example:

```bash
weather.py
```

Inside the file:

- Import the `FastMCP` server
- Initialize the MCP server
- Create and register tools/functions

Example:

```python
        see the weather.py
```

You can use this structure to create your own MCP tools and servers.

---

# Connecting MCP Server to Claude

## Step 4: Configure Claude Desktop

1. Open **Claude Desktop**
2. Go to **Settings**
3. Open **Developer Settings**
4. Click **Edit Config**
5. Open the `claude_desktop_config.json` file
6. Paste the following configuration:

```json
{
  "mcpServers": {
    "weather": {
      "command": "uv",
      "args": [
        "--directory",
        ".",
        "run",
        "weather.py"
      ]
    }
  }
}
```

---

# Alternative Easy Method

An easier way to connect a locally created MCP server to Claude or any MCP host is:

1. Activate your virtual environment
2. Run:

```bash
mcp install weather.py
```

This command automatically:

- Installs the local MCP server
- Updates the developer configuration
- Connects the server to Claude Desktop

After this, you can directly use your locally built MCP server inside Claude.

---

# Useful Commands

## Initialize Project

```bash
uv init
```

## Install Dependency

```bash
uv add mcp[cli]
```

## Run MCP Server

```bash
uv run weather.py
```

## Install MCP Server

```bash
mcp install weather.py
```

---

# References

- MCP Documentation: https://modelcontextprotocol.io/
- UV Documentation: https://docs.astral.sh/uv/
