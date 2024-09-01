"""
Mostly tests from:
https://github.com/google/robotstxt/blob/master/robots_test.cc
implemented with PyTest and intended to validate the compatibility with the robots.txt parser
from Google (written in C++) and released under https://www.apache.org/licenses/LICENSE-2.0

Each ID_<Name> corresponds to a test or set of tests in robots_test.cc

For each test a data row contains the following fields:
robotstxt, useragent, url, allowed/disallowed

allow/disallowed is expressed as a boolean, True/False

Reference:
Robots Exclusion Protocol (REP) draft-koster-rep-01
https://tools.ietf.org/html/draft-koster-rep
"""

import pytest
import robots

from .core import *

google_only_system = """
# GoogleOnly_System

user-agent: FooBot
disallow: /
"""

google_only_system_data = (
    # Empty robots.txt: everything allowed
    ['', FOOBOT_AGENT, '', ALLOWED],
    # Empty user agent to be matched: everything allowed
    [google_only_system, '', '', ALLOWED],

    # Empty url: implicitly disallowed, see method comment for GetPathParamsQuery in robots.cc.
    [google_only_system, FOOBOT_AGENT, '', DISALLOWED],

    # All params empty: same as robots.txt empty, everything allowed.
    ['', '', '', ALLOWED],
)


# Rules are colon separated name-value pairs. The following names are provisioned:
#     user-agent: <value>
#     allow: <value>
#     disallow: <value>
# See REP I-D section "Protocol Definition".
# https://tools.ietf.org/html/draft-koster-rep#section-2.1
# Google specific: webmasters sometimes miss the colon separator, but it's
# obvious what they mean by "disallow /", so we assume the colon if it's missing.

# Note: robotspy discards incorrect lines and does not implicitly assume that it is
# a webmaster mistake if a colon (:) is missing
@pytest.mark.parametrize('robots_txt,agent,path,allowed', google_only_system_data)
def test_useragent_wild_card(robots_txt, agent, path, allowed, can_fetch):
    assert can_fetch(robots_txt, agent, path) is allowed


linesyntax_line_correct = """
# ID_LineSyntax_Line (correct)

user-agent: FooBot
disallow: /
"""

linesyntax_line_incorrect = """
# ID_LineSyntax_Line (incorrect)

foo: FooBot
bar: /
"""

linesyntax_line_incorrect_accepted = """
# ID_LineSyntax_Line (mistake - missing ":" - accepted by Google

user-agent FooBot
disallow /
"""

url = 'http://foo.bar/x/y'

linesyntax_line_data = (
    [linesyntax_line_correct, FOOBOT_AGENT, url, DISALLOWED],
    [linesyntax_line_incorrect, FOOBOT_AGENT, url, ALLOWED],
    [linesyntax_line_incorrect_accepted, FOOBOT_AGENT, url, DISALLOWED],
)


@pytest.mark.parametrize('robots_txt,agent,path,allowed', linesyntax_line_data)
def test_linesyntax_line(robots_txt, agent, path, allowed, can_fetch):
    assert can_fetch(robots_txt, agent, path) is allowed


# A group is one or more user-agent line followed by rules, and terminated
# by a another user-agent line. Rules for same user-agents are combined
# opaquely into one group. Rules outside groups are ignored.
# See REP I-D section "Protocol Definition".
# https://tools.ietf.org/html/draft-koster-rep#section-2.1

linesyntax_group = """
# ID_LineSyntax_Groups

allow: /foo/bar/

user-agent: FooBot
disallow: /
allow: /x/
user-agent: BarBot
disallow: /
allow: /y/


allow: /w/
user-agent: BazBot

user-agent: FooBot
allow: /z/
disallow: /
"""

