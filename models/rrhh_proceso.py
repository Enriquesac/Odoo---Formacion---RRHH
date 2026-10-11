from odoo import models, fields, api, _

class RrhhProceso(models.Model):
    _name = 'rrhh.proceso'
    _description = 'Proceso de Alta / Baja'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'fecha_inicio desc'

    name = fields.Char(compute='_compute_name', store=True)
    tipo = fields.Selection([('alta', 'Alta'), ('baja', 'Baja')], required=True, default='alta', tracking=True)
    persona_id = fields.Many2one('rrhh.persona', required=True, tracking=True)
    puesto_ids = fields.Many2many('rrhh.puesto', string='Puestos')
    fecha_inicio = fields.Date(string='Fecha inicio', default=fields.Date.context_today)
    fecha_prevista = fields.Date(string='Fecha prevista')
    fecha_fin = fields.Date(string='Fecha fin')
    estado = fields.Selection([('planificada', 'Planificada'), ('en_curso', 'En curso'),
                               ('completada', 'Completada'), ('cancelada', 'Cancelada')],
                              default='planificada', tracking=True)
    item_ids = fields.One2many('rrhh.proceso.item', 'proceso_id', string='Items')
    formacion_ids = fields.One2many('formacion.accion', 'proceso_id', string='Formacion generada')
    observaciones = fields.Text()
    company_id = fields.Many2one(related='persona_id.company_id', store=True, readonly=True)

    @api.depends('tipo', 'persona_id')
    def _compute_name(self):
        for r in self:
            r.name = '%s - %s' % (dict(self._fields['tipo'].selection).get(r.tipo, ''), r.persona_id.nombre_completo or '')

    def action_en_curso(self):
        self.write({'estado': 'en_curso'})

    def action_generar_formacion(self):
        for r in self:
            if r.tipo != 'alta':
                continue
            acc = self.env['formacion.accion'].create({
                'name': 'Acogida: %s' % (r.persona_id.nombre_completo or ''),
                'tipo': 'necesidad',
                'estado': 'planificada',
                'persona_prev_ids': [(6, 0, [r.persona_id.id])],
                'proceso_id': r.id,
                'observaciones': 'Generada desde proceso de alta',
            })
            r.message_post(body=_('Accion de formacion planificada: %s') % acc.name)
        return True

    def action_completar(self):
        for r in self:
            r.write({'estado': 'completada', 'fecha_fin': fields.Date.context_today(self)})
            if r.tipo == 'baja':
                r.persona_id.write({'activo': False, 'fecha_baja': fields.Date.context_today(self),
                                    'active': False})
                r.message_post(body=_('Baja aplicada a la persona'))
            else:
                if not r.persona_id.fecha_alta:
                    r.persona_id.fecha_alta = fields.Date.context_today(self)
                r.persona_id.write({'activo': True, 'active': True})
        return True

    def action_cancelar(self):
        self.write({'estado': 'cancelada'})


class RrhhProcesoItem(models.Model):
    _name = 'rrhh.proceso.item'
    _description = 'Item de Proceso Alta/Baja'
    _order = 'id'

    proceso_id = fields.Many2one('rrhh.proceso', required=True, ondelete='cascade')
    name = fields.Char(required=True)
    clase = fields.Selection([('punto', 'Punto info'), ('epi', 'EPI'), ('devolucion', 'Devolucion'),
                              ('formacion', 'Formacion')], default='punto')
    obligatorio = fields.Boolean(default=True)
    hecho = fields.Boolean()
    fecha = fields.Date()
    observaciones = fields.Char()
