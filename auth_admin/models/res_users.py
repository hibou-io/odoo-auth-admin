# -*- coding: utf-8 -*-

from odoo import models, api, exceptions
from odoo.http import request
from datetime import datetime
from time import mktime
import hmac
from hashlib import sha256

from logging import getLogger
_logger = getLogger(__name__)


class ResUsers(models.Model):
    _inherit = 'res.users'

    @api.multi
    def admin_auth_generate_login(self):
        self.ensure_one()
        ir_model_access = self.env['ir.model.access']

        # only allow for users that can delete other users, and only let you login as a 'non-internal' user
        if ir_model_access.check('res.users', mode='unlink', raise_exception=True) and self.share:
            u = str(self.id)
            now = datetime.utcnow()
            fifteen = int(mktime(now.timetuple())) + (15 * 60)
            e = str(fifteen)
            o = str(self.env.uid)

            config = self.env['ir.config_parameter'].sudo()
            key = str(config.search([('key', '=', 'database.secret')], limit=1).value)
            h = hmac.new(key, u+e+o, sha256)

            base_url = str(config.search([('key', '=', 'web.base.url')], limit=1).value)

            _logger.warn('login url for user id: ' + str(self.id) + ' original user id: ' + str(self.env.uid))

            raise exceptions.Warning(base_url + '/auth_admin?u=' + u + '&e=' + e + '&o=' + o + '&h=' + h.hexdigest())

        return False

    @api.model
    def check_credentials(self, password):
        if request.session.get('auth_admin'):
            _logger.warn('check_credentials for user id: ' + str(request.session.uid) + ' original user id: ' + str(request.session.auth_admin))
            return True
        return super(ResUsers, self).check_credentials(password)