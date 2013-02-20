import httplib2
import json

HEADERS = {'Accept': 'application/json',
           'Content-Type': 'application/json; charset=UTF-8'}

class KOBRAClient:
    """
    Quick and dirty KOBRA parser
    """
    def __init__(self, user, api_key, url="https://kobra.ks.liu.se/students/api.json"):
        self.url = url
        self.http = httplib2.Http(disable_ssl_certificate_validation=True)
        self.http.add_credentials(user, api_key)

    def _get_student(self, params):
        res = self.http.request(self.url, 'POST', params, HEADERS)
        # TODO: Error handling... hehe.. :)
        return json.loads(res[1])

    def get_student_by_liu_id(self, liu):
        return self._get_student('liu_id:"{0}"'.format(liu))

    def get_student_by_card(card_number):
        attr = 'rfid_number' if len(card_number > 12) else 'barcode_number'
        return self._get_student('{0}:"{1}"'.format(attr, card_number))
