#Thanks to https://gist.github.com/jpassaro/4d5812290cdca51a8d3fe03c499d4149
from decimal import Decimal
import re

import yaml
from yaml.composer import Composer
from yaml.constructor import SafeConstructor
from yaml.parser import Parser
from yaml.reader import Reader
from yaml.resolver import BaseResolver, Resolver as DefaultResolver
from yaml.scanner import Scanner


class Resolver(BaseResolver):
    pass


Resolver.add_implicit_resolver(  # regex copied from yaml source
    '!decimal',
    re.compile(r'''^(?:
        [-+]?(?:[0-9][0-9_]*)\.[0-9_]*(?:[eE][-+][0-9]+)?
        |\.[0-9_]+(?:[eE][-+][0-9]+)?
        |[-+]?[0-9][0-9_]*(?::[0-9]?[0-9])+\.[0-9_]*
        |[-+]?\.(?:inf|Inf|INF)
        |\.(?:nan|NaN|NAN)
    )$''', re.VERBOSE),
    list('-+0123456789.')
)

for ch, vs in DefaultResolver.yaml_implicit_resolvers.items():
    Resolver.yaml_implicit_resolvers.setdefault(ch, []).extend(
        (tag, regexp) for tag, regexp in vs
        if not tag.endswith('float')
    )


class DecimalLoader(Reader, Scanner, Parser, Composer, SafeConstructor, Resolver):
    def __init__(self, stream):
        Reader.__init__(self, stream)
        Scanner.__init__(self)
        Parser.__init__(self)
        Composer.__init__(self)
        SafeConstructor.__init__(self)
        Resolver.__init__(self)


def decimal_constructor(loader, node):
    value = loader.construct_scalar(node)
    return Decimal(value)

yaml.add_constructor('!decimal', decimal_constructor, DecimalLoader)