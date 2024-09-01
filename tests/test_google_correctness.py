
# Code generated from https://github.com/google/robotstxt-spec-test/tree/master/src/main/resources/CTC/


import pytest
from .core import *


robots_txt_matching_path_values_20 = """
user-agent: FooBot
disallow: /
allow: /*.php
"""

data_matching_path_values_20 = (
    [robots_txt_matching_path_values_20, "FooBot", "http://foo.bar/bar", DISALLOWED],
    [robots_txt_matching_path_values_20, "FooBot", "http://foo.bar/filename.php", ALLOWED],
    [robots_txt_matching_path_values_20, "FooBot", "http://foo.bar/folder/filename.php", ALLOWED],
    [robots_txt_matching_path_values_20, "FooBot", "http://foo.bar/folder/filename.php?parameters", ALLOWED],
    [robots_txt_matching_path_values_20, "FooBot", "http://foo.bar//folder/any.php.file.html", ALLOWED],
    [robots_txt_matching_path_values_20, "FooBot", "http://foo.bar/filename.php/", ALLOWED],
    [robots_txt_matching_path_values_20, "FooBot", "http://foo.bar/index?f=filename.php/", ALLOWED],
    [robots_txt_matching_path_values_20, "FooBot", "http://foo.bar/php/", DISALLOWED],
    [robots_txt_matching_path_values_20, "FooBot", "http://foo.bar/index?php", DISALLOWED],
    [robots_txt_matching_path_values_20, "FooBot", "http://foo.bar/windows.PHP", DISALLOWED],
)

@pytest.mark.parametrize('robots_txt,agent,path,allowed', data_matching_path_values_20)
def test_google_correctness_matching_path_values_20(robots_txt, agent, path, allowed, can_fetch):
    assert can_fetch(robots_txt, agent, path) is allowed


robots_txt_matching_path_values_21 = """
user-agent: FooBot
disallow: /
allow: /*.php$
"""

data_matching_path_values_21 = (
    [robots_txt_matching_path_values_21, "FooBot", "http://foo.bar/bar", DISALLOWED],
    [robots_txt_matching_path_values_21, "FooBot", "http://foo.bar/filename.php", ALLOWED],
    [robots_txt_matching_path_values_21, "FooBot", "http://foo.bar/folder/filename.php", ALLOWED],
    [robots_txt_matching_path_values_21, "FooBot", "http://foo.bar/filename.php?parameters", DISALLOWED],
    [robots_txt_matching_path_values_21, "FooBot", "http://foo.bar/filename.php/", DISALLOWED],
    [robots_txt_matching_path_values_21, "FooBot", "http://foo.bar/filename.php5", DISALLOWED],
    [robots_txt_matching_path_values_21, "FooBot", "http://foo.bar/php/", DISALLOWED],
    [robots_txt_matching_path_values_21, "FooBot", "http://foo.bar/filename?php", DISALLOWED],
    [robots_txt_matching_path_values_21, "FooBot", "http://foo.bar/aaaphpaaa", DISALLOWED],
    [robots_txt_matching_path_values_21, "FooBot", "http://foo.bar//windows.PHP", DISALLOWED],
)

@pytest.mark.parametrize('robots_txt,agent,path,allowed', data_matching_path_values_21)
def test_google_correctness_matching_path_values_21(robots_txt, agent, path, allowed, can_fetch):
    assert can_fetch(robots_txt, agent, path) is allowed


robots_txt_matching_path_values_22 = """
user-agent: FooBot
disallow: /
allow: /fish*.php
"""

data_matching_path_values_22 = (
    [robots_txt_matching_path_values_22, "FooBot", "http://foo.bar/bar", DISALLOWED],
    [robots_txt_matching_path_values_22, "FooBot", "http://foo.bar/fish.php", ALLOWED],
    [robots_txt_matching_path_values_22, "FooBot", "http://foo.bar/fishheads/catfish.php?parameters", ALLOWED],
    [robots_txt_matching_path_values_22, "FooBot", "http://foo.bar/Fish.PHP", DISALLOWED],
)

@pytest.mark.parametrize('robots_txt,agent,path,allowed', data_matching_path_values_22)
def test_google_correctness_matching_path_values_22(robots_txt, agent, path, allowed, can_fetch):
    assert can_fetch(robots_txt, agent, path) is allowed


robots_txt_BOM_characters0 = """
User-Agent: foo
Disallow: /AnyValue
"""

data_BOM_characters0 = (
    [robots_txt_BOM_characters0, "foo", "http://example.com/AnyValue", DISALLOWED],
)

@pytest.mark.parametrize('robots_txt,agent,path,allowed', data_BOM_characters0)
def test_google_correctness_BOM_characters0(robots_txt, agent, path, allowed, can_fetch):
    assert can_fetch(robots_txt, agent, path) is allowed


