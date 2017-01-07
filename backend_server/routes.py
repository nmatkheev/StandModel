import pathlib

from views import submit, extract

PROJECT_ROOT = pathlib.Path(__file__).parent


def setup_routes(app):
    app.router.add_post('/submit', submit)
    app.router.add_post('/extract', extract)