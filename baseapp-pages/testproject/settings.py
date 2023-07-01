import os

from baseapp_core.tests.settings import *  # noqa

# Application definition
INSTALLED_APPS += ["pgtrigger", "baseapp_pages", "baseapp_auth", "testproject.testapp"]
INSTALLED_APPS = ["modeltranslation"] + INSTALLED_APPS

ROOT_URLCONF = "testproject.urls"

# Auth
AUTH_USER_MODEL = "testapp.User"