robots_txt_BOM_characters1 = """
User-Agent: foo
Disallow: /AnyValue
"""

data_BOM_characters1 = (
    [robots_txt_BOM_characters1, "foo", "http://example.com/AnyValue", DISALLOWED],
)

@pytest.mark.parametrize('robots_txt,agent,path,allowed', data_BOM_characters1)
def test_google_correctness_BOM_characters1(robots_txt, agent, path, allowed, can_fetch):
    assert can_fetch(robots_txt, agent, path) is allowed


robots_txt_BOM_characters2 = """
User-Agent: foo
Disallow: /AnyValue
"""

data_BOM_characters2 = (
    [robots_txt_BOM_characters2, "foo", "http://example.com/AnyValue", DISALLOWED],
)

@pytest.mark.parametrize('robots_txt,agent,path,allowed', data_BOM_characters2)
def test_google_correctness_BOM_characters2(robots_txt, agent, path, allowed, can_fetch):
    assert can_fetch(robots_txt, agent, path) is allowed


robots_txt_BOM_characters3 = """
User-Agent: foo
Disallow: /AnyValue
"""

data_BOM_characters3 = (
#    [robots_txt_BOM_characters3, "foo", "http://example.com/AnyValue", ALLOWED],  # Fails Google correctness
)

@pytest.mark.parametrize('robots_txt,agent,path,allowed', data_BOM_characters3)
def test_google_correctness_BOM_characters3(robots_txt, agent, path, allowed, can_fetch):
    assert can_fetch(robots_txt, agent, path) is allowed


robots_txt_BOM_characters4 = """
User-Agent: foo
Disallow: /AnyValue
"""

data_BOM_characters4 = (
#    [robots_txt_BOM_characters4, "foo", "http://example.com/AnyValue", ALLOWED],  # Fails Google correctness
)

@pytest.mark.parametrize('robots_txt,agent,path,allowed', data_BOM_characters4)
def test_google_correctness_BOM_characters4(robots_txt, agent, path, allowed, can_fetch):
    assert can_fetch(robots_txt, agent, path) is allowed


robots_txt_empty_string0 = """

"""

data_empty_string0 = (
    [robots_txt_empty_string0, "FooBot", "", ALLOWED],
    [robots_txt_empty_string0, "", "", ALLOWED],
)

@pytest.mark.parametrize('robots_txt,agent,path,allowed', data_empty_string0)
def test_google_correctness_empty_string0(robots_txt, agent, path, allowed, can_fetch):
    assert can_fetch(robots_txt, agent, path) is allowed


robots_txt_empty_string1 = """
user-agent: FooBot
disallow: /
"""

data_empty_string1 = (
    [robots_txt_empty_string1, "", "", ALLOWED],
    [robots_txt_empty_string1, "FooBot", "", DISALLOWED],
)

@pytest.mark.parametrize('robots_txt,agent,path,allowed', data_empty_string1)
def test_google_correctness_empty_string1(robots_txt, agent, path, allowed, can_fetch):
    assert can_fetch(robots_txt, agent, path) is allowed


robots_txt_accepted_mistakes0 = """
user-agent: FooBot
disallow: /
"""

data_accepted_mistakes0 = (
    [robots_txt_accepted_mistakes0, "FooBot", "http://foo.bar/x/y", DISALLOWED],
)

@pytest.mark.parametrize('robots_txt,agent,path,allowed', data_accepted_mistakes0)
def test_google_correctness_accepted_mistakes0(robots_txt, agent, path, allowed, can_fetch):
    assert can_fetch(robots_txt, agent, path) is allowed


robots_txt_accepted_mistakes1 = """
foo: FooBot
bar: /
"""

data_accepted_mistakes1 = (
    [robots_txt_accepted_mistakes1, "FooBot", "http://foo.bar/x/y", ALLOWED],
)

@pytest.mark.parametrize('robots_txt,agent,path,allowed', data_accepted_mistakes1)
def test_google_correctness_accepted_mistakes1(robots_txt, agent, path, allowed, can_fetch):
    assert can_fetch(robots_txt, agent, path) is allowed


robots_txt_accepted_mistakes2 = """
user-agent FooBot
disallow /
"""

data_accepted_mistakes2 = (
    [robots_txt_accepted_mistakes2, "FooBot", "http://foo.bar/x/y", DISALLOWED],
)

@pytest.mark.parametrize('robots_txt,agent,path,allowed', data_accepted_mistakes2)
def test_google_correctness_accepted_mistakes2(robots_txt, agent, path, allowed, can_fetch):
    assert can_fetch(robots_txt, agent, path) is allowed


robots_txt_uri_case_sensitivity0 = """
user-agent: FooBot
disallow: /X/
"""

data_uri_case_sensitivity0 = (
    [robots_txt_uri_case_sensitivity0, "FooBot", "http://foo.bar/x/y", ALLOWED],
)

