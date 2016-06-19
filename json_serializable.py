from CrowdAnki.utils import merge_dicts


class JsonSerializable(object):
    readable_names = {}
    filter_set = set()

    def __init__(self):
        pass
        # self._update_fields()
        # Todo consider introducing anki_dict and anki_object
        # multiple inheritance?

    @staticmethod
    def default_json(wobject):
        if isinstance(wobject, JsonSerializable):
            return wobject.flatten()

        raise TypeError

    def flatten(self):
        return {self.readable_names[key] if key in self.readable_names else key: value
                for key, value in merge_dicts(self.__dict__, self._dict_extension()).iteritems() if
                key not in self.filter_set}

    def _dict_extension(self):
        return {}

    def _update_fields(self):
        """
        Add necessary fields to anki dicts/objects. E.g. uuid
        """