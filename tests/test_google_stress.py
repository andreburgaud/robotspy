
# Code generated from https://github.com/google/robotstxt-spec-test/tree/master/src/main/resources/CTC/


import pytest
from .core import *


robots_txt_638845 = """
# For more information about the robots.txt standard, see:
# http://www.robotstxt.org/orig.html
#

User-agent: *
Disallow: /main/
Disallow: /store/
Disallow: /scp/
Disallow: /mods/
Disallow: /view/
Disallow: /deps/
Disallow: /setup/
Disallow: /language/
Disallow: /libs/
Disallow: /data/
Disallow: /media/
Disallow: /parts/
Disallow: /plugins/
Disallow: /help/
Disallow: /tmp/

"""

data_638845 = (
    [robots_txt_638845, "foobot", "http://example.com/", ALLOWED],
    [robots_txt_638845, "foobot", "http://example.com/index.html", ALLOWED],
    [robots_txt_638845, "foobot", "http://example.com/scp/data", DISALLOWED],
    [robots_txt_638845, "foobot", "http://example.com/medi", ALLOWED],
    [robots_txt_638845, "foobot", "http://example.com/media", ALLOWED],
    [robots_txt_638845, "foobot", "http://example.com/loogs?user=admin", ALLOWED],
)

@pytest.mark.parametrize('robots_txt,agent,path,allowed', data_638845)
def test_google_stress_638845(robots_txt, agent, path, allowed, can_fetch):
    assert can_fetch(robots_txt, agent, path) is allowed


robots_txt_308278 = """
User-agent: *
Disallow: /asdf-login
Disallow: /asdf-admin
Disallow: /databack/
Disallow: /data/*
Disallow: /?*/
Disallow: /author/
Disallow: /id/*/page/
Disallow: /id/*/data/
Sitemap: http://example.com/page-sitemap.xml
"""

data_308278 = (
    [robots_txt_308278, "foobot", "http://example.com/asdf-login", DISALLOWED],
    [robots_txt_308278, "foobot", "http://example.com/asdf-login/", DISALLOWED],
    [robots_txt_308278, "foobot", "http://example.com/", ALLOWED],
    [robots_txt_308278, "foobot", "http://example.com/databack", ALLOWED],
    [robots_txt_308278, "foobot", "http://example.com/databack/recent", DISALLOWED],
    [robots_txt_308278, "foobot", "http://example.com/foo/?user=admin/data", ALLOWED],
    [robots_txt_308278, "foobot", "http://example.com/?user=admin/data", DISALLOWED],
    [robots_txt_308278, "foobot", "http://example.com/id/page/", ALLOWED],
    [robots_txt_308278, "foobot", "http://example.com/id/some/page/", DISALLOWED],
    [robots_txt_308278, "foobot", "http://example.com/id/some/data", ALLOWED],
    [robots_txt_308278, "foobot", "http://example.com/id/some/data/more", DISALLOWED],
)

@pytest.mark.parametrize('robots_txt,agent,path,allowed', data_308278)
def test_google_stress_308278(robots_txt, agent, path, allowed, can_fetch):
    assert can_fetch(robots_txt, agent, path) is allowed


robots_txt_943687 = """
# Today I heard something new and unmemorable
# If I don’t like something, I’ll stay away from it
# Everyone was busy, so I went to the movie alone
#
# For more information about the robots.txt standard, see:
# http://www.robotstxt.org/orig.html
#
# For syntax checking, see:
# http://example.com/robots-checker.phtml

User-agent: *
Disallow: /admin/
Disallow: /bin/
Disallow: /cache/
Disallow: /clion/
Disallow: /components/
Disallow: /excludes/
Disallow: /deinstallation/
Disallow: /layouts/
Disallow: /libraries/
Disallow: /logs/
Disallow: /plugins/
Disallow: /tmp/

"""

data_943687 = (
    [robots_txt_943687, "foobot", "http://www.example.com/foo/bar", ALLOWED],
    [robots_txt_943687, "foobot", "http://www.example.com/admin/settings", DISALLOWED],
    [robots_txt_943687, "foobot", "http://www.example.com/bin/sh", DISALLOWED],
    [robots_txt_943687, "foo-bot", "http://www.example.com/search?req=123", ALLOWED],
    [robots_txt_943687, "foo_bot", "http://www.example.com/log/113", ALLOWED],
    [robots_txt_943687, "foo_bot", "http://www.example.com/logs/113", DISALLOWED],
    [robots_txt_943687, "foo-bot", "http://www.example.com/example/admin", ALLOWED],
    [robots_txt_943687, "foobot", "http://www.example.com/admin", ALLOWED],
    [robots_txt_943687, "foobot", "http://www.example.com/admin/", DISALLOWED],
    [robots_txt_943687, "foo_bot", "http://www.example.com/dev/null", ALLOWED],
    [robots_txt_943687, "foo_bot", "http://www.example.com/tmp/null", DISALLOWED],
)

@pytest.mark.parametrize('robots_txt,agent,path,allowed', data_943687)
def test_google_stress_943687(robots_txt, agent, path, allowed, can_fetch):
    assert can_fetch(robots_txt, agent, path) is allowed


robots_txt_584234 = """
User-agent: barbot
Disallow: /

User-agent: bazbot
Disallow: /

User-agent: qux_bot
Crawl-delay: 1

User-agent: *
Allow: /

User-agent: *
Crawl-delay: 1
"""

