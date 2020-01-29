import pytest
import robots


@pytest.fixture(scope='function')
def can_fetch():
    def _parser(robots_txt, agent, path):
        p = robots.RobotsParser.from_string(robots_txt)
        return p.can_fetch(agent, path)
    return _parser


def pytest_make_parametrize_id(config, val, argname):
    if isinstance(val, str):
        if not val:
            return f'{argname}=<empty>'
        output = val.strip()
        output = output.split('\n')[0].strip()
        return f"{argname}={output}"
    return f'{argname}={val}'
