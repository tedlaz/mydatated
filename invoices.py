import xml.etree.ElementTree as gfg
from ntuples import CLine, Total


class Invoice:
    def __init__(self, typ, issuer, counterpart, head, payments, lines: list):
        self.typ = typ
        self.issuer = issuer
        self.counterpart = counterpart
        self.head = head
        self.payments = payments
        self.lines = lines
        # self.total = total

    def _render_issuer(self):
        issuer = gfg.Element("issuer")
        issuer_vat_number = gfg.SubElement(issuer, "vatNumber")
        issuer_vat_number.text = self.issuer.afm

        issuer_country = gfg.SubElement(issuer, "country")
        issuer_country.text = self.issuer.country  # GR

        issuer_branch = gfg.SubElement(issuer, "branch")
        issuer_branch.text = self.issuer.branch  # 1
        return issuer

    def _render_counterpart(self):
        counterpart = gfg.Element("counterpart")
        cp_vat_number = gfg.SubElement(counterpart, "vatNumber")
        cp_vat_number.text = self.counterpart.afm

        cp_country = gfg.SubElement(counterpart, "country")
        cp_country.text = self.counterpart.country  # GR

        cp_branch = gfg.SubElement(counterpart, "branch")
        cp_branch.text = self.counterpart.branch  # 0

        cp_address = gfg.Element('address')
        counterpart.append(cp_address)

        cp_pcode = gfg.SubElement(cp_address, "postalCode")
        cp_pcode.text = self.counterpart.postcode

        cp_pcity = gfg.SubElement(cp_address, "city")
        cp_pcity.text = self.counterpart.city

        return counterpart

    def _render_head(self):
        head = gfg.Element("invoiceHeader")

        series = gfg.SubElement(head, "series")
        series.text = str(self.head.series)

        aan = gfg.SubElement(head, "aa")
        aan.text = str(self.head.aa)

        issuedate = gfg.SubElement(head, "issueDate")
        issuedate.text = self.head.date

        invoicetype = gfg.SubElement(head, "invoiceType")
        invoicetype.text = str(self.head.invtype)

        currency = gfg.SubElement(head, "currency")
        currency.text = self.head.currency

        return head

    def _render_payments(self):
        if not self.payments:
            return None

        payments = gfg.Element("paymentMethods")

        for lin in self.payments:
            pay = gfg.Element("paymentMethodDetails")

            typos = gfg.SubElement(pay, 'type')
            typos.text = str(lin.type)

            amount = gfg.SubElement(pay, 'amount')
            amount.text = f'{lin.amount:0.2f}'

            info = gfg.SubElement(pay, 'paymentMethodInfo')
            info.text = lin.info

            payments.append(pay)
        return payments

    def _line_classification(self, line):
        classtyp = 'expensesClassification'
        prefix = 'ecls:'
        if self.typ == 'income':
            classtyp = 'incomeClassification'
            prefix = 'icls:'

        clf = gfg.Element(classtyp)

        clftype = gfg.SubElement(clf, f"{prefix}classificationType")
        clftype.text = line.ctyp

        clfcat = gfg.SubElement(clf, f"{prefix}classificationCategory")
        clfcat.text = line.ccat

        amount = gfg.SubElement(clf, f"{prefix}amount")
        amount.text = f"{line.value:0.2f}"

        return clf

    def _render_details(self):
        details = []
        for i, lin in enumerate(self.lines):
            det = gfg.Element("invoiceDetails")

            linenumber = gfg.SubElement(det, "lineNumber")
            linenumber.text = str(i + 1)

            netvalue = gfg.SubElement(det, "netValue")
            netvalue.text = f"{lin.value:0.2f}"

            vatcategory = gfg.SubElement(det, "vatCategory")
            vatcategory.text = str(lin.vatcategory)

            vatamount = gfg.SubElement(det, "vatAmount")
            vatamount.text = f"{lin.vat:0.2f}"

            discountoption = gfg.SubElement(det, "discountOption")
            discountoption.text = "true"

            det.append(self._line_classification(lin))

            details.append(det)

        return details

    def _render_taxestotals(self, taxes):
        taxest = gfg.Element("taxesTotals")

        for tax in taxes:
            tax = gfg.Element('taxes')

            typ = gfg.SubElement(tax, 'taxType')
            typ.text = '1'

            cat = gfg.SubElement(tax, 'taxCategory')
            cat.text = '2'

            uval = gfg.SubElement(tax, 'underlyingValue')
            uval.text = '500.00'

            amount = gfg.SubElement(tax, 'taxAmount')
            amount.text = '100.00'

        return taxest

    def _summary_classification_lines(self):
        ltot = {}
        for lin in self.lines:
            ltot[lin.ctyp] = ltot.get(lin.ctyp, {})
            ltot[lin.ctyp][lin.ccat] = ltot[lin.ctyp].get(
                lin.ccat, 0) + lin.value

        clines = []
        for ctype, ctypedict in ltot.items():
            for ccat, val in ctypedict.items():
                clines.append(CLine(ctype, ccat, val))
        return clines

    def _calc_total(self):
        tval = tvat = 0
        for line in self.lines:
            tval += line.value
            tvat += line.vat
        tval = round(tval, 2)
        tvat = round(tvat, 2)
        gross = round(tval + tvat, 2)
        return Total(tval, tvat, gross)

    def _render_summary(self):
        summary = gfg.Element("invoiceSummary")

        total = self._calc_total()
        totalnetvalue = gfg.SubElement(summary, "totalNetValue")
        totalnetvalue.text = f"{total.value:0.2f}"

        totalvatamount = gfg.SubElement(summary, "totalVatAmount")
        totalvatamount.text = f"{total.vat:0.2f}"

        totalwithheld = gfg.SubElement(summary, "totalWithheldAmount")
        totalwithheld.text = f"{0:0.2f}"

        totalfees = gfg.SubElement(summary, "totalFeesAmount")
        totalfees.text = f"{0:0.2f}"

        totalstampduty = gfg.SubElement(summary, "totalStampDutyAmount")
        totalstampduty.text = f"{0:0.2f}"

        totalothertaxes = gfg.SubElement(summary, "totalOtherTaxesAmount")
        totalothertaxes.text = f"{0:0.2f}"

        totaldeductions = gfg.SubElement(summary, "totalDeductionsAmount")
        totaldeductions.text = f"{0:0.2f}"

        totalgrossvalue = gfg.SubElement(summary, "totalGrossValue")
        totalgrossvalue.text = f"{total.gross:0.2f}"

        for lin in self._summary_classification_lines():
            summary.append(self._line_classification(lin))

        return summary

    def render_invoice(self):
        payment_methods = ''

        invoice = gfg.Element("invoice")
        invoice.append(self._render_issuer())
        invoice.append(self._render_counterpart())
        invoice.append(self._render_head())

        payment_methods = self._render_payments()
        if payment_methods:
            invoice.append(payment_methods)

        for det in self._render_details():
            invoice.append(det)

        invoice.append(self._render_summary())

        return invoice


def render_invoicesdoc(invoices):
    # invoice = self.render_invoice()
    invoicesdoc = gfg.Element(
        'InvoicesDoc',
        **{'xmlns': "http://www.aade.gr/myDATA/invoice/v1.0"},
        **{'xmlns:xsi': 'http://www.w3.org/2001/XMLSchema-instance'},
        **{'xsi:schemaLocation': 'http://www.aade.gr/myDATA/invoice/v1.0/InvoicesDoc-v0.6.xsd'},
        **{'xmlns:icls': 'https://www.aade.gr/myDATA/incomeClassificaton/v1.0'},
        **{'xmlns:ecls': 'https://www.aade.gr/myDATA/expensesClassificaton/v1.0'}
    )
    for invoice in invoices:
        invoicesdoc.append(invoice.render_invoice())

    tree = gfg.ElementTree(invoicesdoc)
    return tree


def create_xml_file(filename, invoices):
    tree = render_invoicesdoc(invoices)
    with open(filename, "wb") as fil:
        tree.write(fil, xml_declaration=True, encoding='UTF-8')