linesyntax_group_data = (
  [linesyntax_group, FOOBOT_AGENT, 'http://foo.bar/x/b', ALLOWED],
  [linesyntax_group, FOOBOT_AGENT, 'http://foo.bar/z/d', ALLOWED],
  [linesyntax_group, FOOBOT_AGENT, 'http://foo.bar/y/c', DISALLOWED],
  [linesyntax_group, 'BarBot', 'http://foo.bar/y/c', ALLOWED],
  [linesyntax_group, 'BarBot', 'http://foo.bar/w/a', ALLOWED],
  [linesyntax_group, 'BarBot', 'http://foo.bar/z/d', DISALLOWED],
  [linesyntax_group, 'BazBot', 'http://foo.bar/z/d', ALLOWED],

  # Lines with rules outside groups are ignored
  [linesyntax_group, FOOBOT_AGENT, 'http://foo.bar/foo/bar/', DISALLOWED],
  [linesyntax_group, 'BarBot', 'http://foo.bar/foo/bar/', DISALLOWED],
  [linesyntax_group, 'BazBot', 'http://foo.bar/foo/bar/', DISALLOWED],
)


@pytest.mark.parametrize('robots_txt,agent,path,allowed', linesyntax_group_data)
def test_linesyntax_group(robots_txt, agent, path, allowed, can_fetch):
    assert can_fetch(robots_txt, agent, path) is allowed


# Robot Exclusion Protocol (REP) lines are case insensitive.
# See REP I-D section "Protocol Definition".
# https://tools.ietf.org/html/draft-koster-rep#section-2.1

line_names_camel = """
# ID_REPLineNamesCaseInsensitive (camel)

uSeR-aGeNt: FooBot
AlLoW: /x/
dIsAlLoW: /
"""

line_names_lower = """
# ID_REPLineNamesCaseInsensitive (lower)

user-agent: FooBot
allow: /x/
disallow: /
"""

line_names_upper = """
# ID_REPLineNamesCaseInsensitive (upper)

USER-AGENT: FooBot
ALLOW: /x/
DISALLOW: /
"""

url_allowed = 'http://foo.bar/x/y'
url_disallowed = 'http://foo.bar/a/b'

line_names_case_insensitive_data = (
    [line_names_upper, FOOBOT_AGENT, url_allowed, ALLOWED],
    [line_names_lower, FOOBOT_AGENT, url_allowed, ALLOWED],
    [line_names_camel, FOOBOT_AGENT, url_allowed, ALLOWED],
    [line_names_upper, FOOBOT_AGENT, url_disallowed, DISALLOWED],
    [line_names_lower, FOOBOT_AGENT, url_disallowed, DISALLOWED],
    [line_names_upper, FOOBOT_AGENT, url_disallowed, DISALLOWED],
)


@pytest.mark.parametrize('robots_txt,agent,path,allowed', line_names_case_insensitive_data)
def test_line_names_case_insensitive(robots_txt, agent, path, allowed, can_fetch):
    assert can_fetch(robots_txt, agent, path) is allowed


# A user-agent line is expected to contain only [a-zA-Z_-] characters and must
# not be empty. See REP I-D section "The user-agent line".
# https://tools.ietf.org/html/draft-koster-rep#section-2.2.1
# ID_VerifyValidUserAgentsToObey
useragents_data = (
    ['Foobot', True],
    ['Foobot-Bar', True],
    ['Foo_Bar', True],
    #[None, False],
    ['', False],
    ['ツ', False],
    ['Foobot*', False],
    ['Foobot/2.1', False],
    ['Foobot Bar', False],
)


@pytest.mark.parametrize('agent,valid', useragents_data)
def test_valid_agent(agent, valid):
    assert robots.RobotsParser.is_agent_valid(agent) is valid


# The following test data is google specific as the Google robots parses the first string of the agent
# and ignore the rest. robotspy is intentionally stricter.
robots_upper = """
# ID_UserAgentValueCaseInsensitive (upper)

User-Agent: FOO BAR
Allow: /x/
Disallow: /
"""

robots_lower = """
# ID_UserAgentValueCaseInsensitive (lower)

User-Agent: foo bar
Allow: /x/
Disallow: /
"""

robots_camel = """
# ID_UserAgentValueCaseInsensitive (camel)

User-Agent: FoO bAr
Allow: /x/
Disallow: /
"""

url_allowed = "http://foo.bar/x/y"
url_disallowed = "http://foo.bar/a/b"

