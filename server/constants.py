import os
VERSION = '0.1'
DEFAULT_WEB_HOST = '0.0.0.0'
DEFAULT_WEB_PORT = 443
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
BINARIES_DIR = os.path.join(ROOT_DIR, 'binaries')
CERTIFICATE_DIR = os.path.join(ROOT_DIR, 'certificate')
AGENT_CONFIGURATION_DIR = os.path.join(ROOT_DIR, 'config')
RESPONSE_BASE = {
    'appli': 'FastIR',
    'version': VERSION
}
