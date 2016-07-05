from flask.json import JSONEncoder as BaseJSONEncoder


class JSONEncoder(BaseJSONEncoder):
    def default(self, o):
        if isinstance(o, bytes):
            return str(o)[2:-1]

        return super(JSONEncoder).default(self, o)
