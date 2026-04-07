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
    'name': 'OpenEduCat Support',
    'category': 'Planner',
    'summary': 'Help to configure OpenEduCat',
    'version': '18.0.0.0.1',
    'license': 'LGPL-3',
    "sequence": 3,
    'author': 'Tech Receptives',
    'website': 'http://www.openeducat.org',
    'depends': ['web'],
    'data': [
        'views/web_planner_templates.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'openeducat_support/static/src/js/user_menu.js',
        ],
    },
    'images': [
        'static/description/openeducat_support_banner.jpg',
    ],
    'installable': False,
    'auto_install': False,
}