data_584234 = (
    [robots_txt_584234, "barbot", "http://example.com/foo/bar", DISALLOWED],
    [robots_txt_584234, "barbot", "http://example.com/foo/foo/foo", DISALLOWED],
    [robots_txt_584234, "barbot", "http://example.com/index.html", DISALLOWED],
    [robots_txt_584234, "bazbot", "http://example.com/secrets/123", DISALLOWED],
    [robots_txt_584234, "bazbot", "http://example.com/log?id=113", DISALLOWED],
    [robots_txt_584234, "qux_bot", "http://example.com/index.html", ALLOWED],
    [robots_txt_584234, "qux_bot", "http://example.com/foo/bar", ALLOWED],
    [robots_txt_584234, "qux_bot", "http://example.com/", ALLOWED],
    [robots_txt_584234, "foobot", "http://example.com/foo/bar", ALLOWED],
    [robots_txt_584234, "foobot", "http://example.com/log?id=113", ALLOWED],
)

@pytest.mark.parametrize('robots_txt,agent,path,allowed', data_584234)
def test_google_stress_584234(robots_txt, agent, path, allowed, can_fetch):
    assert can_fetch(robots_txt, agent, path) is allowed


robots_txt_912555 = """
User-Agent: *
Disallow: /error$
Disallow: /jm/com.example.FooController
Disallow: /log
Disallow: /admin$
Disallow: /adminactions$
Disallow: /adminactions?
Disallow: /baz
Disallow: /jm/com.example.BarController
Sitemap: https://example.com/sitemap.xml
"""

data_912555 = (
    [robots_txt_912555, "foobot", "http://example.com/error?user=admin", ALLOWED],
    [robots_txt_912555, "foobot", "http://example.com/error", DISALLOWED],
    [robots_txt_912555, "foo_bot", "http://example.com/search/foo", ALLOWED],
    [robots_txt_912555, "foo_bot", "http://example.com/log", DISALLOWED],
    [robots_txt_912555, "foo-bot", "http://example.com/adminactions", DISALLOWED],
    [robots_txt_912555, "foo-bot", "http://example.com/adminactions?id=123", DISALLOWED],
    [robots_txt_912555, "foo-bot", "http://example.com/adminactions/new", ALLOWED],
    [robots_txt_912555, "foobot", "http://example.com/jm/test.txt", ALLOWED],
    [robots_txt_912555, "foobot", "http://example.com/jm/com.example.BarController", DISALLOWED],
    [robots_txt_912555, "foobot", "http://example.com/foo/bar", ALLOWED],
)

@pytest.mark.parametrize('robots_txt,agent,path,allowed', data_912555)
def test_google_stress_912555(robots_txt, agent, path, allowed, can_fetch):
    assert can_fetch(robots_txt, agent, path) is allowed


robots_txt_174022 = """
User-agent: *
Disallow: /view-responses.html
Disallow: /help.html
Disallow: /chat/reviews/view/
Disallow: /chat/view/
Disallow: /chat/view/hg/
Disallow: /chat/view/asd/
Disallow: /chat/asd/
Disallow: /chat/trackback/
Disallow: /chat/wp/
Disallow: /chat/*/reviews/view/$
Disallow: /chat/*/view/$
Disallow: /chat/*/view/hg/$
Disallow: /chat/*/view/asd/$
Disallow: /chat/*/asd/$
Disallow: /chat/*/trackback/$
Disallow: /contact-someone.html
"""

data_174022 = (
    [robots_txt_174022, "FooBot", "http://example.com/", ALLOWED],
    [robots_txt_174022, "foobot", "http://example.com/search?req=123", ALLOWED],
    [robots_txt_174022, "Foo_Bot", "http://example.com/view-responses.html", DISALLOWED],
    [robots_txt_174022, "barbot", "http://example.com/chat/", ALLOWED],
    [robots_txt_174022, "BarBot", "http://example.com/chat/reviews/view/112", DISALLOWED],
    [robots_txt_174022, "BazBot", "http://example.com/chat/view", ALLOWED],
    [robots_txt_174022, "BazBot", "http://example.com/chat/view/hg", DISALLOWED],
    [robots_txt_174022, "FooBot", "http://example.com/chat/foo/bar/baz/view/", DISALLOWED],
    [robots_txt_174022, "barbot", "http://example.com/chat/something/asd/", DISALLOWED],
    [robots_txt_174022, "BarBot", "http://example.com/chat/asd/", DISALLOWED],
    [robots_txt_174022, "QuxBot", "http://example.com/contact-someone.html?user=foo", DISALLOWED],
)

@pytest.mark.parametrize('robots_txt,agent,path,allowed', data_174022)
def test_google_stress_174022(robots_txt, agent, path, allowed, can_fetch):
    assert can_fetch(robots_txt, agent, path) is allowed


robots_txt_860237 = """
User-Agent: *
Crawl-delay : 60
Disallow : /*baz*
Disallow : /*qux*

User-agent: XYZ123bot
Crawl-delay : 60
Disallow: /

"""

data_860237 = (
    [robots_txt_860237, "Foobot", "http://example.com/", ALLOWED],
    [robots_txt_860237, "foo-bot", "http://example.com/foo/bar", ALLOWED],
    [robots_txt_860237, "foo_bot", "http://example.com/robots.txt", ALLOWED],
    [robots_txt_860237, "foo_bot", "http://example.com/new_baz", DISALLOWED],
    [robots_txt_860237, "foo_bot", "http://example.com/baz/new", DISALLOWED],
    [robots_txt_860237, "foo-bot", "http://example.com/move/qux/add", DISALLOWED],
    [robots_txt_860237, "foo_bot", "http://example.com/baznew/start", DISALLOWED],
    [robots_txt_860237, "Foobot", "http://example.com/foo_qux_bar", DISALLOWED],
    [robots_txt_860237, "XYZ123bot", "http://example.com/robots.txt", ALLOWED],
    [robots_txt_860237, "XYZ", "http://example.com/robots.txt", DISALLOWED],
)

