# Formación y RRHH (SGI) — Módulo Odoo

Módulo custom de Odoo que lleva al ERP el bloque de **Personas, Puestos y Formación** de la Suite-SGI (ISO 9001/45001/27001): perfiles de personas, organigrama, ficha de la persona, altas y bajas, asignación de recursos, requisitos por puesto, evaluación de requisitos, matriz de polivalencia y plan de formación.

Probado en **Odoo 19.0 Community** sobre **CasaOS (BigBear)** en red local. Código compatible con **Odoo 18 y 19** (mismas fuentes, versión `19.0.x` en el manifiesto para instalar en el 19).

## Origen funcional

Replica `Suite-SGI/js/modules/formacion.js` (dashboard, evaluación, matriz, plan), `Suite-SGI/js/shared/personas.js` (listado, ficha, altas, bajas, asignaciones, configuración RRHH) y `Suite-SGI/js/shared/puestos.js` (puestos, organigrama + versiones, requisitos).

## Qué incluye

- **Personas**: ficha (nombre, apellidos, departamento, email), vínculo opcional a `hr.employee`, fecha de alta/baja, activo, puestos con rol titular/polivalencia, notebook con puestos, valoraciones y asignaciones, % medio de cumplimiento, chatter.
- **Puestos**: vínculo opcional a `hr.job`, jerarquía `depende de` con vista organigrama (`hierarchy`), tareas con nivel esperado 0-4, formación obligatoria/recomendable y habilidades, contadores de titulares y polivalentes.
- **Evaluación de requisitos**: una valoración por persona×puesto, botón **Cargar requisitos del puesto**, líneas de tarea (cumple si nivel ≥ esperado) y de formación/habilidad (check), % con barra de progreso.
- **Matriz de polivalencia**: vista pivot persona×puesto con % de cumplimiento.
- **Plan de formación**: título, objetivo, tipo, formador (catálogo o texto), workflow planificada→en curso→realizada, previstas/reales, fechas, horas, eficacia con criterio y valoración, informe PDF, cron diario de vencidas.
- **Altas y bajas**: procesos con items verificables, botón de generar formación en altas; al completar una baja desactiva a la persona (y al completar un alta la reactiva).
- **Asignaciones**: recursos multiorigen (equipo informático, calibración, mantenimiento, software, activo de información, propio) con entrega/devolución.
- **Organigrama**: versiones snapshot (JSON de puestos + titulares) con botón de captura.
- **Seguridad**: grupos `Formacion Usuario/Gestor` + respaldo para `base.group_user` en todos los modelos.
- **Demos**: 3 puestos jerárquicos, 4 personas, 2 tareas, 1 valoración al 100% y 2 acciones de plan.

## Requisitos

- Odoo 18 o 19 Community.
- App **Empleados** (`hr`) instalada (vínculos opcionales a `hr.employee` / `hr.job`).
- En CasaOS BigBear: volumen de addons en `/mnt/extra-addons` y en `odoo.conf`:
  ```ini
  addons_path = /mnt/extra-addons,/usr/lib/python3/dist-packages/odoo/addons
  ```

## Instalación

1. Copiar la carpeta `formacion_rrhh` (**en minúsculas**, sin doble carpeta `formacion_rrhh/formacion_rrhh`) en `/DATA/AppData/big-bear-odoo/data/addons/`, o subir `formacion_rrhh.zip` y **Extraer**.
2. Reiniciar el contenedor y esperar a `En ejecución`.
3. En Odoo: `Apps → Actualizar lista de aplicaciones → Actualizar` → buscar `Formacion` → **Activar** sin salir de la página.
4. Asignar el grupo en `Ajustes → Técnico → Grupos → Formacion Gestor → Usuarios` (no aparece en la vista simplificada de permisos).
5. Recargar con `Ctrl+Shift+R`. Menú **Formacion** con 10 entradas.

## Estructura

```
formacion_rrhh/__manifest__.py      # 19.0.1.0.0, depends base/mail/hr
formacion_rrhh/models/              # persona, puesto, tarea, valoracion, accion, proceso, asignacion, organigrama, catalogos
formacion_rrhh/views/               # list/form/search/pivot/hierarchy + menus
formacion_rrhh/security/            # grupos (sin category_id) + access con respaldo base.group_user
formacion_rrhh/data/                # sequence FORM/, catalogos, cron, demo.xml
formacion_rrhh/reports/             # QWeb: informe de accion + ficha de persona
```

## Notas de compatibilidad 18/19

Listas con `<list>` (no `<tree>`), chatter con `<chatter/>`, sin `category_id` en grupos ni `numbercall` en cron, claves de `Selection` siempre `str`, referencias XML sin prefijo de módulo, carpeta en minúsculas, sin `graph`/`default_group_by` en `Selection` por limitaciones del build BigBear (dashboard con `pivot`).

## Publicar en GitHub

```bash
git init
git add formacion_rrhh README.md
git commit -m "Modulo Odoo Formacion y RRHH (SGI)"
git branch -M main
git remote add origin <tu-repo>.git
git push -u origin main
```

Licencia: **LGPL-3**.
