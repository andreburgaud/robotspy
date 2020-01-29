"""
Thin facade in front of robots.parser to mimic the api from the Python standard library
urllib.robotparser https://docs.python.org/3/library/urllib.robotparser.html
"""

import time
from typing import List
from . import parser


def gen_lines(lines: List[str]):
    """Instantiate a generator from a list"""
    return (line for line in lines)


class RobotFileParser(parser.RobotsParser):
    """Thin wrapper on RobotsParser to enable some level of compatibility with
    urllib.robotparser.RobotFileParser. The implementation is incomplete, for
    example, crawl_delay and request_rate are hard-coded to return None. The
    unit tests take into account the implementation."""

    def set_url(self, url):
        """Sets the URL referring to a robots.txt file."""
        self.url = url

    def read(self):
        """Populate the tokens if a URL is assigned to the url attribute"""
        if self.url:
            self.parse_tokens(parser.gen_tokens(self.gen_uri, self.url))
        else:
            self._errors.append(
                (
                    self.url,
                    "RobotFileParser.read requires RobotFileParser.url to be set",
                )
            )

    def parse(self, lines):
        """Method 'parse' compatible with urllib.robotparser.RobotFileParser. Parses the tokens
        given an iterator."""
        self.parse_tokens(parser.gen_tokens(gen_lines, lines))

    def mtime(self):
        """Method 'mtime' compatible with urllib.robotparser.RobotFileParser. Return the timestamp
        initialized when parsing a robots.txt url."""
        return self.timestamp

    def modified(self):
        """Method 'modified' compatible with urllib.robotparser.RobotFileParser. When invoked,
        instantiate the internal timestamp to the current time."""
        self.timestamp = time.time()

    def crawl_delay(self, _: str):
        """The 'crawl-delay' directive is not recognize by the Google robots parser. Ignoring it in
        robotspy. Keep this method for compatibility with urllib.robotparser."""
        self._warnings.append(
            ("crawl-delay", parser.Errors.WARNING_CRAWL_DELAY_IGNORED)
        )

    def request_rate(self, _: str):
        """The 'request-rate' directive is not recognize by the Google robots parser. Ignoring it in
        robotspy. Keep this method for compatibility with urllib.robotparser."""
        self._warnings.append(
            ("request-rate", parser.Errors.WARNING_REQUEST_RATE_IGNORED)
        )

    def site_maps(self):
        """Method site_maps compatible with urllib.robotparser.RobotFileParser. Return the list of
        sitemaps encountered while parsing a robots.txt content."""
        return self.sitemaps
