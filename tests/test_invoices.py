from collections import namedtuple
import invoices as inv

Issuer = namedtuple('Issuer', 'afm country branch')
Counterpart = namedtuple('Counterpart', 'afm country branch postcode city')
Head = namedtuple('Head', 'series aa date invtype currency')
Payment = namedtuple('Payment', 'type amount info')
Line = namedtuple('Line', 'value vatcategory vat ctyp ccat')
Total = namedtuple('Total', 'value vat gross')


def test_01():
    invoice1 = inv.Invoice(
        'expenses',
        Issuer('123123123', 'GR', '0'),
        Counterpart('111222333', 'GR', '0', '11534', 'VRILISSIA'),
        Head('0', 101, '2021-01-13', '1.1', 'EUR'),
        [Payment(3, 237, 'ΠΙΣΤΩΣΗ 30 ΗΜΕΡΩΝ')],
        [Line(100, 1, 24, 'E3_881_001', 'category1_7'),
         Line(100, 2, 13, 'E3_881_001', 'category1_8')],
        # Total(200, 37, 237)
    )
    invoice2 = inv.Invoice(
        'income',
        Issuer('123123123', 'GR', '1'),
        Counterpart('555444333', 'GR', '0', '11221', 'ΑΘΗΝΑ'),
        Head('A', 102, '2021-01-14', '1.1', 'EUR'),
        [Payment(3, 124, '.')],
        [Line(100, 1, 24, 'E3_561_001', 'category1_1'),
         Line(200, 1, 48, 'E3_561_001', 'category1_2')],
        # Total(100, 24, 124)
    )
    inv.create_xml_file('test.xml', [invoice1, invoice2])
