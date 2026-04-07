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
from odoo import models, api, fields, _
from odoo.exceptions import UserError


class OpStudentFeesDetails(models.Model):
    _name = 'op.student.fees.details'
    _description = 'Student Fees Details'

    fees_line_id = fields.Many2one('op.fees.terms.line', 'Fees Line')
    invoice_id = fields.Many2one('account.move', 'Invoice')
    amount = fields.Float('Fees Amount')
    date = fields.Date('Submit Date')
    product_id = fields.Many2one('product.product', 'Product')
    student_id = fields.Many2one('op.student', 'Student')
    state = fields.Selection([
        ('draft', 'Draft'), ('invoice', 'Invoice Created')], 'Status')
    invoice_state = fields.Selection(
        related="invoice_id.state", string='Invoice State', readonly=True)

    def get_invoice(self):
        """Create invoice for fee payment process of student."""
        if self.amount <= 0.00:
            raise UserError(_('The value of the deposit amount must be positive.'))
        partner = self.student_id.partner_id
        invoice = self.env['account.move'].create({
            'move_type': 'out_invoice',
            'ref': self.student_id.gr_no or False,
            'partner_id': partner.id,
            'invoice_line_ids': [(0, 0, {
                'name': self.product_id.name,
                'price_unit': self.amount,
                'quantity': 1.0,
                'product_id': self.product_id.id,
                'product_uom_id': self.product_id.uom_id.id,
            })],
        })
        self.state = 'invoice'
        self.invoice_id = invoice.id
        return True

    def action_get_invoice(self):
        if self.invoice_id:
            return {
                'domain': [('id', '=', self.invoice_id.id)],
                'view_mode': 'form',
                'res_model': 'account.move',
                'type': 'ir.actions.act_window',
                'res_id': self.invoice_id.id,
                'target': 'current',
            }
        return True


class OpStudent(models.Model):
    _inherit = 'op.student'

    fees_detail_ids = fields.One2many('op.student.fees.details', 'student_id',
                                      'Fees Collection Details')
    admission_ids = fields.One2many('op.admission', 'student_id',
                                      'Admissions')