import anki.utils
from anki.decks import DeckManager


def get_card_ids(self, did, children=False, include_from_dynamic=False):
    deck_ids = [did] + ([deck_id for _, deck_id in self.children(did)] if children else [])

    request = "select id from cards where did in {}" + ("or odid in {}" if include_from_dynamic else "")
    parameters = (anki.utils.ids2str(deck_ids),) + ((anki.utils.ids2str(deck_ids),)
                                                    if include_from_dynamic else tuple())

    return self.col.db.list(request.format(*parameters))


def get_note_ids(self, deck_id, children=False, include_from_dynamic=False):
    card_ids_str = anki.utils.ids2str(self.get_card_ids(deck_id, children, include_from_dynamic))
    request = "SELECT DISTINCT nid FROM cards WHERE id IN " + card_ids_str
    return self.col.db.list(request)


DeckManager.get_card_ids = get_card_ids
DeckManager.get_note_ids = get_note_ids
