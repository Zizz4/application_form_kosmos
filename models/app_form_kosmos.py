from odoo import fields, models, api, _
from datetime import date

class HrExpenseSheetAppFormKosmos(models.Model):
    _inherit = 'hr.expense.sheet'

    budget_code = fields.Char(string='Budget Code', stored=True)
    submit_date = fields.Date(string='Submit Date', readonly=True)
    approved_date = fields.Date(string='Approved Date', readonly=True)

    # submit action
    def action_submit_sheet(self):
        self.write({'state': 'submit',
                    'submit_date': date.today()})
        self.sudo().activity_update()

    # approve action
    def _do_approve(self):
        self._check_can_approve()

        notification = {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('There are no expense reports to approve.'),
                'type': 'warning',
                'sticky': False,  # True/False will display for few seconds if false
            },
        }

        filtered_sheet = self.filtered(lambda s: s.state in ['submit', 'draft'])
        if not filtered_sheet:
            return notification
        for sheet in filtered_sheet:
            sheet.write({
                'state': 'approve',
                'user_id': sheet.user_id.id or self.env.user.id,
                'approval_date': fields.Date.context_today(sheet),
                'approved_date': date.today(),
            })
        notification['params'].update({
            'title': _('The expense reports were successfully approved.'),
            'type': 'success',
            'next': {'type': 'ir.actions.act_window_close'},
        })

        self.activity_update()
        return notification