@pytest.mark.parametrize('robots_txt,agent,path,allowed', data_860237)
def test_google_stress_860237(robots_txt, agent, path, allowed, can_fetch):
    assert can_fetch(robots_txt, agent, path) is allowed


robots_txt_777406 = """
User-agent: *
Allow: /

# Optimization for Baz Bot
User-Agent: FunBot-Baz-Mobile
User-Agent: FunBot-Baz
Disallow: /_api/*
Disallow: /_misc*
Disallow: /media/v1/view/*

Sitemap: https://www.example.com/sitemap.xml
"""

data_777406 = (
    [robots_txt_777406, "foobot", "http://www.example.com/foo/bar", ALLOWED],
    [robots_txt_777406, "foo_bot", "http://www.example.com/", ALLOWED],
    [robots_txt_777406, "foo-bot", "http://www.example.com/robots.txt", ALLOWED],
    [robots_txt_777406, "FunBot-Baz-Mobile", "http://www.example.com/_api/index.html", DISALLOWED],
    [robots_txt_777406, "FunBot-Baz-Mobile", "http://www.example.com/_misc", DISALLOWED],
    [robots_txt_777406, "FunBot-Baz-Mobile", "http://www.example.com/_media/v2/foo", ALLOWED],
    [robots_txt_777406, "FunBot-Baz-Mobile", "http://www.example.com/media/v1/view/", DISALLOWED],
    [robots_txt_777406, "FunBot-Baz", "http://www.example.com/media/v1/view/foo", DISALLOWED],
    [robots_txt_777406, "foo-bot", "http://www.example.com/media/v1/view/foo", ALLOWED],
    [robots_txt_777406, "foo_bot", "http://www.example.com/_misc/index.html", ALLOWED],
)

@pytest.mark.parametrize('robots_txt,agent,path,allowed', data_777406)
def test_google_stress_777406(robots_txt, agent, path, allowed, can_fetch):
    assert can_fetch(robots_txt, agent, path) is allowed


robots_txt_768939 = """
User-agent: *
Crawl-delay: 3500
Disallow: /ab_controller
Disallow: /ab_imports
Disallow: /ab_content/bar
Disallow: /ab_content/cache
Disallow: /ab_content/baz
"""

data_768939 = (
    [robots_txt_768939, "foobot", "http://www.example.com/ab_controller", DISALLOWED],
    [robots_txt_768939, "foo_bot", "http://www.example.com/ab_controller-foo", DISALLOWED],
    [robots_txt_768939, "foo-bot", "http://www.example.com/ab_imports/foo.txt", DISALLOWED],
    [robots_txt_768939, "foobot", "http://www.example.com/foo/bar", ALLOWED],
    [robots_txt_768939, "foobot", "http://www.example.com/ab_content/foo", ALLOWED],
    [robots_txt_768939, "foo_bot", "http://www.example.com/ab_content/bar/foo.bar", DISALLOWED],
    [robots_txt_768939, "foo-bot", "http://www.example.com/ab_content/cache-foo", DISALLOWED],
    [robots_txt_768939, "foo-bot", "http://www.example.com/", ALLOWED],
)

@pytest.mark.parametrize('robots_txt,agent,path,allowed', data_768939)
def test_google_stress_768939(robots_txt, agent, path, allowed, can_fetch):
    assert can_fetch(robots_txt, agent, path) is allowed


robots_txt_517712 = """
# Some comment
# http://www.exapmle.com/something.html



# Some more explanation to lines below
# (and some line wrapping)

User-agent: *
Disallow:



# Some comments regarding some specific robot restrictions
# maybe regarding his functionality
# and some website to visit
# http://www.example.com/some/help/about/quxbot?arg=123

User-Agent: Quxbot
Disallow: /*dispatch_request$
Disallow: /*directory_ctors$
"""

data_517712 = (
    [robots_txt_517712, "foobot", "http://example.com/", ALLOWED],
    [robots_txt_517712, "FooBot", "http://example.com/search?req=123", ALLOWED],
    [robots_txt_517712, "foobot", "http://example.com/foo/bar/dispatch_request", ALLOWED],
    [robots_txt_517712, "foo-bot", "http://example.com/bar/baz/foler_ctors", ALLOWED],
    [robots_txt_517712, "Quxbot", "http://example.com/", ALLOWED],
    [robots_txt_517712, "barbot", "http://example.com/robots.txt", ALLOWED],
    [robots_txt_517712, "Quxbot", "http://example.com/baz/dispatch_request", DISALLOWED],
    [robots_txt_517712, "Quxbot", "http://example.com/baz/dispatch_request?args=123", ALLOWED],
    [robots_txt_517712, "Quxbot", "http://example.com/new_directory_ctors", DISALLOWED],
    [robots_txt_517712, "Quxbot", "http://example.com/bar/baz/directory_ctors", DISALLOWED],
)

@pytest.mark.parametrize('robots_txt,agent,path,allowed', data_517712)
def test_google_stress_517712(robots_txt, agent, path, allowed, can_fetch):
    assert can_fetch(robots_txt, agent, path) is allowed


robots_txt_894248 = """
User-agent: *
Disallow: /ab-baz/
Allow: /ab-baz/baz-ajax.php

Sitemap: https://example.com/ab-sitemap.xml
"""

