import asyncio
import os
import json
from openai import AsyncOpenAI
from fastmcp import Client
from dotenv import load_dotenv

load_dotenv()

# Configurar el cliente de OpenAI
openai_client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# URL de tu servidor publicado en FastMCP Cloud
# IMPORTANTE: Reemplaza esta URL con la URL de tu servidor publicado
MCP_SERVER_URL = os.getenv("MCP_SERVER_URL", "https://tu-servidor.fastmcp.app/mcp")
FAST_MCP_API_KEY = os.getenv("FAST_MCP_API_KEY", "")

# Crear el cliente para conectarse al servidor publicado
if FAST_MCP_API_KEY:
    mcp_client = Client(MCP_SERVER_URL, auth=FAST_MCP_API_KEY)
else:
    mcp_client = Client(MCP_SERVER_URL)


async def chat_with_tools(user_message: str):
    """
    Envía un mensaje a OpenAI y permite que use las tools del servidor MCP remoto.
    """
    async with mcp_client:
        # Obtener las tools del servidor remoto
        tools_list = await mcp_client.list_tools()
        
        # Convertir las tools al formato de OpenAI
        tools = []
        for tool in tools_list.tools:
            tools.append({
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description or "",
                    "parameters": tool.inputSchema
                }
            })
        
        print(f"\n{'='*60}")
        print(f"Usuario: {user_message}")
        print(f"{'='*60}\n")
        
        # Crear el historial de mensajes
        messages = [
            {
                "role": "user",
                "content": user_message
            }
        ]
        
        # Loop para manejar múltiples llamadas de tools
        max_iterations = 5
        iteration = 0
        
        while iteration < max_iterations:
            iteration += 1
            
            # Llamar a OpenAI con las tools disponibles
            response = await openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                tools=tools,
                tool_choice="auto"
            )
            
            assistant_message = response.choices[0].message
            
            # Agregar la respuesta del asistente al historial
            messages.append(assistant_message)
            
            # Si no hay tool calls, terminamos
            if not assistant_message.tool_calls:
                print(f"Asistente: {assistant_message.content}\n")
                return assistant_message.content
            
            # Procesar cada tool call
            for tool_call in assistant_message.tool_calls:
                tool_name = tool_call.function.name
                tool_args_str = tool_call.function.arguments
                
                print(f"🔧 Ejecutando tool remota: {tool_name}")
                print(f"   Argumentos: {tool_args_str}")
                
                # Parsear los argumentos JSON
                tool_args = json.loads(tool_args_str)
                
                # Ejecutar la tool en el servidor remoto
                result = await mcp_client.call_tool(tool_name, tool_args)
                
                # Extraer el contenido del resultado
                result_content = ""
                if hasattr(result, 'content') and len(result.content) > 0:
                    result_content = result.content[0].text
                else:
                    result_content = str(result)
                
                print(f"   Resultado: {result_content}\n")
                
                # Agregar el resultado al historial
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": tool_name,
                    "content": result_content
                })
        
        print("⚠️ Se alcanzó el número máximo de iteraciones")
        return None


async def main():
    """
    Función principal para demostrar el uso de la integración OpenAI + FastMCP
    """
    print("\n" + "="*60)
    print("INTEGRACIÓN OpenAI API + FastMCP Cloud")
    print("Modelo: gpt-4o-mini")
    print("="*60)
    
    # Verificar que tenemos la API key de OpenAI
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ ERROR: No se encontró OPENAI_API_KEY en las variables de entorno")
        print("   Por favor, configura tu API key en el archivo .env")
        return
    
    print("✅ API Key de OpenAI configurada")
    
    # Verificar que tenemos la URL del servidor MCP
    if MCP_SERVER_URL == "https://tu-servidor.fastmcp.app/mcp":
        print("⚠️  ADVERTENCIA: Debes configurar MCP_SERVER_URL con la URL de tu servidor publicado")
        print("   En el archivo .env, agrega: MCP_SERVER_URL=https://tu-servidor.fastmcp.app/mcp")
        return
    
    print(f"✅ Servidor MCP: {MCP_SERVER_URL}")
    
    if FAST_MCP_API_KEY:
        print("✅ API Key de FastMCP configurada\n")
    else:
        print("⚠️  Sin API Key de FastMCP (servidor público o local)\n")
    
    # Ejemplos de uso
    ejemplos = [
        "¿Cuántas letras 'r' hay en la palabra 'desarrollador'?",
        "Cuenta las letras r en: 'Roma es una ciudad hermosa'",
        "¿Cuántas r tiene la frase 'Rápido y furioso'?",
    ]
    
    for ejemplo in ejemplos:
        await chat_with_tools(ejemplo)
        print()
    
    # Modo interactivo (opcional)
    print("\n" + "="*60)
    print("MODO INTERACTIVO")
    print("Escribe 'salir' para terminar")
    print("="*60 + "\n")
    
    while True:
        try:
            user_input = input("Tú: ")
            if user_input.lower() in ['salir', 'exit', 'quit']:
                print("\n¡Hasta luego!")
                break
            
            if user_input.strip():
                await chat_with_tools(user_input)
                
        except KeyboardInterrupt:
            print("\n\n¡Hasta luego!")
            break
        except Exception as e:
            print(f"❌ Error: {e}\n")


if __name__ == "__main__":
    asyncio.run(main())

