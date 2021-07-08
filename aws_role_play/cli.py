#!/usr/bin/env python3

import uuid
import os
from importlib.metadata import version

import boto3
import click
from botocore import credentials
from botocore.session import Session

from . import AWS_CONFIG_PATH, AWS_CREDENTIALS_PATH
from .config import load_config
from .sts import update_session_credentials, write_session_credentials
from .roles import get_list_of_roles


def get_version():
    return "aws-role-play v" + version("aws-role-play")


def print_version(ctx, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo(get_version(), nl=True)
    ctx.exit()


@click.group(invoke_without_command=True)
@click.option(
    "-v",
    "--version",
    is_flag=True,
    callback=print_version,
    expose_value=False,
    is_eager=True,
)
@click.pass_context
def cli(ctx):
    """A CLI tool that makes assuming IAM roles easier"""
    if not ctx.invoked_subcommand:
        click.echo(ctx.get_help())


@cli.command(short_help="Assumes a role and updates session credentials")
@click.option(
    "--profile",
    prompt="AWS Profile",
    help="The profile you wish to assume (it must have a role_arn defined).",
)
def assume(profile):
    credentials_config = load_config(AWS_CREDENTIALS_PATH)
    config = load_config(AWS_CONFIG_PATH)

    source_profile = config[f"profile {profile}"].get("source_profile")

    # Re-use the same cache as awscli
    working_dir = os.path.join(os.path.expanduser("~"), ".aws/cli/cache")

    # Construct botocore session with cache
    cached_session = Session(profile=profile)
    provider = cached_session.get_component("credential_provider").get_provider(
        "assume-role"
    )
    provider.cache = credentials.JSONFileCache(working_dir)

    # Authenticate using the source profile
    session = boto3.session.Session(
        profile_name=source_profile, botocore_session=cached_session
    )
    session_credentials = session.get_credentials().get_frozen_credentials()
    updated_config = update_session_credentials(
        credentials_config, session_credentials, profile
    )
    write_session_credentials(updated_config, AWS_CREDENTIALS_PATH)


@cli.command(short_help="List all roles defined in the aws config")
def list():
    config = load_config(AWS_CONFIG_PATH)
    roles = get_list_of_roles(config)
    for role, profile in roles:
        print(f"{role} ({profile})")
