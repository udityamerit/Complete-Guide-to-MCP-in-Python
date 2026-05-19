from mcp.server.fastmcp import FastMCP

mcp = FastMCP("weather")  ## initialize the mcp server


# defining the mcp tools to acceded by the mcp server
@mcp.tool()
def get_weather(location: str)->str:
        """
        Gets the weather given a location
        Args:
                location: location, can be city, country, state, etc.
        """
        return f"The Weather of your {location} is hot and dry"


if __name__=="__main__":
        mcp.run()