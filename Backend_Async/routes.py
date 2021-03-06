import pathlib

from views import handler

PROJECT_ROOT = pathlib.Path(__file__).parent


def setup_routes(app):
    app.router.add_post('/', handler)