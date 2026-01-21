# Copyright (c) 2026
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.en.html).


from odoo import api, fields, models

class PrintComposerWizard(models.TransientModel):
    _name = 'print.composer.wizard'
    _description = 'Asistente de Composición de Impresión'

    name = fields.Char('Nombre del trabajo', required=True)
    width_mm = fields.Float('Ancho (mm)', required=True)
    height_mm = fields.Float('Alto (mm)', required=True)
    quantity = fields.Integer('Cantidad', default=1)
    substrate_id = fields.Many2one('print.substrate', string='Sustrato', required=True)
    print_type = fields.Selection([
        ('uv','UV'), ('eco','Eco-solvente'), ('latex','Látex'), ('sublimation','Sublimación')
    ], string='Tipo de impresión', required=True)
    quality = fields.Selection([
        ('draft','Borrador'), ('normal','Normal'), ('high','Alta')
    ], string='Calidad', default='normal')
    create_mo = fields.Boolean('Crear orden de fabricación', default=True)

    def action_create(self):
        self.ensure_one()
        job = self.env['print.job'].create({
            'name': self.name,
            'width_mm': self.width_mm,
            'height_mm': self.height_mm,
            'quantity': self.quantity,
            'substrate_id': self.substrate_id.id,
            'print_type': self.print_type,
            'quality': self.quality,
            'state': 'approved',
        })
        if self.create_mo:
            job.action_create_mo()
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'print.job',
            'view_mode': 'form',
            'res_id': job.id,
        }
