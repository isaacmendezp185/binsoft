# Copyright (c) 2026
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.en.html).


from odoo import api, fields, models

class PrintMachine(models.Model):
    _name = 'print.machine'
    _description = 'Máquina de impresión / acabado'

    name = fields.Char(required=True)
    machine_type = fields.Selection([
        ('printer','Impresora'),
        ('laminator','Laminadora'),
        ('cutter','Cortadora'),
        ('sewing','Costura'),
        ('finishing','Acabado')
    ], string='Tipo', default='printer')
    technology = fields.Selection([
        ('uv','UV'), ('eco','Eco-solvente'), ('latex','Látex'), ('sublimation','Sublimación'), ('na','N/A')
    ], string='Tecnología', default='na')
    speed_m2_h = fields.Float('Velocidad (m²/h)')
    cost_hour = fields.Float('Costo por hora', digits='Product Price')
    width_max_mm = fields.Float('Ancho máximo (mm)')
    active = fields.Boolean(default=True)