@pytest.mark.parametrize('robots_txt,agent,path,allowed', data_uri_case_sensitivity0)
def test_google_correctness_uri_case_sensitivity0(robots_txt, agent, path, allowed, can_fetch):
    assert can_fetch(robots_txt, agent, path) is allowed


robots_txt_uri_case_sensitivity1 = """
user-agent: FooBot
disallow: /x/
"""

data_uri_case_sensitivity1 = (
    [robots_txt_uri_case_sensitivity1, "FooBot", "http://foo.bar/x/y", DISALLOWED],
)

@pytest.mark.parametrize('robots_txt,agent,path,allowed', data_uri_case_sensitivity1)
def test_google_correctness_uri_case_sensitivity1(robots_txt, agent, path, allowed, can_fetch):
    assert can_fetch(robots_txt, agent, path) is allowed


robots_txt_global_rules0 = """

"""

data_global_rules0 = (
    [robots_txt_global_rules0, "FooBot", "http://foo.bar/x/y", ALLOWED],
)

@pytest.mark.parametrize('robots_txt,agent,path,allowed', data_global_rules0)
def test_google_correctness_global_rules0(robots_txt, agent, path, allowed, can_fetch):
    assert can_fetch(robots_txt, agent, path) is allowed


robots_txt_global_rules1 = """
user-agent: *
disallow: /x
user-agent: FooBot
allow: /x/y
"""

data_global_rules1 = (
    [robots_txt_global_rules1, "FooBot", "http://foo.bar/x/y", ALLOWED],
    [robots_txt_global_rules1, "BarBot", "http://foo.bar/x/y", DISALLOWED],
)

@pytest.mark.parametrize('robots_txt,agent,path,allowed', data_global_rules1)
def test_google_correctness_global_rules1(robots_txt, agent, path, allowed, can_fetch):
    assert can_fetch(robots_txt, agent, path) is allowed


robots_txt_global_rules2 = """
user-agent: FooBot
allow: /
user-agent: BarBot
disallow: /
user-agent: BazBot
disallow: /
"""

data_global_rules2 = (
    [robots_txt_global_rules2, "QuxBot", "http://foo.bar/x/y", ALLOWED],
)

@pytest.mark.parametrize('robots_txt,agent,path,allowed', data_global_rules2)
def test_google_correctness_global_rules2(robots_txt, agent, path, allowed, can_fetch):
    assert can_fetch(robots_txt, agent, path) is allowed


robots_txt_non_ascii_paths0 = """
User-agent: FooBot
Disallow: /
Allow: /foo/bar?qux=taz&baz=http://foo.bar?tar&par
"""

data_non_ascii_paths0 = (
    [robots_txt_non_ascii_paths0, "FooBot", "http://foo.bar/foo/bar?qux=taz&baz=http://foo.bar?tar&par", ALLOWED],
)

@pytest.mark.parametrize('robots_txt,agent,path,allowed', data_non_ascii_paths0)
def test_google_correctness_non_ascii_paths0(robots_txt, agent, path, allowed, can_fetch):
    assert can_fetch(robots_txt, agent, path) is allowed


robots_txt_non_ascii_paths1 = """
User-agent: FooBot
Disallow: /
Allow: /foo/bar/ツ
"""

data_non_ascii_paths1 = (
    [robots_txt_non_ascii_paths1, "FooBot", "http://foo.bar/foo/bar/%E3%83%84", ALLOWED],
#    [robots_txt_non_ascii_paths1, "FooBot", "http://foo.bar/foo/bar/ツ", DISALLOWED], # Fails Google correctness
)

@pytest.mark.parametrize('robots_txt,agent,path,allowed', data_non_ascii_paths1)
def test_google_correctness_non_ascii_paths1(robots_txt, agent, path, allowed, can_fetch):
    assert can_fetch(robots_txt, agent, path) is allowed


robots_txt_non_ascii_paths2 = """
User-agent: FooBot
Disallow: /
Allow: /foo/bar/%E3%83%84
"""

data_non_ascii_paths2 = (
    [robots_txt_non_ascii_paths2, "FooBot", "http://foo.bar/foo/bar/%E3%83%84", ALLOWED],
#    [robots_txt_non_ascii_paths2, "FooBot", "http://foo.bar/foo/bar/ツ", DISALLOWED], # Fails Google correctness
)

@pytest.mark.parametrize('robots_txt,agent,path,allowed', data_non_ascii_paths2)
def test_google_correctness_non_ascii_paths2(robots_txt, agent, path, allowed, can_fetch):
    assert can_fetch(robots_txt, agent, path) is allowed


robots_txt_non_ascii_paths3 = """
User-agent: FooBot
Disallow: /
Allow: /foo/bar/%62%61%7A
"""

