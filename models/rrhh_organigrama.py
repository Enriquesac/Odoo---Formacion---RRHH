import json
from odoo import models, fields, api, _

class RrhhOrganigramaVersion(models.Model):
    _name = 'rrhh.organigrama.version'
    _description = 'Version de Organigrama (snapshot)'
    _order = 'fecha desc'

    name = fields.Char(required=True)
    fecha = fields.Date(default=fields.Date.context_today)
    motivo = fields.Char()
    snapshot = fields.Text(string='Snapshot JSON', readonly=True)
    puesto_count = fields.Integer(compute='_compute_counts', string='Puestos')
    persona_count = fields.Integer(compute='_compute_counts', string='Personas')
    company_id = fields.Many2one('res.company', default=lambda self: self.env.company)

    def _compute_counts(self):
        for r in self:
            try:
                data = json.loads(r.snapshot or '{}')
                r.puesto_count = len(data.get('puestos', []))
                r.persona_count = len(data.get('titulares', []))
            except Exception:
                r.puesto_count = 0
                r.persona_count = 0

    def action_snapshot(self):
        for r in self:
            puestos = [{'id': p.id, 'nombre': p.name, 'padre': p.parent_id.id or False,
                        'departamento': p.departamento or ''} for p in self.env['rrhh.puesto'].search([])]
            titulares = []
            for rel in self.env['rrhh.persona.puesto'].search([('persona_id.activo', '=', True)]):
                titulares.append({'persona': rel.persona_id.nombre_completo, 'puesto_id': rel.puesto_id.id,
                                  'puesto': rel.puesto_id.name, 'rol': rel.rol})
            r.snapshot = json.dumps({'puestos': puestos, 'titulares': titulares}, ensure_ascii=False)
            r.message_post(body=_('Snapshot capturado: %s puestos') % len(puestos))
        return True
