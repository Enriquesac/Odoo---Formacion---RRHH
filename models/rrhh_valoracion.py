from odoo import models, fields, api, _

class RrhhValoracion(models.Model):
    _name = 'rrhh.valoracion'
    _description = 'Valoracion de Requisitos Persona x Puesto'
    _inherit = ['mail.thread']
    _order = 'persona_id, puesto_id'

    persona_id = fields.Many2one('rrhh.persona', required=True, ondelete='cascade', tracking=True)
    puesto_id = fields.Many2one('rrhh.puesto', required=True, ondelete='restrict', tracking=True)
    fecha = fields.Date(default=fields.Date.context_today)
    line_ids = fields.One2many('rrhh.valoracion.linea', 'valoracion_id', string='Requisitos')
    cumplimiento = fields.Float(compute='_compute_cumplimiento', store=True, string='% cumplimiento')
    company_id = fields.Many2one(related='persona_id.company_id', store=True, readonly=True)

    _sql_constraints = [('uniq_pers_puesto', 'unique(persona_id, puesto_id)', 'Ya existe valoracion para esa persona y puesto')]

    @api.depends('line_ids.cumple')
    def _compute_cumplimiento(self):
        for r in self:
            total = len(r.line_ids)
            ok = len(r.line_ids.filtered(lambda l: l.cumple))
            r.cumplimiento = round(ok * 100.0 / total, 1) if total else 0.0

    def action_cargar_requisitos(self):
        for r in self:
            r.line_ids.unlink()
            vals = []
            for t in r.puesto_id.tarea_ids:
                try:
                    esperado = int(t.nivel_esperado or 0)
                except (TypeError, ValueError):
                    esperado = 0
                vals.append((0, 0, {'name': t.name, 'tipo': 'tarea', 'tarea_id': t.id,
                                    'nivel_esperado': esperado, 'nivel': '0'}))
            for line in (r.puesto_id.formacion_obligatoria or '').splitlines():
                if line.strip():
                    vals.append((0, 0, {'name': line.strip(), 'tipo': 'form_oblig'}))
            for line in (r.puesto_id.formacion_recomendable or '').splitlines():
                if line.strip():
                    vals.append((0, 0, {'name': line.strip(), 'tipo': 'form_recom'}))
            for line in (r.puesto_id.habilidades or '').splitlines():
                if line.strip():
                    vals.append((0, 0, {'name': line.strip(), 'tipo': 'habilidad'}))
            r.write({'line_ids': vals})
        self.message_post(body=_('Requisitos cargados del puesto'))
        return True


class RrhhValoracionLinea(models.Model):
    _name = 'rrhh.valoracion.linea'
    _description = 'Linea de Valoracion'
    _order = 'id'

    valoracion_id = fields.Many2one('rrhh.valoracion', required=True, ondelete='cascade')
    name = fields.Char(string='Requisito', required=True)
    tipo = fields.Selection([('tarea', 'Tarea'), ('form_oblig', 'Form. obligatoria'),
                             ('form_recom', 'Form. recomendable'), ('habilidad', 'Habilidad')],
                            default='tarea', required=True)
    tarea_id = fields.Many2one('rrhh.puesto.tarea', string='Tarea origen')
    nivel_esperado = fields.Integer(default=3)
    nivel = fields.Selection([('0', '0'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')], default='0', string='Nivel obtenido')
    cumplido = fields.Boolean(string='Cumple (form/hab)')
    cumple = fields.Boolean(compute='_compute_cumple', store=True)

    @api.depends('tipo', 'nivel', 'nivel_esperado', 'cumplido')
    def _compute_cumple(self):
        for r in self:
            if r.tipo == 'tarea':
                try:
                    r.cumple = int(r.nivel or 0) >= int(r.nivel_esperado or 0)
                except (TypeError, ValueError):
                    r.cumple = False
            else:
                r.cumple = bool(r.cumplido)