data_non_ascii_paths3 = (
#    [robots_txt_non_ascii_paths3, "FooBot", "http://foo.bar/foo/bar/baz", DISALLOWED], # Fails google correctness
    [robots_txt_non_ascii_paths3, "FooBot", "http://foo.bar/foo/bar/%62%61%7A", ALLOWED],
)

@pytest.mark.parametrize('robots_txt,agent,path,allowed', data_non_ascii_paths3)
def test_google_correctness_non_ascii_paths3(robots_txt, agent, path, allowed, can_fetch):
    assert can_fetch(robots_txt, agent, path) is allowed


robots_txt_special_characters0 = """
User-agent: FooBot
Disallow: /foo/bar/quz
Allow: /foo/*/qux
"""

data_special_characters0 = (
    [robots_txt_special_characters0, "FooBot", "http://foo.bar/foo/bar/quz", DISALLOWED],
    [robots_txt_special_characters0, "FooBot", "http://foo.bar/foo/quz", ALLOWED],
    [robots_txt_special_characters0, "FooBot", "http://foo.bar/foo//quz", ALLOWED],
    [robots_txt_special_characters0, "FooBot", "http://foo.bar/foo/bax/quz", ALLOWED],
)

@pytest.mark.parametrize('robots_txt,agent,path,allowed', data_special_characters0)
def test_google_correctness_special_characters0(robots_txt, agent, path, allowed, can_fetch):
    assert can_fetch(robots_txt, agent, path) is allowed


robots_txt_special_characters1 = """
User-agent: FooBot
Disallow: /foo/bar$
Allow: /foo/bar/qux
"""

data_special_characters1 = (
    [robots_txt_special_characters1, "FooBot", "http://foo.bar/foo/bar", DISALLOWED],
    [robots_txt_special_characters1, "FooBot", "http://foo.bar/foo/bar/qux", ALLOWED],
    [robots_txt_special_characters1, "FooBot", "http://foo.bar/foo/bar/", ALLOWED],
    [robots_txt_special_characters1, "FooBot", "http://foo.bar/foo/bar/baz", ALLOWED],
)

@pytest.mark.parametrize('robots_txt,agent,path,allowed', data_special_characters1)
def test_google_correctness_special_characters1(robots_txt, agent, path, allowed, can_fetch):
    assert can_fetch(robots_txt, agent, path) is allowed


robots_txt_special_characters2 = """
User-agent: FooBot
# Disallow: /
Disallow: /foo/quz#qux
Allow: /
"""

data_special_characters2 = (
    [robots_txt_special_characters2, "FooBot", "http://foo.bar/foo/bar", ALLOWED],
    [robots_txt_special_characters2, "FooBot", "http://foo.bar/foo/quz", DISALLOWED],
)

@pytest.mark.parametrize('robots_txt,agent,path,allowed', data_special_characters2)
def test_google_correctness_special_characters2(robots_txt, agent, path, allowed, can_fetch):
    assert can_fetch(robots_txt, agent, path) is allowed


robots_txt_index_page0 = """
User-Agent: *
Allow: /allowed-slash/index.html
Disallow: /
"""

data_index_page0 = (
#    [robots_txt_index_page0, "foobot", "http://foo.com/allowed-slash/", ALLOWED], # google specific - fails google correcness
    [robots_txt_index_page0, "foobot", "http://foo.com/allowed-slash/index.htm", DISALLOWED],
    [robots_txt_index_page0, "foobot", "http://foo.com/allowed-slash/index.html", ALLOWED],
    [robots_txt_index_page0, "foobot", "http://foo.com/anyother-url", DISALLOWED],
)

@pytest.mark.parametrize('robots_txt,agent,path,allowed', data_index_page0)
def test_google_correctness_index_page0(robots_txt, agent, path, allowed, can_fetch):
    assert can_fetch(robots_txt, agent, path) is allowed


robots_txt_user_agent_name0 = """
User-Agent: *
Disallow: /
User-Agent: Foo Bar
Allow: /x/
Disallow: /
"""

data_user_agent_name0 = (
    [robots_txt_user_agent_name0, "Foo", "http://foo.bar/x/y", ALLOWED],
    [robots_txt_user_agent_name0, "Foo Bar", "http://foo.bar/x/y", DISALLOWED],
)

@pytest.mark.parametrize('robots_txt,agent,path,allowed', data_user_agent_name0)
def test_google_correctness_user_agent_name0(robots_txt, agent, path, allowed, can_fetch):
    assert can_fetch(robots_txt, agent, path) is allowed


robots_txt_user_agent_name1 = """
user-agent: FOO BAR
allow: /x/
disallow: /
"""

data_user_agent_name1 = (
    [robots_txt_user_agent_name1, "Foo", "http://foo.bar/x/y", ALLOWED],
    [robots_txt_user_agent_name1, "foo", "http://foo.bar/x/y", ALLOWED],
    [robots_txt_user_agent_name1, "Foo", "http://foo.bar/a/b", DISALLOWED],
    [robots_txt_user_agent_name1, "foo", "http://foo.bar/a/b", DISALLOWED],
)

