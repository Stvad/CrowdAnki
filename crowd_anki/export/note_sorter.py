from ..config.config_settings import ConfigSettings


class NoteSorter():
    sorting_definitions = {
        ConfigSettings.DeckExportSortMethods.NO_SORTING: None,
        ConfigSettings.DeckExportSortMethods.GUID: lambda i: i.anki_object.guid,
        ConfigSettings.DeckExportSortMethods.FLAG: lambda i: i.anki_object.flags,
        ConfigSettings.DeckExportSortMethods.TAG: lambda i: i.anki_object.tags,
        ConfigSettings.DeckExportSortMethods.NOTE_MODEL: lambda i: i.anki_object._model["name"],
        ConfigSettings.DeckExportSortMethods.NOTE_MODEL_ID: lambda i: i.anki_object._model["crowdanki_uuid"],
        ConfigSettings.DeckExportSortMethods.FIELD1: lambda i: i.anki_object.fields[0],
        ConfigSettings.DeckExportSortMethods.FIELD2: lambda i: i.anki_object.fields[1]
    }
    
    def __init__(self, config: ConfigSettings):
        self.sort_methods = [
            ConfigSettings.DeckExportSortMethods(method)
            for method in config.export_deck_sort_methods
        ]
        self.is_reversed = config.export_deck_sort_reversed

    def should_skip_sorting(self):
        return self.sort_methods[0] == ConfigSettings.DeckExportSortMethods.NO_SORTING and not self.is_reversed

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