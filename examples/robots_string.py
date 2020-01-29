import robots

r = """
# GoogleOnly_System

user-agent: FooBot
disallow: /

BAD LINE
"""

parser = robots.RobotsParser.from_string(r)

if parser.errors:
    print("ERRORS:")
    print(parser.errors)

if parser.errors:
    print("WARNINGS:")
    print(parser.errors)

assert not parser.can_fetch("FooBot", "/toto")

r = """
# CrawlDelayAndCustomAgentTest

User-agent: *
Crawl-delay: 1
Request-rate: 3/15
Disallow: /cyberworld/map/ # This is an infinite virtual URL space

# Cybermapper knows where to go.
User-agent: cybermapper
Disallow:
"""

parser = robots.RobotsParser.from_string(r)

if parser.errors:
    print("ERRORS:")
    print(parser.errors)

if parser.warnings:
    print("WARNINGS:")
    print(parser.warnings)

assert parser.can_fetch("cybermapper", "/cyberworld/map/index.html")
