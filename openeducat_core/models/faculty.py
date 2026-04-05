# -*- coding: utf-8 -*-
###############################################################################
#
#    Tech-Receptives Solutions Pvt. Ltd.
#    Copyright (C) 2009-TODAY Tech-Receptives(<http://www.techreceptives.com>).
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
###############################################################################

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class OpFaculty(models.Model):
    _name = 'op.faculty'
    _description = 'Faculty'
    _inherits = {
        'res.partner': 'partner_id',
        'hr.employee': 'emp_id'
    }
    _inherit = ['mail.thread']

    active = fields.Boolean(tracking=True, default=True)
    partner_id = fields.Many2one(
        'res.partner', 'Partner', required=True, ondelete="restrict")
    emp_id = fields.Many2one('hr.employee', 'Employee', required=True, ondelete="cascade")
    # first_name = fields.Char('First Name', size=128, required=True)
    #     middle_name = fields.Char('Middle Name', size=128)
    # last_name = fields.Char('Last Name', size=128, required=True)
    #     birth_date = fields.Date('Birth Date', required=True)
    #     blood_group = fields.Selection(
    #         [('A+', 'A+ve'), ('B+', 'B+ve'), ('O+', 'O+ve'), ('AB+', 'AB+ve'),
    #          ('A-', 'A-ve'), ('B-', 'B-ve'), ('O-', 'O-ve'), ('AB-', 'AB-ve')],
    #         'Blood Group')
    #     gender = fields.Selection(
    #          [('male', 'Male'), ('female', 'Female')], 'Gender', required=True)
    #     nationality = fields.Many2one('res.country', 'Nationality')
    #     emergency_contact = fields.Many2one(
    #         'res.partner', 'Emergency Contact')
    #     visa_info = fields.Char('Visa Info', size=64)
    #     id_number = fields.Char('ID Card Number', size=64)
    #     login = fields.Char(
    #         'Login', related='emp_id.user_id.login', readonly=1)
    #     last_login = fields.Datetime(
    #         'Latest Connection', related='emp_id.user_id.login_date',
    #         readonly=1)
    faculty_subject_ids = fields.Many2many('op.subject', string='Subject(s)', tracking=True)
    course_ids = fields.Many2many('op.course', 'faculty_course_rel', string='Course(s)', tracking=True)
    work_function = fields.Char()
    career = fields.Char()
    curriculum = fields.Html()
    batch_ids = fields.Many2many('op.batch', 'batch_faculty_rel', string="Batch(es)", tracking=True)

    # contact_address = fields.Char(related="work_contact_id.contact_address")
    # street = fields.Char(related='work_contact_id.street')
    # street2 = fields.Char(related='work_contact_id.street2')
    # city = fields.Char(related='work_contact_id.city')
    # zip = fields.Char(related='work_contact_id.zip')
    # state_id = fields.Many2one(related='work_contact_id.state_id')
    # country_id = fields.Many2one(related='work_contact_id.country_id')
    # zip_id = fields.Many2one(related='work_contact_id.zip_id')

    @api.onchange('firstname', 'lastname')
    def _onchange_name(self):
        if self.firstname and self.lastname:
            self.name = u'{} {}'.format(self.firstname, self.lastname)

    @api.model_create_multi
    def create(self, vals_list):
        for data in vals_list:
            data.update(
                work_phone=data.get('phone', False),
                mobile_phone=data.get('mobile', False),
                identification_id=data.get('vat', False),
                work_email=data.get('email', False),
                faculty=True,
                supplier_rank=max(data.get('supplier_rank', 0), 1),
            )
            if not data.get("name") and 'firstname' in data and 'lastname' in data:
                data.update(name='{} {}'.format(data['firstname'], data['lastname']))
        records = super().create(vals_list)
        for record in records:
            if not record.work_contact_id:
                record.write({'work_contact_id': record.partner_id.id})
        return records

    @api.onchange('zip_id')
    def onchange_zip_id(self):
        if self.zip_id:
            self.zip = self.zip_id.name
            self.city = self.zip_id.city_id.name
            self.state_id = self.zip_id.city_id.state_id
            self.country_id = self.zip_id.city_id.country_id
