import robots

content = """
User-agent: mozilla/5
Disallow: /
"""

check_url = "https://example.com"
user_agent = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"

parser = robots.RobotsParser.from_string(content)

print(parser.can_fetch(user_agent, check_url))
print(parser.is_agent_valid(user_agent))


content = """
User-agent: mozilla
Disallow: /
"""

check_url = "https://example.com"
user_agent = "Mozilla"

parser = robots.RobotsParser.from_string(content)

print(parser.can_fetch(user_agent, check_url))
print(parser.is_agent_valid(user_agent))