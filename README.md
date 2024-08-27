# Robots Exclusion Standard Parser for Python

The `robotspy` Python module implements a parser for `robots.txt` files. The recommended class to use is
`robots.RobotsParser`. 

A thin facade `robots.RobotFileParser` can also be used as  a substitute for [`urllib.robotparser.RobotFileParser`](https://docs.python.org/3/library/urllib.robotparser.html),
available in the Python standard library. The class `robots.RobotFileParser` exposes an API that is mostly compatible
with `urllib.robotparser.RobotFileParser`.

The main reasons for this rewrite are the following:

1. It was initially intended to experiment with parsing `robots.txt` files for a link checker project (not implemented yet).
1. It (mostly) follows the specs from the [RFC 9309 - Robots Exclusion Protocol](https://www.rfc-editor.org/rfc/rfc9309).
1. It does not try to be compliant with commonly accepted directives that are not in the current specs such as `request-rate` 
and `crawl-delay`, but it currently supports `sitemaps`.
1. It satisfies the same tests as the [Google Robots.txt Parser](https://github.com/google/robotstxt), except for some custom behaviors specific to Google Robots.

To use the `robots` command line tool (CLI) in a Docker container, read the following section **Docker Image**.

To install `robotspy` globally as a tool on your system with `pipx` skip to the **Global Installation** section.

If you are interested in using `robotspy` in a local Python environment or as a library, skip to section **Module Installation**.

## Docker Image

The Robotspy CLI, `robots`, is available as a [Docker](https://www.docker.com/) automated built image at https://hub.docker.com/r/andreburgaud/robotspy.

If you already have [Docker](https://docs.docker.com/get-docker/) installed on your machine, first pull the image from Docker Hub:

```
$ docker pull andreburgaud/robotspy
```

Then, you can exercise the tool against the following remote Python `robots.txt` test file located at http://www.pythontest.net/elsewhere/robots.txt:

```
# Used by NetworkTestCase in Lib/test/test_robotparser.py

User-agent: Nutch
Disallow: /
Allow: /brian/

User-agent: *
Disallow: /webstats/
```

The following examples demonstrate how to use the `robots` command line with the Docker container:

```
$ # Example 1: User agent "Johnny" is allowed to access path "/"
$ docker run --rm andreburgaud/robotspy http://www.pythontest.net/elsewhere/robots.txt Johnny /
user-agent 'Johnny' with path '/': ALLOWED
```

```
$ # Example 2:  User agent "Nutch" is not allowed to access path "/brian"
$ docker run --rm andreburgaud/robotspy http://www.pythontest.net/elsewhere/robots.txt Nutch /brian
user-agent 'Nutch' with path '/brian': DISALLOWED
```

```
$ # Example 3: User agent "Johnny" is not allowed to access path "/webstats/"
docker run --rm andreburgaud/robotspy http://www.pythontest.net/elsewhere/robots.txt Johnny /webstats/
user-agent 'Johnny' with path '/webstats/': DISALLOWED
```

The arguments are the following:

1. Location of the robots.txt file (`http://www.pythontest.net/elsewhere/robots.txt`)
1. User agent name (`Johnny`)
1. Path or URL (`/`)

Without any argument, `robots` displays the help:

```
docker run --rm andreburgaud/robotspy
usage: robots <robotstxt> <useragent> <path>

Shows whether the given user agent and path combination are allowed or disallowed by the given robots.txt file.

positional arguments:
  robotstxt      robots.txt file path or URL
  useragent      User agent name
  path           Path or URI

optional arguments:
  -h, --help     show this help message and exit
  -v, --version  show program's version number and exit
```

To use the CLI `robots` as a global tools, continue to the following section. If you want to use `robotspy` as a Python module, skip to **Module Installation**.

## Global Installation with pipx

If you only want to use the command line tool `robots`, you may want to use [pipx](https://pipxproject.github.io/pipx/installation/) to install it as a global tool on your system.

To install `robotspy` using `pipx` execute the following command:

```bash
$  pipx install robotspy
```

When `robotspy` is installed globally on your system, you can invoke it from any folder locations. For example, you can execute:

```bash
$  robots --version
robots 0.8.0
```

You can see more detailed usages in section **Usage**.

## Module Installation

**Note**: Python 3.8.x or 3.9.x required

You preferably want to install the `robotspy` package after creating a Python virtual environment,
in a newly created directory, as follows:

```
$ mkdir project && cd project
$ python -m venv .venv
$ . .venv/bin/activate
(.venv) $ python -m pip install --upgrade pip
(.venv) $ python -m pip install --upgrade setuptools
(.venv) $ python -m pip install robotspy
(.venv) $ python -m robots --help
...
```

On Windows:

```
C:/> mkdir project && cd project
C:/> python -m venv .venv
C:/> .venv\scripts\activate
(.venv) c:\> python -m pip install --upgrade pip
(.venv) c:\> python -m pip install --upgrade setuptools
(.venv) c:\> python -m pip install robotspy
(.venv) c:\> python -m robots --help
...
```

## Usage

The `robotspy` package can be imported as a module and also exposes an executable, `robots`, invocable with
`python -m`. If installed globally with `pipx`, the command `robots` can be invoked from any folders. The usage examples in the following section use the command `robots`, but you can also substitute it with `python -m robots` in a virtual environment.

### Execute the Tool

After installing `robotspy`, you can validate the installation by running the following command:

```
$ robots --help
usage: robots <robotstxt> <useragent> <path>

Shows whether the given user agent and path combination are allowed or disallowed by the given robots.txt file.

positional arguments:
  robotstxt      robots.txt file path or URL
  useragent      User agent name
  path           Path or URI

optional arguments:
  -h, --help     show this help message and exit
  -v, --version  show program's version number and exit
```

### Examples

The content of http://www.pythontest.net/elsewhere/robots.txt is the following:

```
# Used by NetworkTestCase in Lib/test/test_robotparser.py

User-agent: Nutch
Disallow: /
Allow: /brian/

User-agent: *
Disallow: /webstats/
```

To check if the user agent `Nutch` can fetch the path `/brian/` you can execute:

```
$ robots http://www.pythontest.net/elsewhere/robots.txt Nutch /brian/
user-agent 'Nutch' with path '/brian/': ALLOWED
```

Or, you can also pass the full URL, http://www.pythontest.net/brian/:

```
$ robots http://www.pythontest.net/elsewhere/robots.txt Nutch /brian/
user-agent 'Nutch' with url 'http://www.pythontest.net/brian/': ALLOWED
```

Can user agent `Nutch` fetch the path `/brian`?

```
$ robots http://www.pythontest.net/elsewhere/robots.txt Nutch /brian
user-agent 'Nutch' with path '/brian': DISALLOWED
```

Or, `/`?

```
$ robots http://www.pythontest.net/elsewhere/robots.txt Nutch /
user-agent 'Nutch' with path '/': DISALLOWED
```

How about user agent `Johnny`?

```
$ robots http://www.pythontest.net/elsewhere/robots.txt Johnny /
user-agent 'Johnny' with path '/': ALLOWED
```

### Use the Module in a Project

If you have a virtual environment with the `robotspy` package installed, you can use the `robots` module from the Python shell:

```
(.venv) $ python
>>> import robots
>>> parser = robots.RobotsParser.from_uri('http://www.pythontest.net/elsewhere/robots.txt')
>>> useragent = 'Nutch'
>>> path = '/brian/'
>>> result = parser.can_fetch(useragent, path)
>>> print(f'Can {useragent} fetch {path}? {result}')
Can Nutch fetch /brian/? True
>>>
```

### Bug in the Python standard library

There is a bug in [`urllib.robotparser`](https://docs.python.org/3/library/urllib.robotparser.html)
from the Python standard library that causes the following test to differ from the example above with `robotspy`.

The example with `urllib.robotparser` is the following:

```
$ python
>>> import urllib.robotparser
>>> rp = urllib.robotparser.RobotFileParser()
>>> rp.set_url('http://www.pythontest.net/elsewhere/robots.txt')
>>> rp.read()
>>> rp.can_fetch('Nutch', '/brian/')
False
```

Notice that the result is `False` whereas `robotspy` returns `True`.

Bug [bpo-39187](https://bugs.python.org/issue39187) was open to raise awareness on this issue and PR
https://github.com/python/cpython/pull/17794 was submitted as a possible fix. `robotspy` does not
exhibit this problem.

## Development

The main development dependency is `pytest` for executing the tests. It is automatically
installed if you perform the following steps:

```
$ git clone https://github.com/andreburgaud/robotspy
$ cd robotspy
$ python -m venv .venv --prompt robots
$ . .venv/bin/activate
(robots) $ python -m pip install -r requirements.txt
(robots) $ python -m pip install -e .
(robots) $ make test
(robots) $ deactivate
$
```

On Windows:

```
C:/> git clone https://github.com/andreburgaud/robotspy
C:/> cd robotspy
C:/> python -m venv .venv --prompt robotspy
C:/> .venv\scripts\activate
(robots) c:\> python -m pip install -r requirements.txt
(robots) c:\> python -m pip install -e .
(robots) c:\> make test
(robots) c:\> deactivate
```

## Global Tools

The following tools were used during the development of `robotspy`:

* [Black](https://github.com/psf/black)
* [Mypy](http://mypy-lang.org/)
* [Pylint](https://www.pylint.org/)
* [twine](https://pypi.org/project/twine/)

See the build file, `Makefile` or `make.bat` on Windows, for the commands and parameters.

## Release History

* 0.10.0:
  * Fixed bugs in the URL path pattern matching ('?' is now handled correctly as the character '?' instead of matching any one character)
  * Added tests 541230 and 541230 from Google project https://github.com/google/robotstxt-spec-test
  * Contribution from https://github.com/kox-solid
* 0.9.0:
  * Updated the parser to behave like the Google robots parser. It now handles the product token in the user-agent line up to the last correct character instead of discarding it. See [issue #209](https://github.com/andreburgaud/robotspy/issues/209) for more details.
  * Contribution from https://github.com/kox-solid
* 0.8.0:
  * Addressed an issue raised when a robots.txt file is not UTF-8 encoded
  * Added a user agent to fetch the robots.txt, as some websites, such as pages hosted on Cloudflare, may return a 403 error
  * Updated the documentation to link to RFC 9309, Robots Exclusion Protocol (REP)
  * Added a GitHub action job to execute the tests against Python versions 3.8 to 3.12
  * Contribution from https://github.com/tumma72
* 0.7.0:
  * Fixed bug with the argument path when using the CLI
  * Print 'url' when the argument is a URL, 'path' otherwise
* 0.6.0:
  * Simplified dependencies by keeping only `pytest` in `requirements.txt`
* 0.5.0:
  * Updated all libraries. Tested with Python 3.9.
* 0.4.0:
  * Fixed issue with robots text pointed by relative paths
  * Integration of [Mypy](http://mypy-lang.org/), [Black](https://github.com/psf/black) and [Pylint](https://www.pylint.org/) as depencencies to ease cross-platform development
  * Limited `make.bat` build file for Windows
  * Git ignore vscode files, `tmp` directory, multiple virtual env (`.venv*`)
  * Fixed case insensitive issues on Windows
  * Tests successful on Windows
  * Added an ATRIBUTIONS files and build task to generate it
  * Upgraded `pyparsing` and `certifi`
* 0.3.3:
  * Upgraded `tqdm`, and `cryptography` packages
  * 0.3.2:
  * Upgraded `bleach`, `tqdm`, and `setuptools` packages
* 0.3.1:
  * Updated `idna` and `wcwidth` packages
  * Added `pipdeptree` package to provide visibility on dependencies
  * Fixed `mypy` errors
  * Explicitly ignored `pylint` errors related to commonly used names like `f`, `m`, or `T`
* 0.3.0: Updated `bleach` package to address CVE-2020-6802
* 0.2.0: Updated the documentation
* 0.1.0: Initial release

## License

[MIT License](LICENSE.md)