# Copyright (c) 2026
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.en.html).


from odoo import api, fields, models

class PrintSubstrate(models.Model):
    _name = 'print.substrate'
    _description = 'Sustrato de impresión gran formato'

    name = fields.Char('Nombre', required=True)
    code = fields.Char('Código')
    width_usable_mm = fields.Float('Ancho útil (mm)', help='Ancho útil del rollo en milímetros')
    thickness_microns = fields.Float('Espesor (µm)')
    uom_area_id = fields.Many2one('uom.uom', string='UdM Área', domain=[('category_id.measure_type', '=', 'area')])
    cost_roll = fields.Float('Costo por rollo', digits='Product Price')
    length_roll_m = fields.Float('Largo por rollo (m)')
    area_roll_m2 = fields.Float('Área por rollo (m²)', compute='_compute_area_roll', store=True)
    waste_rate = fields.Float('Merma (%)', default=3.0)
    description = fields.Text('Descripción')

    @api.depends('width_usable_mm', 'length_roll_m')
    def _compute_area_roll(self):
        for rec in self:
            width_m = (rec.width_usable_mm or 0.0) / 1000.0
            rec.area_roll_m2 = width_m * (rec.length_roll_m or 0.0)

class PrintInk(models.Model):
    _name = 'print.ink'
    _description = 'Tinta para impresión'

    name = fields.Char(required=True)
    technology = fields.Selection([
        ('uv','UV'), ('eco','Eco-solvente'), ('latex','Látex'), ('sublimation','Sublimación')
    ], string='Tecnología')
    cost_per_ml = fields.Float('Costo por ml')
    consumption_ml_m2 = fields.Float('Consumo (ml/m²)', help='Promedio de consumo por m²')