data_894248 = (
    [robots_txt_894248, "FooBot", "http://example.com/", ALLOWED],
    [robots_txt_894248, "Foo_Bot", "http://example.com/foo/bar.php", ALLOWED],
    [robots_txt_894248, "foobot", "http://example.com/ab-baz/index.htm", DISALLOWED],
    [robots_txt_894248, "foo-bot", "http://example.com/ab-baz/foo/bar", DISALLOWED],
    [robots_txt_894248, "foo_bot", "http://example.com/ab-baz/baz-ajax.php", ALLOWED],
    [robots_txt_894248, "foo-bot", "http://example.com/ab-baz/baz-ajax.php?user=123", ALLOWED],
)

@pytest.mark.parametrize('robots_txt,agent,path,allowed', data_894248)
def test_google_stress_894248(robots_txt, agent, path, allowed, can_fetch):
    assert can_fetch(robots_txt, agent, path) is allowed


robots_txt_155227 = """
User-agent: *
Crawl-delay: 10
# Foo
Disallow: /asdf-main/
Disallow: /asdf-media/
Disallow: /asdf-shared/
# Bar
Disallow: /asdf-control.php
Disallow: /asdf-control-sample.php
Disallow: /asdf-settings.php
"""

data_155227 = (
    [robots_txt_155227, "foobot", "http://example.com/", ALLOWED],
    [robots_txt_155227, "foo_bot", "http://example.com/bar/index.html", ALLOWED],
    [robots_txt_155227, "foo-bot", "http://example.com/asdf-control.pdf", ALLOWED],
    [robots_txt_155227, "foobot", "http://example.com/asdf-control.php", DISALLOWED],
    [robots_txt_155227, "foobot", "http://example.com/asdf-control-sample.php", DISALLOWED],
    [robots_txt_155227, "foobot", "http://example.com/asdf-control-simple.php", ALLOWED],
    [robots_txt_155227, "FooBot", "http://example.com/asdf-settings.php", DISALLOWED],
    [robots_txt_155227, "Foo-Bot", "http://example.com/asdf-shared/index.html", DISALLOWED],
)

@pytest.mark.parametrize('robots_txt,agent,path,allowed', data_155227)
def test_google_stress_155227(robots_txt, agent, path, allowed, can_fetch):
    assert can_fetch(robots_txt, agent, path) is allowed


robots_txt_701159 = """
User-agent: foofoobot*
Disallow: /workers/
Disallow: /media/common/
Disallow: /misc/
Disallow: /bin/
Disallow: /trash/

User-agent: barbarbot*
Disallow: /workers/
Disallow: /media/common/
Disallow: /misc/
Disallow: /bin/
Disallow: /trash/

User-agent: quxbot
Disallow: /workers/
Disallow: /media/common/
Disallow: /misc/
Disallow: /bin/
Disallow: /trash/

User-agent: ddbot
Disallow: /workers/
Disallow: /media/common/
Disallow: /misc/
Disallow: /bin/
Disallow: /trash/

User-agent: toebot
Disallow: /workers/
Disallow: /media/common/
Disallow: /misc/
Disallow: /bin/
Disallow: /trash/

User-agent: io_tester
Disallow: /workers/
Disallow: /media/common/
Disallow: /misc/
Disallow: /bin/
Disallow: /trash/

User-agent: *
Disallow: /


Sitemap: http://www.example.com/sitemap.xml
"""

data_701159 = (
    [robots_txt_701159, "foofoobot-exp", "http://example.com/workers/log", DISALLOWED],
    [robots_txt_701159, "foofoobot", "http://example.com/trash/index.html", DISALLOWED],
    [robots_txt_701159, "barbarbot-prod", "http://example.com/bin/bash", DISALLOWED],
    [robots_txt_701159, "barbarbot-prod", "http://example.com/foo/bar", DISALLOWED],
    [robots_txt_701159, "barbarbot", "http://example.com/bin/bash", DISALLOWED],
    [robots_txt_701159, "barbarbot", "http://example.com/foo/bar", ALLOWED],
    [robots_txt_701159, "quxbot", "http://example.com/qux/qux/qux", ALLOWED],
    [robots_txt_701159, "quxbot", "http://example.com/trash/view.html", DISALLOWED],
    [robots_txt_701159, "io_tester", "http://example.com/search?req=123", ALLOWED],
    [robots_txt_701159, "io_tester", "http://example.com/media/common/123", DISALLOWED],
    [robots_txt_701159, "foo_bot", "http://example.com/search?req=123", DISALLOWED],
)

@pytest.mark.parametrize('robots_txt,agent,path,allowed', data_701159)
def test_google_stress_701159(robots_txt, agent, path, allowed, can_fetch):
    assert can_fetch(robots_txt, agent, path) is allowed


robots_txt_541230 = """
User-agent: *
Allow: /*.js
Allow: /*.css
Allow: /*.jpg
Allow: /*.png
Allow: /*.gif
Allow: /*?page
Allow: /*?ref=
Disallow: /*?
Disallow: /stat/
Disallow: /id/1
Disallow: /id/3
Disallow: /register
Disallow: /id/5
Disallow: /id/7
Disallow: /id/8
Disallow: /id/9
Disallow: /id/sub/
Disallow: /panel/
Disallow: /admin/
Disallow: /informer/
Disallow: /secure/
Disallow: /poll/
Disallow: /search/
Disallow: /abnl/
Disallow: /*_escaped_pattern_=
Disallow: /*-*-*-*-321$
Disallow: /baz/order/
Disallow: /baz/printorder/
Disallow: /baz/checkout/
Disallow: /baz/user/
Disallow: /baz/search
Disallow: /*0-*-0-03$
Disallow: /*-0-0-

Sitemap: http://example.com/sitemap.xml
Sitemap: http://example.com/sitemap-forum.xml
"""

