from odoo import models, fields

class FormacionDestreza(models.Model):
    _name = 'formacion.destreza'
    _description = 'Destreza / Competencia'
    _order = 'name'
    name = fields.Char(required=True)
    descripcion = fields.Text()
    active = fields.Boolean(default=True)


class FormacionFormador(models.Model):
    _name = 'formacion.formador'
    _description = 'Formador'
    _order = 'name'
    name = fields.Char(required=True)
    email = fields.Char()
    externo = fields.Boolean(string='Externo')
    active = fields.Boolean(default=True)
