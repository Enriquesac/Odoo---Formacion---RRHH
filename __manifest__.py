{
    'name': 'Formacion y RRHH (SGI)',
    'version': '19.0.1.0.0',
    'summary': 'Personas, puestos, organigrama, altas/bajas, asignaciones, requisitos, matriz polivalencia y plan de formacion',
    'description': """
Formacion y RRHH compatible Odoo 18 y 19 (mismo codigo, version 19.0 para tu 19).
Basado en Suite-SGI: js/modules/formacion.js + js/shared/personas.js + js/shared/puestos.js.
Personas vinculadas a hr.employee (opcional), puestos vinculados a hr.job (opcional).
Valoracion persona x puesto 0-4, matriz polivalencia titular/polivalencia, plan con eficacia.
Para CasaOS: /DATA/AppData/big-bear-odoo/data/addons/formacion_rrhh -> /mnt/extra-addons
    """,
    'author': 'Formacion SGI',
    'category': 'Custom/RRHH',
    'depends': ['base', 'mail', 'hr'],
    'data': [
        'security/formacion_security.xml',
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'data/catalogs.xml',
        'data/cron.xml',
        'data/demo.xml',
        'reports/formacion_report.xml',
        'views/rrhh_persona_views.xml',
        'views/rrhh_puesto_views.xml',
        'views/rrhh_valoracion_views.xml',
        'views/formacion_accion_views.xml',
        'views/rrhh_proceso_views.xml',
        'views/rrhh_asignacion_views.xml',
        'views/rrhh_organigrama_views.xml',
        'views/rrhh_menus.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
