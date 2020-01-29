"""
Mostly tests from:
https://github.com/python/cpython/blob/a796d8ef9dd1af65f7e4d7a857b56f35b7cb6e78/Lib/test/test_robotparser.py
converted to PyTest and intended to validate the compatibility with the Python standard library
package: urllib.robotparser

For each test a data row contains the following fields:
robotstxt, useragent, url, allowed/disallowed

allow/disallowed is expressed as a boolean, True/False
"""

import pytest
import robots
from .core import *


# Same robots.txt as http://www.pythontest.net/elsewhere/robots.txt
network = """
# NetworkTestCase

User-agent: Nutch
Disallow: /
Allow: /brian/

User-agent: *
Disallow: /webstats/
"""

network_data = (
    [network, '*', '/elsewhere/', ALLOWED],
    [network, 'Nutch', '/', DISALLOWED],
    [network, 'Nutch', '/brian', DISALLOWED],
    [network, 'Nutch', '/brian/', ALLOWED],
    [network, 'Nutch', '/webstats/', DISALLOWED],
    [network, '*', '/webstats/', DISALLOWED],
    [network, '*',  '/', ALLOWED],
)


@pytest.mark.parametrize('robots_txt,agent,path,allowed', network_data)
def test_py01_network(robots_txt, agent, path, allowed, can_fetch):
    assert can_fetch(robots_txt, agent, path) is allowed


useragent_wild_card = """
# UserAgentWildcardTest

User-agent: *
Disallow: /cyberworld/map/ # This is an infinite virtual URL space
Disallow: /tmp/ # these will soon disappear
Disallow: /foo.html
"""

useragent_wild_card_data = (
    [useragent_wild_card, DEFAULT_AGENT, '/', ALLOWED],
    [useragent_wild_card, DEFAULT_AGENT, '/test.html', ALLOWED],
    [useragent_wild_card, DEFAULT_AGENT, '/cyberworld/map/index.html', DISALLOWED],
    [useragent_wild_card, DEFAULT_AGENT, '/tmp/xxx', DISALLOWED],
    [useragent_wild_card, DEFAULT_AGENT, '/foo.html', DISALLOWED],
)


@pytest.mark.parametrize('robots_txt,agent,path,allowed', useragent_wild_card_data)
def test_useragent_wild_card(robots_txt, agent, path, allowed, can_fetch):
    assert can_fetch(robots_txt, agent, path) is allowed


# This test does not take into account crawl-delay. See crawl_delay_request_rate for that.
crawl_delay_custom_agent = """
# CrawlDelayAndCustomAgentTest 

User-agent: *
Crawl-delay: 1
Request-rate: 3/15
Disallow: /cyberworld/map/ # This is an infinite virtual URL space

# Cybermapper knows where to go.
User-agent: cybermapper
Disallow:
"""

crawl_delay_custom_agent_data = (
    [crawl_delay_custom_agent, DEFAULT_AGENT, '/', ALLOWED],
    [crawl_delay_custom_agent, DEFAULT_AGENT, '/test.html', ALLOWED],
    [crawl_delay_custom_agent, 'cybermapper', '/cyberworld/map/index.html', ALLOWED],
    [crawl_delay_custom_agent, DEFAULT_AGENT, '/cyberworld/map/index.html', DISALLOWED],
)


@pytest.mark.parametrize('robots_txt,agent,path,allowed', crawl_delay_custom_agent_data)
def test_crawl_delay_custom_agent(robots_txt, agent, path, allowed, can_fetch):
    assert can_fetch(robots_txt, agent, path) is allowed


sitemap = """
# SitemapTest

User-agent: *
Sitemap: http://www.gstatic.com/s2/sitemaps/profiles-sitemap.xml
Sitemap: http://www.google.com/hostednews/sitemap_index.xml
Request-rate: 3/15
Disallow: /cyberworld/map/ # This is an infinite virtual URL space
"""

