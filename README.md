# Robots Exclusion Standard Parser for Python

The `robots` Python module implements a parser for robots.txt file. The recommended class to use is
`robots.RobotsParser`. Besides, a thin facade `robots.RobotFileParser` also exists to be used as
a substitute for [`urllib.robotparser.RobotFileParser`](https://docs.python.org/3/library/urllib.robotparser.html),
available in the Python standard library. The facade `robots.RobotFileParser` exposes an API that is
mostly compatible with `urllib.robotparser.RobotFileParser`.

The main reasons for this rewrite are the following:

1. It was initially intended to experiment with parsing `robots.txt` for a link checker project
(not implemented).
1. It is attempting to follow the latest internet draft
[Robots Exclusion Protocol](https://tools.ietf.org/html/draft-koster-rep-00).
1. It does not try to be compliant with commonly accepted directives that are not in the current
[specs](https://tools.ietf.org/html/draft-koster-rep-00) such as `request-rate` and `crawl-delay`,
but it currently supports `sitemaps`.
1. It satisfies the same tests as the [Google Robots.txt Parser](https://github.com/google/robotstxt),
except for some custom behaviors specific to Google Robots.

## Installation

**Note**: Python 3.8.x or 3.9.x required

You preferably want to install the `robots` package after creating a Python virtual environment,
in a newly created directory, as follows:

```
$ mkdir project && cd project
$ python -m venv .venv --prompt playground
$ . .venv/bin/activate
(playground) $ python -m pip install --upgrade pip
(playground) $ python -m pip install --upgrade setuptools
(playground) $ python -m pip install robotspy
(playground) $ python -m robots --help
...
```

On Windows:

```
C:/> mkdir project && cd project
C:/> python -m venv .venv --prompt playground
C:/> .venv\scripts\activate
(playground) c:\> python -m pip install --upgrade pip
(playground) c:\> python -m pip install --upgrade setuptools
(playground) c:\> python -m pip install robotspy
(playground) c:\> python -m robots --help
...
```

## Usage

The `robots` package can be imported as a module and also exposes an executable invokable with
`python -m`.

### Execute the Package

After installing `robotspy`, you can validate the installation by running the following command:

```
(playground) $ python -m robots --help
usage: robots (<robots_path>|<robots_url>) <user_agent> <URI>

Shows whether the given user agent and URI combination are allowed or disallowed
by the given robots.txt file.

positional arguments:
  robotstxt      robots.txt file path or URL
  useragent      User agent name
  uri            Path or URI

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
(playground) $ python -m robots http://www.pythontest.net/elsewhere/robots.txt Nutch /brian/
user-agent 'Nutch' with URI '/brian/': ALLOWED
```

Or, you can also pass the full URL, http://www.pythontest.net/brian/:

```
(playground) $ python -m robots http://www.pythontest.net/elsewhere/robots.txt Nutch /brian/
user-agent 'Nutch' with URI 'http://www.pythontest.net/brian/': ALLOWED
```

Can user agent `Nutch` fetch the path `/brian`?

```
(playground) $ python -m robots http://www.pythontest.net/elsewhere/robots.txt Nutch /brian
user-agent 'Nutch' with URI '/brian': DISALLOWED
```

Or, `/`?

```
(playground) $ python -m robots http://www.pythontest.net/elsewhere/robots.txt Nutch /
user-agent 'Nutch' with URI '/': DISALLOWED
```

How about user agent `Johnny`?

```
(playground) $ python -m robots http://www.pythontest.net/elsewhere/robots.txt Johnny /
user-agent 'Johnny' with URI '/': ALLOWED
```

### Use the Module in a Project

Here is an example with the same data as above, using the `robots` package from the Python shell:

```
(playground) $ python
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
$ python -m venv .venv --prompt robotspy
$ . .venv/bin/activate
(robotspy) $ python -m pip install -r requirements.txt
(robotspy) $ python -m pip install -e .
(robotspy) $ make test
(robotspy) $ deactivate
$
```

On Windows:

```
C:/> git clone https://github.com/andreburgaud/robotspy
C:/> cd robotspy
C:/> python -m venv .venv --prompt robotspy
C:/> .venv\scripts\activate
(robotspy) c:\> python -m pip install -r requirements.txt
(robotspy) c:\> python -m pip install -e .
(robotspy) c:\> make test
(robotspy) c:\> deactivate
```

Other dependencies are intended for deployment to the [Cheese Shop](https://wiki.python.org/moin/CheeseShop) ([PyPI](https://pypi.org/)):

* [Wheel](https://pypi.org/project/wheel/0.22.0/)
* [twine](https://pypi.org/project/twine/)
* [Black](https://github.com/psf/black)
* [Mypy](http://mypy-lang.org/)
* [Pylint](https://www.pylint.org/)

See the build file, `Makefile` or `make.bat` on Windows, for the commands and parameters.

### Dependency Tree

To display the dependency tree:

```
$ pipdeptree
```

or

```
$ make tree
```

To display the reverse dependency tree of a particular package, `idna` in the example below:

```
$ pipdeptree --reverse --packages idna
```

## Attributions

Although `robotspy` does not have any dependencies other than packages in the Python standard libraries, a few tools are used for testing, validating, packaging and deploying this library. You can check out [ATTRIBUTIONS](ATTRIBUTIONS.md) that outlines tools with their respective versions, licenses and web sites URL's.

## Release History

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