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

from datetime import datetime
from dateutil.relativedelta import relativedelta

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError


class OpAdmission(models.Model):
    _name = 'op.admission'
    _inherit = 'mail.thread'
    _rec_name = 'application_number'
    _order = "application_number desc"
    _description = "Admission"

    name = fields.Char(
        'First Name', size=128, required=True)
    middle_name = fields.Char(
        'Middle Name', size=128)
    lastname = fields.Char(
        'Last Name', size=128, required=True)
    title = fields.Many2one(
        'res.partner.title', 'Title')
    application_number = fields.Char(
        'Application Number', size=16, required=True, copy=False,
        default=lambda self:
        self.env['ir.sequence'].next_by_code('op.admission'))
    admission_date = fields.Date(
        'Admission Date', copy=False)
    application_date = fields.Datetime(
        'Application Date', required=True, copy=False,
        default=lambda self: fields.Datetime.now())
    birth_date = fields.Date(
        'Birth Date', required=True)
    course_id = fields.Many2one(
        'op.course', 'Course', required=True)
    batch_id = fields.Many2one(
        'op.batch', 'Batch', required=False)
    street = fields.Char(
        'Street', size=256)
    street2 = fields.Char(
        'Street2', size=256)
    phone = fields.Char(
        'Phone', size=16)
    mobile = fields.Char(
        'Mobile', size=16)
    email = fields.Char(
        'Email', size=256, required=True)
    city = fields.Char('City', size=64)
    zip = fields.Char('Zip', size=8)
    state_id = fields.Many2one(
        'res.country.state', 'States')
    country_id = fields.Many2one(
        'res.country', 'Country')
    fees = fields.Float('Fees')
    image = fields.Binary('image')
    state = fields.Selection(
        [('draft', 'Draft'), ('submit', 'Submitted'),
         ('confirm', 'Confirmed'), ('admission', 'Admission Confirm'),
         ('reject', 'Rejected'), ('pending', 'Pending'),
         ('cancel', 'Cancelled'), ('done', 'Done')],
        'State', default='draft', track_visibility='onchange')
    due_date = fields.Date('Due Date')
    prev_institute_id = fields.Many2one(
        'res.partner', 'Previous Institute')
    prev_course_id = fields.Many2one(
        'op.course', 'Previous Course')
    prev_result = fields.Char(
        'Previous Result', size=256)
    family_business = fields.Char(
        'Family Business', size=256)
    family_income = fields.Float(
        'Family Income')
    gender = fields.Selection(
        [('m', 'Male'), ('f', 'Female'), ('o', 'Other')], 'Gender',
        required=True)
    student_id = fields.Many2one(
        'op.student', 'Student')
    nbr = fields.Integer('No of Admission', readonly=True)
    register_id = fields.Many2one(
        'op.admission.register', 'Admission Register', required=True)
    partner_id = fields.Many2one('res.partner', 'Partner')
    is_student = fields.Boolean('Is Already Student')
    fees_term_id = fields.Many2one('op.fees.terms', 'Fees Term')

    @api.onchange('student_id', 'is_student')
    def onchange_student(self):
        if self.is_student and self.student_id:
            student = self.student_id
            self.title = student.title and student.title.id or False
            self.name = student.name
            self.middle_name = student.middle_name
            self.lastsname = student.lastsname
            self.birth_date = student.birth_date
            self.gender = student.gender
            self.image = student.image or False
            self.street = student.street or False
            self.street2 = student.street2 or False
            self.phone = student.phone or False
            self.mobile = student.mobile or False
            self.email = student.email or False
            self.zip = student.zip or False
            self.city = student.city or False
            self.country_id = student.country_id and \
                student.country_id.id or False
            self.state_id = student.state_id and \
                student.state_id.id or False
            self.partner_id = student.partner_id and \
                student.partner_id.id or False
        else:
            self.title = ''
            self.name = ''
            self.middle_name = ''
            self.lastsname = ''
            self.birth_date = ''
            self.gender = ''
            self.image = False
            self.street = ''
            self.street2 = ''
            self.phone = ''
            self.mobile = ''
            self.zip = ''
            self.city = ''
            self.country_id = False
            self.state_id = False
            self.partner_id = False

    @api.onchange('register_id')
    def onchange_register(self):
        self.course_id = self.register_id.course_id
        self.fees = self.register_id.product_id.lst_price

    @api.onchange('course_id')
    def onchange_course(self):
        self.batch_id = False
        term_id = False
        if self.course_id and self.course_id.fees_term_id:
            term_id = self.course_id.fees_term_id.id
        self.fees_term_id = term_id

    @api.constrains('register_id', 'application_date')
    def _check_admission_register(self):
        for record in self:
            start_date = fields.Date.from_string(record.register_id.start_date)
            end_date = fields.Date.from_string(record.register_id.end_date)
            application_date = fields.Date.from_string(record.application_date)
            if application_date < start_date or application_date > end_date:
                raise ValidationError(_(
                    "Application Date should be between Start Date & \
                    End Date of Admission Register."))

    @api.constrains('birth_date')
    def _check_birthdate(self):
        for record in self:
            if record.birth_date > fields.Date.today():
                raise ValidationError(_(
                    "Birth Date can't be greater than current date!"))

    def submit_form(self):
        self.state = 'submit'

    def admission_confirm(self):
        self.state = 'admission'

    def confirm_in_progress(self):
        for record in self:
            if not record.batch_id:
                raise ValidationError(_('Please assign batch.'))
            if not record.partner_id:
                partner_id = self.env['res.partner'].create({
                    'name': '{} {}'.format(record.name,record.lastsname)
                })
                record.partner_id = partner_id.id
            record.state = 'confirm'

    def get_student_vals(self):
        for student in self:
            return {
                'title': student.title and student.title.id or False,
                'name': student.name,
                'middle_name': student.middle_name,
                'lastsname': student.lastsname,
                'birth_date': student.birth_date,
                'gender': student.gender,
                'course_id':
                student.course_id and student.course_id.id or False,
                'batch_id':
                student.batch_id and student.batch_id.id or False,
                'image': student.image or False,
                'street': student.street or False,
                'street2': student.street2 or False,
                'phone': student.phone or False,
                'email': student.email or False,
                'mobile': student.mobile or False,
                'zip': student.zip or False,
                'city': student.city or False,
                'country_id':
                student.country_id and student.country_id.id or False,
                'state_id': student.state_id and student.state_id.id or False,
                'course_detail_ids': [[0, False, {
                    'date': fields.Date.today(),
                    'course_id':
                    student.course_id and student.course_id.id or False,
                    'batch_id':
                    student.batch_id and student.batch_id.id or False,
                }]],
            }

    def enroll_student(self):
        for record in self:
            total_admission = self.env['op.admission'].search_count(
                [('register_id', '=', record.register_id.id),
                 ('state', '=', 'done')])
            if record.register_id.max_count:
                if not total_admission < record.register_id.max_count:
                    msg = 'Max Admission In Admission Register :- (%s)' % (
                        record.register_id.max_count)
                    raise ValidationError(_(msg))
            if not record.student_id:
                vals = record.get_student_vals()
                vals.update({'partner_id': record.partner_id.id})
                student_id = self.env['op.student'].create(vals).id
            else:
                student_id = record.student_id.id
                record.student_id.write({
                    'course_detail_ids': [[0, False, {
                        'date': fields.Date.today(),
                        'course_id':
                        record.course_id and record.course_id.id or False,
                        'batch_id':
                        record.batch_id and record.batch_id.id or False,
                    }]],
                })
            if record.fees_term_id:
                val = []
                product_id = record.register_id.product_id.id
                for line in record.fees_term_id.line_ids:
                    no_days = line.due_days
                    per_amount = line.value
                    amount = (per_amount * record.fees) / 100
                    date = (
                        datetime.today() + relativedelta(days=no_days)).date()
                    dict_val = {
                        'fees_line_id': line.id,
                        'amount': amount,
                        'date': date,
                        'product_id': product_id,
                        'state': 'draft',
                    }
                    val.append([0, False, dict_val])
                self.env['op.student'].browse(student_id).write({
                    'fees_detail_ids': val
                })
            record.write({
                'nbr': 1,
                'state': 'done',
                'admission_date': fields.Date.today(),
                'student_id': student_id,
            })
            reg_id = self.env['op.subject.registration'].create({
                'student_id': student_id,
                'batch_id': record.batch_id.id,
                'course_id': record.course_id.id,
                'min_unit_load': record.course_id.min_unit_load or 0.0,
                'max_unit_load': record.course_id.max_unit_load or 0.0,
                'state': 'draft',
            })
            reg_id.get_subjects()

    def confirm_rejected(self):
        self.state = 'reject'

    def confirm_pending(self):
        self.state = 'pending'

    def confirm_to_draft(self):
        self.state = 'draft'

    def confirm_cancel(self):
        self.state = 'cancel'

    def payment_process(self):
        self.state = 'fees_paid'

    def open_student(self):
        form_view = self.env.ref('openeducat_core.view_op_student_form')
        tree_view = self.env.ref('openeducat_core.view_op_student_tree')
        value = {
            'domain': str([('id', '=', self.student_id.id)]),
            'view_type': 'form',
            'view_mode': 'list, form',
            'res_model': 'op.student',
            'view_id': False,
            'views': [(form_view and form_view.id or False, 'form'),
                      (tree_view and tree_view.id or False, 'tree')],
            'type': 'ir.actions.act_window',
            'res_id': self.student_id.id,
            'target': 'current',
            'nodestroy': True
        }
        self.state = 'done'
        return value

    def create_invoice(self):
        """Create invoice for fee payment process of student."""
        if self.fees <= 0.00:
            raise UserError(_('The value of the deposit amount must be positive.'))
        partner = self.env['res.partner'].create({'name': self.name})
        product = self.register_id.product_id
        invoice = self.env['account.move'].create({
            'move_type': 'out_invoice',
            'ref': self.application_number,
            'partner_id': partner.id,
            'invoice_line_ids': [(0, 0, {
                'name': product.name,
                'price_unit': self.fees,
                'quantity': 1.0,
                'product_id': product.id,
                'product_uom_id': product.uom_id.id,
            })],
        })
        self.partner_id = partner
        self.state = 'payment_process'
        return {
            'domain': [('id', '=', invoice.id)],
            'view_mode': 'form',
            'res_model': 'account.move',
            'type': 'ir.actions.act_window',
            'res_id': invoice.id,
            'target': 'current',
        }
