import httplib2
import json

HEADERS = {'Accept': 'application/json',
           'Content-Type': 'application/json; charset=UTF-8'}


class StudentNotFound(Exception):
    pass


class KOBRAClient:
    """
    Quick and dirty KOBRA parser
    """
    def __init__(self, user, api_key, url="https://kobra.ks.liu.se/students/api.json"):
        self.url = url
        self.http = httplib2.Http(disable_ssl_certificate_validation=True)
        self.http.add_credentials(user, api_key)

    def _get_student(self, params):
        try:
            status, result = self.http.request(self.url, 'POST', params, HEADERS)

            if status.get('status') == '404' or not result.strip():
                raise StudentNotFound()

        except ValueError:
            raise StudentNotFound()
        return json.loads(result)

    def get_student_by_liu_id(self, liu):
        return self._get_student('liu_id:"{0}"'.format(liu))

    def get_student_by_card(self, card_number):
        attr = 'rfid_number' if len(card_number) < 12 else 'barcode_number'
        return self._get_student('{0}:"{1}"'.format(attr, card_number))

    def get_student(self, id_or_card_number):
        # LiU-ID is normally 8 chars long (or 5 chars for some employees)
        if len(id_or_card_number) <= 8:
            return self.get_student_by_liu_id(id_or_card_number)
        return self.get_student_by_card(id_or_card_number)
