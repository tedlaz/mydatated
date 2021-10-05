import xml.etree.ElementTree as gfg


class Invoice:
    def __init__(self, issuer, counterpart, payments, lines: list, total):
        self.issuer = issuer
        self.counterpart = counterpart
        self.payments = payments
        self.lines = lines
        self.total = total

    def render_issuer(self):
        issuer = gfg.Element("issuer")
        issuer_vat_number = gfg.SubElement(issuer, "vatNumber")
        issuer_vat_number.text = self.issuer.afm

        issuer_country = gfg.SubElement(issuer, "country")
        issuer_country.text = self.issuer.country  # GR

        issuer_branch = gfg.SubElement(issuer, "branch")
        issuer_branch.text = self.issuer.branch  # 1
        return issuer

    def render_counterpart(self):
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

    def render_head(self):
        head = gfg.Element("invoiceHeader")

        series = gfg.SubElement(head, "series")
        series.text = 'A'

        issuedate = gfg.SubElement(head, "issueDate")
        issuedate.text = "2021-01-15"

        invoicetype = gfg.SubElement(head, "invoiceType")
        invoicetype.text = '1.1'

        currency = gfg.SubElement(head, "currency")
        currency.text = 'EUR'

        return head

    def render_payments(self):
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

    def render_details(self):
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

            details.append(det)

        return details

    def render_summary(self):
        summary = gfg.Element("invoiceSummary")

        totalnetvalue = gfg.SubElement(summary, "totalNetValue")
        totalnetvalue.text = f"{self.total.value:0.2f}"

        totalvatamount = gfg.SubElement(summary, "totalVatAmount")
        totalvatamount.text = f"{self.total.vat:0.2f}"

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
        totalgrossvalue.text = f"{self.total.gross:0.2f}"

        return summary

    def render_invoice(self):
        payment_methods = ''

        invoice = gfg.Element("invoice")
        invoice.append(self.render_issuer())
        invoice.append(self.render_counterpart())

        payment_methods = self.render_payments()
        if payment_methods:
            invoice.append(payment_methods)

        invoice.append(self.render_head())

        for det in self.render_details():
            invoice.append(det)

        invoice.append(self.render_summary())

        return invoice

    def render_xml(self):
        # nsp = {
        #     '': 'http://www.aade.gr/myDATA/invoice/v1.0',
        #     'xsi': 'http://www.w3.org/2001/XMLSchema-instance'
        # }
        # for key, val in nsp.items():
        #     gfg.register_namespace(key, val)

        invoice = self.render_invoice()
        invoicesdoc = gfg.Element(
            'InvoicesDoc',
            **{'xmlns': "http://www.aade.gr/myDATA/invoice/v1.0"},
            **{'xsi:schemaLocation': 'http://www.aade.gr/myDATA/invoice/v1.0/InvoicesDoc-v0.6.xsd'},
            **{'xmlns:icls': 'https://www.aade.gr/myDATA/incomeClassificaton/v1.0'},
            **{'xmlns:ecls': 'https://www.aade.gr/myDATA/expensesClassificaton/v1.0'}
        )
        invoicesdoc.append(invoice)

        tree = gfg.ElementTree(invoicesdoc)
        return tree

    def create_xml_file(self, filename):
        tree = self.render_xml()
        with open(filename, "wb") as fil:
            tree.write(fil, xml_declaration=True, encoding='UTF-8')
