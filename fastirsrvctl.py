#!/usr/bin/env python3
import os
import click
from server.app import app
from server.model import Ping, Order
from server.db import DB
from server.constants import AGENT_CONFIGURATION_DIR


@click.group()
def cli():
    pass


@cli.command('hosts', help="Show list of hosts.")
def list_hosts():
    click.echo("List of hosts:")
    with app.app_context():
        results = Ping.query
        if results.count() == 0:
            click.echo("** Empty **")
        else:
            for ping in results:
                click.echo(" - %s" % ping.hostname)


@cli.command('configs', help="Show list of configuration files")
def list_config():
    click.echo("List of configuration files:")
    config_list = os.listdir(AGENT_CONFIGURATION_DIR)
    if config_list:
        for config in config_list:
            click.echo(" - %s" % config)
    else:
        click.echo("** Empty **")


@cli.command('order', help="Create an order for given host.")
@click.argument('hostname')
@click.argument('config')
@click.pass_context
def create_order(ctx, hostname, config):
    click.echo("Creating order for hostname %s ..." % hostname)

    if config not in os.listdir(AGENT_CONFIGURATION_DIR):
        click.echo("The configuration file did not exist.")
        ctx.exit(-1)

    with app.app_context():
        if not Ping.query.filter_by(hostname=hostname).first():
            click.echo("The hostname %s was not referenced in DB." % hostname)
            ctx.exit(-1)

        results = Order.query.filter_by(hostname=hostname)
        order = results.first()

        if order is not None:
            if order.active:
                click.echo("An order for %s was already exist and was activated." % hostname)
            else:
                order.active = True
                order.config_filename = config
                DB.session.add(order)
                try:
                    DB.session.commit()
                    click.echo("An order for %s was already exist and has been updated." % hostname)
                except:
                    click.echo("Failed to update order for %s." % hostname)
                    ctx.exit(-1)

        else:
            order = Order(hostname=hostname, active=True, config_filename=config)
            DB.session.add(order)

            try:
                DB.session.commit()
                click.echo("A new order has been created for the hostname %s." % hostname)
            except:
                click.echo(
                    "Unable to create a new order for the hostname %s with configuration file %s." % (
                        hostname,
                        config
                    )
                )
                ctx.exit(-1)


if __name__ == '__main__':
    cli()
