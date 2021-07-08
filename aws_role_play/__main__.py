#!/usr/bin/env python3
"""
The main entry point. Invoke as `aws-role-play' or `python -m aws-role-play'.
"""
from .cli import cli


def main():
    cli()


if __name__ == "__main__":
    main()
