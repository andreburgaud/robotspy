"""
Unit tests for robots.RobotFileParser
"""

import pytest
import robots

url_data = (
    ['https://example.com/index', 'example.com', '/index'],
    ['https://example.com/', 'example.com', '/'],
    ['https://example.com', 'example.com', '/'],
    ['http://example.com//%7Ejoe/index.html', 'example.com', '/~joe/index.html']
)


@pytest.mark.parametrize('url,host,path', url_data)
def test_normalize_url(url, host, path):
    h, p = robots.RobotsParser.normalize_url(url)
    assert (h, p) == (host, path)


dedup_data = (
    ['///path///index.html', '/path/index.html'],
    ['/path/index.html', '/path/index.html'],
    ['//', '/'],
    ['/', '/'],
    ['/foo/bar?qux=taz&baz=http://foo.bar?tar&par', '/foo/bar?qux=taz&baz=http://foo.bar?tar&par'],
    ['///foo//bar?qux=taz&baz=http://foo.bar?tar&par', '/foo/bar?qux=taz&baz=http://foo.bar?tar&par'],
    ['///foo//bar?qux=taz&baz=https://foo.bar?tar&par', '/foo/bar?qux=taz&baz=https://foo.bar?tar&par']
)


@pytest.mark.parametrize('path,dedup', dedup_data)
def test_dedup_slash(path, dedup):
    assert robots.RobotsParser.dedup_slash(path) == dedup


path_pattern_data = (
    ['/path/index.html', '/path/*.html', True],
    ['/path/index.html', '/path/*.html$', True],
    ['/path/index.html?test=1', '/path/*.html$', False],
    ['/path/index.html?test=1', '/path*', True],
    ['/path/index.html?test=1', '/p*/i*', True],
    ['/path', '/p*/i*', False],
)


@pytest.mark.parametrize('path,pattern,expected', path_pattern_data)
def test_startswith_pattern(path, pattern, expected):
    assert robots.RobotsParser.startswith_pattern(path, pattern) is expected
