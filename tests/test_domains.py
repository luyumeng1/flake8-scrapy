import ast
import os

from flake8_scrapy import ScrapyStyleChecker
from finders.domains import (
    UnreachableDomainIssueFinder, UrlInAllowedDomainsIssueFinder,
)


def load_sample_file(filename):
    path = os.path.join(
        os.path.dirname(__file__),
        'samples',
        filename
    )
    return open(path).read()


def run_checker(code):
    tree = ast.parse(code)
    checker = ScrapyStyleChecker(tree, None)
    return list(checker.run())


def test_url_not_in_allowed_domains():
    code = load_sample_file('allowed_domains.py')
    issues = run_checker(code)

    assert len(issues) == 2
    # first issue
    assert issues[0][0] == 14  # line
    assert issues[0][1] == 8   # col
    assert UnreachableDomainIssueFinder.msg_code in issues[0][2]
    assert UnreachableDomainIssueFinder.msg_info in issues[0][2]
    # second issue
    assert issues[1][0] == 15  # line
    assert issues[1][1] == 8   # col
    assert UnreachableDomainIssueFinder.msg_code in issues[1][2]
    assert UnreachableDomainIssueFinder.msg_info in issues[1][2]


def test_url_in_allowed_domains():
    code = load_sample_file('url_in_allowed_domains.py')
    issues = run_checker(code)

    assert len(issues) == 1
    # first issue
    assert issues[0][0] == 10  # line
    assert issues[0][1] == 8   # col
    assert UrlInAllowedDomainsIssueFinder.msg_code in issues[0][2]
    assert UrlInAllowedDomainsIssueFinder.msg_info in issues[0][2]
