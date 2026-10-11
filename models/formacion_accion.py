from odoo import models, fields, api, _

class FormacionAccion(models.Model):
    _name = 'formacion.accion'
    _description = 'Accion de Plan de Formacion'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'fecha_prevista, id'

    name = fields.Char(string='Titulo', required=True, tracking=True)
    objetivo = fields.Text()
    tipo = fields.Selection([('necesidad', 'Necesidad'), ('polivalencia', 'Polivalencia'),
                             ('estrategica', 'Estrategica'), ('oportunidad', 'Oportunidad')], default='necesidad')
    formador_id = fields.Many2one('formacion.formador', string='Formador')
    formador_txt = fields.Char(string='Formador (texto)')
    estado = fields.Selection([('planificada', 'Planificada'), ('en_curso', 'En curso'),
                               ('realizada', 'Realizada'), ('cancelada', 'Cancelada')],
                              default='planificada', tracking=True)
    fecha_prevista = fields.Date(string='Fecha prevista')
    horas = fields.Float()
    persona_prev_ids = fields.Many2many('rrhh.persona', 'form_accion_prev_rel', 'accion_id', 'persona_id', string='Personas previstas')
    fecha_real = fields.Date(string='Fecha real inicio')
    fecha_real_fin = fields.Date(string='Fecha real fin')
    persona_ids = fields.Many2many('rrhh.persona', 'form_accion_real_rel', 'accion_id', 'persona_id', string='Asistentes')
    observaciones = fields.Text()
    eficacia = fields.Selection([('eficaz', 'Eficaz'), ('no_eficaz', 'No eficaz')], string='Eficacia')
    criterio_eficacia = fields.Char(string='Criterio')
    valoracion_eficacia = fields.Text(string='Valoracion eficacia')
    proceso_id = fields.Many2one('rrhh.proceso', string='Proceso origen')
    active = fields.Boolean(default=True)
    company_id = fields.Many2one('res.company', default=lambda self: self.env.company)

    def action_en_curso(self):
        self.write({'estado': 'en_curso'})

    def action_realizada(self):
        self.write({'estado': 'realizada'})
        self.message_post(body=_('Accion realizada, pendiente evaluar eficacia'))

    @api.model
    def cron_avisos_vencidas(self):
        hoy = fields.Date.context_today(self)
        vencidas = self.search([('estado', '=', 'planificada'), ('fecha_prevista', '<', hoy)])
        for a in vencidas:
            a.message_post(body=_('Formacion vencida sin realizar'))
            a.activity_schedule('mail.mail_activity_data_todo', summary=_('Formacion vencida: %s') % a.name)
        return True
