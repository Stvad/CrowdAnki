from mamba import description, it, before
from unittest.mock import MagicMock

from crowd_anki.history.archiver.Archiver import AllDeckArchiver

with description(AllDeckArchiver) as self:
    with before.each:
        self.deck_without_children = MagicMock()

        self.deck_manager = MagicMock()
        self.deck_manager.leaf_decks.return_value = [self.deck_without_children]

        self.archiver_supplier = MagicMock()

        self.all_deck_archiver = AllDeckArchiver(self.deck_manager, self.archiver_supplier)

    with it("should call archival on all leaf decks by default"):
        self.all_deck_archiver.archive()
        self.archiver_supplier.assert_called_once_with(self.deck_without_children)
