from mamba import description, it, _it
from pathlib import Path
from unittest.mock import MagicMock

from crowd_anki.anki_adapters.anki_deck import AnkiDeck
from crowd_anki.history.anki_deck_archiver import AnkiDeckArchiver

with description(AnkiDeckArchiver) as self:
    with it("inits repo, archives the deck there and commits"):
        base_path = Path('dummy_dir')
        deck_path = base_path.joinpath('deck_name')

        deck_exporter_mock = MagicMock()
        deck_exporter_mock.export_to_directory.return_value = deck_path

        repo_mock = MagicMock()
        deck = AnkiDeck({})
        archival_reason = "whee"

        AnkiDeckArchiver(deck_exporter_mock, lambda _: repo_mock, deck, base_path).archive(reason=archival_reason)

        deck_exporter_mock.export_to_directory.assert_called_once_with(deck, base_path)
        repo_mock.init.assert_called_once()
        repo_mock.stage_all.assert_called_once()
        repo_mock.commit.assert_called_once_with(archival_reason)

    with _it("should delete all existing content of the repo before adding new one"):
        ''' 
        Not sure if this is a good idea, this will help with cleaning out the media files not used anymore 
        but may adversely affect the user if they are to add custom things to the repo. 
        I can consider making this configurable per repo.
        '''

    with _it("if deck renamed it should rename the archival directory instead of creating a new one"):
        '''todo'''

    with _it("should push changes to specified branch in origin"):
        '''todo'''
