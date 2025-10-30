from fastmcp import FastMCP

mcp = FastMCP("My MCP Server")

@mcp.tool
def say_hello(name: str) -> str:
    return f"Hello, {name}!"

if __name__ == "__main__":
    mcp.run(transport="stdio")