sitemap_data = (
    [sitemap, DEFAULT_AGENT, '/', ALLOWED],
    [sitemap, DEFAULT_AGENT, '/test.html', ALLOWED],
    [sitemap, DEFAULT_AGENT, '/cyberworld/map/index.html', DISALLOWED],
)


@pytest.mark.parametrize('robots_txt,agent,path,allowed', sitemap_data)
def test_sitemap(robots_txt, agent, path, allowed, can_fetch):
    assert can_fetch(robots_txt, agent, path) is allowed


reject_all = """
# RejectAllRobotsTest

User-agent: *
Disallow: /
"""

reject_all_data = (
    [reject_all, DEFAULT_AGENT, '/cyberworld/map/index.html', DISALLOWED],
    [reject_all, DEFAULT_AGENT, '/', DISALLOWED],
    [reject_all, DEFAULT_AGENT, '/tmp/', DISALLOWED],
)


@pytest.mark.parametrize('robots_txt,agent,path,allowed', reject_all_data)
def test_reject_all(robots_txt, agent, path, allowed, can_fetch):
    assert can_fetch(robots_txt, agent, path) is allowed


# TODO: implement handling request-rate and crawl-delay
# Following tests take into account crawl-delay and request-rate

empty_data = (
   ['# Empty', DEFAULT_AGENT, '/foo', ALLOWED],
   ['# Empty', '', '', ALLOWED],  # No user agent, no path provided
)


@pytest.mark.parametrize('robots_txt,agent,path,allowed', empty_data)
def test_empty(robots_txt, agent, path, allowed, can_fetch):
    assert can_fetch(robots_txt, agent, path) is allowed


crawl_delay_request_rate = """
# CrawlDelayAndRequestRate

User-agent: figtree
Crawl-delay: 3
Request-rate: 9/30
Disallow: /tmp
Disallow: /a%3cd.html
Disallow: /a%2fb.html
Disallow: /%7ejoe/index.html
"""

crawl_delay_request_rate_data = (
    [crawl_delay_request_rate, 'figtree', '/foo.html', ALLOWED],
    [crawl_delay_request_rate, 'figtree', '/tmp', DISALLOWED],
    [crawl_delay_request_rate, 'figtree', '/tmp/a.html', DISALLOWED],
    [crawl_delay_request_rate, 'figtree', '/a%3cd.html', DISALLOWED],
    [crawl_delay_request_rate, 'figtree', '/a%3Cd.html', DISALLOWED],
    [crawl_delay_request_rate, 'figtree', '/a%2fb.html', DISALLOWED],
    [crawl_delay_request_rate, 'figtree', '/~joe/index.html', DISALLOWED],
)


@pytest.mark.parametrize('robots_txt,agent,path,allowed', crawl_delay_request_rate_data)
def test_crawl_delay_request_rate(robots_txt, agent, path, allowed, can_fetch):
    assert can_fetch(robots_txt, agent, path) is allowed


crawl_delay_request_rate_diff_agent_data = (
    [crawl_delay_request_rate, '/foo.html', ALLOWED],
    [crawl_delay_request_rate, '/tmp', ALLOWED],
    [crawl_delay_request_rate, '/tmp/a.html', ALLOWED],
    [crawl_delay_request_rate, '/a%3cd.html', ALLOWED],
    [crawl_delay_request_rate, '/a%3Cd.html', ALLOWED],
    [crawl_delay_request_rate, '/a%2fb.html', ALLOWED],
    [crawl_delay_request_rate, '/~joe/index.html', ALLOWED],
)


# The behavior is different than urllib.robotparser that applies 'figtree' and
# 'FigTree Robot libwww-perl/5.04' with the same rules.
@pytest.mark.parametrize('robots_txt,path,allowed', crawl_delay_request_rate_diff_agent_data)
def test_different_agent(robots_txt, path, allowed, can_fetch):
    agent = 'FigTree Robot libwww-perl/5.04'
    assert can_fetch(robots_txt, agent, path) is allowed


