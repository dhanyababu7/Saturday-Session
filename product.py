from traceback import print_tb

from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    variant_template_id = fields.Many2one('variant.template', string="Variant Template")
    variant_category_id = fields.Many2one(related='variant_template_id.categ_id', string="Category", store=True)
    variant_attribute_ids = fields.Many2many('product.attribute', compute='_compute_attribute_ids')
    product_attribute_value_ids = fields.Many2many('product.attribute.value', store=True, compute='_compute_attribute_value_ids')
    product_attribute_ids = fields.Many2many('product.attribute', store=True, compute='_compute_attribute_value_ids')

    @api.depends('attribute_line_ids', 'attribute_line_ids.value_ids')
    def _compute_attribute_value_ids(self):
        for rec in self:
            rec.product_attribute_value_ids = rec.attribute_line_ids.mapped('value_ids').ids
            print(rec.product_attribute_value_ids,'342443242432432')
            print(rec.product_attribute_value_ids.name,'342443242432432')

    @api.depends('attribute_line_ids', 'attribute_line_ids.attribute_id',
                 'attribute_line_ids.value_ids')
    def _compute_attribute_value_ids(self):
        for rec in self:
            print('poreigreguongdgoug')
            # Get all attribute IDs
            attribute_ids = rec.attribute_line_ids.mapped('attribute_id').ids

            # Get all attribute value IDs
            attribute_value_ids = rec.attribute_line_ids.mapped('value_ids').ids

            # Store the attributes and values separately or combined as needed
            rec.product_attribute_value_ids = attribute_value_ids
            rec.product_attribute_ids = attribute_ids


    @api.depends('attribute_line_ids')
    def _compute_attribute_ids(self):
        for rec in self:
            rec.variant_attribute_ids = rec.attribute_line_ids.mapped('attribute_id_readonly')

    def get_current_categories(self):
        return self.env['variant.template.category'].search_read(fields=['id', 'name'], order='name')

    def get_current_templates(self):
        return self.env['variant.template'].search_read(fields=['id', 'name', 'categ_id', 'attribute_ids', 'line_ids'], order='name')

    def get_attributes(self):
        print(self.env.context,'77777777777777777')
        if self.env.context.get('variant_template'):
            variant_template = self.env['variant.template'].browse(
                self.env.context.get('variant_template'))
            if variant_template:
                attributes = self.env['product.attribute.value'].search_read(
                    [(
                     'attribute_id', 'in', variant_template.attribute_ids.ids)],
                    fields=['id', 'name', 'display_name', 'attribute_id'],
                    order='display_name'
                )
                # Group attributes by attribute_id
                attribute_mapping = {}
                for item in attributes:
                    attribute_id = item['attribute_id'][
                        0]  # Ensure it's an ID, not a tuple
                    if attribute_id not in attribute_mapping:
                        attribute_mapping[attribute_id] = {'id': attribute_id,
                                                           'name': item[
                                                               'attribute_id'][
                                                               1],
                                                           'options': []}
                    attribute_mapping[attribute_id]['options'].append({
                        'id': item['id'],
                        'name': item['name']
                    })
                print('popopopopo', list(attribute_mapping.values()))
                return list(attribute_mapping.values())
        return []

    # @api.model
    def get_attributes_values(self):
        print("Entered get_attributes_values")

        context = self.env.context
        if not context.get('variant_template'):
            return []

        variant_template_id = context['variant_template']
        variant_template = self.env['variant.template'].browse(
            variant_template_id)

        if not variant_template:
            return []

        # Fetch attribute values linked to the variant template
        attributes = self.env['product.attribute.value'].search_read(
            [('attribute_id', 'in', variant_template.attribute_ids.ids)],
            fields=['id', 'name', 'display_name', 'attribute_id'],
            order='display_name'
        )

        # Group attributes by attribute_id
        attribute_mapping = {}
        for item in attributes:
            attribute_id, attribute_name = item['attribute_id']
            if attribute_id not in attribute_mapping:
                attribute_mapping[attribute_id] = {
                    'id': attribute_id,
                    'name': attribute_name,
                    'options': []
                }
            attribute_mapping[attribute_id]['options'].append({
                'id': item['id'],
                'name': item['name']
            })

        print("Grouped Attribute Mapping:", list(attribute_mapping.values()))


