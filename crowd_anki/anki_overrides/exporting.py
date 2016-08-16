import os

from anki.exporting import AnkiExporter


def get_files_for_models(self, model_ids, media_dir):
    result = set()
    for file_name in os.listdir(media_dir):
        if file_name.startswith("_"):
            # Scan all models in model_ids for reference to file_name
            for model in self.src.models.all():
                if int(model['id']) in model_ids:
                    if self._modelHasMedia(model, file_name):
                        result.add(file_name)
                        break
    return result


#todo need?
def get_exporter_id(exporter):
    return "%s (*%s)".format(exporter.key, exporter.ext), exporter


AnkiExporter.get_files_for_models = get_files_for_models