agent_case_insensitive_google_data = (
    [robots_upper, 'Foo', url_allowed, ALLOWED],
    [robots_lower, 'Foo', url_allowed, ALLOWED],
    [robots_camel, 'Foo', url_allowed, ALLOWED],
    [robots_upper, 'Foo', url_disallowed, DISALLOWED],
    [robots_lower, 'Foo', url_disallowed, DISALLOWED],
    [robots_camel, 'Foo', url_disallowed, DISALLOWED],
    [robots_upper, 'foo', url_allowed, ALLOWED],
    [robots_lower, 'foo', url_allowed, ALLOWED],
    [robots_camel, 'foo', url_allowed, ALLOWED],
    [robots_upper, 'foo', url_disallowed, DISALLOWED],
    [robots_lower, 'foo', url_disallowed, DISALLOWED],
    [robots_camel, 'foo', url_disallowed, DISALLOWED],
)


@pytest.mark.parametrize('robots_txt,agent,path,allowed', agent_case_insensitive_google_data)
def test_agent_case_insensitive_google(robots_txt, agent, path, allowed, can_fetch):
    assert can_fetch(robots_txt, agent, path) is allowed


# The following test data is modified from the google test data above and eliminates the space
# It allows to validate the case insensitivity of the user agent.
robots_upper = """
# ID_UserAgentValueCaseInsensitive (upper)

User-Agent: FOO
Allow: /x/
Disallow: /
"""

robots_lower = """
# ID_UserAgentValueCaseInsensitive (lower)

User-Agent: foo
Allow: /x/
Disallow: /
"""

robots_camel = """
# ID_UserAgentValueCaseInsensitive (camel)

User-Agent: FoO
Allow: /x/
Disallow: /
"""

agent_case_insensitive_data = (
    [robots_upper, 'Foo', url_allowed, ALLOWED],
    [robots_lower, 'Foo', url_allowed, ALLOWED],
    [robots_camel, 'Foo', url_allowed, ALLOWED],
    [robots_upper, 'Foo', url_disallowed, DISALLOWED],
    [robots_lower, 'Foo', url_disallowed, DISALLOWED],
    [robots_camel, 'Foo', url_disallowed, DISALLOWED],
    [robots_upper, 'foo', url_allowed, ALLOWED],
    [robots_lower, 'foo', url_allowed, ALLOWED],
    [robots_camel, 'foo', url_allowed, ALLOWED],
    [robots_upper, 'foo', url_disallowed, DISALLOWED],
    [robots_lower, 'foo', url_disallowed, DISALLOWED],
    [robots_camel, 'foo', url_disallowed, DISALLOWED],
)


@pytest.mark.parametrize('robots_txt,agent,path,allowed', agent_case_insensitive_data)
def test_agent_case_insensitive(robots_txt, agent, path, allowed, can_fetch):
    assert can_fetch(robots_txt, agent, path) is allowed


robotstxt_global = """
# ID_GlobalGroups_Secondary

user-agent: *
allow: /
user-agent: FooBot
disallow: /
"""

robotstxt_only_specific = """
# ID_GlobalGroups_Secondary

user-agent: FooBot
allow: /
user-agent: BarBot
disallow: /
user-agent: BazBot
disallow: /
"""

url = 'http://foo.bar/x/y'

robotstxt_global_data = (
    ['', FOOBOT_AGENT, url, ALLOWED],
    [robotstxt_global, FOOBOT_AGENT, url, DISALLOWED],
    [robotstxt_global, 'BarBot', url, ALLOWED],
    [robotstxt_only_specific, 'QusBot', url, ALLOWED],
)


@pytest.mark.parametrize('robots_txt,agent,path,allowed', robotstxt_global_data)
def test_robotstxt_global(robots_txt, agent, path, allowed, can_fetch):
    assert can_fetch(robots_txt, agent, path) is allowed


# Matching rules against URIs is case sensitive.
# See REP I-D section "The Allow and Disallow lines".
# https://tools.ietf.org/html/draft-koster-rep#section-2.2.2

robots_url_lower = """
# ID_AllowDisallow_Value_CaseSensitive (lower)

user-agent: FooBot
disallow: /x/
"""

robots_url_upper = """
# ID_AllowDisallow_Value_CaseSensitive (upper)
user-agent: FooBot
disallow: /X/
"""

