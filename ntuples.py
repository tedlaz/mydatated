from collections import namedtuple

Line = namedtuple('Line', 'value vatcategory vat ctyp ccat')
CLine = namedtuple('CLine', 'ctyp ccat value')
Total = namedtuple('Total', 'value vat gross')
