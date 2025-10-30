import asyncio
from fastmcp import Client

# Opción 1: Usar stdio - pasar el nombre del archivo del servidor
# FastMCP maneja automáticamente el transporte stdio
client = Client("server.py")

# Opción 2: Usar HTTP local si el servidor está corriendo en puerto 8000
# client = Client("http://localhost:8000/mcp")

async def call_tool(name: str):
    async with client:
        # Nota: el nombre del tool debe coincidir con el definido en server.py
        result = await client.call_tool("say_hello", {"name": name})
        print(result)

asyncio.run(call_tool("Ford"))