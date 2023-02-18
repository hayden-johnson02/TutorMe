import dj_database_url
DEBUG = False

ALLOWED_HOSTS = ['project-a-03-tutorme.herokuapp.com']

DATABASES = {
    "default": dj_database_url.config(conn_max_age=600, ssl_require=True),
}

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        # For each OAuth based provider, either add a ``SocialApp``
        # (``socialaccount`` app) containing the required client
        # credentials, or list them here:
        'APP': {
            'client_id': '143334719618-ak4l0p3qm2fceo8m47chvq74gr3f5d7p.apps.googleusercontent.com',
            'secret': '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',
            'key': ''
        }
        #         'SCOPE': [
        #             'profile',
        #             'email',
        #         ],
        #         'AUTH_PARAMS': {
        #             'access_type': 'online',
        #         }
    }
}