data_541230 = (
    [robots_txt_541230, "foobot", "http://example.com/foo.js", ALLOWED],
    [robots_txt_541230, "foobot", "http://example.com/foo/bar.css", ALLOWED],
    [robots_txt_541230, "foobot", "http://example.com/x/y/z?ref=bar", ALLOWED],
    [robots_txt_541230, "foobot", "http://example.com/x/y/z", ALLOWED],
    [robots_txt_541230, "foobot", "http://example.com/status/x", ALLOWED],
    [robots_txt_541230, "foobot", "http://example.com/stat/perf", DISALLOWED],
    [robots_txt_541230, "foobot", "http://example.com/id/13579", DISALLOWED],
    [robots_txt_541230, "foobot", "http://example.com/id/24680", ALLOWED],
    [robots_txt_541230, "foobot", "http://example.com/search/stats", DISALLOWED],
    [robots_txt_541230, "foobot", "http://example.com/foo_bar_escaped_pattern_=123", DISALLOWED],
    [robots_txt_541230, "foobot", "http://example.com/foo-bar-vaz-qux-321", DISALLOWED],
    [robots_txt_541230, "foobot", "http://example.com/foo-bar-vaz-qux-3216", ALLOWED],
    [robots_txt_541230, "foobot", "http://example.com/-0-0-312", DISALLOWED],
    [robots_txt_541230, "foobot", "http://example.com/baz", ALLOWED],
    [robots_txt_541230, "foobot", "http://example.com/baz/user/123", DISALLOWED],
)

@pytest.mark.parametrize('robots_txt,agent,path,allowed', data_541230)
def test_google_stress_541230(robots_txt, agent, path, allowed, can_fetch):
    assert can_fetch(robots_txt, agent, path) is allowed


robots_txt_824664 = """
Sitemap: http://example.com/sitemap.xml
Sitemap: http://example.com/news-sitemap.xml
User-agent: *
Disallow: /controller/
Allow: /controller/admin-ajax.php
"""

data_824664 = (
    [robots_txt_824664, "foo-bot", "http://example.com/index.html", ALLOWED],
    [robots_txt_824664, "foo-bot", "http://example.com/controller/index.html", DISALLOWED],
    [robots_txt_824664, "foo_bot", "http://example.com/controller/foo/bar/index.htm", DISALLOWED],
    [robots_txt_824664, "foobot", "http://example.com/controller/admin-ajax.php", ALLOWED],
    [robots_txt_824664, "foobot", "http://example.com/log?id=234", ALLOWED],
)

@pytest.mark.parametrize('robots_txt,agent,path,allowed', data_824664)
def test_google_stress_824664(robots_txt, agent, path, allowed, can_fetch):
    assert can_fetch(robots_txt, agent, path) is allowed


robots_txt_327748 = """
User-agent: asdfbot
Disallow: /
User-agent: *
Disallow:
Crawl-delay: 15
Sitemap: http://example.com/sitemap.xml
"""

data_327748 = (
    [robots_txt_327748, "foobot", "http://m.example.com/", ALLOWED],
    [robots_txt_327748, "FooBot", "http://m.example.com/foo/bar/baz.php", ALLOWED],
    [robots_txt_327748, "Foo_Bot", "http://m.example.com/index.html", ALLOWED],
    [robots_txt_327748, "asdfbot", "http://m.example.com/", DISALLOWED],
    [robots_txt_327748, "asdfbot", "http://m.example.com/foo/bar/baz.js", DISALLOWED],
    [robots_txt_327748, "asdfbot", "http://m.example.com/robots.txt", DISALLOWED],
)

@pytest.mark.parametrize('robots_txt,agent,path,allowed', data_327748)
def test_google_stress_327748(robots_txt, agent, path, allowed, can_fetch):
    assert can_fetch(robots_txt, agent, path) is allowed


robots_txt_278501 = """
User-agent: *
Disallow: /dump-*
Disallow: /vlog/dump-*
Disallow: /_pcms/preview/
Disallow: /tf/manage-roles/

Sitemap: https://www.example.com/sitemap.xml
Disallow: /_pcms/preview/
Disallow: /tf/manage-roles/
"""

data_278501 = (
    [robots_txt_278501, "foobot", "http://www.example.com/index.html", ALLOWED],
    [robots_txt_278501, "foo-bot", "http://www.example.com/dump-", DISALLOWED],
    [robots_txt_278501, "foobot", "http://www.example.com/dump", ALLOWED],
    [robots_txt_278501, "foo_bot", "http://www.example.com/dump-786", DISALLOWED],
    [robots_txt_278501, "foo-bot", "http://www.example.com/vlog/123", ALLOWED],
    [robots_txt_278501, "foo-bot", "http://www.example.com/vlog/dump-123", DISALLOWED],
    [robots_txt_278501, "foobot", "http://www.example.com/_pcms/test.txt", ALLOWED],
    [robots_txt_278501, "foo_bot", "http://www.example.com/_pcms/preview/test.txt", DISALLOWED],
    [robots_txt_278501, "foo-bot", "http://www.example.com/pcms/preview/test.txt", ALLOWED],
    [robots_txt_278501, "foo_bot", "http://www.example.com/tf/manage-roles/foo/bar", DISALLOWED],
    [robots_txt_278501, "foobot", "http://www.example.com/tf/manage-roles/", DISALLOWED],
    [robots_txt_278501, "foo_bot", "http://www.example.com/tf/index.html", ALLOWED],
)

@pytest.mark.parametrize('robots_txt,agent,path,allowed', data_278501)
def test_google_stress_278501(robots_txt, agent, path, allowed, can_fetch):
    assert can_fetch(robots_txt, agent, path) is allowed


