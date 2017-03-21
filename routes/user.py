from webapp2_extras.routes import RedirectRoute
from handlers import user

secure_scheme = 'https'

_routes = [
    RedirectRoute('/api/items', user.ListHandler, name='user-list', strict_slash=True),
    # RedirectRoute('/api/items/<id>', user.ProfileHandler, name='user-profile', strict_slash=True),
    # RedirectRoute('/api/create/<id>', user.CreateHandler, name='user-create', strict_slash=True),
    # RedirectRoute('/api/edit/<id>', user.EditHandler, name='user-edit', strict_slash=True),
    # RedirectRoute('/api/delete/<id>', user.DeleteHandler, name='user-edit', strict_slash=True),
    # RedirectRoute('/api/register', user.RegisterHandler, name='user-register', strict_slash=True),
    # RedirectRoute('/api/login', user.LoginHandler, name='user-login', strict_slash=True),
    # RedirectRoute('/api/logout', user.LogoutHandler, name='user-logout', strict_slash=True)
]

def get_routes():
    return _routes

def add(app):
    if app.debug:
        secure_scheme = 'http'
    for r in _routes:
        app.router.add(r)