url = 'http://foo.bar/x/y'

uri_case_sensitive_data = (
    [robots_url_lower, FOOBOT_AGENT, url, DISALLOWED],
    [robots_url_upper, FOOBOT_AGENT, url, ALLOWED],
)


@pytest.mark.parametrize('robots_txt,agent,path,allowed', uri_case_sensitive_data)
def test_uri_case_sensitive(robots_txt, agent, path, allowed, can_fetch):
    assert can_fetch(robots_txt, agent, path) is allowed


longest_match_01 = """
# ID_LongestMatch 01

user-agent: FooBot
disallow: /x/page.html
allow: /x/
"""

longest_match_02 = """
# ID_LongestMatch 02

user-agent: FooBot
allow: /x/page.html
disallow: /x/
"""

longest_match_03 = """
# ID_LongestMatch 03

user-agent: FooBot
disallow:
allow:
"""

longest_match_04 = """
# ID_LongestMatch 04

user-agent: FooBot
disallow: /
allow: /
"""

longest_match_05 = """
# ID_LongestMatch 05

user-agent: FooBot
disallow: /x
allow: /x/
"""

longest_match_06 = """
# ID_LongestMatch 06

user-agent: FooBot
disallow: /x/page.html
allow: /x/page.html
"""

longest_match_07 = """
# ID_LongestMatch 07

user-agent: FooBot
allow: /page
disallow: /*.html
"""

longest_match_08 = """
# ID_LongestMatch 08

user-agent: FooBot
allow: /x/page.
disallow: /*.html
"""

longest_match_09 = """
# ID_LongestMatch 09

User-agent: *
Disallow: /x/
User-agent: FooBot
Disallow: /y/
"""

url = 'http://foo.bar/x/page.html'

longest_match_data = (
    [longest_match_01, FOOBOT_AGENT, url, DISALLOWED],
    [longest_match_02, FOOBOT_AGENT, url, ALLOWED],
    [longest_match_02, FOOBOT_AGENT, 'http://foo.bar/x/', DISALLOWED],
    [longest_match_03, FOOBOT_AGENT, url, ALLOWED],
    [longest_match_04, FOOBOT_AGENT, url, ALLOWED],
    [longest_match_05, FOOBOT_AGENT, 'http://foo.bar/x', DISALLOWED],
    [longest_match_05, FOOBOT_AGENT, 'http://foo.bar/x/', ALLOWED],
    [longest_match_06, FOOBOT_AGENT, url, ALLOWED],
    [longest_match_07, FOOBOT_AGENT, 'http://foo.bar/page.html', DISALLOWED],
    [longest_match_07, FOOBOT_AGENT, 'http://foo.bar/page', ALLOWED],
    [longest_match_08, FOOBOT_AGENT, url, ALLOWED],
    [longest_match_08, FOOBOT_AGENT, 'http://foo.bar/x/y.html', DISALLOWED],

    [longest_match_09, FOOBOT_AGENT, 'http://foo.bar/x/page', ALLOWED],
    [longest_match_09, FOOBOT_AGENT, 'http://foo.bar/y/page', DISALLOWED],

)


@pytest.mark.parametrize('robots_txt,agent,path,allowed', longest_match_data)
def test_longest_match(robots_txt, agent, path, allowed, can_fetch):
    assert can_fetch(robots_txt, agent, path) is allowed


# Octets in the URI and robots.txt paths outside the range of the US-ASCII
# coded character set, and those in the reserved range defined by RFC3986,
# MUST be percent-encoded as defined by RFC3986 prior to comparison.
# See REP I-D section "The Allow and Disallow lines".
# https://tools.ietf.org/html/draft-koster-rep#section-2.2.2
#
# NOTE: It's up to the caller to percent encode a URL before passing it to the
# parser. Percent encoding URIs in the rules is unnecessary.


encoding_01 = """
# ID_Encoding 01

User-agent: FooBot
Disallow: /
Allow: /foo/bar?qux=taz&baz=http://foo.bar?tar&par
"""

encoding_02 = """
# ID_Encoding 02

User-agent: FooBot
Disallow: /
Allow: /foo/bar/ツ
"""

