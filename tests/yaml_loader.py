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
        # We force the string representation of the float here to avoid things like:
        # In [11]: decimal.Decimal(10.11)
        # Out[11]: Decimal('10.1099999999999994315658113919198513031005859375')
        return decimal.Decimal(f"{value}")


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
