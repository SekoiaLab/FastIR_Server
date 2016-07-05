#!/usr/bin/env python3
import os
import copy
import datetime
from base64 import b64encode
from flask import Flask
from flask import request
from flask import jsonify
from .config import CONFIG
from .constants import RESPONSE_BASE, AGENT_CONFIGURATION_DIR
from .db import DB
from .model import Ping, Order
from .binary import Binary
from .utils import JSONEncoder

app = Flask(__name__)
app.json_encoder = JSONEncoder
app.config['SQLALCHEMY_DATABASE_URI'] = CONFIG['db']['uri']

DB.init_app(app)
with app.app_context():
    DB.create_all()

Master_APIKey = None
try:
    Master_APIKey = CONFIG['api']['key']
except KeyError:
    raise KeyError("The api key was missing in configuration file")


def generate_response(**kwargs):
    response = copy.deepcopy(RESPONSE_BASE)
    response.update(kwargs)
    return jsonify(response)


@app.before_request
def before_request():
    if request.endpoint != 'root':
        if request.method != 'POST':
            response = generate_response(
                **{
                    'return': 'KO',
                    'data': 'Unsupported HTTP method'
                }
            )
            return response, 400
        elif request.form.get('APIKey') != Master_APIKey:
            response = generate_response(
                **{
                    'return': 'KO',
                    'data': 'Bad API key'
                }
            )
            return response, 403


@app.route('/', endpoint='root')
def root():
    return generate_response(**{'return': 'OK'})


@app.route('/getbinary/', methods=['POST'])
def getbinary():
    sha256 = request.form.get('sha256')
    arch = request.form.get('arch')
    app.logger.info(
        "Remote:%s SHA256:%s ARCH:%s",
        request.remote_addr,
        sha256,
        arch
    )

    if arch not in ['x86', 'x64']:
        app.logger.warn(
            "Remote: %s getbinary unsupported architecture (%s)",
            request.remote_addr,
            arch
        )
        response = generate_response(
            **{
                'return': 'KO',
                'data': 'Unsupported architecture'
            }
        )
        return response, 400

    if sha256 is None:
        response = generate_response(
            **{
                'return': 'KO',
                'data': 'sha256 was missing'
            }
        )
        app.logger.warn(
            "Remote %s getbinary sha256 was missing",
            request.remote_addr
        )
        return response, 400
    elif not isinstance(sha256, str):
        message = "sha256 must be a string"
        app.logger.warn(
            "Remote: %s getbinary message: %s",
            request.remote_addr,
            message
        )
        response = generate_response(
            **{
                'return': 'KO',
                'data': message
            }
        )
        return response, 400
    else:
        sha256 = sha256.lower()

    binary = Binary(arch)

    try:
        local_sha256 = binary.sha256
        app.logger.info(
            "Remote: %s local sha256 %s",
            request.remote_addr,
            local_sha256
        )
    except:
        app.logger.exception(
            "Remote: %s cannot get the hash of %s",
            request.remote_addr,
            binary.filename
        )

        response = generate_response(
            **{
                'return': "KO",
                'binary': "0"
            }
        )

        return response, 500

    if sha256 != local_sha256:
        app.logger.info(
            "REMOTE: %s Send new file",
            request.remote_addr
        )

        return generate_response(
            **{
                'return': "OK",
                'binary': "1",
                'data': binary.base64_data
            }
        )

    app.logger.info("REMOTE: %s No new file sent", request.remote_addr)

    return generate_response(
        **{
            'binary': "0",
            'return': "OK"
        }
    )


@app.route('/getorder/', methods=['POST'])
def getorder():
    hostname = request.form.get('hostname')

    if hostname is None:
        response = generate_response(
            **{
                'return': "KO",
                'data': 'The data field was missing.'
            }
        )

        return response, 400

    app.logger.info(
        "REMOTE: %s Hostname: %s",
        request.remote_addr,
        hostname
    )

    # Update ping DB
    results = Ping.query.filter_by(hostname=hostname)

    if not results.count():
        ping = Ping(hostname=hostname, date=datetime.datetime.utcnow())
        DB.session.add(ping)
        DB.session.commit()
    else:
        results.update({'date': datetime.datetime.utcnow()})

    try:
        DB.session.commit()
        app.logger.info(
            "Remote: %s Ping result: the ping DB is updated",
            request.remote_addr
        )
    except:
        app.logger.exception(
            "Remote: % Ping result: unable to update the ping DB",
            request.remote_addr
        )

    # Get order now...
    results = Order.query.filter_by(hostname=hostname)

    order = results.first()

    if order is None or not order.active:
        app.logger.info(
            "Remote: %s Order result: no orders for hostname %s",
            request.remote_addr,
            hostname
        )
        return generate_response(
            **{
                'order': "0",
                'return': "OK"
            }
        )

    try:
        config_path = os.path.join(
            AGENT_CONFIGURATION_DIR,
            order.config_filename
        )
        with open(config_path, "rb") as f:
            config_data = f.read()
            file_content = b64encode(config_data)

    except:
        app.logger.exception(
            "REMOTE: %s Result: bad config file path",
            request.remote_addr
        )

        response = generate_response(
            **{
                'return': "KO",
                'data': "Cannot find the config file"
            }
        )

        return response, 500

    results.delete()
    app.logger.info(
        "Remote: %s Order result: A scan will be scheduled",
        request.remote_addr
    )

    try:
        DB.session.commit()
    except:
        app.logger.info(
            "Remote: %s Order result: Unable to update the order DB",
            request.remote_addr
        )

        return generate_response(
            **{
                'return': "KO",
                'data': "database troubles..."
            }
        )

    return generate_response(
        **{
            'return': 'OK',
            'order': '1',
            'data': file_content
        }
    )