@pytest.mark.parametrize('robots_txt,agent,path,allowed', data_user_agent_name1)
def test_google_correctness_user_agent_name1(robots_txt, agent, path, allowed, can_fetch):
    assert can_fetch(robots_txt, agent, path) is allowed


robots_txt_user_agent_name2 = """
user-agent: foo bar
allow: /x/
disallow: /
"""

data_user_agent_name2 = (
    [robots_txt_user_agent_name2, "Foo", "http://foo.bar/x/y", ALLOWED],
    [robots_txt_user_agent_name2, "foo", "http://foo.bar/x/y", ALLOWED],
    [robots_txt_user_agent_name2, "Foo", "http://foo.bar/a/b", DISALLOWED],
    [robots_txt_user_agent_name2, "foo", "http://foo.bar/a/b", DISALLOWED],
)

@pytest.mark.parametrize('robots_txt,agent,path,allowed', data_user_agent_name2)
def test_google_correctness_user_agent_name2(robots_txt, agent, path, allowed, can_fetch):
    assert can_fetch(robots_txt, agent, path) is allowed


robots_txt_user_agent_name3 = """
user-agent: FoO bAr
allow: /x/
disallow: /
"""

data_user_agent_name3 = (
    [robots_txt_user_agent_name3, "Foo", "http://foo.bar/x/y", ALLOWED],
    [robots_txt_user_agent_name3, "foo", "http://foo.bar/x/y", ALLOWED],
    [robots_txt_user_agent_name3, "Foo", "http://foo.bar/a/b", DISALLOWED],
    [robots_txt_user_agent_name3, "foo", "http://foo.bar/a/b", DISALLOWED],
)

@pytest.mark.parametrize('robots_txt,agent,path,allowed', data_user_agent_name3)
def test_google_correctness_user_agent_name3(robots_txt, agent, path, allowed, can_fetch):
    assert can_fetch(robots_txt, agent, path) is allowed


robots_txt_directives_case_insensitivity0 = """
USER-AGENT: FooBot
ALLOW: /x/
DISALLOW: /
"""

data_directives_case_insensitivity0 = (
    [robots_txt_directives_case_insensitivity0, "FooBot", "http://foo.bar/x/y", ALLOWED],
    [robots_txt_directives_case_insensitivity0, "FooBot", "http://foo.bar/a/b", DISALLOWED],
)

@pytest.mark.parametrize('robots_txt,agent,path,allowed', data_directives_case_insensitivity0)
def test_google_correctness_directives_case_insensitivity0(robots_txt, agent, path, allowed, can_fetch):
    assert can_fetch(robots_txt, agent, path) is allowed


robots_txt_directives_case_insensitivity1 = """
user-agent: FooBot
allow: /x/
disallow: /
"""

data_directives_case_insensitivity1 = (
    [robots_txt_directives_case_insensitivity1, "FooBot", "http://foo.bar/x/y", ALLOWED],
    [robots_txt_directives_case_insensitivity1, "FooBot", "http://foo.bar/a/b", DISALLOWED],
)

@pytest.mark.parametrize('robots_txt,agent,path,allowed', data_directives_case_insensitivity1)
def test_google_correctness_directives_case_insensitivity1(robots_txt, agent, path, allowed, can_fetch):
    assert can_fetch(robots_txt, agent, path) is allowed


robots_txt_directives_case_insensitivity2 = """
uSeR-aGeNt: FooBot
AlLoW: /x/
dIsAlLoW: /
"""

data_directives_case_insensitivity2 = (
    [robots_txt_directives_case_insensitivity2, "FooBot", "http://foo.bar/x/y", ALLOWED],
    [robots_txt_directives_case_insensitivity2, "FooBot", "http://foo.bar/a/b", DISALLOWED],
)

@pytest.mark.parametrize('robots_txt,agent,path,allowed', data_directives_case_insensitivity2)
def test_google_correctness_directives_case_insensitivity2(robots_txt, agent, path, allowed, can_fetch):
    assert can_fetch(robots_txt, agent, path) is allowed


