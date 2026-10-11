from odoo import models, fields, api

class RrhhPersona(models.Model):
    _name = 'rrhh.persona'
    _description = 'Persona SGI'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'apellidos, name'

    name = fields.Char(string='Nombre', required=True, tracking=True)
    apellidos = fields.Char(string='Apellidos')
    nombre_completo = fields.Char(compute='_compute_completo', store=True)
    email = fields.Char()
    departamento = fields.Char()
    employee_id = fields.Many2one('hr.employee', string='Empleado vinculado')
    fecha_alta = fields.Date(string='Fecha alta', default=fields.Date.context_today)
    fecha_baja = fields.Date(string='Fecha baja')
    activo = fields.Boolean(default=True, tracking=True)
    puesto_rel_ids = fields.One2many('rrhh.persona.puesto', 'persona_id', string='Puestos')
    valoracion_ids = fields.One2many('rrhh.valoracion', 'persona_id', string='Valoraciones')
    asignacion_ids = fields.One2many('rrhh.asignacion', 'persona_id', string='Asignaciones')
    cumplimiento_medio = fields.Float(compute='_compute_cumplimiento', string='% medio')
    active = fields.Boolean(default=True)
    company_id = fields.Many2one('res.company', default=lambda self: self.env.company)

    @api.depends('name', 'apellidos')
    def _compute_completo(self):
        for r in self:
            r.nombre_completo = ((r.name or '') + ' ' + (r.apellidos or '')).strip()

    @api.depends('valoracion_ids.cumplimiento')
    def _compute_cumplimiento(self):
        for r in self:
            vals = r.valoracion_ids.mapped('cumplimiento')
            r.cumplimiento_medio = round(sum(vals) / len(vals), 1) if vals else 0.0


class RrhhPersonaPuesto(models.Model):
    _name = 'rrhh.persona.puesto'
    _description = 'Puesto de Persona con Rol'
    _order = 'puesto_id'

    persona_id = fields.Many2one('rrhh.persona', required=True, ondelete='cascade')
    puesto_id = fields.Many2one('rrhh.puesto', required=True, ondelete='restrict')
    rol = fields.Selection([('titular', 'Titular'), ('polivalencia', 'Polivalencia')], default='titular', required=True)
    company_id = fields.Many2one(related='persona_id.company_id', store=True, readonly=True)

    _sql_constraints = [('uniq_pers_puesto', 'unique(persona_id, puesto_id)', 'Ese puesto ya esta asignado a la persona')]
