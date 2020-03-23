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
[specs]((https://tools.ietf.org/html/draft-koster-rep-00)) such as `request-rate` and `crawl-delay`,
but it currently supports `sitemaps`.
1. It satisfies the same tests as the [Google Robots.txt Parser](https://github.com/google/robotstxt),
except for some custom behaviors specific to Google Robots.

## Installation

**Note**: Python 3.8.x is required

You preferably want to install the `robots` package after creating a Python virtual environment,
in a newly created directory, as follows:

```
$ mkdir project && cd project
$ python3 -m pip install robotspy
```

## Usage

The `robots` package can be imported as a module and also exposes an executable invokable with
`python -m`.

### Execute the Package

After installing `robotspy`, you can validate the installation by running the following command:

```
$ python -m robots --help
usage: robots (<robots_path>|<robots_url>) <user_agent> <URI>

Shows whether the given user agent and URI combination are allowed or
disallowed by the given robots.txt file.

positional arguments:
  robotstxt      robots.txt file path or URL
  useragent      User agent name
  uri            Path or URI

optional arguments:
  -h, --help     show this help message and exit
  -v, --version  show program's version number and exit
```

A concrete example to check against http://www.pythontest.net/elsewhere/robots.txt if the user agent
`Nutch` can fetch the path `/brian/` would be done as follows:

```
$ python -m robots http://www.pythontest.net/elsewhere/robots.txt Nutch /brian/
user-agent 'Nutch' with URI '/brian/': ALLOWED
```

### Use the Module in a Project

Here is an example with the same data as above, using the `robots` package from the Python shell:

```
>>> import robots
>>> parser = robots.RobotsParser.from_uri('http://www.pythontest.net/elsewhere/robots.txt')
>>> useragent = 'Nutch'
>>> path = '/brian/'
>>> result = parser.can_fetch(useragent, path)
>>> print(f"Can {useragent} fetch {path}? {result}")
Can Nutch fetch /brian/? True
>>>
```

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

Other dependencies are intended for deployment to the **Cheese Shop** (PyPI):

* wheel
* twine

The `Makefile` also invokes the following tools:

* [Black](https://github.com/psf/black)
* [Mypy](http://mypy-lang.org/)
* [Pylint](https://www.pylint.org/)

At this stage of the development, version 0.3.0, these development tools are expected to be installed globally.

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

## Release History

* 0.3.0: Updated `bleach` package to address CVE-2020-6802
* 0.2.0: Updated the documentation
* 0.1.0: Initial release

## License

MIT License