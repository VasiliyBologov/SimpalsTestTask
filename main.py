#!/usr/bin/env python
import os
import subprocess
import sys

import click


def _run_command(command, replace=False):
    if replace:
        import shlex
        args = shlex.split(command)
        os.execvpe(args[0], args, os.environ)

    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError:
        sys.exit(1)


@click.group()
def cli():
    pass


@cli.command()
def start_cron():
    """Start the scheduler.
    """

    _run_command('yacron --config=crontab.yaml')


@cli.command()
def start_supervisor():
    """Start the supervisor.
    """
    _run_command('supervisord -c ./supervisord.conf')


@cli.command()
def start():
    """
    Start server
    :return:
    """

    import uvicorn
    uvicorn.run("server.server:app",
                host='localhost',
                port=8000,
                reload=True,
                # reload_dir='server',
                debug=True,
                workers=3)


@cli.command()
def update_db():
    from services.update_db import update_all
    update_all()


if __name__ == '__main__':
    cli()
