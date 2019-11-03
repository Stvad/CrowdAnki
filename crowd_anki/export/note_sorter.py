from ..config.config_settings import ConfigSettings, NoteSortingMethods


class NoteSorter:
    sorting_definitions = {
        NoteSortingMethods.NO_SORTING: None,
        NoteSortingMethods.GUID: lambda i: i.anki_object.guid,
        NoteSortingMethods.FLAG: lambda i: i.anki_object.flags,
        NoteSortingMethods.TAG: lambda i: i.anki_object.tags,
        NoteSortingMethods.NOTE_MODEL: lambda i: i.anki_object._model["name"],
        NoteSortingMethods.NOTE_MODEL_ID: lambda i: i.anki_object._model["crowdanki_uuid"],
        NoteSortingMethods.FIELD1: lambda i: i.anki_object.fields[0],
        NoteSortingMethods.FIELD2: lambda i: i.anki_object.fields[1]
    }
    
    def __init__(self, config: ConfigSettings):
        self.sort_methods = [
            NoteSortingMethods(method)
            for method in config.export_note_sort_methods
        ]
        self.is_reversed = config.export_notes_reverse_order

    def should_skip_sorting(self):
        return self.sort_methods[0] == NoteSortingMethods.NO_SORTING and not self.is_reversed

    def sort_notes(self, notes):
        if not self.should_skip_sorting():
            notes = sorted(notes, key=self.get_sort_key, reverse=self.is_reversed)

        return notes

    def get_sort_key(self, note):   
        return tuple(
            key(note) 
            for key in tuple(
                self.sorting_definitions[method_name]
                for method_name in self.sort_methods
            )
        )
