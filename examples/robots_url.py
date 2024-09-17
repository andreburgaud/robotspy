# Content of http://www.musi-cal.com/robots.txt:
"""
User-agent: *
Disallow: /wp-admin/
Allow: /wp-admin/admin-ajax.php
"""

# The first implementation is using the Python standard library urllib.robotparser

import urllib.robotparser
import robots

rp = urllib.robotparser.RobotFileParser()
rp.set_url("http://www.musi-cal.com/robots.txt")
rp.read()

assert rp.can_fetch("*", "http://www.musi-cal.com/cgi-bin/search?city=San+Francisco")
assert rp.can_fetch("*", "http://www.musi-cal.com/")
assert not rp.can_fetch("*", "http://www.musi-cal.com/wp-admin/")
assert not rp.can_fetch("*", "/wp-admin/")

# The second implementation is using the robotspy thin layer supporting the same api as
# the python standard library urllib.robotparser

parser = robots.RobotFileParser()
parser.set_url("http://www.musi-cal.com/robots.txt")
parser.read()

assert parser.can_fetch(
    "*", "http://www.musi-cal.com/cgi-bin/search?city=San+Francisco"
)
assert parser.can_fetch("*", "http://www.musi-cal.com/")
assert not parser.can_fetch("*", "http://www.musi-cal.com/wp-admin/")
assert not parser.can_fetch("*", "/wp-admin/")

# The third implementation is directly using robots.RobotsParser

parser = robots.RobotsParser.from_uri("http://www.musi-cal.com/robots.txt")

if parser.errors:
    print("ERRORS:")
    print(parser.errors)

if parser.warnings:
    print("WARNINGS:")
    print(parser.errors)

assert parser.can_fetch(
    "*", "http://www.musi-cal.com/cgi-bin/search?city=San+Francisco"
)
assert parser.can_fetch("*", "http://www.musi-cal.com/")
assert not parser.can_fetch("*", "http://www.musi-cal.com/wp-admin/")
assert not parser.can_fetch("*", "/wp-admin/")

# Examples with custom timeout
parser = robots.RobotsParser.from_uri("https://robotspy.org/robots.txt", 2)

if parser.errors:
    print("ERRORS:")
    print(parser.errors)

if parser.warnings:
    print("WARNINGS:")
    print(parser.errors)

assert parser.can_fetch(
    "Googlebot", "https://robotspy.org/"
)
assert parser.can_fetch("*", "https://robotspy.org/")

# Set a 0 timeout should result in an error

parser = robots.RobotsParser.from_uri("https://robotspy.org/robots.txt", 0)
assert parser.errors
if parser.errors:
    print("ERRORS:")
    print(parser.errors)


# Timeout error
parser = robots.RobotsParser.from_uri("https://robotspy.org:555/robots.txt", 2)

# The duration may be greater than the timeout because the urllib.request.urlopen timeout does not equate to a total timeout
assert parser.errors
if parser.errors:
    print("ERRORS:")
    print(parser.errors)
