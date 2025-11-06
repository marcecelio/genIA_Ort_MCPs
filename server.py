from fastmcp import FastMCP

mcp = FastMCP("My MCP Server")

@mcp.tool
def say_hello(name: str) -> str:
    """Saluda a una persona por su nombre."""
    return f"Hello, {name}!"

@mcp.tool
def count_r(text: str) -> str:
    """Cuenta cuántas letras 'r' (mayúsculas y minúsculas) hay en un texto.
    
    Args:
        text: La palabra o frase en la que se contarán las letras 'r'
        
    Returns:
        Un mensaje indicando cuántas letras 'r' se encontraron
    """
    count = text.lower().count('r')
    return f"La frase '{text}' contiene {count} letra(s) 'r'."

if __name__ == "__main__":
    mcp.run(transport="stdio")