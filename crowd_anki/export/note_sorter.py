from ..config.config_settings import ConfigSettings, NoteSortingMethods


class NoteSorter:
    sorting_definitions = {
        NoteSortingMethods.NO_SORTING: lambda i: i,
        NoteSortingMethods.GUID: lambda i: i.anki_object.guid,
        NoteSortingMethods.FLAG: lambda i: i.anki_object.flags,
        NoteSortingMethods.TAG: lambda i: i.anki_object.tags,
        NoteSortingMethods.NOTE_MODEL: lambda i: i.anki_object._model["name"],
        NoteSortingMethods.NOTE_MODEL_ID: lambda i: i.anki_object._model["crowdanki_uuid"],
        NoteSortingMethods.FIELD1: lambda i: i.anki_object.fields[0],
        NoteSortingMethods.FIELD2: lambda i: i.anki_object.fields[1]
    }
    
    def __init__(self, config: ConfigSettings):
        self.sort_methods = config.get_note_sort_methods()
        self.is_reversed = getattr(config, ConfigSettings.Properties.EXPORT_NOTES_REVERSE_ORDER.value.config_name)

    def should_sort(self):
        return self.sort_methods[0] != NoteSortingMethods.NO_SORTING

    def sort_notes(self, notes):
        if self.should_sort():
            notes = sorted(notes, key=self.get_sort_key)

        if self.is_reversed:
            notes = list(reversed(notes))

        return notes

    def get_sort_key(self, note):   
        return tuple(
            key(note) 
            for key in tuple(
                self.sorting_definitions[method_name]
                for method_name in self.sort_methods
            )
        )
