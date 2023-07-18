from odoo import fields, models, api


class HrExpenseSheetAppFormKosmos(models.Model):
    _inherit = 'hr.expense.sheet'

    budget_code = fields.Char(string='Budget Code', stored=True)