robots_txt_974982 = """
# Some Robots Txt


User-agent: *
Disallow: /data
Disallow: /find
Disallow: /stuff$
Disallow: /stuff/
Disallow: /contacts/
Disallow: /dynamic/
Disallow:/*?creator=*
Disallow:/*&creator=*
Disallow:/*?finder=*
Disallow:/*&finder=*
Disallow:/*?locator=*
Disallow:/*&locator=*
Disallow:/*?viewer=*
Disallow:/*&viewer=*
Disallow:/*?format=json
Disallow:/*&format=json
Disallow:/*?format=page-context
Disallow:/*&format=page-context
Disallow:/*?format=main-content
Disallow:/*&format=main-content
Disallow:/*?format=json-pretty
Disallow:/*&format=json-pretty
Disallow:/*?format=ical
Disallow:/*&format=ical
Disallow:/*?someStuff=*
Disallow:/*&someStuff=*


Sitemap: https://example.com/sitemap.xml
"""

data_974982 = (
    [robots_txt_974982, "foobot", "http://www.example.com/", ALLOWED],
    [robots_txt_974982, "foobot", "http://www.example.com/robots.txt", ALLOWED],
    [robots_txt_974982, "foobot", "http://www.example.com/find", DISALLOWED],
    [robots_txt_974982, "foobot", "http://www.example.com/find/", DISALLOWED],
    [robots_txt_974982, "foobot", "http://www.example.com/find?id=123", DISALLOWED],
    [robots_txt_974982, "foobot", "http://www.example.com/stuff", DISALLOWED],
    [robots_txt_974982, "foobot", "http://www.example.com/stuffstats", ALLOWED],
    [robots_txt_974982, "foobot", "http://www.example.com/stuff/new", DISALLOWED],
    [robots_txt_974982, "foobot", "http://www.example.com/foo?creator=bar", DISALLOWED],
    [robots_txt_974982, "foobot", "http://www.example.com/foo?finder=baz", DISALLOWED],
    [robots_txt_974982, "foobot", "http://www.example.com/foo?creator=bar&finder=baz", DISALLOWED],
    [robots_txt_974982, "foobot", "http://www.example.com/foo?viewer=qux", DISALLOWED],
    [robots_txt_974982, "foobot", "http://www.example.com/foo?creator=bar&stuff=baz", DISALLOWED],
    [robots_txt_974982, "foobot", "http://www.example.com/contacts/index.html", DISALLOWED],
)

@pytest.mark.parametrize('robots_txt,agent,path,allowed', data_974982)
def test_google_stress_974982(robots_txt, agent, path, allowed, can_fetch):
    assert can_fetch(robots_txt, agent, path) is allowed


robots_txt_371856 = """
User-agent: Foobot
User-agent: Barbot
User-agent: Bazbot
User-agent: Quxbot
Crawl-delay: 10
Disallow:

User-agent: *
Disallow: /
"""

data_371856 = (
    [robots_txt_371856, "Foobot", "http://example.com/foo/bar", ALLOWED],
    [robots_txt_371856, "Barbot", "http://example.com/foo/bar", ALLOWED],
    [robots_txt_371856, "Bazbot", "http://example.com/foo/baz", ALLOWED],
    [robots_txt_371856, "Bazbot", "http://example.com/", ALLOWED],
    [robots_txt_371856, "Bazbot", "http://example.com/index.html", ALLOWED],
    [robots_txt_371856, "zazbot", "http://example.com/", DISALLOWED],
    [robots_txt_371856, "zazbot", "http://example.com/index.html", DISALLOWED],
    [robots_txt_371856, "zazbot", "http://example.com/foo/zaz", DISALLOWED],
)

@pytest.mark.parametrize('robots_txt,agent,path,allowed', data_371856)
def test_google_stress_371856(robots_txt, agent, path, allowed, can_fetch):
    assert can_fetch(robots_txt, agent, path) is allowed


robots_txt_923994 = """
User-agent: *
Disallow: /resources/bazbaz/baz/more_stuff
Disallow: /wha/some_dir/files
Disallow: /lib
Disallow: /sys
Disallow: /foo
Disallow: /bar
Disallow: /baz
Sitemap: http://www.example.com/wha/some_dir/resources/sitemap.xml

User-agent: quxbot
Disallow: /resources/bazbaz/baz/more_stuff
Disallow: /wha/some_dir/files
Disallow: /lib
Disallow: /sys
Disallow: /foo
Disallow: /bar
Disallow: /baz
Disallow: /users/big_foo/some_stuff
Disallow: /users/big_foo/other_stuff
Disallow: /en/stuff/arr
Disallow: /en/stuff/dep
Disallow: /sk/stuff/pri
Disallow: /sk/stuff/odl
Disallow: /cz/stuff/pri
Disallow: /cz/stuff/odl
Disallow: /hu/stuff/rke
Disallow: /hu/stuff/ind
Disallow: /addfightyos
Disallow: /addfightnope
Crawl-delay: 29
"""

data_923994 = (
    [robots_txt_923994, "foobot", "http://example.com/home", ALLOWED],
    [robots_txt_923994, "foobot", "http://example.com/foo?id=12", DISALLOWED],
    [robots_txt_923994, "foobot", "http://example.com/qux", ALLOWED],
    [robots_txt_923994, "foobot", "http://example.com/home/scripts/s.js", ALLOWED],
    [robots_txt_923994, "foobot", "http://example.com/baz/112", DISALLOWED],
    [robots_txt_923994, "foobot", "http://example.com/resources/index.html", ALLOWED],
    [robots_txt_923994, "foobot", "http://example.com/resources/bazbaz/baz/more_stuff", DISALLOWED],
    [robots_txt_923994, "quxbot", "http://example.com/resources/bazbaz/baz/more_stuff", DISALLOWED],
    [robots_txt_923994, "quxbot", "http://example.com/users/big_foo/some_stuff/new", DISALLOWED],
    [robots_txt_923994, "quxbot", "http://example.com/addfightyos", DISALLOWED],
    [robots_txt_923994, "foobot", "http://example.com/addfight/new", ALLOWED],
    [robots_txt_923994, "quxbot", "http://example.com/addfight/new", ALLOWED],
    [robots_txt_923994, "quxbot", "http://example.com/addfightnope?dest=ULLI", DISALLOWED],
    [robots_txt_923994, "quxbot", "http://example.com/cz", ALLOWED],
)