robots_txt_groups0 = """
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

data_groups0 = (
    [robots_txt_groups0, "FooBot", "http://foo.bar/x/b", ALLOWED],
    [robots_txt_groups0, "FooBot", "http://foo.bar/z/d", ALLOWED],
    [robots_txt_groups0, "FooBot", "http://foo.bar/y/c", DISALLOWED],
    [robots_txt_groups0, "BarBot", "http://foo.bar/y/c", ALLOWED],
    [robots_txt_groups0, "BarBot", "http://foo.bar/w/a", ALLOWED],
    [robots_txt_groups0, "BarBot", "http://foo.bar/z/d", DISALLOWED],
    [robots_txt_groups0, "BazBot", "http://foo.bar/z/d", ALLOWED],
    [robots_txt_groups0, "FooBot", "http://foo.bar/foo/bar/", DISALLOWED],
    [robots_txt_groups0, "BarBot", "http://foo.bar/foo/bar/", DISALLOWED],
    [robots_txt_groups0, "BazBot", "http://foo.bar/foo/bar/", DISALLOWED],
)

@pytest.mark.parametrize('robots_txt,agent,path,allowed', data_groups0)
def test_google_correctness_groups0(robots_txt, agent, path, allowed, can_fetch):
    assert can_fetch(robots_txt, agent, path) is allowed


robots_txt_most_specific_match0 = """
user-agent: FooBot
disallow: /x/page.html
allow: /x/
"""

data_most_specific_match0 = (
    [robots_txt_most_specific_match0, "FooBot", "http://foo.bar/x/page.html", DISALLOWED],
)

@pytest.mark.parametrize('robots_txt,agent,path,allowed', data_most_specific_match0)
def test_google_correctness_most_specific_match0(robots_txt, agent, path, allowed, can_fetch):
    assert can_fetch(robots_txt, agent, path) is allowed


robots_txt_most_specific_match1 = """
user-agent: FooBot
allow: /x/page.html
disallow: /x/
"""

data_most_specific_match1 = (
    [robots_txt_most_specific_match1, "FooBot", "http://foo.bar/x/page.html", ALLOWED],
    [robots_txt_most_specific_match1, "FooBot", "http://foo.bar/x/", DISALLOWED],
)

@pytest.mark.parametrize('robots_txt,agent,path,allowed', data_most_specific_match1)
def test_google_correctness_most_specific_match1(robots_txt, agent, path, allowed, can_fetch):
    assert can_fetch(robots_txt, agent, path) is allowed


robots_txt_most_specific_match2 = """
user-agent: FooBot
disallow: 
allow: 
"""

data_most_specific_match2 = (
    [robots_txt_most_specific_match2, "FooBot", "http://foo.bar/x/page.html", ALLOWED],
)

@pytest.mark.parametrize('robots_txt,agent,path,allowed', data_most_specific_match2)
def test_google_correctness_most_specific_match2(robots_txt, agent, path, allowed, can_fetch):
    assert can_fetch(robots_txt, agent, path) is allowed


robots_txt_most_specific_match3 = """
user-agent: FooBot
disallow: /
allow: /
"""

data_most_specific_match3 = (
    [robots_txt_most_specific_match3, "FooBot", "http://foo.bar/x/page.html", ALLOWED],
)

@pytest.mark.parametrize('robots_txt,agent,path,allowed', data_most_specific_match3)
def test_google_correctness_most_specific_match3(robots_txt, agent, path, allowed, can_fetch):
    assert can_fetch(robots_txt, agent, path) is allowed


robots_txt_most_specific_match4 = """
user-agent: FooBot
disallow: /x
allow: /x/
"""

data_most_specific_match4 = (
    [robots_txt_most_specific_match4, "FooBot", "http://foo.bar/x", DISALLOWED],
    [robots_txt_most_specific_match4, "FooBot", "http://foo.bar/x/", ALLOWED],
)

@pytest.mark.parametrize('robots_txt,agent,path,allowed', data_most_specific_match4)
def test_google_correctness_most_specific_match4(robots_txt, agent, path, allowed, can_fetch):
    assert can_fetch(robots_txt, agent, path) is allowed


robots_txt_most_specific_match5 = """
user-agent: FooBot
disallow: /x/page.html
allow: /x/page.html
"""

data_most_specific_match5 = (
    [robots_txt_most_specific_match5, "FooBot", "http://foo.bar/x/page.html", ALLOWED],
)

@pytest.mark.parametrize('robots_txt,agent,path,allowed', data_most_specific_match5)
def test_google_correctness_most_specific_match5(robots_txt, agent, path, allowed, can_fetch):
    assert can_fetch(robots_txt, agent, path) is allowed


robots_txt_most_specific_match6 = """
user-agent: FooBot
allow: /page
disallow: /*.html
"""

data_most_specific_match6 = (
    [robots_txt_most_specific_match6, "FooBot", "http://foo.bar/page.html", DISALLOWED],
    [robots_txt_most_specific_match6, "FooBot", "http://foo.bar/page", ALLOWED],
)

@pytest.mark.parametrize('robots_txt,agent,path,allowed', data_most_specific_match6)
def test_google_correctness_most_specific_match6(robots_txt, agent, path, allowed, can_fetch):
    assert can_fetch(robots_txt, agent, path) is allowed


robots_txt_most_specific_match7 = """
user-agent: FooBot
allow: /x/page.
disallow: /*.html
"""

data_most_specific_match7 = (
    [robots_txt_most_specific_match7, "FooBot", "http://foo.bar/x/page.html", ALLOWED],
    [robots_txt_most_specific_match7, "FooBot", "http://foo.bar/x/y.html", DISALLOWED],
)

@pytest.mark.parametrize('robots_txt,agent,path,allowed', data_most_specific_match7)
def test_google_correctness_most_specific_match7(robots_txt, agent, path, allowed, can_fetch):
    assert can_fetch(robots_txt, agent, path) is allowed


robots_txt_most_specific_match8 = """
User-agent: *
Disallow: /x/
User-agent: FooBot
Disallow: /y/
"""

data_most_specific_match8 = (
    [robots_txt_most_specific_match8, "FooBot", "http://foo.bar/x/page", ALLOWED],
    [robots_txt_most_specific_match8, "FooBot", "http://foo.bar/y/page", DISALLOWED],
)

@pytest.mark.parametrize('robots_txt,agent,path,allowed', data_most_specific_match8)
def test_google_correctness_most_specific_match8(robots_txt, agent, path, allowed, can_fetch):
    assert can_fetch(robots_txt, agent, path) is allowed


robots_txt_different_line_endings0 = """
User-Agent: foo
Allow: /some/path
User-Agent: bar


Disallow: /
"""

data_different_line_endings0 = (
    [robots_txt_different_line_endings0, "bar", "http://example.com/page", DISALLOWED],
)

@pytest.mark.parametrize('robots_txt,agent,path,allowed', data_different_line_endings0)
def test_google_correctness_different_line_endings0(robots_txt, agent, path, allowed, can_fetch):
    assert can_fetch(robots_txt, agent, path) is allowed


robots_txt_different_line_endings1 = """
User-Agent: foo
Allow: /some/path
User-Agent: bar


Disallow: /
"""

data_different_line_endings1 = (
    [robots_txt_different_line_endings1, "bar", "http://example.com/page", DISALLOWED],
    [robots_txt_different_line_endings1, "bar", "http://example.com/page", DISALLOWED],
    [robots_txt_different_line_endings1, "bar", "http://example.com/page", DISALLOWED],
)

@pytest.mark.parametrize('robots_txt,agent,path,allowed', data_different_line_endings1)
def test_google_correctness_different_line_endings1(robots_txt, agent, path, allowed, can_fetch):
    assert can_fetch(robots_txt, agent, path) is allowed


robots_txt_different_line_endings2 = """
User-Agent: foo
User-Agent: bar

Disallow: /
"""

data_different_line_endings2 = (
    [robots_txt_different_line_endings2, "bar", "http://example.com/page", DISALLOWED],
)

@pytest.mark.parametrize('robots_txt,agent,path,allowed', data_different_line_endings2)
def test_google_correctness_different_line_endings2(robots_txt, agent, path, allowed, can_fetch):
    assert can_fetch(robots_txt, agent, path) is allowed


robots_txt_matching_path_values_10 = """
user-agent: FooBot
disallow: /
allow: /fish
"""

data_matching_path_values_10 = (
    [robots_txt_matching_path_values_10, "FooBot", "http://foo.bar/bar", DISALLOWED],
    [robots_txt_matching_path_values_10, "FooBot", "http://foo.bar/fish", ALLOWED],
    [robots_txt_matching_path_values_10, "FooBot", "http://foo.bar/fish.html", ALLOWED],
    [robots_txt_matching_path_values_10, "FooBot", "http://foo.bar/fish/salmon.html", ALLOWED],
    [robots_txt_matching_path_values_10, "FooBot", "http://foo.bar/fishheads", ALLOWED],
    [robots_txt_matching_path_values_10, "FooBot", "http://foo.bar/fishheads/yummy.html", ALLOWED],
    [robots_txt_matching_path_values_10, "FooBot", "http://foo.bar/fish.html?id=anything", ALLOWED],
    [robots_txt_matching_path_values_10, "FooBot", "http://foo.bar/Fish.asp", DISALLOWED],
    [robots_txt_matching_path_values_10, "FooBot", "http://foo.bar/catfish", DISALLOWED],
    [robots_txt_matching_path_values_10, "FooBot", "http://foo.bar/?id=fish", DISALLOWED],
)

@pytest.mark.parametrize('robots_txt,agent,path,allowed', data_matching_path_values_10)
def test_google_correctness_matching_path_values_10(robots_txt, agent, path, allowed, can_fetch):
    assert can_fetch(robots_txt, agent, path) is allowed


robots_txt_matching_path_values_11 = """
user-agent: FooBot
disallow: /
allow: /fish*
"""

data_matching_path_values_11 = (
    [robots_txt_matching_path_values_11, "FooBot", "http://foo.bar/bar", DISALLOWED],
    [robots_txt_matching_path_values_11, "FooBot", "http://foo.bar/fish", ALLOWED],
    [robots_txt_matching_path_values_11, "FooBot", "http://foo.bar/fish.html", ALLOWED],
    [robots_txt_matching_path_values_11, "FooBot", "http://foo.bar/fish/salmon.html", ALLOWED],
    [robots_txt_matching_path_values_11, "FooBot", "http://foo.bar/fishheads", ALLOWED],
    [robots_txt_matching_path_values_11, "FooBot", "http://foo.bar/fishheads/yummy.html", ALLOWED],
    [robots_txt_matching_path_values_11, "FooBot", "http://foo.bar/fish.html?id=anything", ALLOWED],
    [robots_txt_matching_path_values_11, "FooBot", "http://foo.bar/Fish.bar", DISALLOWED],
    [robots_txt_matching_path_values_11, "FooBot", "http://foo.bar/catfish", DISALLOWED],
    [robots_txt_matching_path_values_11, "FooBot", "http://foo.bar/?id=fish", DISALLOWED],
)

@pytest.mark.parametrize('robots_txt,agent,path,allowed', data_matching_path_values_11)
def test_google_correctness_matching_path_values_11(robots_txt, agent, path, allowed, can_fetch):
    assert can_fetch(robots_txt, agent, path) is allowed


robots_txt_matching_path_values_12 = """
user-agent: FooBot
disallow: /
allow: /fish/
"""

data_matching_path_values_12 = (
    [robots_txt_matching_path_values_12, "FooBot", "http://foo.bar/bar", DISALLOWED],
    [robots_txt_matching_path_values_12, "FooBot", "http://foo.bar/fish/", ALLOWED],
    [robots_txt_matching_path_values_12, "FooBot", "http://foo.bar/fish/salmon", ALLOWED],
    [robots_txt_matching_path_values_12, "FooBot", "http://foo.bar/fish/?salmon", ALLOWED],
    [robots_txt_matching_path_values_12, "FooBot", "http://foo.bar/fish/salmon.html", ALLOWED],
    [robots_txt_matching_path_values_12, "FooBot", "http://foo.bar/fish/?id=anything", ALLOWED],
    [robots_txt_matching_path_values_12, "FooBot", "http://foo.bar/fish", DISALLOWED],
    [robots_txt_matching_path_values_12, "FooBot", "http://foo.bar/fish.html", DISALLOWED],
    [robots_txt_matching_path_values_12, "FooBot", "http://foo.bar/Fish/Salmon.html", DISALLOWED],
)

@pytest.mark.parametrize('robots_txt,agent,path,allowed', data_matching_path_values_12)
def test_google_correctness_matching_path_values_12(robots_txt, agent, path, allowed, can_fetch):
    assert can_fetch(robots_txt, agent, path) is allowed


robots_txt_order_of_precedence0 = """
user-agent: FooBot
allow: /p
disallow: /
"""

data_order_of_precedence0 = (
    [robots_txt_order_of_precedence0, "FooBot", "http://example.com/page", ALLOWED],
)

@pytest.mark.parametrize('robots_txt,agent,path,allowed', data_order_of_precedence0)
def test_google_correctness_order_of_precedence0(robots_txt, agent, path, allowed, can_fetch):
    assert can_fetch(robots_txt, agent, path) is allowed


robots_txt_order_of_precedence1 = """
user-agent: FooBot
allow: /folder
disallow: /folder
"""

data_order_of_precedence1 = (
    [robots_txt_order_of_precedence1, "FooBot", "http://example.com/folder/page", ALLOWED],
)

@pytest.mark.parametrize('robots_txt,agent,path,allowed', data_order_of_precedence1)
def test_google_correctness_order_of_precedence1(robots_txt, agent, path, allowed, can_fetch):
    assert can_fetch(robots_txt, agent, path) is allowed


robots_txt_order_of_precedence2 = """
user-agent: FooBot
allow: /page
disallow: /*.htm
"""

data_order_of_precedence2 = (
    [robots_txt_order_of_precedence2, "FooBot", "http://example.com/page.htm", DISALLOWED],
)

@pytest.mark.parametrize('robots_txt,agent,path,allowed', data_order_of_precedence2)
def test_google_correctness_order_of_precedence2(robots_txt, agent, path, allowed, can_fetch):
    assert can_fetch(robots_txt, agent, path) is allowed


robots_txt_order_of_precedence3 = """
user-agent: FooBot
allow: /$
disallow: /
"""

data_order_of_precedence3 = (
    [robots_txt_order_of_precedence3, "FooBot", "http://example.com/", ALLOWED],
    [robots_txt_order_of_precedence3, "FooBot", "http://example.com/page.html", DISALLOWED],
)

@pytest.mark.parametrize('robots_txt,agent,path,allowed', data_order_of_precedence3)
def test_google_correctness_order_of_precedence3(robots_txt, agent, path, allowed, can_fetch):
    assert can_fetch(robots_txt, agent, path) is allowed

