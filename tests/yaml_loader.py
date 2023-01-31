import decimal

from yaml.composer import Composer
from yaml.constructor import SafeConstructor
from yaml.parser import Parser
from yaml.reader import Reader
from yaml.resolver import Resolver
from yaml.scanner import Scanner


class DecimalSafeConstructor(SafeConstructor):
    """Special constructor to override construct_yaml_float() in order to cast "Decimal" types to the value"""

    def construct_yaml_float(self, node):
        value = super().construct_yaml_float(node)
        return decimal.Decimal(value)


DecimalSafeConstructor.add_constructor(
    "tag:yaml.org,2002:float", DecimalSafeConstructor.construct_yaml_float
)


class DecimalSafeLoader(Reader, Scanner, Parser, Composer, DecimalSafeConstructor, Resolver):
    def __init__(self, stream):
        Reader.__init__(self, stream)
        Scanner.__init__(self)
        Parser.__init__(self)
        Composer.__init__(self)
        DecimalSafeConstructor.__init__(self)
        Resolver.__init__(self)
