import robots

parser = robots.RobotsParser.from_file("robots_multiple_agents.txt")

if parser.errors:
    print("ERRORS:")
    print(parser.errors)

if parser.errors:
    print("WARNINGS:")
    print(parser.errors)

assert parser.can_fetch("GoogleBot", "/")
assert parser.can_fetch("GoogleBot", "/tmp")
assert not parser.can_fetch("GoogleBot", "/tmp/")

assert parser.can_fetch("FacebookBot", "/")
assert parser.can_fetch("FacebookBot", "/tmp")
assert not parser.can_fetch("FacebookBot", "/tmp/")