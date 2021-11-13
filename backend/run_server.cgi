#!/usr/bin/python3.6
print("Content-Type: text/html\n\n")
msg = "Hello, World!"
print("""%s""" % msg)

from wsgiref.handlers import CGIHandler
from config import activate_venv_path

exec(open(activate_venv_path).read(), dict(__file__=activate_venv_path))

from app import create_app


class ProxyFix(object):
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        environ["SERVER_NAME"] = ""
        environ["SERVER_PORT"] = "80"
        environ["REQUEST_METHOD"] = "GET"
        environ["SCRIPT_NAME"] = ""
        environ["QUERY_STRING"] = ""
        environ["SERVER_PROTOCOL"] = "HTTP/1.1"
        return self.app(environ, start_response)


if __name__ == "__main__":
    app = create_app()
    app.wsgi_app = ProxyFix(app.wsgi_app)
    CGIHandler().run(app)
