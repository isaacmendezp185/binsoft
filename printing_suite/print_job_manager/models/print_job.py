# Copyright (c) 2026
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.en.html).


from odoo import api, fields, models
from odoo.exceptions import UserError

class PrintJob(models.Model):
    _name = 'print.job'
    _description = 'Trabajo de Impresión'
    _order = 'create_date desc'

    name = fields.Char('Referencia', required=True, default=lambda self: self._default_name())
    sale_order_id = fields.Many2one('sale.order', string='Pedido de venta')
    partner_id = fields.Many2one(related='sale_order_id.partner_id', store=True)

    width_mm = fields.Float('Ancho (mm)', required=True)
    height_mm = fields.Float('Alto (mm)', required=True)
    quantity = fields.Integer('Cantidad', default=1)
    area_m2 = fields.Float('Área (m²)', compute='_compute_area', store=True)

    substrate_id = fields.Many2one('print.substrate', string='Sustrato', required=True)
    print_type = fields.Selection([
        ('uv','UV'), ('eco','Eco-solvente'), ('latex','Látex'), ('sublimation','Sublimación')
    ], string='Tipo de impresión', required=True)
    quality = fields.Selection([
        ('draft','Borrador'), ('normal','Normal'), ('high','Alta')
    ], string='Calidad', default='normal')

    state = fields.Selection([
        ('draft','Borrador'),
        ('quoted','Cotizado'),
        ('approved','Aprobado'),
        ('in_production','En producción'),
        ('done','Terminado'),
        ('cancel','Cancelado')
    ], string='Estado', default='draft', tracking=True)

    mo_id = fields.Many2one('mrp.production', string='Orden de fabricación')
    notes = fields.Text('Notas')

    cost_estimated = fields.Monetary('Costo estimado', currency_field='currency_id', readonly=True)
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id)

    @api.model
    def _default_name(self):
        return self.env['ir.sequence'].next_by_code('print.job') or 'JOB-0000'

    @api.depends('width_mm', 'height_mm', 'quantity')
    def _compute_area(self):
        for rec in self:
            area_single = (rec.width_mm or 0.0) * (rec.height_mm or 0.0) / 1_000_000.0
            rec.area_m2 = area_single * (rec.quantity or 0)

    def action_create_mo(self):
        self.ensure_one()
        if not self.substrate_id:
            raise UserError('Defina el sustrato para generar la producción.')
        product = self.env['product.product'].create({
            'name': f"Trabajo {self.name}",
            'type': 'product',
        })
        mo = self.env['mrp.production'].create({
            'product_id': product.id,
            'product_qty': self.quantity,
            'name': self.name,
        })
        self.mo_id = mo.id
        self.state = 'in_production'
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'mrp.production',
            'res_id': mo.id,
            'view_mode': 'form',
        }

