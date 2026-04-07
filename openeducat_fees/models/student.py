# -*- coding: utf-8 -*-
##############################################################################
#
#    Tech-Receptives Solutions Pvt. Ltd.
#    Copyright (C) 2009-TODAY Tech Receptives(<http://www.techreceptives.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from odoo import models


class OpStudent(models.Model):
    _inherit = 'op.student'

    def action_view_invoice(self):
        """Display existing invoices of given student."""
        inv_ids = self.mapped('invoice_ids').ids
        action = {
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'context': {'default_partner_id': self[:1].partner_id.id},
        }
        if len(inv_ids) > 1:
            action['view_mode'] = 'list,form'
            action['domain'] = [('id', 'in', inv_ids)]
        else:
            action['view_mode'] = 'form'
            action['res_id'] = inv_ids[0] if inv_ids else False
        return action
