# Installation
Tested on Ubuntu 16.04

## Dependencies

`apt-get install -y python3-flask python3-flask-sqlalchemy python3-click openssl`

## Certificate
 
`./gen_ssl.sh`

# Usage

## Launch server

`./start.py`

## Management

```
Usage: fastirsrvctl.py [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  configs  Show list of configuration files
  hosts    Show list of hosts.
  order    Create an order for given host.
```
