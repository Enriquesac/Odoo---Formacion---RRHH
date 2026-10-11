from odoo import models, fields

class RrhhAsignacion(models.Model):
    _name = 'rrhh.asignacion'
    _description = 'Asignacion de Recurso a Persona'
    _inherit = ['mail.thread']
    _order = 'fecha_entrega desc'

    persona_id = fields.Many2one('rrhh.persona', required=True, tracking=True)
    tipo = fields.Selection([('eq_info', 'Equipo informatico'), ('eq_cal', 'Equipo calibracion'),
                             ('eq_mant', 'Equipo mantenimiento'), ('software', 'Software'),
                             ('activo', 'Activo informacion'), ('propio', 'Recurso propio')],
                            required=True, default='propio')
    recurso_nombre = fields.Char(string='Recurso', required=True)
    recurso_codigo = fields.Char(string='Codigo')
    fecha_entrega = fields.Date(string='Fecha entrega', default=fields.Date.context_today)
    estado = fields.Selection([('asignado', 'Asignado'), ('devuelto', 'Devuelto')], default='asignado', tracking=True)
    fecha_devolucion = fields.Date(string='Fecha devolucion')
    observaciones = fields.Text()
    company_id = fields.Many2one(related='persona_id.company_id', store=True, readonly=True)

    def action_devolver(self):
        self.write({'estado': 'devuelto', 'fecha_devolucion': fields.Date.context_today(self)})
        return True
