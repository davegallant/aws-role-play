#!/usr/bin/env python3

import os
from importlib.metadata import version

import boto3
import click
from botocore import credentials
from botocore.session import Session

from . import AWS_CONFIG_FILE, AWS_SHARED_CREDENTIALS_FILE, AWS_PROFILE
from .config import load_config
from .sts import (
    export_session_credentials,
    update_session_credentials,
    write_session_credentials,
)
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
    help="The profile you wish to assume (it must have a role_arn defined)",
)
@click.option(
    "--write",
    default=False,
    is_flag=True,
    help="Whether or not to write credentials to the profile in AWS_CONFIG_FILE",
)
@click.option(
    "--export",
    default=False,
    is_flag=True,
    help="Whether or not to export the temporary security credentials as environment variables",
)
@click.option(
    "--aws-cache-dir",
    default=None,
    help="The cache directory that awscli uses for either cli or sso. Defaults to ~/.aws/cli/cache",
)
def assume(profile, write, export, aws_cache_dir):

    if write is False and export is False:
        exit("Must choose to --export and/or --write")

    if profile is None:
        if AWS_PROFILE is None:
            profile = click.prompt("AWS Profile")
        else:
            profile = AWS_PROFILE

    credentials_config = load_config(AWS_SHARED_CREDENTIALS_FILE)
    config = load_config(AWS_CONFIG_FILE)

    source_profile = config[f"profile {profile}"].get("source_profile")

    # Re-use the same cache as awscli
    if aws_cache_dir is None:
        aws_cache_dir = os.path.join(os.path.expanduser("~"), ".aws/cli/cache")

    # Construct botocore session with cache
    cached_session = Session(profile=profile)
    provider = cached_session.get_component("credential_provider").get_provider(
        "assume-role"
    )
    provider.cache = credentials.JSONFileCache(aws_cache_dir)

    # Authenticate using the source profile
    session = boto3.session.Session(
        profile_name=source_profile, botocore_session=cached_session
    )
    session_credentials = session.get_credentials().get_frozen_credentials()

    if write:
        updated_config = update_session_credentials(
            credentials_config, session_credentials, profile
        )
        write_session_credentials(updated_config, AWS_SHARED_CREDENTIALS_FILE)

    if export:
        export_session_credentials(session_credentials)


@cli.command(short_help="List all roles defined in the aws config")
def list():
    config = load_config(AWS_CONFIG_FILE)
    roles = get_list_of_roles(config)
    for role, profile in roles:
        print(f"{role} ({profile})")
