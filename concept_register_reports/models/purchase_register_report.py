from odoo import models, fields, api

class PurchaseRegisterReport(models.Model):
    _name = 'purchase.register.report'
    _description = 'Purchase Register Report'
    _auto = False  # SQL view

    product_id = fields.Many2one('product.product', string='Product', readonly=True)
    company_id = fields.Many2one('res.company', string="Company")
    invoice_id = fields.Many2one('account.move', string="Bill", readonly=True)
    invoice_date = fields.Date(string="Bill Date")
    invoice_number = fields.Char(string="Bill Number")
    customer_id = fields.Many2one('res.partner', string='Customer', readonly=True)
    quantity = fields.Float(string="Quantity", readonly=True)
    price_unit = fields.Float(string='Unit Price', readonly=True)
    taxable_amount = fields.Monetary(string='Taxable Amount', readonly=True, currency_field='currency_id')
    tax_amount = fields.Monetary(string='Tax Amount', readonly=True, currency_field='currency_id')
    total_with_tax = fields.Monetary(string='Total', readonly=True, currency_field='currency_id')

    currency_id = fields.Many2one('res.currency', string='Currency', readonly=True)

    move_type = fields.Selection(
        [
            ('in_invoice', 'Vendor Invoice')
        ],
        string="Invoice Type",
        readonly=True
    )

    @api.model
    def init(self):
        self._cr.execute("DROP VIEW IF EXISTS purchase_register_report")
        self._cr.execute("""
            CREATE VIEW purchase_register_report AS
            SELECT
                aml.id AS id,
                aml.product_id AS product_id,
                aml.company_id AS company_id,
                aml.move_id AS invoice_id,
                am.invoice_date AS invoice_date,
                am.name AS invoice_number,
                am.partner_id AS customer_id,
                aml.price_unit AS price_unit,
                aml.quantity AS quantity,
                aml.price_subtotal AS taxable_amount,
                (aml.price_total - aml.price_subtotal) AS tax_amount,
                aml.price_total AS total_with_tax,
                aml.currency_id AS currency_id,
                am.move_type AS move_type
            FROM account_move_line aml
            JOIN account_move am ON aml.move_id = am.id
            WHERE am.move_type = 'in_invoice'
            AND am.state = 'posted'
            AND aml.product_id IS NOT NULL
        """)
