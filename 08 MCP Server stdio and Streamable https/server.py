from mcp.server.fastmcp import FastMCP

mcp = FastMCP("server")


@mcp.tool()
def greeting(name: str) -> str:
    "send a greeting"
    return f"hi {name}"

if __name__=="__main__":
    mcp.run(transport="streamable-http")


# https://www.npmjs.com/package/mcp-remote refer this for the more details

