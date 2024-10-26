import robots

parser = robots.RobotsParser.from_file("robots_file_large.txt")

if parser.errors:
    print("ERRORS:")
    print(parser.errors)

if parser.errors:
    print("WARNINGS:")
    print(parser.errors)

assert parser.can_fetch("Googlebot", "/")
assert not  parser.can_fetch("Exabot", "/")