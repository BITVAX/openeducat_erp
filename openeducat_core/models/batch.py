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


class OpBatch(models.Model):
    _name = 'op.batch'
    _description = 'Batch'
    _inherit = ['mail.thread']

    active = fields.Boolean(tracking=True,default=True)
    code = fields.Char('Code', size=16, required=True ,tracking=True)
    name = fields.Char('Name', size=32, required=True ,tracking=True)
    start_date = fields.Date(
        'Start Date', required=True, default=fields.Date.today() ,tracking=True)
    end_date = fields.Date('End Date' ,tracking=True)
    course_id = fields.Many2one('op.course', 'Course', required=True ,tracking=True,ondelete='restrict')
    faculty_ids = fields.Many2many('op.faculty','batch_faculty_rel' ,tracking=True)
    register_ids = fields.One2many('op.student.course', 'batch_id',string='Students',tracking=True)
    category_id = fields.Many2one('product.category',
                                  related='course_id.category_id',
                                  store=True,
                                  readonly=True)
    
    _sql_constraints = [
        ('unique_batch_code',
         'unique(code,course_id)', 'Course and Code combination should be unique per batch!')]

    @api.constrains('start_date', 'end_date')
    def check_dates(self):
        for record in self:
            if record.end_date:
                start_date = fields.Date.from_string(record.start_date)
                end_date = fields.Date.from_string(record.end_date)
                if start_date > end_date:
                    raise ValidationError(_("End Date cannot be set before \
                    Start Date."))

