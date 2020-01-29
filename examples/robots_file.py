import robots

AGENT = "test_robotparser"

parser = robots.RobotsParser.from_file("robots.txt")

if parser.errors:
    print("ERRORS:")
    print(parser.errors)

if parser.errors:
    print("WARNINGS:")
    print(parser.errors)

assert parser.can_fetch(AGENT, "/tmp")
assert not parser.can_fetch(AGENT, "/tmp/")
assert not parser.can_fetch(AGENT, "/tmp/a.html")
assert not parser.can_fetch(AGENT, "/a%3cd.html")
assert not parser.can_fetch(AGENT, "/a%3Cd.html")
assert not parser.can_fetch(AGENT, "/a/b.html")
assert not parser.can_fetch(AGENT, "/%7Ejoe/index.html")
