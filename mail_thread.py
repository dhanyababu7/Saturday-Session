from odoo import models, fields


class MailThread(models.AbstractModel):
    _inherit = 'mail.thread'

    prod_list_ids = fields.Many2many('product.template', 'mail_thread_product_tmpl_rel')