encoding_03 = """
# ID_Encoding 03

User-agent: FooBot
Disallow: /
Allow: /foo/bar/%E3%83%84
"""

encoding_04 = """
# ID_Encoding 04

User-agent: FooBot
Disallow: /
Allow: /foo/bar/%62%61%7A
"""

# TODO: Revisit the encoding to match Google robots?
encoding_data = (
    [encoding_01, FOOBOT_AGENT, 'http://foo.bar/foo/bar?qux=taz&baz=http://foo.bar?tar&par', ALLOWED],
    [encoding_02, FOOBOT_AGENT, 'http://foo.bar/foo/bar/%E3%83%84"', ALLOWED],
    [encoding_02, FOOBOT_AGENT, 'http://foo.bar/foo/bar/ツ', ALLOWED],     # Google -> DISALLOWED
    [encoding_03, FOOBOT_AGENT, 'http://foo.bar/foo/bar/%E3%83%84', ALLOWED],
    [encoding_03, FOOBOT_AGENT, 'http://foo.bar/foo/bar/ツ', ALLOWED],      # Google -> DISALLOWED
    [encoding_04, FOOBOT_AGENT, 'http://foo.bar/foo/bar/baz', ALLOWED],     # Google -> DISALLOWED
    [encoding_04, FOOBOT_AGENT, 'http://foo.bar/foo/bar/%62%61%7A', ALLOWED],
)


@pytest.mark.parametrize('robots_txt,agent,path,allowed', encoding_data)
def test_encoding(robots_txt, agent, path, allowed, can_fetch):
    assert can_fetch(robots_txt, agent, path) is allowed


special_characters_01 = """
# ID_SpecialCharacters 01

User-agent: FooBot
Disallow: /foo/bar/quz
Allow: /foo/*/qux
"""

special_characters_02 = """
# ID_SpecialCharacters 02

User-agent: FooBot
Disallow: /foo/bar$
Allow: /foo/bar/qux
"""

special_characters_03 = """
# ID_SpecialCharacters 03

User-agent: FooBot
# Disallow: /
Disallow: /foo/quz#qux
Allow: /
"""

special_characters_data = (
    [special_characters_01, FOOBOT_AGENT, 'http://foo.bar/foo/bar/quz', DISALLOWED],
    [special_characters_01, FOOBOT_AGENT, 'http://foo.bar/foo/quz', ALLOWED],
    [special_characters_01, FOOBOT_AGENT, 'http://foo.bar/foo//quz', ALLOWED],
    [special_characters_01, FOOBOT_AGENT, 'http://foo.bar/foo/bax/quz', ALLOWED],
    [special_characters_02, FOOBOT_AGENT, 'http://foo.bar/foo/bar', DISALLOWED],
    [special_characters_02, FOOBOT_AGENT, 'http://foo.bar/foo/bar/qux', ALLOWED],
    [special_characters_02, FOOBOT_AGENT, 'http://foo.bar/foo/bar/', ALLOWED],
    [special_characters_02, FOOBOT_AGENT, 'http://foo.bar/foo/bar/baz', ALLOWED],
    [special_characters_03, FOOBOT_AGENT, 'http://foo.bar/foo/bar', ALLOWED],
    [special_characters_03, FOOBOT_AGENT, 'http://foo.bar/foo/quz', DISALLOWED],
)

# Skip:
# - GoogleOnly_IndexHTMLisDirectory
# - GoogleOnly_LineTooLong

google_doc_01 = """
# GoogleOnly_DocumentationChecks 01

user-agent: FooBot
disallow: /
allow: /fish
"""

google_doc_02 = """
# GoogleOnly_DocumentationChecks 02

user-agent: FooBot
disallow: /
allow: /fish*
"""

google_doc_03 = """
# GoogleOnly_DocumentationChecks 03

user-agent: FooBot
disallow: /
allow: /fish/
"""

