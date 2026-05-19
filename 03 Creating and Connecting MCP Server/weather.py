from mcp.server.fastmcp import FastMCP

mcp = FastMCP("weather")  ## initialize the mcp server


# defining the mcp tools to acceded by the mcp server
@mcp.tool()
def get_weather(location: str)->str:
        return "The Weather is hot and dry"


if __name__=="__main__":
        mcp.run()