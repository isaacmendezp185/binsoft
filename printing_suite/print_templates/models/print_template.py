# Copyright (c) 2026
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.en.html).


from odoo import api, fields, models

class PrintTemplate(models.Model):
    _name = 'print.template'
    _description = 'Plantilla de trabajo de impresión'

    name = fields.Char(required=True)
    width_mm = fields.Float('Ancho (mm)', required=True)
    height_mm = fields.Float('Alto (mm)', required=True)
    substrate_id = fields.Many2one('print.substrate', string='Sustrato', required=True)
    print_type = fields.Selection([
        ('uv','UV'), ('eco','Eco-solvente'), ('latex','Látex'), ('sublimation','Sublimación')
    ], string='Tipo de impresión', required=True)
    quality = fields.Selection([
        ('draft','Borrador'), ('normal','Normal'), ('high','Alta')
    ], string='Calidad', default='normal')

    def action_create_job(self):
        self.ensure_one()
        job = self.env['print.job'].create({
            'name': f"{self.name}",
            'width_mm': self.width_mm,
            'height_mm': self.height_mm,
            'quantity': 1,
            'substrate_id': self.substrate_id.id,
            'print_type': self.print_type,
            'quality': self.quality,
            'state': 'approved',
        })
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'print.job',
            'view_mode': 'form',
            'res_id': job.id,
        }