google_doc_data = (
    [google_doc_01, FOOBOT_AGENT, 'http://foo.bar/bar', DISALLOWED],
    [google_doc_01, FOOBOT_AGENT, 'http://foo.bar/fish', ALLOWED],
    [google_doc_01, FOOBOT_AGENT, 'http://foo.bar/fish.html', ALLOWED],
    [google_doc_01, FOOBOT_AGENT, 'http://foo.bar/fish/salmon.html', ALLOWED],
    [google_doc_01, FOOBOT_AGENT, 'http://foo.bar/fishheads', ALLOWED],
    [google_doc_01, FOOBOT_AGENT, 'http://foo.bar/fishheads/yummy.html', ALLOWED],
    [google_doc_01, FOOBOT_AGENT, 'http://foo.bar/fish.html?id=anything', ALLOWED],
    [google_doc_01, FOOBOT_AGENT, 'http://foo.bar/Fish.asp', DISALLOWED],
    [google_doc_01, FOOBOT_AGENT, 'http://foo.bar/catfish', DISALLOWED],
    [google_doc_01, FOOBOT_AGENT, 'http://foo.bar/?id=fish', DISALLOWED],

    # "/fish*" equals "/fish"
    [google_doc_02, FOOBOT_AGENT, 'http://foo.bar/bar', DISALLOWED],
    [google_doc_02, FOOBOT_AGENT, 'http://foo.bar/fish', ALLOWED],
    [google_doc_02, FOOBOT_AGENT, 'http://foo.bar/fish.html', ALLOWED],
    [google_doc_02, FOOBOT_AGENT, 'http://foo.bar/fish/salmon.html', ALLOWED],
    [google_doc_02, FOOBOT_AGENT, 'http://foo.bar/fishheads', ALLOWED],
    [google_doc_02, FOOBOT_AGENT, 'http://foo.bar/fishheads/yummy.html', ALLOWED],
    [google_doc_02, FOOBOT_AGENT, 'http://foo.bar/fish.html?id=anything', ALLOWED],
    [google_doc_02, FOOBOT_AGENT, 'http://foo.bar/Fish.bar', DISALLOWED],
    [google_doc_02, FOOBOT_AGENT, 'http://foo.bar/catfish', DISALLOWED],
    [google_doc_02, FOOBOT_AGENT, 'http://foo.bar/?id=fish', DISALLOWED],

    # "/fish/" does not equal "/fish"
    [google_doc_03, FOOBOT_AGENT, 'http://foo.bar/bar', DISALLOWED],
    [google_doc_03, FOOBOT_AGENT, 'http://foo.bar/fish/', ALLOWED],
    [google_doc_03, FOOBOT_AGENT, 'http://foo.bar/fish/salmon', ALLOWED],
    [google_doc_03, FOOBOT_AGENT, 'http://foo.bar/fish/?salmon', ALLOWED],
    [google_doc_03, FOOBOT_AGENT, 'http://foo.bar/fish/salmon.html', ALLOWED],
    [google_doc_03, FOOBOT_AGENT, 'http://foo.bar/fish/?id=anything', ALLOWED],
    [google_doc_03, FOOBOT_AGENT, 'http://foo.bar/fish', DISALLOWED],
    [google_doc_03, FOOBOT_AGENT, 'http://foo.bar/fish.html', DISALLOWED],
    [google_doc_03, FOOBOT_AGENT, 'http://foo.bar/Fish/Salmon.html', DISALLOWED],
)


@pytest.mark.parametrize('robots_txt,agent,path,allowed', google_doc_data)
def test_google_doc(robots_txt, agent, path, allowed, can_fetch):
    assert can_fetch(robots_txt, agent, path) is allowed


google_php_01 = """
# GoogleOnly_DocumentationChecks PHP 01

user-agent: FooBot
disallow: /
allow: /*.php
"""

google_php_02 = """
# GoogleOnly_DocumentationChecks PHP 02

user-agent: FooBot
disallow: /
allow: /*.php$
"""

google_php_03 = """
# GoogleOnly_DocumentationChecks PHP 03

user-agent: FooBot
disallow: /
allow: /fish*.php
"""