invalid_request_rate = """
# InvalidRequestRate

User-agent: *
Disallow: /tmp/
Disallow: /a%3Cd.html
Disallow: /a/b.html
Disallow: /%7ejoe/index.html
Crawl-delay: 3
Request-rate: 9/banana
"""

invalid_request_rate_data = (
    [invalid_request_rate, DEFAULT_AGENT, '/tmp', ALLOWED],
    [invalid_request_rate, DEFAULT_AGENT, '/tmp/', DISALLOWED],
    [invalid_request_rate, DEFAULT_AGENT, '/tmp/a.html', DISALLOWED],
    [invalid_request_rate, DEFAULT_AGENT, '/a%3cd.html', DISALLOWED],
    [invalid_request_rate, DEFAULT_AGENT, '/a%3Cd.html', DISALLOWED],
    [invalid_request_rate, DEFAULT_AGENT, '/a/b.html', DISALLOWED],
    [invalid_request_rate, DEFAULT_AGENT, '/%7Ejoe/index.html', DISALLOWED],
)


@pytest.mark.parametrize('robots_txt,agent,path,allowed', invalid_request_rate_data)
def test_invalid_request_rate(robots_txt, agent, path, allowed, can_fetch):
    assert can_fetch(robots_txt, agent, path) is allowed


invalid_crawl_delay = """
# InvalidCrawlDelay

User-Agent: *
Disallow: /.
Crawl-delay: pears
"""


def test_invalid_crawl_delay(can_fetch):
    assert can_fetch(invalid_crawl_delay, DEFAULT_AGENT, '/foo.html') is ALLOWED


other_invalid_request_rate = """
# OtherInvalidCrawlDelay

User-agent: Googlebot
Allow: /folder1/myfile.html
Disallow: /folder1/
Request-rate: whale/banana
"""

other_invalid_request_rate_data = (
    [other_invalid_request_rate, 'Googlebot', '/folder1/myfile.html', ALLOWED],
    [other_invalid_request_rate, 'Googlebot', '/folder1/anotherfile.html', DISALLOWED],
)


@pytest.mark.parametrize('robots_txt,agent,path,allowed', other_invalid_request_rate_data)
def test_other_invalid_request_rate(robots_txt, agent, path, allowed, can_fetch):
    assert can_fetch(robots_txt, agent, path) is allowed


useragent_ordering = """
# UserAgentOrdering

User-agent: Googlebot
Disallow: /

User-agent: Googlebot-Mobile
Allow: /
"""


def test_useragent_ordering(can_fetch):
    assert can_fetch(useragent_ordering, 'Googlebot', '/something.jpg') is DISALLOWED


# Different behavior than urllib.robotparser that applies the same rule to googlebot and
# googlebot-mobile. It ends up validating if the ua saved by the parser is in the ua that
# we want to validate (if 'googlebot' in 'googlebot-mobile') and disallow for google-mobile
# Google robots respects Googlebot-Mobile as a different ua and allow. Same for robotspy.
def test_useragent_google_mobile(can_fetch):
    assert can_fetch(useragent_ordering, 'Googlebot-Mobile', '/something.jpg') is ALLOWED


google_url_ordering = """
# GoogleURLOrdering

User-agent: Googlebot
Allow: /folder1/myfile.html
Disallow: /folder1/
"""

google_url_ordering_data = (
    [google_url_ordering, 'googlebot', '/folder1/myfile.html', ALLOWED],
    [google_url_ordering, 'googlebot', '/folder1/anotherfile.html', DISALLOWED],
)


@pytest.mark.parametrize('robots_txt,agent,path,allowed', google_url_ordering_data)
def test_google_url_ordering(robots_txt, agent, path, allowed, can_fetch):
    assert can_fetch(robots_txt, agent, path) is allowed


disallow_query_string = """
# DisallowQueryString

User-agent: *
Disallow: /some/path?name=value
"""

disallow_query_string_data = [
    [disallow_query_string, DEFAULT_AGENT, '/some/path', ALLOWED],
    [disallow_query_string, DEFAULT_AGENT, '/some/path?name=value', DISALLOWED],
]


