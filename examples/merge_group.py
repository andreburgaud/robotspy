import robots

parser = robots.RobotsParser.from_file("merge_group.txt")

assert parser.can_fetch("ExampleBot", "/")
assert not parser.can_fetch("ExampleBot", "/foo")
assert not parser.can_fetch("ExampleBot", "/bar")
assert not parser.can_fetch("ExampleBot", "/baz")
