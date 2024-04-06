# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions, _

class Comp(models.Model):
    _inherit = 'res.company'
    def del_exp_date_msg(self):
        self.env.cr.execute("""
        delete from ir_config_parameter where key='database.expiration_date'
        """)
