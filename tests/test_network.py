"""
NetworkTestCase from:
https://github.com/python/cpython/blob/a796d8ef9dd1af65f7e4d7a857b56f35b7cb6e78/Lib/test/test_robotparser.py
converted to PyTest
"""

import pytest
import robots
from .core import *

BASE_URL = 'http://www.pythontest.net'


@pytest.fixture(scope='module')
def parser():
    p = robots.RobotsParser.from_uri(f'{BASE_URL}/elsewhere/robots.txt')
    return p


def test_basic_disallow_all(parser):
    assert not parser.disallow_all


def test_basic_allow_all(parser):
    assert not parser.allow_all


can_fetch_data = (
    ['*', f'{BASE_URL}/elsewhere', ALLOWED],
    ['Nutch', f'{BASE_URL}/', DISALLOWED],
    ['Nutch', f'{BASE_URL}/brian', DISALLOWED],
    ['Nutch', f'{BASE_URL}/brian/', ALLOWED],
    ['Nutch', f'{BASE_URL}/webstats', DISALLOWED],
    ['Nutch', f'{BASE_URL}/webstats/', DISALLOWED],
    ['*', f'{BASE_URL}/webstats', ALLOWED],
    ['*', f'{BASE_URL}/webstats/', DISALLOWED],
    ['*', f'{BASE_URL}/', ALLOWED],
)


@pytest.mark.parametrize('agent,path,allowed', can_fetch_data)
def test_can_fetch(agent, path, allowed, parser):
    assert parser.can_fetch(agent, path) is allowed


def test_404():
    p = robots.RobotsParser.from_uri('https://robotspy.org/non_existing_robots.txt')
    assert p.allow_all  # no robots file => allow access to all paths
    assert p.can_fetch('FooBot', '/admin')


def test_utf16():
    p = robots.RobotsParser.from_uri('https://robotspy.org/tests/robots_utf16.txt')
    assert p.allow_all  # robots file with unexpected encoding (must be UTF-8) => allow access to all paths
    assert p.can_fetch('FooBot', '/admin')

def test_short_timeout():
    p = robots.RobotsParser.from_uri("https://robotspy.org/robots.txt", 0)
    assert p.errors
    assert p.disallow_all
    assert not p.can_fetch('FooBot', '/admin')

def test_error_timetout():
    p = robots.RobotsParser.from_uri("https://robotspy.org:555/robots.txt", 1)

    # The duration may be greater than the timeout because the urllib.request.urlopen timeout does not equate to a total timeout
    assert p.errors
    assert p.disallow_all
    assert not p.can_fetch('FooBot', '/admin')
