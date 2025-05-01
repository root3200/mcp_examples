import os
import asyncio
from typing import Any
import httpx
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

# Carga variables del .env
load_dotenv()
BASE_URL = os.getenv("ANSIBLE_BASE_URL").rstrip("/")
TOKEN    = os.getenv("ANSIBLE_TOKEN")

# Inicializa el servidor MCP
mcp = FastMCP("ansible_tower")

# Encabezados comunes para AWX
HEADERS = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}

async def awx_request(method: str, path: str, json: Any = None) -> dict:
    """Llama a la API de AWX y devuelve el JSON."""
    url = f"{BASE_URL}/api/v2/{path.lstrip('/')}"
    async with httpx.AsyncClient(verify=False) as client:
        resp = await client.request(method, url, headers=HEADERS, json=json, timeout=30)
        resp.raise_for_status()
        return resp.json()

# — Herramientas MCP —

@mcp.tool()
async def list_inventories(limit: int = 20, offset: int = 0) -> list[dict]:
    """
    Lista inventarios de AWX.

    Args:
        limit: número máximo de resultados.
        offset: desplazamiento para paginación.
    """
    data = await awx_request("get", f"inventories/?limit={limit}%26offset={offset}")
    return data["results"]

@mcp.tool()
async def get_inventory(inventory_id: int) -> dict:
    """Obtiene detalles de un inventario."""
    return await awx_request("get", f"inventories/{inventory_id}/")

@mcp.tool()
async def list_job_templates(limit: int = 20, offset: int = 0) -> list[dict]:
    """Lista plantillas de job."""
    data = await awx_request("get", f"job_templates/?limit={limit}%26offset={offset}")
    return data["results"]

@mcp.tool()
async def launch_job(template_id: int, extra_vars: dict[str, Any] = {}) -> dict:
    """
    Lanza un job a partir de una plantilla.

    Args:
        template_id: ID de la plantilla.
        extra_vars: variables extra para el job.
    """
    payload = {"extra_vars": extra_vars}
    return await awx_request("post", f"job_templates/{template_id}/launch/", json=payload)

@mcp.tool()
async def get_job_status(job_id: int) -> str:
    """Consulta el estado de un job."""
    job = await awx_request("get", f"jobs/{job_id}/")
    return job.get("status", "unknown")

@mcp.tool()
async def get_job_stdout(job_id: int, format: str = "txt") -> str:
    """
    Recupera la salida estándar de un job.

    Args:
        job_id: ID del job.
        format: txt, html, json o ansi.
    """
    resp = await awx_request("get", f"jobs/{job_id}/stdout/?format={format}")
    return resp  # devuelve texto plano o JSON según el formato

# — Ejecuta el servidor —

if __name__ == "__main__":
    # Usa stdio para transporte (compatible con Claude Desktop, CLI MCP, etc.)
    mcp.run(transport="stdio")
