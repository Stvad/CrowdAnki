import re
from dataclasses import dataclass

DEBUG = True

@dataclass
class NoteSorter():
    sort_method: list
    is_reversed: bool
    skip_sorting: bool
    sorting_definitions: list
    sort_map: set
    sort_key_tuple: tuple


    @classmethod
    def from_config(cls, config):
        cls.skip_sorting = False
        cls.setup_sorting_definitions(cls)

        if not config or "method" not in config:
            cls.skip_sorting = True
            cls.sort_method = ""
            cls.is_reversed = False
        else:
            cls.sort_method = config["method"]
            cls.is_reversed = config["reversed"] if "reversed" in config else False

        def _formatted_sort_method(method):
            return re.sub("[-_\s+]", "", method).lower()

        # Make sure formatting of sort_method is correct, and format each entry
        if isinstance(cls.sort_method, str):
            cls.sort_method = [_formatted_sort_method(cls.sort_method)]
        elif isinstance(cls.sort_method, list):
            if len(cls.sort_method) >= 1:
                cls.sort_method = [_formatted_sort_method(sm) for sm in cls.sort_method]
            else:
                cls.sort_method = [""]
        else:
            cls.sort_method = [""]

        if not cls.confirm_sortmethods_are_valid(cls):
            cls.skip_sorting = True
            cls.sort_key_tuple = None
        else:
            cls.setup_sorting_keys(cls)

        return NoteSorter(
            sort_method=cls.sort_method,
            is_reversed=cls.is_reversed,
            skip_sorting=cls.skip_sorting,
            sorting_definitions=cls.sorting_definitions,
            sort_map=cls.sort_map,
            sort_key_tuple=cls.sort_key_tuple
        )

    def sort_notes(self, notes):
        if DEBUG:
            print([note.anki_object.guid for note in notes])

        if not self.skip_sorting:
            if self.sort_method[0] in ["default", "none", "nosorting"]:      # Only the first method is considered for these pass variables
                if not self.is_reversed:
                    pass
                else:
                    notes = list(reversed(notes))
            else:
                notes = sorted(notes, key=self.get_sort_key, reverse=self.is_reversed)

        if DEBUG:
            print([note.anki_object.guid for note in notes])

        return notes

    def confirm_sortmethods_are_valid(self):
        for method in self.sort_method:
            if method not in self.sort_map:
                return False

        return True

    def setup_sorting_definitions(self):
            # Create mapping of sortable_values variable, to sort_method keys, to sortable_values lambda
        self.sorting_definitions = [
            (("guid", "guids"), lambda i: i.anki_object.guid),
            (("flag", "flags"), lambda i: i.anki_object.flags),
            (("tag", "tags"), lambda i: i.anki_object.tags),
            (("notemodel", "notemodels", "notemodelname", "notemodelsname", "notemodelnames", "notemodelsnames"), lambda i: i.anki_object._model["name"]),
            (("notemodelid", "notemodelsid", "notemodelids", "notemodelsids"), lambda i: i.anki_object._model["crowdanki_uuid"]),
            (("field1", "firstfield", "first"), lambda i: i.anki_object.fields[0]),
            (("field2", "secondfield", "second"), lambda i: i.anki_object.fields[1])
        ]

        # Flatten out the sorting_definitions to a map with one value per entry
        self.sort_map = {singlekey:lam for keytuple, lam in self.sorting_definitions for singlekey in keytuple}

    def setup_sorting_keys(self):
        self.sort_key_tuple = tuple(self.sort_map[method_name] for method_name in self.sort_method)

    def get_sort_key(self, note):   
        return tuple(key(note) for key in self.sort_key_tuple)