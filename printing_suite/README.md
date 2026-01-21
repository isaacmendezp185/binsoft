
# Odoo 18 Community – Printing Suite (Gran Formato)

Conjunto de módulos base para la industria de **impresión de gran formato**.
Incluye:
- `print_job_manager`: Gestión de trabajos de impresión.
- `print_composer`: Asistente de composición (wizard) para configurar trabajos.
- `print_materials`: Catálogo de sustratos y materiales.
- `print_costing_engine`: Motor de costeo por m²/tiempo/máquina/tintas.
- `print_workshop`: Operación en taller sobre `print.job` (tablero Kanban y acciones).
- `print_templates`: Plantillas de trabajos repetitivos.
- `print_postproduction`: Control de calidad y postproducción.

> Esta suite es base y está lista para extenderse a requerimientos específicos.

## Instalación
1. Copiar las carpetas de los módulos dentro de tu ruta de addons.
2. Activar modo desarrollador en Odoo, actualizar lista de aplicaciones.
3. Instalar primero `print_materials` y `print_job_manager`, luego el resto.

## Requisitos
- Odoo 18 Community
- Módulos estándar: `base`, `sale`, `stock`, `mrp` (según el módulo).

## Créditos
- Arquitectura y scaffolding generado por M365 Copilot.