google_php_data = (
    # "/*.php"
    [google_php_01, FOOBOT_AGENT, 'http://foo.bar/bar', DISALLOWED],
    [google_php_01, FOOBOT_AGENT, 'http://foo.bar/filename.php', ALLOWED],
    [google_php_01, FOOBOT_AGENT, 'http://foo.bar/folder/filename.php', ALLOWED],
    [google_php_01, FOOBOT_AGENT, 'http://foo.bar/folder/filename.php?parameters', ALLOWED],
    [google_php_01, FOOBOT_AGENT, 'http://foo.bar/filename.php/', ALLOWED],
    [google_php_01, FOOBOT_AGENT, 'http://foo.bar/index?f=filename.php/', ALLOWED],
    [google_php_01, FOOBOT_AGENT, 'http://foo.bar/php/', DISALLOWED],
    [google_php_01, FOOBOT_AGENT, 'http://foo.bar/index?php', DISALLOWED],
    [google_php_01, FOOBOT_AGENT, 'http://foo.bar/windows.PHP', DISALLOWED],

    # "/*.php$"
    [google_php_02, FOOBOT_AGENT, 'http://foo.bar/bar', DISALLOWED],
    [google_php_02, FOOBOT_AGENT, 'http://foo.bar/filename.php', ALLOWED],
    [google_php_02, FOOBOT_AGENT, 'http://foo.bar/folder/filename.php', ALLOWED],
    [google_php_02, FOOBOT_AGENT, 'http://foo.bar/filename.php?parameters', DISALLOWED],
    [google_php_02, FOOBOT_AGENT, 'http://foo.bar/filename.php/', DISALLOWED],
    [google_php_02, FOOBOT_AGENT, 'http://foo.bar/filename.php5', DISALLOWED],
    [google_php_02, FOOBOT_AGENT, 'http://foo.bar/filename?php', DISALLOWED],
    [google_php_02, FOOBOT_AGENT, 'http://foo.bar/aaaphpaaa', DISALLOWED],
    [google_php_02, FOOBOT_AGENT, 'http://foo.bar//windows.PHP', DISALLOWED],

    # "/fish*.php"
    [google_php_03, FOOBOT_AGENT, 'http://foo.bar/bar', DISALLOWED],
    [google_php_03, FOOBOT_AGENT, 'http://foo.bar/fish.php', ALLOWED],
    [google_php_03, FOOBOT_AGENT, 'http://foo.bar/fishheads/catfish.php?parameters', ALLOWED],
    [google_php_03, FOOBOT_AGENT, 'http://foo.bar/Fish.PHP', DISALLOWED],
)


@pytest.mark.parametrize('robots_txt,agent,path,allowed', google_php_data)
def test_google_php(robots_txt, agent, path, allowed, can_fetch):
    assert can_fetch(robots_txt, agent, path) is allowed


# Order of precedence for group-member records
order_precedence_01 = """
# GoogleOnly_DocumentationChecks 01 (Order Precedence)

user-agent: FooBot
allow: /folder
disallow: /folder
"""

order_precedence_02 = """
# GoogleOnly_DocumentationChecks 02 (Order Precedence)

user-agent: FooBot
allow: /folder
disallow: /folder
"""

order_precedence_03 = """
# GoogleOnly_DocumentationChecks 03 (Order Precedence)

user-agent: FooBot
allow: /page
disallow: /*.htm
"""

order_precedence_04 = """
# GoogleOnly_DocumentationChecks 04 (Order Precedence)

user-agent: FooBot
allow: /$
disallow: /
"""

order_precedence_data = (
    [order_precedence_01, FOOBOT_AGENT, 'http://example.com/page', ALLOWED],
    [order_precedence_02, FOOBOT_AGENT, 'http://example.com/folder/page', ALLOWED],
    [order_precedence_03, FOOBOT_AGENT, 'http://example.com/page.htm', DISALLOWED],
    [order_precedence_04, FOOBOT_AGENT, 'http://example.com/', ALLOWED],
    [order_precedence_04, FOOBOT_AGENT, 'http://example.com/page.html', DISALLOWED],
)


@pytest.mark.parametrize('robots_txt,agent,path,allowed', order_precedence_data)
def test_order_precedence(robots_txt, agent, path, allowed, can_fetch):
    assert can_fetch(robots_txt, agent, path) is allowed