@pytest.mark.parametrize('robots_txt,agent,path,allowed', data_923994)
def test_google_stress_923994(robots_txt, agent, path, allowed, can_fetch):
    assert can_fetch(robots_txt, agent, path) is allowed


robots_txt_797409 = """
User-agent: quxbot
Disallow: /
User-agent: *
Disallow:
Sitemap: https://example.com/sitemap.xml
"""

data_797409 = (
    [robots_txt_797409, "foobot", "http://example.com/foo/bar", ALLOWED],
    [robots_txt_797409, "foobot", "http://example.com/", ALLOWED],
    [robots_txt_797409, "foo_bot", "http://example.com/log?id=132", ALLOWED],
    [robots_txt_797409, "quxbot", "http://example.com/", DISALLOWED],
    [robots_txt_797409, "quxbot", "http://example.com/baz/baz", DISALLOWED],
    [robots_txt_797409, "quxbot", "http://example.com/index.htm", DISALLOWED],
)

@pytest.mark.parametrize('robots_txt,agent,path,allowed', data_797409)
def test_google_stress_797409(robots_txt, agent, path, allowed, can_fetch):
    assert can_fetch(robots_txt, agent, path) is allowed


robots_txt_715135 = """
User-agent: admin
Disallow:

User-agent: *
Disallow: /buzz
Allow: /

Sitemap: http://example.com/sitemap.xml

"""

data_715135 = (
    [robots_txt_715135, "foobot", "http://example.com/buzz/settings", DISALLOWED],
    [robots_txt_715135, "foobot", "http://example.com/buzz-lite", DISALLOWED],
    [robots_txt_715135, "barbot", "http://example.com/qux/bar", ALLOWED],
    [robots_txt_715135, "quxbot", "http://example.com/buzz", DISALLOWED],
    [robots_txt_715135, "bazbot", "http://example.com/prod/buzz", ALLOWED],
    [robots_txt_715135, "barbot", "http://example.com/anotherbuzz/x", ALLOWED],
    [robots_txt_715135, "foobot", "http://example.com/rebuzz/x", ALLOWED],
    [robots_txt_715135, "foobot", "http://example.com/buzz/buzz/buzz", DISALLOWED],
    [robots_txt_715135, "foo-bot", "http://example.com/searc/buzz", ALLOWED],
    [robots_txt_715135, "bar-bot", "http://example.com/buzz/searc", DISALLOWED],
    [robots_txt_715135, "admin", "http://example.com/buzz/ses", ALLOWED],
    [robots_txt_715135, "admin", "http://example.com/foo/bar", ALLOWED],
    [robots_txt_715135, "admin", "http://example.com/buzz", ALLOWED],
)

@pytest.mark.parametrize('robots_txt,agent,path,allowed', data_715135)
def test_google_stress_715135(robots_txt, agent, path, allowed, can_fetch):
    assert can_fetch(robots_txt, agent, path) is allowed


robots_txt_478151 = """


User-agent: Whoosh-Qux
Allow: /

User-agent: Baz-Qux
Allow: /

User-agent: barbot
Allow: /
Disallow: /braa

User-agent: BeepBot
Disallow: /braa

User-agent: Sample-web-crawler
Disallow: /braa

User-agent: *
Disallow: /

User-agent: *
Disallow: /braa

Sitemap: /sitemap.xml
"""

data_478151 = (
    [robots_txt_478151, "Whoosh-Qux", "http://example.com/robots.txt", ALLOWED],
    [robots_txt_478151, "Baz-Qux", "http://example.com/foo/bar", ALLOWED],
    [robots_txt_478151, "BeepBot", "http://example.com/braallaboration/index.htm", DISALLOWED],
    [robots_txt_478151, "BeepBot", "http://example.com/foo/bar", ALLOWED],
    [robots_txt_478151, "BeepBot", "http://example.com/", ALLOWED],
    [robots_txt_478151, "BeepBot", "http://example.com/braa/balt", DISALLOWED],
    [robots_txt_478151, "foobot", "http://example.com/index.htm", DISALLOWED],
    [robots_txt_478151, "foo_bot", "http://example.com/braabalt", DISALLOWED],
    [robots_txt_478151, "foo-bot", "http://example.com/", DISALLOWED],
)

@pytest.mark.parametrize('robots_txt,agent,path,allowed', data_478151)
def test_google_stress_478151(robots_txt, agent, path, allowed, can_fetch):
    assert can_fetch(robots_txt, agent, path) is allowed


robots_txt_369883 = """
User-agent: *
<br />
Allow: /
<br />
User-agent: BarBot
<br />
Disallow: /
<br />
User-agent: AB42bot
<br />
Disallow: /
<br />
sitemap: http://example.com/sitemap.xml
"""

