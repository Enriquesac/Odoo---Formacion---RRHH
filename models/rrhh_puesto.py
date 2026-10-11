from odoo import models, fields, api

class RrhhPuesto(models.Model):
    _name = 'rrhh.puesto'
    _description = 'Puesto de Trabajo'
    _inherit = ['mail.thread']
    _order = 'name'
    _parent_name = 'parent_id'
    _parent_store = True

    name = fields.Char(required=True, tracking=True)
    departamento = fields.Char()
    descripcion = fields.Text()
    job_id = fields.Many2one('hr.job', string='Puesto hr.job vinculado')
    parent_id = fields.Many2one('rrhh.puesto', string='Depende de', ondelete='set null')
    child_ids = fields.One2many('rrhh.puesto', 'parent_id', string='Subordinados')
    parent_path = fields.Char(index=True, unaccent=False)
    tarea_ids = fields.One2many('rrhh.puesto.tarea', 'puesto_id', string='Tareas')
    formacion_obligatoria = fields.Text(string='Formacion obligatoria (una por linea)')
    formacion_recomendable = fields.Text(string='Formacion recomendable (una por linea)')
    habilidades = fields.Text(string='Habilidades (una por linea)')
    titular_count = fields.Integer(compute='_compute_plantilla', string='Titulares')
    polivalencia_count = fields.Integer(compute='_compute_plantilla', string='Polivalentes')
    active = fields.Boolean(default=True)
    company_id = fields.Many2one('res.company', default=lambda self: self.env.company)

    def _compute_plantilla(self):
        Rel = self.env['rrhh.persona.puesto']
        for r in self:
            rels = Rel.search([('puesto_id', '=', r.id), ('persona_id.activo', '=', True)])
            r.titular_count = len(rels.filtered(lambda x: x.rol == 'titular'))
            r.polivalencia_count = len(rels.filtered(lambda x: x.rol == 'polivalencia'))


class RrhhPuestoTarea(models.Model):
    _name = 'rrhh.puesto.tarea'
    _description = 'Tarea de Puesto con Nivel Esperado'
    _order = 'id'

    puesto_id = fields.Many2one('rrhh.puesto', required=True, ondelete='cascade')
    name = fields.Char(string='Descripcion', required=True)
    nivel_esperado = fields.Selection([('0', '0-No'), ('1', '1-Formacion'), ('2', '2-Apoyo'), ('3', '3-Autonomo'), ('4', '4-Formador')], default='3', required=True)
