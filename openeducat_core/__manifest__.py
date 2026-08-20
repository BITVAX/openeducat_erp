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

{
    'name': 'OpenEduCat Core',
    'version': '18.0.0.0.1',
    'license': 'LGPL-3',
    'category': 'Education',
    'summary': 'Manage Students, Faculties and Education Institute',
    'author': 'Tech Receptives',
    'website': 'http://www.openeducat.org',
    'depends': ['board', 'hr', 'web', 'product', 'base_location', 'partner_firstname', 'account', 'connector_magento'],
    'data': [
        'report/report_menu.xml',
        'report/report_student_bonafide.xml',
        'report/report_student_idcard.xml',
        'wizard/faculty_create_employee_wizard_view.xml',
        'wizard/faculty_create_user_wizard_view.xml',
        'wizard/students_create_user_wizard_view.xml',
        'security/op_security.xml',
        'security/ir.model.access.csv',
        'views/student_view.xml',
        'views/hr_view.xml',
        'views/category_view.xml',
        'views/course_view.xml',
        'views/batch_view.xml',
        'views/subject_view.xml',
        'views/faculty_view.xml',
        'views/res_company_view.xml',
        'views/openeducat_template.xml',
        # 'views/website_assets.xml',
        'views/subject_registration_view.xml',
        'views/res_partner_view.xml',
        'dashboard/student_dashboard_view.xml',
        'dashboard/faculty_dashboard_view.xml',
        'menu/openeducat_core_menu.xml',
        #         'menu/faculty_menu.xml',
        #         'menu/student_menu.xml',
    ],
    'demo': [],
    'assets': {
        # TODO: dashboard_ext.js needs full rewrite from odoo.define/Widget to ES6/OWL3
        # 'web.assets_backend': [
        #     'openeducat_core/static/src/css/base.css',
        #     'openeducat_core/static/src/js/dashboard_ext.js',
        #     'openeducat_core/static/src/xml/base.xml',
        #     'openeducat_core/static/src/xml/dashboard_ext_openeducat.xml',
        # ],
    },
    'installable': True,
    'auto_install': False,
    'application': True,
}