data_369883 = (
    [robots_txt_369883, "foobot", "http://example.com/", ALLOWED],
    [robots_txt_369883, "foo-bot", "http://example.com/foo/bar", ALLOWED],
    [robots_txt_369883, "foo_bot", "http://example.com/robots.txt", ALLOWED],
    [robots_txt_369883, "BarBot", "http://example.com/", DISALLOWED],
    [robots_txt_369883, "BarBot", "http://example.com/foo/bar/baz", DISALLOWED],
    [robots_txt_369883, "BarBot", "http://example.com/robots.txt", DISALLOWED],
    [robots_txt_369883, "AB42bot", "http://example.com/foo/bar", ALLOWED],
    [robots_txt_369883, "AB42bot", "http://example.com/", ALLOWED],
    [robots_txt_369883, "AB", "http://example.com/", DISALLOWED],
    [robots_txt_369883, "AB", "http://example.com/robots.txt", DISALLOWED],
)

@pytest.mark.parametrize('robots_txt,agent,path,allowed', data_369883)
def test_google_stress_369883(robots_txt, agent, path, allowed, can_fetch):
    assert can_fetch(robots_txt, agent, path) is allowed


robots_txt_434582 = """
#
# robots.txt
#
# This is robots.txt
# and it saves server resources
# some more comment lines
# and an empty one
#
# Don't forget to put robots.txt in root of your host
# Used:    http://example.com/robots.txt
# Ignored: http://example.com/site/robots.txt
#
# For more information about the robots.txt standard, see:
# http://www.robotstxt.org/robotstxt.html

User-agent: *
Crawl-delay: 15
# Foo
Allow: /stuff/*.css$
Allow: /stuff/*.css?
Allow: /stuff/*.js$
Allow: /stuff/*.js?
Allow: /stuff/*.gif
Allow: /stuff/*.jpg
Allow: /stuff/*.jpeg
Allow: /stuff/*.png
Allow: /things/*.css$
Allow: /things/*.css?
Allow: /things/*.js$
Allow: /things/*.js?
Allow: /things/*.gif
Allow: /things/*.jpg
Allow: /things/*.jpeg
Allow: /things/*.png
Allow: /data/*.css$
Allow: /data/*.css?
Allow: /data/*.js$
Allow: /data/*.js?
Allow: /data/*.gif
Allow: /data/*.jpg
Allow: /data/*.jpeg
Allow: /data/*.png
Allow: /more_data/*.css$
Allow: /more_data/*.css?
Allow: /more_data/*.js$
Allow: /more_data/*.js?
Allow: /more_data/*.gif
Allow: /more_data/*.jpg
Allow: /more_data/*.jpeg
Allow: /more_data/*.png
# Bar
Disallow: /something/
Disallow: /stuff/
Disallow: /things/
Disallow: /data/
Disallow: /scripts/
Disallow: /more_data/
# Baz
Disallow: /SOME_TEXT.txt
Disallow: /some_script.php
Disallow: /INSTALL.foo.txt
Disallow: /INSTALL.bar.txt
Disallow: /INSTALL.baz.txt
Disallow: /get.php
Disallow: /GET.txt
Disallow: /LICENSE.txt
Disallow: /HELPERS.txt
Disallow: /update.php
Disallow: /UPGRADE.txt
Disallow: /what.php
# Some more stuff to disallow
Disallow: /?q=main/
Disallow: /?q=comment/reply/
Disallow: /?q=filter/ads/
Disallow: /?q=data/add/
Disallow: /?q=find/
Disallow: /?q=baz/password/
Disallow: /?q=baz/register/
Disallow: /?q=baz/login/
Disallow: /?q=baz/logout/
"""

data_434582 = (
    [robots_txt_434582, "foobot", "https://www.example.com/", ALLOWED],
    [robots_txt_434582, "foobot", "https://www.example.com/help.html", ALLOWED],
    [robots_txt_434582, "foobot", "https://www.example.com/some.css", ALLOWED],
    [robots_txt_434582, "foobot", "https://www.example.com/foo/some.css", ALLOWED],
    [robots_txt_434582, "foobot", "https://www.example.com/stuff/some.css", ALLOWED],
    [robots_txt_434582, "foobot", "https://www.example.com/stuff/some.html", DISALLOWED],
    [robots_txt_434582, "foobot", "https://www.example.com/stuff/some.jpeg", ALLOWED],
    [robots_txt_434582, "foobot", "https://www.example.com/things/some.css?user=main", ALLOWED],
    [robots_txt_434582, "foobot", "https://www.example.com/things/some.jpeg?user=main", ALLOWED],
    [robots_txt_434582, "foobot", "https://www.example.com/something/foo.cpp", DISALLOWED],
    [robots_txt_434582, "foobot", "https://www.example.com/more_data/dark", DISALLOWED],
    [robots_txt_434582, "foobot", "https://www.example.com/some_script.php", DISALLOWED],
    [robots_txt_434582, "foobot", "https://www.example.com/upgrade.txt", ALLOWED],
    [robots_txt_434582, "foobot", "https://www.example.com/UPGRADE.txt", DISALLOWED],
    [robots_txt_434582, "foobot", "https://www.example.com/data/main", DISALLOWED],
    [robots_txt_434582, "foobot", "https://www.example.com/?q=baz/", ALLOWED],
    [robots_txt_434582, "foobot", "https://www.example.com/?q=baz/login", ALLOWED],
    [robots_txt_434582, "foobot", "https://www.example.com/?q=baz/login/", DISALLOWED],
    [robots_txt_434582, "foobot", "https://www.example.com/?q=data/discard/", ALLOWED],
    [robots_txt_434582, "foobot", "https://www.example.com/?q=data/add/", DISALLOWED],
)

@pytest.mark.parametrize('robots_txt,agent,path,allowed', data_434582)
def test_google_stress_434582(robots_txt, agent, path, allowed, can_fetch):
    assert can_fetch(robots_txt, agent, path) is allowed

