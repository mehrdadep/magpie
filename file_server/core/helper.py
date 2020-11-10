import hashlib
import json
import uuid
from json import JSONDecodeError

from file_server.core import api_exceptions


class Helper:
    @staticmethod
    def generate_token():
        return hashlib.sha512(
            str(uuid.uuid4().hex).encode("utf-8")
        ).hexdigest()


    @staticmethod
    def get_dict_from_json(json_string):
        """
        Convert json string to dict (API Exception handled)
        :param json_string:
        :return: dict
        """
        try:
            json_dict = json.loads(json_string)
        except JSONDecodeError:
            raise api_exceptions.ValidationError400({
                'non_fields': _('JSON is not valid')
            })

        return json_dict
