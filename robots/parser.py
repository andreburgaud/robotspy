"""
Alternate implementation of RobotParser (alternative to standard library urllib.robotparser)

Reference:
Robots Exclusion Protocol (REP) https://www.rfc-editor.org/rfc/rfc9309
"""

from typing import Dict, Iterator, List, NamedTuple, Tuple, Type, TypeVar

import enum
import fnmatch
import re
import time

import urllib.parse
import urllib.error
import urllib.request

import robots

# Pattern used to validate a user agent token (not used by the parser)
RE_AGENT_TOKEN = re.compile(r"^[a-zA-Z_-]+$")

# Pattern to read and identify a product token, user agent.
# Match up to the first invalid character (for example stops at a number but does not error out)
# Note: the hash character ('#') needs to be escaped in VERBOSE mode, otherwise it would be
# interpreted as a comment.
RE_AGENT = re.compile(
    r"^\s*user-agent\s*:?\s*(?P<AGENT>\*|[a-zA-Z_-]+)[^]s]*\s*(?:\#.*)?$",
    re.IGNORECASE | re.VERBOSE,
)

RE_SITEMAP = re.compile(
    r"^\s*sitemap\s*:\s*(?P<SITEMAP>https?://[^\n\s]+)\s*$",
    re.IGNORECASE | re.VERBOSE,
)

# Product token in the user-agent line:
RE_PRODUCT = re.compile(r"^[a-zA-Z_-]+$|\*")

# Rule allow
RE_RULE_ALLOW = re.compile(
    r"^\s*(?P<RULE>allow)\s*:?\s*(?P<PATH>\*|[^\s#]+)?\s*(?:\#.*)?$",
    re.IGNORECASE | re.VERBOSE,
)

# Rule disallow
RE_RULE_DISALLOW = re.compile(
    r"^\s*(?P<RULE>disallow)\s*:?\s*(?P<PATH>\*|[^\s#]+)?\s*(?:\#.*)?$",
    re.IGNORECASE | re.VERBOSE,
)

# NamedTuple used to store rules. Each record includes:
# - A path or path pattern
# - A boolean indicating if the given path can be access or not
Rule = NamedTuple("Rule", [("path", str), ("allowed", bool)])

RequestRate = NamedTuple("RequestRate", [("requests", int), ("seconds", int)])


class State(enum.Enum):
    """Define states while parsing the robotstxt file"""

    BEGIN = enum.auto()  # Begin parsing
    AGENT = enum.auto()  # User-agent line
    RULE = enum.auto()  # Rule line


class TokenType(enum.Enum):
    """Token definitions for the parser"""

    AGENT = enum.auto()
    ALLOW = enum.auto()
    DISALLOW = enum.auto()
    SITEMAP = enum.auto()
    CRAWL_DELAY = enum.auto()
    REQ_RATE = enum.auto()
    UNEXPECTED = enum.auto()


class Errors(enum.Enum):
    """Errors definitions and messages"""

    WARNING_EMPTY_ALLOW_RULE = (
        "Warning: An empty allow rule has no effect and is confusing"
    )
    WARNING_RULE_WITHOUT_AGENT = "Warning: Rule without an agent is ignored"
    WARNING_NOTFOUND = "Warning: No remote robots.txt file found"
    WARNING_CRAWL_DELAY_IGNORED = "Warning: Directive 'crawl-delay' ignored"
    WARNING_REQUEST_RATE_IGNORED = "Warning: Directive 'request-rate' ignored"
    WARNING_UNEXPECTED_OR_IGNORED = "Warning: Unexpected or ignored token"
    ERROR_NO_FILE_FOUND = "Error: No file found"


Token = NamedTuple("Token", [("type", TokenType), ("value", str), ("linenum", int)])