@pytest.mark.parametrize('robots_txt,agent,path,allowed', disallow_query_string_data)
def test_disallow_query_string(robots_txt, agent, path, allowed, can_fetch):
    assert can_fetch(robots_txt, agent, path) is allowed


use_first_useragent_wildcard = """
# UseFirstUserAgentWildcard

User-agent: *
Disallow: /some/path

User-agent: *
Disallow: /another/path
"""

test_use_first_useragent_wildcard = (
    [use_first_useragent_wildcard, DEFAULT_AGENT, '/another/path', DISALLOWED],
    [use_first_useragent_wildcard, DEFAULT_AGENT, '/some/path', DISALLOWED],
)


# The logic in robotspy is to combine the entries with the same useragent, as per the specs:
# https://tools.ietf.org/html/draft-koster-rep-00#section-2.2.1
# TODO: consider renaming this test combine_rules or something similar
#       Mark it as a difference with urllib.robotparser in the Differences section in the README
@pytest.mark.parametrize('robots_txt,agent,path,allowed', test_use_first_useragent_wildcard)
def test_use_first_useragent_wildcard(robots_txt, agent, path, allowed, can_fetch):
    assert can_fetch(robots_txt, agent, path) is allowed


empty_query_string = """
# EmptyQueryString

User-agent: *
Allow: /some/path?
Disallow: /another/path?
"""

empty_query_string_data = (
    [empty_query_string, DEFAULT_AGENT, '/some/path?', ALLOWED],
    [empty_query_string, DEFAULT_AGENT, '/another/path?', DISALLOWED],
)


@pytest.mark.parametrize('robots_txt,agent,path,allowed', empty_query_string_data)
def test_empty_query_string(robots_txt, agent, path, allowed, can_fetch):
    assert can_fetch(robots_txt, agent, path) is allowed


default_entry = """
# DefaultEntry

User-agent: *
Crawl-delay: 1
Request-rate: 3/15
Disallow: /cyberworld/map/
"""

default_entry_data = (
    [default_entry, DEFAULT_AGENT, '/', ALLOWED],
    [default_entry, DEFAULT_AGENT, '/test.html', ALLOWED],
    [default_entry, DEFAULT_AGENT, '/cyberworld/map/index.html', DISALLOWED],
)


@pytest.mark.parametrize('robots_txt,agent,path,allowed', default_entry_data)
def test_default_entry(robots_txt, agent, path, allowed, can_fetch):
    assert can_fetch(robots_txt, agent, path) is allowed


robots_input = """
# StringFormatting

User-agent: *
Crawl-delay: 1
Request-rate: 3/15
Disallow: /cyberworld/map/ # This is an infinite virtual URL space

# Cybermapper knows where to go.
User-agent: cybermapper
Disallow: /some/path
"""

expected_robots_output = """User-agent: *
Disallow: /cyberworld/map/

User-agent: cybermapper
Disallow: /some/path
"""


def test_string_formatting():
    parser = robots.RobotsParser().from_string(robots_input)
    print(str(parser))
    assert str(parser) == expected_robots_output


robots_sitemap_input = """
# StringFormatting

User-agent: *
Crawl-delay: 1
Request-rate: 3/15
Disallow: /cyberworld/map/ # This is an infinite virtual URL space

# Cybermapper knows where to go.
User-agent: cybermapper
Disallow: /some/path

Sitemap: https://www.example.com/sitemap1.xml
Sitemap: https://www.example.com/sitemap2.xml
"""

expected_robots_sitemap_output = """User-agent: *
Disallow: /cyberworld/map/

User-agent: cybermapper
Disallow: /some/path

Sitemap: https://www.example.com/sitemap1.xml
Sitemap: https://www.example.com/sitemap2.xml
"""


def test_string_formatting_sitemaps():
    parser = robots.RobotsParser().from_string(robots_sitemap_input)
    print(str(parser))
    assert str(parser) == expected_robots_sitemap_output
