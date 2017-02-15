# -*- coding: utf-8 -*-

{
    'name': 'Auth Admin',
    'author': 'Hibou Corp. <hello@hibou.io>',
    'category': 'Hidden',
    'version': '1.0',
    'description':
        """
Login as other user
===================

Provides a way for an authenticated user, with certain permissions, to login as a different user.
Can also create a URL that logs in as that user.

Out of the box, only allows you to generate a login for an 'External User', e.g. portal users.
        """,
    'depends': [
        'base',
        'website'
    ],
    'auto_install': False,
    'data': [
        'views/res_users.xml',
    ],
}
