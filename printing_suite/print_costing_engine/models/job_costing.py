# Copyright (c) 2026
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.en.html).


from odoo import api, fields, models

class PrintJob(models.Model):
    _inherit = 'print.job'

    cost_material = fields.Monetary('Costo Material', currency_field='currency_id', readonly=True)
    cost_machine = fields.Monetary('Costo Máquina', currency_field='currency_id', readonly=True)
    cost_ink = fields.Monetary('Costo Tinta', currency_field='currency_id', readonly=True)
    cost_total = fields.Monetary('Costo Total', currency_field='currency_id', compute='_compute_total', store=True)

    @api.depends('cost_material', 'cost_machine', 'cost_ink')
    def _compute_total(self):
        for rec in self:
            rec.cost_total = (rec.cost_material or 0.0) + (rec.cost_machine or 0.0) + (rec.cost_ink or 0.0)

    def action_estimate_cost(self):
        for job in self:
            # Estimación básica: material por m² + máquina por hora + tinta por m²
            area = job.area_m2 or 0.0
            # Material
            material_cost_m2 = 0.0
            if job.substrate_id and job.substrate_id.cost_roll and job.substrate_id.area_roll_m2:
                material_cost_m2 = job.substrate_id.cost_roll / job.substrate_id.area_roll_m2
            cost_material = material_cost_m2 * area

            # Máquina (suponiendo velocidad promedio de 25 m²/h si no hay máquina definida)
            speed = 25.0
            machine = self.env['print.machine'].search([('machine_type','=','printer')], limit=1)
            if machine:
                speed = machine.speed_m2_h or speed
                cost_hour = machine.cost_hour or 0.0
            else:
                cost_hour = 0.0
            hours = area / speed if speed else 0.0
            cost_machine = hours * cost_hour

            # Tinta (si hay registro de tinta con consumo medio)
            ink = self.env['print.ink'].search([], limit=1)
            if ink:
                cost_ink = (ink.cost_per_ml or 0.0) * (ink.consumption_ml_m2 or 0.0) * area
            else:
                cost_ink = 0.0

            job.write({
                'cost_material': cost_material,
                'cost_machine': cost_machine,
                'cost_ink': cost_ink,
                'cost_estimated': cost_material + cost_machine + cost_ink,
            })
        return True
