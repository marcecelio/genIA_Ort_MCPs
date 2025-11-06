# genIA_Ort_MCPs

Integración entre OpenAI API y FastMCP para el curso de Ingeniería de Aplicaciones GenIA en ORT.

## Descripción

Este proyecto demuestra cómo integrar la API de OpenAI (modelo `gpt-4o-mini`) con FastMCP (Model Context Protocol). Incluye:

- **Servidor MCP** (`server.py`): Expone herramientas como servicios MCP
- **Cliente OpenAI** (`openai_client.py`): Integra OpenAI con las herramientas del servidor MCP

### Herramientas disponibles

1. **say_hello**: Saluda a una persona por su nombre
2. **count_r**: Cuenta las letras 'r' (mayúsculas y minúsculas) en una palabra o frase

## Instalación

1. Instalar dependencias:
```bash
pip install -r requirements.txt
```

2. Publicar el servidor MCP en FastMCP Cloud:
```bash
fastmcp publish server.py
```
   Esto te dará una URL como: `https://tu-servidor.fastmcp.app/mcp`

3. Configurar variables de entorno:
```bash
# Crear archivo .env
type nul > .env
```

   Editar `.env` y agregar:
   ```env
   OPENAI_API_KEY=tu_api_key_de_openai
   MCP_SERVER_URL=https://tu-servidor.fastmcp.app/mcp
   FAST_MCP_API_KEY=tu_api_key_de_fastmcp  # Opcional si el servidor requiere auth
   ```

4. Obtener tu API key de OpenAI en: https://platform.openai.com/api-keys

## Uso

### Servidor MCP (modo standalone)

Para ejecutar el servidor MCP en modo stdio:

```bash
python server.py
```

### Cliente OpenAI + MCP

Para ejecutar la integración completa con OpenAI:

```bash
python openai_client.py
```

Este script:
- Ejecuta algunos ejemplos predefinidos
- Entra en modo interactivo donde puedes hacer preguntas
- El modelo GPT-4o-mini usará automáticamente las herramientas MCP cuando sea necesario

### Ejemplos de uso

```
Usuario: ¿Cuántas letras 'r' hay en la palabra 'desarrollador'?
Asistente: [Usa la tool count_r] La palabra 'desarrollador' contiene 3 letra(s) 'r'.

Usuario: Cuenta las letras r en: 'Roma es una ciudad hermosa'
Asistente: [Usa la tool count_r] La frase contiene 2 letra(s) 'r'.
```

## Arquitectura

```
┌─────────────────┐
│   Usuario       │
└────────┬────────┘
         │
         ▼
┌─────────────────────────┐
│  openai_client.py       │
│  (OpenAI gpt-4o-mini)   │
└────────┬────────────────┘
         │ (FastMCP Client)
         ▼
┌─────────────────────────┐
│  FastMCP Cloud          │
│  server.py publicado    │
│  - say_hello            │
│  - count_r              │
└─────────────────────────┘
```

**Flujo:**
1. Usuario hace una pregunta al cliente OpenAI
2. OpenAI decide si necesita usar una tool
3. El cliente se conecta al servidor MCP publicado en FastMCP Cloud
4. Ejecuta la tool remotamente (count_r, say_hello, etc.)
5. Devuelve el resultado a OpenAI
6. OpenAI formula la respuesta final

## Referencias

- [FastMCP Documentation](https://gofastmcp.com/)
- [OpenAI Integration Guide](https://gofastmcp.com/integrations/openai)
- [OpenAI API Documentation](https://platform.openai.com/docs)