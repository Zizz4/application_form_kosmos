from odoo import fields, models, api
from datetime import date

class HrExpenseSheetAppFormKosmos(models.Model):
    _inherit = 'hr.expense.sheet'

    budget_code = fields.Char(string='Budget Code', stored=True)
    submit_date = fields.Date(string='Submit Date', readonly=True)
    approved_date = fields.Date(string='Approved Date', readonly=True)

    def action_submit_sheet(self):
        self.write({'state': 'submit',
                    'submit_date': date.today()})
        self.sudo().activity_update()
