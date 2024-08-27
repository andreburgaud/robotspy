# https://github.com/google/robotstxt-spec-test/tree/master/src/main/resources/CTC/stress

import pytest
from .core import *

FOOBOT = "foobot"

# https://github.com/google/robotstxt-spec-test/blob/master/src/main/resources/CTC/stress/541230.textproto
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
Disallow: /id/sub
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
    [robots_txt_541230, FOOBOT, "http://example.com/foo.js", ALLOWED],
    [robots_txt_541230, FOOBOT, "http://example.com/foo/bar.css", ALLOWED],
    [robots_txt_541230, FOOBOT, "http://example.com/x/y/z?ref=bar", ALLOWED],
    [robots_txt_541230, FOOBOT, "http://example.com/x/y/z", ALLOWED],
    [robots_txt_541230, FOOBOT, "http://example.com/status/x", ALLOWED],
    [robots_txt_541230, FOOBOT, "http://example.com/stat/perf", DISALLOWED],
    [robots_txt_541230, FOOBOT, "http://example.com/id/13579", DISALLOWED],
    [robots_txt_541230, FOOBOT, "http://example.com/id/24680", ALLOWED],
    [robots_txt_541230, FOOBOT, "http://example.com/search/stats", DISALLOWED],
    [robots_txt_541230, FOOBOT, "http://example.com/foo_bar_escaped_pattern_=123", DISALLOWED],
    [robots_txt_541230, FOOBOT, "http://example.com/foo-bar-vaz-qux-321", DISALLOWED],
    [robots_txt_541230, FOOBOT, "http://example.com/foo-bar-vaz-qux-3216", ALLOWED],
    [robots_txt_541230, FOOBOT, "http://example.com/-0-0-312", DISALLOWED],
    [robots_txt_541230, FOOBOT, "http://example.com/baz", ALLOWED],
    [robots_txt_541230, FOOBOT, "http://example.com/baz/user/123", DISALLOWED],
)

@pytest.mark.parametrize('robots_txt,agent,path,allowed', data_541230)
def test_google_stress_541230(robots_txt, agent, path, allowed, can_fetch):
    assert can_fetch(robots_txt, agent, path) is allowed


# https://github.com/google/robotstxt-spec-test/blob/master/src/main/resources/CTC/stress/308278.textproto
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
    [robots_txt_308278, FOOBOT, "http://example.com/asdf-login", DISALLOWED],
    [robots_txt_308278, FOOBOT, "http://example.com/asdf-login/", DISALLOWED],
    [robots_txt_308278, FOOBOT, "http://example.com/", ALLOWED],
    [robots_txt_308278, FOOBOT, "http://example.com/databack", ALLOWED],
    [robots_txt_308278, FOOBOT, "http://example.com/databack/recent", DISALLOWED],
    [robots_txt_308278, FOOBOT, "http://example.com/foo/?user=admin/data", ALLOWED],
    [robots_txt_308278, FOOBOT, "http://example.com/?user=admin/data", DISALLOWED],
    [robots_txt_308278, FOOBOT, "http://example.com/id/page/", ALLOWED],
    [robots_txt_308278, FOOBOT, "http://example.com/id/some/page/", DISALLOWED],
    [robots_txt_308278, FOOBOT, "http://example.com/id/some/data", ALLOWED],
    [robots_txt_308278, FOOBOT, "http://example.com/id/some/data/more", DISALLOWED],
)

@pytest.mark.parametrize('robots_txt,agent,path,allowed', data_308278)
def test_google_stress_308278(robots_txt, agent, path, allowed, can_fetch):
    assert can_fetch(robots_txt, agent, path) is allowed
