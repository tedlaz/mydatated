from collections import namedtuple
from unicodedata import name
import invoices as inv

Issuer = namedtuple('Issuer', 'afm country branch')
Counterpart = namedtuple('Counterpart', 'afm country branch postcode city')
Payment = namedtuple('Payment', 'type amount info')
Line = namedtuple('Line', 'value vatcategory vat')
Total = namedtuple('Total', 'value vat gross')


def test_01():
    invoice = inv.Invoice(
        Issuer('123123123', 'GR', '1'),
        Counterpart('111222333', 'GR', '0', '11534', 'VRILISSIA'),
        [Payment(3, 1000, '30 meres')],
        [Line(100, 1, 24), Line(100, 2, 13)],
        Total(1234.45, 234.45, 1000)
    )
    invoice.create_xml_file('test1.xml')
