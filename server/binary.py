import os
import base64
import hashlib
from .config import CONFIG
from .constants import BINARIES_DIR


class Binary(object):
    def __init__(self, arch):
        if not isinstance(arch, str):
            raise ValueError("arch must be an instance of str")
        self.arch = arch
        self.filename = CONFIG.get('binaries', arch)
        if self.filename is None:
            raise ValueError("Unable to get the filename for arch %s" % self.filename)

    @property
    def path(self):
        return os.path.join(BINARIES_DIR, self.filename)

    @property
    def sha256(self):
        hasher = hashlib.sha256()
        BLOCKSIZE = 65536
        with open(self.path, 'rb') as f:
            buf = f.read(BLOCKSIZE)
            while len(buf) > 0:
                hasher.update(buf)
                buf = f.read(BLOCKSIZE)
        return hasher.hexdigest()

    @property
    def base64_data(self):
        data = None
        with open(self.path, 'rb') as f:
            data = f.read()

        if data is not None:
            return base64.b64encode(data)
