# -*- coding: utf-8 -*-

from odoo import http, exceptions
import hmac
from hashlib import sha256
from datetime import datetime
from time import mktime

from logging import getLogger
_logger = getLogger(__name__)


class AuthAdmin(http.Controller):

    @http.route(['/auth_admin'], type='http', auth='public', website=True)
    def index(self, *args, **post):
        u = post.get('u')
        e = post.get('e')
        o = post.get('o')
        h = post.get('h')

        if not all([u, e, o, h]):
            exceptions.Warning('Invalid Request')

        u = str(u)
        e = str(e)
        o = str(o)
        h = str(h)

        now = datetime.utcnow()
        now = int(mktime(now.timetuple()))
        fifteen = now + (15 * 60)

        config = http.request.env['ir.config_parameter'].sudo()
        key = str(config.search([('key', '=', 'database.secret')], limit=1).value)

        myh = hmac.new(key, str(u + e + o), sha256)

        if not hmac.compare_digest(h, myh.hexdigest()):
            raise exceptions.Warning('Invalid Request')

        if not (int(e) >= now and int(e) <= fifteen):
            exceptions.Warning('Expired')

        user = http.request.env['res.users'].sudo().search([('id', '=', int(u))], limit=1)
        if not user.id:
            exceptions.Warning('Invalid User')

        http.request.session.uid = user.id
        http.request.session.login = user.login
        http.request.session.password = ''
        http.request.session.auth_admin = int(o)
        http.request.uid = user.id
        uid = http.request.session.authenticate(http.request.session.db, user.login, 'x')
        if uid is not False:
            http.request.params['login_success'] = True
            return http.redirect_with_hash('/my/home')
        return http.local_redirect('/my/home')
