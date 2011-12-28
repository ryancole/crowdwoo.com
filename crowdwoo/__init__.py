from flask import Flask

# application

app = Flask(__name__)
app.secret_key = 'foo'

# modules

from crowdwoo.views.auth import auth
from crowdwoo.views.core import core

app.register_module(auth, url_prefix='/auth')
app.register_module(core)