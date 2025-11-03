import asyncio
import os
from fastmcp import Client, FastMCP
from dotenv import load_dotenv

load_dotenv()

# Obtener el API key de una variable de entorno
# IMPORTANTE: Obtén el API key desde el dashboard de FastMCP después de publicar tu servidor
# Configúralo en un archivo .env con: FAST_MCP_API_KEY=tu_api_key_aqui
api_key = os.getenv("FAST_MCP_API_KEY", "")

# Configurar el cliente con autenticación
# FastMCP Client acepta el parámetro 'auth' para autenticación
if api_key:
    client = Client(
        "https://say-hello-mcp-server.fastmcp.app/mcp",
        auth=api_key
    )
    print("✓ Cliente configurado con autenticación")
else:
    client = Client("https://say-hello-mcp-server.fastmcp.app/mcp")
    print("⚠️  ADVERTENCIA: No se encontró API key (FAST_MCP_API_KEY).")
    print("   El servidor publicado requiere autenticación (error 401).")
    print("   Configura la variable de entorno FAST_MCP_API_KEY en tu archivo .env")

async def main():
    async with client:
        # Ensure client can connect
        await client.ping()

        # List available operations
        tools = await client.list_tools()
        resources = await client.list_resources()
        prompts = await client.list_prompts()

        print("tools:")
        print(tools)
        print("resources:")
        print(resources)
        print("prompts:")
        print(prompts)  

        # Ex. execute a tool call
        result = await client.call_tool("say_hello", {"name": "pepe"})
        print(result)

asyncio.run(main())