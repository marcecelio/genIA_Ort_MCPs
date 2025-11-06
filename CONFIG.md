# Configuración del Proyecto

## Variables de Entorno

Este proyecto requiere configurar las siguientes variables de entorno. Crea un archivo `.env` en la raíz del proyecto con el siguiente contenido:

```env
# OpenAI API Key (OBLIGATORIO)
# Obtén tu API key en: https://platform.openai.com/api-keys
OPENAI_API_KEY=tu_openai_api_key_aqui

# URL del servidor MCP publicado en FastMCP Cloud (OBLIGATORIO)
# Ejemplo: https://my-mcp-server.fastmcp.app/mcp
MCP_SERVER_URL=https://tu-servidor.fastmcp.app/mcp

# FastMCP API Key (OPCIONAL - solo si tu servidor requiere autenticación)
FAST_MCP_API_KEY=tu_fastmcp_api_key_aqui
```

## Pasos para configurar

1. **Crear el archivo .env**
   ```bash
   # En Windows
   type nul > .env
   
   # En Linux/Mac
   touch .env
   ```

2. **Editar el archivo .env**
   - Abre el archivo `.env` con tu editor de texto favorito
   - Agrega tu API key de OpenAI (obligatorio)
   - Agrega la URL de tu servidor MCP publicado (obligatorio)
   - La API key de FastMCP es opcional (solo si tu servidor requiere autenticación)

3. **Obtener tu API Key de OpenAI**
   - Ve a https://platform.openai.com/api-keys
   - Inicia sesión o crea una cuenta
   - Crea una nueva API key
   - Copia la key y pégala en el archivo .env

4. **Publicar tu servidor MCP en FastMCP Cloud**
   - Ejecuta: `fastmcp publish server.py`
   - Sigue las instrucciones para publicar tu servidor
   - Copia la URL del servidor publicado (ejemplo: https://my-server.fastmcp.app/mcp)
   - Pégala en el archivo .env como `MCP_SERVER_URL`

## Verificación

Para verificar que tu configuración es correcta, ejecuta:

```bash
python openai_client.py
```

Si ves el mensaje "✅ API Key de OpenAI configurada", todo está funcionando correctamente.

## Seguridad

⚠️ **IMPORTANTE**: 
- Nunca compartas tu archivo `.env` en control de versiones
- El archivo `.env` debe estar en `.gitignore`
- No compartas tus API keys con nadie

