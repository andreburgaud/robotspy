"""
Main module for package robots. The script is executed when invoking:
python -m robots <options> <arguments>

For help, use:
python -m robots -h | --help

It mimics the behavior of Google robotstxt available at:
https://github.com/google/robotstxt
"""

import argparse
import pathlib
import sys
import urllib.parse

import robots


def init_cli() -> argparse.ArgumentParser:
    """Initialize the argument parser to handle the command line interface."""

    cli: argparse.ArgumentParser = argparse.ArgumentParser(
        usage="%(prog)s <robotstxt> <useragent> <path>",
        description=(
            "Shows whether a given user agent and path/url combination "
            "is allowed or disallowed by a given robots.txt file."
        ),
    )
    cli.prog = __package__
    cli.add_argument(
        "-v", "--version", action="version", version=f"{cli.prog} {robots.__version__}"
    )
    cli.add_argument("robotstxt", help="robots.txt file path or URL")
    cli.add_argument("useragent", help="User agent name")
    cli.add_argument("path", help="Path or URL")

    return cli


def is_url(path_uri: str) -> bool:
    """Validate if a given string is a URL."""

    res = urllib.parse.urlsplit(path_uri)
    return res.scheme in ("http", "https", "ftp", "file")


def normalize_uri(path_uri: str) -> str:
    """Convert any path to URI. If not a path, return the URI."""

    if not isinstance(path_uri, pathlib.Path) and is_url(path_uri):
        return path_uri

    return pathlib.Path(path_uri).resolve().as_uri()


def create_robots(robots_uri: str) -> robots.RobotsParser:
    """Instantiate a RobotParser object with a URI."""

    parser: robots.RobotsParser = robots.RobotsParser.from_uri(robots_uri)
    return parser


def main() -> None:
    """Entry point for the package as a Python module (python -m)"""

    cli = init_cli()
    args = cli.parse_args()

    robots_uri = normalize_uri(args.robotstxt)
    robots_parser = create_robots(robots_uri)

    allowed = robots_parser.can_fetch(args.useragent, args.path)

    allowed_str = "ALLOWED" if allowed else "DISALLOWED"
    url_or_path = "url" if is_url(args.path) else "path"
    print(f"user-agent '{args.useragent}' with {url_or_path} '{args.path}': {allowed_str}")

    if errors := robots_parser.errors:
        for error in errors:
            print(f"{error[0]} -> {error[1]}", file=sys.stderr)

    if warnings := robots_parser.warnings:
        for warning in warnings:
            print(f"{warning[0]} -> {warning[1]}", file=sys.stderr)


if __name__ == "__main__":
    main()
