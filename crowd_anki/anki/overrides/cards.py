from anki.cards import Card


def move_to_deck(self, deck_id):
    """
    Moves self to the deck with specified deck_id.
    This function will not persist or flush card modifications, callers must flush in order to persist changes.

    :parameter deck_id Destination deck id.
    :return: True if card was changed, False otherwise.
    """
    changed = False

    if self.odid:
        if self.odid != deck_id:
            self.odid = deck_id
            changed = True
    else:
        if self.did != deck_id:
            self.did = deck_id
            changed = True

    return changed


Card.move_to_deck = move_to_deck
