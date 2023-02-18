import os

from project_A03.settings.base import BASE_DIR

DEBUG = True

ALLOWED_HOSTS = ['project-a-03-tutorme.herokuapp.com', 'localhost', '0.0.0.0', '127.0.0.1']

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3")
    }
}


SOCIALACCOUNT_PROVIDERS = {
    'google': {
        # For each OAuth based provider, either add a ``SocialApp``
        # (``socialaccount`` app) containing the required client
        # credentials, or list them here:
        'APP': {
            'client_id': '143334719618-ga4l9ghm05vo89ubp536b06rpoukutab.apps.googleusercontent.com',
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