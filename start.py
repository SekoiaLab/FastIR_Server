#!/usr/bin/env python3
import os
from server import app
from server.config import CONFIG
from server.constants import ROOT_DIR, DEFAULT_WEB_HOST, DEFAULT_WEB_PORT
import logging
from logging.handlers import RotatingFileHandler

if __name__ == '__main__':
    import ssl
    cert_dir_path = os.path.join(
        os.path.dirname(__file__),
        'certificate'
    )
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    context.load_cert_chain(
        os.path.join(cert_dir_path, 'server.crt'),
        os.path.join(cert_dir_path, 'server.key')
    )
    formatter = logging.Formatter(
        "[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s")
    handler = RotatingFileHandler(os.path.join(ROOT_DIR, 'flask.log'), maxBytes=10000, backupCount=1)
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.DEBUG)

    host = CONFIG.get('web', 'host', fallback=DEFAULT_WEB_HOST)
    port = CONFIG.get('web', 'port', fallback=DEFAULT_WEB_PORT)
    if isinstance(port, str):
        port = int(port)

    app.run(host=host, port=port, debug=False, ssl_context=context)
