# Módulos Odoo a medida — SGI (Sistema de Gestión Integrado)

Módulos custom de Odoo desarrollados como proyecto de formación y prueba de hasta dónde llega el desarrollo a medida en Odoo. Migran a Odoo la lógica de la **Suite-SGI** (apps HTML/JS de gestión ISO 9001 / 14001 / 45001 / 27001).

Probados en **Odoo 19.0 Community** sobre **CasaOS (BigBear)** en red local (`http://192.168.1.90:8069`). Código compatible con **Odoo 18 y 19** (mismas fuentes, versión `19.0.x` en el manifiesto para instalar en el 19).

## Módulos

| Carpeta | Nombre en Odoo | Qué hace | Depende de |
|---|---|---|---|
| `sgi_demo` | SGI Demo - No Conformidades | Gestión de No Conformidades en 5 pasos (datos → reparadoras → causas → correctivas → eficacia), 28 tipologías ISO, workflow `Abierta → En proceso → Pendiente Verificación → Cerrada`, secuencia `NC/AAAA/0001`, informe PDF QWeb, dashboard pivot, cron de plazos vencidos | `base`, `mail` |
| `sgsi` | SGSI - Seguridad de la Información (ISO 27001) | Activos (C-I-D 1-10), amenazas (impacto×probabilidad), revisiones de análisis con umbral, matriz activo×amenaza con cálculo `valor=(C+I+D)·(I×P)`, tratamientos multi-riesgo con seguimiento, software aprobado, equipos TI **reutilizando `maintenance.equipment`** (sin duplicar), informe PDF, cron de pendientes | `base`, `mail`, `maintenance` |
| `formacion_rrhh` | Formación y RRHH (SGI) | Personas (vinculadas a `hr.employee`), puestos jerárquicos (vinculados a `hr.job`, vista organigrama), requisitos por puesto con niveles 0-4, evaluación persona×puesto con % cumplimiento, matriz de polivalencia (pivot), plan de formación con eficacia, procesos de alta/baja, asignaciones de recursos, versiones snapshot de organigrama, informes PDF | `base`, `mail`, `hr` |
| `sgi_hello` | SGI Hello (Test) | Módulo mínimo de prueba de detección de addons, sin uso productivo | `base` |

Todos incluyen datos demo instalables y grupos de seguridad `Usuario/Gestor` + respaldo para `base.group_user`.

## Requisitos

- Odoo 18 o 19 Community (probado en `19.0-20251121`).
- Apps estándar instaladas según dependencias: **Debate** (`mail`), **Mantenimiento** (`maintenance`), **Empleados** (`hr`).
- Si usas CasaOS BigBear: volumen de addons personalizados montado en `/mnt/extra-addons` y esta línea en `odoo.conf`:
  ```ini
  addons_path = /mnt/extra-addons,/usr/lib/python3/dist-packages/odoo/addons
  ```

## Instalación (CasaOS)

1. En **Archivos** ve a `/DATA/AppData/big-bear-odoo/data/addons/` (carpeta en **minúsculas**, p. ej. `sgsi`, nunca `SGSI`: en Linux el nombre de carpeta es el nombre técnico y las referencias son sensibles a mayúsculas).
2. Copia dentro la carpeta del módulo (o sube el `.zip` y **Extrae**). Debe quedar `.../addons/sgsi/__manifest__.py`, sin doble carpeta `sgsi/sgsi/`.
3. **Reinicia** el contenedor `big-bear-odoo` y espera a `En ejecución`.
4. En Odoo: `Apps → Actualizar lista de aplicaciones → Actualizar` → busca el módulo → **Activar** sin salir de la página (la instalación puede tardar 1-3 min).
5. Asigna grupos al usuario en `Ajustes → Técnico → Grupos` (`SGSI Gestor`, `Formacion Gestor`...), ya que al no usar categoría no salen en la vista simplificada de permisos.
6. Refresca con `Ctrl+Shift+R`.

## Estructura de cada módulo

```
<modulo>/__manifest__.py      # version 19.0.x, depends, data en orden
<modulo>/models/              # modelos + computes + constraints + workflow + cron
<modulo>/views/               # list/form/search/pivot + menus (sin kanban/graph por defecto)
<modulo>/security/            # grupos (sin category_id) + ir.model.access.csv con respaldo base.group_user
<modulo>/data/                # sequence.xml, catalogs.xml, cron.xml, demo.xml
<modulo>/reports/             # informes QWeb PDF
<modulo>/static/description/icon.png
```

## Notas de compatibilidad 18/19 (lecciones del proyecto)

- Vistas de lista con `<list>`, nunca `<tree>` (el 19 lo rechaza).
- Kanban con `t-name="card"` y sin `default_group_by` sobre `Selection` (provoca `OwlError` / salida del módulo en este build).
- Sin `graph` en `view_mode` por defecto (falla `chartjs_lib` en BigBear); dashboard con `pivot`.
- Chatter con `<chatter/>`, no `oe_chatter`.
- Sin campo `numbercall` en `ir.cron` (eliminado en 19) ni `category_id` en `res.groups`.
- Claves de `Selection` siempre `str` (los enteros dan `Error de validación`).
- Referencias XML internas sin prefijo de módulo (`ref="group_..."`, no `ref="sgsi.group_..."`).
- Sin `widget="badge"` dentro de `list editable` (lo deja solo-lectura).

## Publicar en GitHub

```bash
git init
git add sgi_demo sgsi formacion_rrhh README.md
git commit -m "Modulos Odoo SGI: sgi_demo, sgsi, formacion_rrhh"
git branch -M main
git remote add origin <tu-repo>.git
git push -u origin main
```

No subir los `.zip` (se regeneran) ni credenciales. Licencia de los módulos: **LGPL-3**.