def gen_tokens(gen_func, source):
    """Token generator.

    Emit tokens when parsing the content of a robots.txt
    """

    linenum = 0
    for line in gen_func(source):
        linenum += 1
        # pylint: disable=superfluous-parens
        if not (line := line.strip()):
            continue  # Skip empty lines
        if line.startswith("#"):
            continue  # Skip line comment
        if m := RE_AGENT.match(line):
            agent = m.group("AGENT")
            yield Token(TokenType.AGENT, agent, linenum)
        elif m := RE_RULE_ALLOW.match(line):
            path = m.group("PATH")
            yield Token(TokenType.ALLOW, path, linenum)
        elif m := RE_RULE_DISALLOW.match(line):
            path = m.group("PATH")
            yield Token(TokenType.DISALLOW, path, linenum)
        elif m := RE_SITEMAP.match(line):
            sitemap = m.group("SITEMAP")
            yield Token(TokenType.SITEMAP, sitemap, linenum)
        else:
            yield Token(TokenType.UNEXPECTED, line, linenum)


T = TypeVar("T", bound="RobotsParser")


class RobotsParser:
    """Encapsulates functions and data to parse a robotstxt file and get
    feedback on what a crawler is allowed to access to on a given website.
    """

    AGENT_NOT_VALID = "User agent [%s] is not valid"
    UNEXPECTED_LINE = "Unexpected line: [%s]"

    def __init__(self, url=""):
        self.agents_rules: Dict[str, List[Rule]] = {}
        self._sitemaps = []
        self._errors = []
        self._warnings = []
        self.url = url
        self.disallow_all = False
        self.allow_all = False
        self.timeout = 5
        self._host = ""
        self._path = "/robots.txt"
        self._time = 0.0  # Time the robots.txt is fetched

    @property
    def errors(self):
        """Property pointing to the errors list"""
        return self._errors

    @property
    def warnings(self):
        """Property pointing to the warning list"""
        return self._warnings

    @property
    def url(self):
        """Url pointing to the robots.txt. For example: https://example.com/robots.com"""
        return self._url

    @url.setter
    def url(self, url):
        """Set the url (example: 'https://www.example.com/robots.txt'), the path of the robots.txt
        file, example: '/robots.txt', and the hostname, example 'www.example.com'.

        It discards the scheme ('http' or 'https') for compatibility with the Python standard
        library module 'urllib.robotparser'."""

        self._url = url
        self._host, self._path = urllib.parse.urlparse(url)[1:3]

    @property
    def host(self):
        """Host of the server serving the robots.txt file."""
        return self._host

    @property
    def path(self):
        """Path of the robots.txt file.

        Example: '/robots.txt'.
        """
        return self._path

    @property
    def timestamp(self):
        """Property pointing to the time the robots.txt was parsed"""
        return self._time

    @timestamp.setter
    def timestamp(self, timestamp):
        self._time = timestamp

    @property
    def sitemaps(self):
        """Property pointing to the private sitemaps list"""
        return self._sitemaps or None

    @classmethod
    def from_string(cls: Type[T], robotstxt: str) -> T:
        """Build a robots parser from a string representing the content of a robots.txt file."""
        parser = cls()
        gen_string = lambda txt: (line for line in txt.split("\n"))
        parser.parse_tokens(gen_tokens(gen_string, robotstxt))
        return parser

    def gen_uri(self, uri: str):
        """Instantiate a generator from a URI (either http:// or https:// or file:///"""

        try:
            useragent = f"robotspy/{robots.__version__}"
            req = urllib.request.Request(uri, headers={'User-Agent': useragent})
            self.timestamp = time.time()
            with urllib.request.urlopen(req, timeout=self.timeout) as f:
                for line in f:
                    try:
                        yield line.decode("utf-8-sig") # uft-8-sig to handle BOM characters
                    except UnicodeDecodeError as err:
                        self.allow_all = True
                        self._errors.append(("robots.txt must be UTF-8 encoded", f"{str(err)} for {uri}"))
                        return
        except urllib.error.HTTPError as err:
            if err.code in (401, 403):
                self.disallow_all = True
                self._errors.append((str(err.code), f"{str(err)} for {uri}"))
            elif 400 <= err.code < 500: # Unavailable status
                self.allow_all = True
                self._warnings.append((str(err.code), f"{str(err)} for {uri}"))
            elif 500 <= err.code < 600: # Unreachable status
                self.disallow_all = True
                self._warnings.append((str(err.code), f"{str(err)} for {uri}"))
            self.timestamp = 0
        except urllib.error.URLError as err: # Unreachable status?
            self.disallow_all = True
            now = time.time()
            duration = round(now - self.timestamp)
            self._errors.append(("", f"{str(err)} for {uri} (duration={duration}s)"))

    @classmethod
    def from_uri(cls: Type[T], uri: str, timeout=5) -> T:
        """Build a robots parser given a url or uri pointing to a robots.txt."""
        parser = cls()
        parser.timeout = timeout
        parser.parse_tokens(gen_tokens(parser.gen_uri, uri))
        return parser

    def gen_file(self, filename):
        """Instantiate a generator from a file"""

        try:
            with open(filename) as f:
                for line in f:

                    yield line
        except FileNotFoundError:
            self._errors.append((filename, Errors.ERROR_NO_FILE_FOUND.value))

    @classmethod
    def from_file(cls: Type[T], filename: str) -> T:
        """Build a robots parser given a local path pointing to a robots.txt file."""
        parser = cls()
        parser.parse_tokens(gen_tokens(parser.gen_file, filename))
        return parser

    @staticmethod
    def is_agent_valid(useragent: str) -> bool:
        """Helper function not used internally by the parser. Useful to validate user agent token.

        https://tools.ietf.org/html/draft-koster-rep#section-2.2.1
        User agent in robots.txt should only include the following characters: "a-zA-Z_-"
        """
        if RE_AGENT_TOKEN.match(useragent):
            return True
        return False

    def update_rules(self, agents: List[str], rules: List[Rule]) -> None:
        """Sort the rules for a given group.

        The rules are sorted with the longest path first and the allowed first in case of both
        'diasallowed' and 'allowed' rule for same path
        See: https://tools.ietf.org/html/draft-koster-rep-00#section-3.2
        """
        rules.sort(key=lambda x: (len(x.path), x.allowed), reverse=True)

        # Need to dedup agents `list(set(agents))` caused by intentional lax parsing stopping at the first invalid character.
        # For example, GoogleBot and GoogleBot* will both result in googlebot
        for agent in list(set(agents)):
            if existing_rules := self.agents_rules.get(agent, None):
                rules = (
                    existing_rules + rules
                )  # Combine rules if agent found several times
                rules.sort(key=lambda x: (len(x.path), x.allowed), reverse=True)
            self.agents_rules[agent] = rules

    def parse_tokens(self, tokens: Iterator) -> None:
        """Main function of the parser.

        Parse a robots.txt file and generate a data structure that can then be used by the
        Robots object to answer question (can_fetch?) given a URL and a robots ID.
        """

        state = State.BEGIN
        current_agents: List[str] = []
        current_rules: List[Rule] = []

        for token in tokens:
            if token.type == TokenType.AGENT:
                if state == State.RULE:
                    self.update_rules(current_agents, current_rules)
                    current_agents = []
                    current_rules = []
                state = State.AGENT
                current_agents.append(token.value.lower())
            elif token.type in (TokenType.ALLOW, TokenType.DISALLOW):
                if state == State.BEGIN:
                    self._warnings.append(
                        (
                            f"line {token.linenum}",
                            Errors.WARNING_RULE_WITHOUT_AGENT.value,
                        )
                    )
                    continue  # A rule without an agent is ignored
                state = State.RULE
                if path := token.value:
                    current_rules.append(
                        Rule(urllib.parse.unquote(path), token.type == TokenType.ALLOW)
                    )
                else:
                    if token.type == TokenType.ALLOW:
                        self._warnings.append(
                            (f"line {token.linenum}", Errors.WARNING_EMPTY_ALLOW_RULE.value)
                        )
            elif token.type == TokenType.SITEMAP:
                self._sitemaps.append(token.value)
            else:
                # Unprocessed or unexpected token
                self._warnings.append(
                    (
                        f"line {token.linenum}",
                        f"{Errors.WARNING_UNEXPECTED_OR_IGNORED.value}: {token.value}",
                    )
                )

        self.update_rules(current_agents, current_rules)

    def find_rules(self, agent: str) -> List[Rule]:
        """Return rules for a given agent. If agent is not stored, return
        rules for wild card agent ('*'), if no rule for '*', return empty list.
        """

        # Crawlers MUST use case-insensitive matching to find the group that matches the product token =>
        # convert the product token (agent) to lower case.
        rules = self.agents_rules.get(agent.lower(), self.agents_rules.get("*", []))
        return rules

    @staticmethod
    def dedup_slash(path: str) -> str:
        """Replace multiple slashes in a path to one slash.
        Keep the duplicate slash after https: or http: (a URL can appear in a query string)
        Note: This would be a problem with other patterns like file:/// or ftp://
        """

        # Regex lookbehind with http or https not possible as it has to be fixed length
        path = re.sub(r"//+", "/", path)
        # Inject back double slash after any scheme contained in the query string (http or https)
        return re.sub(r"(https:/|http:/)", r"\1/", path)

    @staticmethod
    def normalize_url(url: str) -> Tuple[str, str]:
        """Normalize a URL to extract a quoted path to be used to compare with
        a saved rule.

        Returns a tuple containing the host part of the URL if any and a normalized path
        """

        url = urllib.parse.unquote(url)
        result = urllib.parse.urlsplit(url)

        # extract the path portion of the URL as-is (e.g. preserve a standalone ?)
        host_url = urllib.parse.urlunsplit((result.scheme, result.netloc, "", "", ""))
        path = url[len(host_url):] or "/"
        return result.netloc, RobotsParser.dedup_slash(path)

    @staticmethod
    def startswith_pattern(path: str, pattern: str) -> bool:
        """A match is intended to be a 'startswith' match. To accommodate, add a
        star ('*') at the end of the pattern if it does not exist already.
        """

        if pattern.endswith("$"):
            # When ending with '$', needs to be an exact match
            return fnmatch.fnmatchcase(path, pattern[:-1])

        if not pattern.endswith("*"):
            pattern += "*"

        # In unix file name pattern a `?' is a single character. In a url path, it is a '?'. To take it as character
        # replace with [?] (https://docs.python.org/3/library/fnmatch.html)
        pattern = pattern.replace("?", "[?]")

        return fnmatch.fnmatchcase(path, pattern)

    # pylint: disable=too-many-return-statements
    def can_fetch(self, useragent: str, url: str) -> bool:
        """Answer the question if a user agent can fetch a particular URL.

        The parser checks the group of rules applying to the given robots ID (user-agent),
        and then check the rule that may apply to the given URL.
        """

        if self.allow_all:
            return True
        if self.disallow_all:
            return False

        host, path = RobotsParser.normalize_url(url)

        if host and self.host and host != self.host:
            return False

        rules = self.find_rules(useragent)

        for rule in rules:
            # $ is a special character for robots and indicate the exact end of the pattern
            if rule.path.endswith("$") and rule.path[:-1] == path:
                return rule.allowed

            if path.startswith(rule.path):
                return rule.allowed

            if rule.path != "*" and "*" in rule.path:
                if RobotsParser.startswith_pattern(path, rule.path):
                    return rule.allowed

            if rule.path == "*":
                return rule.allowed

        return True

    def __str__(self):
        """Produces a robots.txt from the structure of the rules memorized by the parser."""

        lines = []
        for agent, rules in self.agents_rules.items():
            lines.append(f"User-agent: {agent}")
            for rule in rules:
                lines.append(
                    ("Allow" if rule.allowed else "Disallow") + ": " + rule.path
                )
            lines.append("")

        if self._sitemaps:
            for sitemap in self._sitemaps:
                lines.append(f"Sitemap: {sitemap}")

            lines.append("")

        return "\n".join(lines)
