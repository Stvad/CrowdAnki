import operator

from expects.matchers import Matcher
from expects.matchers.built_in import contain
from functional import seq


# noinspection PyPep8Naming
class contain_any(Matcher):
    def __init__(self, *expected):
        self.expected = expected

    def _match(self, subject):
        return seq(self.expected).map(contain).reduce(operator.or_)._match(subject)
