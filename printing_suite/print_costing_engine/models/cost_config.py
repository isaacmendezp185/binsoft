# Copyright (c) 2026
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.en.html).


from odoo import fields, models

class PrintCostConfig(models.Model):
    _name = 'print.cost.config'
    _description = 'Parámetros de Costeo'

    name = fields.Char(default='Parámetros de Costeo', required=True)
    overhead_rate = fields.Float('CIF (%)', help='Cargos indirectos de fabricación sobre el costo de máquina', default=10.0)
    default_machine_id = fields.Many2one('print.machine', string='Máquina por defecto')
    active = fields.Boolean(default=True)
