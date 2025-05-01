# AWX MCP Server

Este proyecto implementa un **MCP Server** para interactuar con una instancia de **AWX/Ansible Tower** mediante el protocolo Model Context Protocol (MCP).

## Descripción
- Expone herramientas (`@mcp.tool()`) que permiten listar inventarios, lanzar jobs, consultar estados o recuperar salidas.
- Basado en **FastMCP** y **HTTPX** para llamadas asíncronas a la API de AWX.

## Prerrequisitos
- Python 3.10+
- Acceso a una instancia de AWX/Tower y token de API (o usuario/contraseña) configurados en un fichero `.env`

## Instalación
1. Clona este repositorio.
2. Crea y activa un entorno virtual (opcional pero recomendado):
   ```bash
   python -m venv .venv
   source .venv/bin/activate     # Linux/macOS
   .\.venv\Scripts\Activate.ps1 # Windows PowerShell
   ```
3. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

## Configuración
Configura tus credenciales en un fichero `.env` en la raíz del proyecto:
```dotenv
ANSIBLE_BASE_URL=https://tu-awx.example.com
ANSIBLE_TOKEN=eyJ0eXAiOiJKV1QiLCJh...  # o ANSIBLE_USERNAME y ANSIBLE_PASSWORD
```

## Estructura de archivos
```
awx-mcp-server/
├── README.md
├── requirements.txt
├── .env
└── awx_mcp.py    # Script principal del servidor MCP
```

## Uso
1. Ejecuta el servidor:
   ```bash
   python awx_mcp.py
   ```
2. Desde tu cliente MCP (p. ej. Claude Desktop), configura el servidor:
   ```jsonc
   {
     "mcpServers": {
       "ansible_tower": {
         "command": "python",
         "args": ["/ruta/a/awx_mcp.py"]
       }
     }
   }
   ```
3. En el chat, invoca las herramientas:
   - `list_inventories(limit, offset)`
   - `get_inventory(inventory_id)`
   - `list_job_templates(limit, offset)`
   - `launch_job(template_id, extra_vars)`
   - `get_job_status(job_id)`
   - `get_job_stdout(job_id, format)`

## Herramientas MCP disponibles
| Tool                   | Descripción                                  |
|------------------------|----------------------------------------------|
| `list_inventories`     | Lista inventarios de AWX                    |
| `get_inventory`        | Detalles de un inventario por su ID          |
| `list_job_templates`   | Lista plantillas de jobs                     |
| `launch_job`           | Lanza un job a partir de una plantilla      |
| `get_job_status`       | Consulta el estado de un job                 |
| `get_job_stdout`       | Recupera la salida (stdout) en varios formatos |

## Contribuciones
¡Puedes añadir más herramientas o mejoras! Sigue el mismo patrón `@mcp.tool()` y reinicia el servidor.

---

