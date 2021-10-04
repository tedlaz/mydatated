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
            return data
        except Exception as err:
            print(f"Error: {err}")

    def cancel_invoice(self, mark: str):
        """Ακύρωση τιμολογίου χωρίς αντικατάσταση με νέο"""
        params = urllib.parse.urlencode({
            'mark': mark,
        })
        return self.send("POST", f"/CancelInvoice?{params}", "")

    def request_docs(self, mark):
        """Η κλήση επιστρέφει όσα παραστατικά, χαρακτηρισμούς και ακυρώσεις
        παραστατικών έχουν υποβάλλει άλλοι χρήστες και αφορούν ως λήπτη την
        οντότητα που αντιστοιχεί στο όνομα χρήστη και subscription key,
        και αναγνωριστικό Μοναδικό Αριθμό Καταχώρησης μεγαλύτερο του mark.
        """
        params = urllib.parse.urlencode({
            'mark': mark,
        })
        return self.send("GET", f"/RequestDocs?{params}", "")

    def request_transmitted_docs(self, mark: str):
        """Η κλήση επιστρέφει όσα παραστατικά, χαρακτηρισμούς και ακυρώσεις
        παραστατικών έχει υποβάλει η οντότητα που αντιστοιχεί στο όνομα χρήστη
        και subscription key, και αναγνωριστικό Μοναδικό Αριθμό Καταχώρησης
        μεγαλύτερο του mark
        """
        params = urllib.parse.urlencode({
            'mark': mark,
        })
        return self.send("GET", f"/RequestTransmittedDocs?{params}", "")

    def send_expenses_classification(self, body: str):
        """Με τη κλήση αποστέλλεται μία ακολουθία από ένα ή περισσότερους
        χαρακτηρισμούς εξόδων.
        """
        params = urllib.parse.urlencode({
        })
        return self.send("POST", f"/SendExpensesClassification?{params}", body)

    def send_income_classification(self, body):
        """Με τη κλήση αποστέλλεται μία ακολουθία από ένα ή περισσότερους
        χαρακτηρισμούς εσόδων.
        """
        params = urllib.parse.urlencode({
        })
        return self.send("POST", f"/SendIncomeClassification?{params}", body)

    def send_invoices(self, body):
        """Με τη κλήση αποστέλλεται ακολουθία από ένα ή περισσότερα παραστατικά"""
        params = urllib.parse.urlencode({
        })
        return self.send("POST", f"/SendInvoices?{params}", body)
