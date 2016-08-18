import os

import anki.hooks
import aqt.exporting
import re
from anki.hooks import addHook, remHook
from anki.lang import ngettext
from anki.utils import intTime
from aqt import QDialog
from aqt import QFileDialog
from aqt import QStandardPaths
from anki.exporting import AnkiExporter
from aqt.exporting import ExportDialog
from aqt.utils import askUser, checkInvalidFilename, getSaveFile, tooltip, showWarning


def get_files_for_models(self, model_ids, media_dir):
    result = set()
    for file_name in os.listdir(media_dir):
        if file_name.startswith("_"):
            # Scan all models in model_ids for reference to file_name
            for model in self.col.models.all():
                if int(model['id']) in model_ids:
                    if self._modelHasMedia(model, file_name):
                        result.add(file_name)
                        break
    return result


def get_exporter_id(exporter):
    return "{} (*{})".format(exporter.key, exporter.ext), exporter


AnkiExporter.get_files_for_models = get_files_for_models

# aqt part:


def exporter_changed(self, exporter_id):
    self.exporter = aqt.exporting.exporters()[exporter_id][1](self.col)
    self.frm.includeMedia.setVisible(hasattr(self.exporter, "includeMedia"))


def accept(self):
    self.exporter.includeSched = (
        self.frm.includeSched.isChecked())
    self.exporter.includeMedia = (
        self.frm.includeMedia.isChecked())
    self.exporter.includeTags = (
        self.frm.includeTags.isChecked())
    if not self.frm.deck.currentIndex():
        self.exporter.did = None
    else:
        name = self.decks[self.frm.deck.currentIndex()]
        self.exporter.did = self.col.decks.id(name)

    directory_export = hasattr(self.exporter, "directory_export")
    directory = None
    export_file = None

    if (self.isApkg and self.exporter.includeSched and not
    self.exporter.did):
        verbatim = True
        # it's a verbatim apkg export, so place on desktop instead of
        # choosing file; use homedir if no desktop
        usingHomedir = False
        export_file = os.path.join(QStandardPaths.writableLocation(
            QStandardPaths.DesktopLocation), "collection.apkg")
        if not os.path.exists(os.path.dirname(export_file)):
            usingHomedir = True
            export_file = os.path.join(QStandardPaths.writableLocation(
                QStandardPaths.HomeLocation), "collection.apkg")
        if os.path.exists(export_file):
            if usingHomedir:
                question = ("%s already exists in your home directory. Overwrite it?")
            else:
                question = ("%s already exists on your desktop. Overwrite it?")
            if not askUser(question % "collection.apkg"):
                return
    else:
        verbatim = False
        # Get deck name and remove invalid filename characters
        deck_name = self.decks[self.frm.deck.currentIndex()]
        deck_name = re.sub('[\\\\/?<>:*|"^]', '_', deck_name)
        filename = os.path.join(aqt.mw.pm.base,
                                '{0}{1}'.format(deck_name, self.exporter.ext))
        while 1:
            if directory_export:
                directory = str(QFileDialog.getExistingDirectory(caption="Select Export Directory",
                                                                 directory=filename))
                if directory:
                    export_file = os.path.join(directory, str(intTime()))
            else:
                export_file = getSaveFile(self, ("Export"), "export",
                                          self.exporter.key, self.exporter.ext,
                                          fname=filename)
            if not export_file:
                return
            if checkInvalidFilename(os.path.basename(export_file), dirsep=False):
                continue
            break
    self.hide()
    if export_file:
        self.mw.progress.start(immediate=True)
        try:
            f = open(export_file, "wb")
            f.close()
        except (OSError, IOError) as e:
            showWarning(_("Couldn't save file: %s") % str(e))
        else:
            os.unlink(export_file)
            exportedMedia = lambda cnt: self.mw.progress.update(
                label=ngettext("Exported %d media file",
                               "Exported %d media files", cnt) % cnt
            )
            addHook("exportedMediaFiles", exportedMedia)
            self.exporter.exportInto(directory if directory_export else export_file)
            remHook("exportedMediaFiles", exportedMedia)
            if verbatim:
                if usingHomedir:
                    msg = ("A file called %s was saved in your home directory.")
                else:
                    msg = ("A file called %s was saved on your desktop.")
                msg = msg % "collection.apkg"
                period = 5000
            else:
                period = 3000
                if self.isTextNote:
                    msg = ngettext("%d note exported.", "%d notes exported.",
                                   self.exporter.count) % self.exporter.count
                else:
                    msg = ngettext("%d card exported.", "%d cards exported.",
                                   self.exporter.count) % self.exporter.count
            tooltip(msg, period=period)
        finally:
            self.mw.progress.finish()
    QDialog.accept(self)


ExportDialog.exporterChanged = anki.hooks.wrap(ExportDialog.exporterChanged, exporter_changed)
ExportDialog.accept = accept