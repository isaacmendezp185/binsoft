# Copyright (c) 2026
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.en.html).


from odoo import fields, models

class PrintQualityCheck(models.Model):
    _name = 'print.quality.check'
    _description = 'Control de calidad de impresión'

    name = fields.Char('Referencia', required=True)
    job_id = fields.Many2one('print.job', string='Trabajo', required=True)
    passed = fields.Boolean('Aprobado?')
    notes = fields.Text('Notas')
    attachment_ids = fields.Many2many('ir.attachment', string='Evidencias')
