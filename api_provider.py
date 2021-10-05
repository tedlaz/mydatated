import http.client
import urllib.request
import urllib.parse
import urllib.error


class MyDataAPI:
    api_url = 'mydata-dev.azure-api.net'

    def __init__(self, credentials):
        self.headers = credentials

    def send(self, typ, params, body):
        try:
            conn = http.client.HTTPSConnection(self.api_url)
            conn.request(typ, params, body, self.headers)
            response = conn.getresponse()
            data = response.read()
            conn.close()
            return data.decode()
        except Exception as err:
            print(f"Error: {err}")

    def request_receiver_info(self, vat_number):
        """Η κλήση επιστρέφει πληροφορίες σχετικά με την δήλωση αποδοχής
        της οντότητας για λήψη παραστατικών ηλεκτρονικής τιμολόγησης
        """
        params = urllib.parse.urlencode({
            'vatNumber': vat_number,
        })
        return self.send("GET", f"/myDATAProvider/RequestReceiverInfo?{params}", "")

    def request_transmitted_docs(self, mark: str):
        """Η κλήση επιστρέφει όσα παραστατικά, χαρακτηρισμούς και ακυρώσεις
        παραστατικών έχει υποβάλει η οντότητα που αντιστοιχεί στο όνομα χρήστη
        και subscription key, και αναγνωριστικό Μοναδικό Αριθμό Καταχώρησης
        μεγαλύτερο του mark
        """
        params = urllib.parse.urlencode({
            'mark': mark,
            'issuervat': '094025817'
        })
        return self.send("GET", f"/MyDataProvider/RequestTransmittedDocs?{params}", "")

    def send_invoices(self, body):
        """Με τη κλήση αποστέλλεται ακολουθία από ένα ή περισσότερα παραστατικά"""
        params = urllib.parse.urlencode({
        })
        return self.send("POST", f"/MyDataProvider/SendInvoices?{params}", body)
