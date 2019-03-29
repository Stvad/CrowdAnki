from anki.cards import Card


def move_to_deck(self, deck_id, move_from_dynamic_deck=False):
    """
    Moves self to the deck with specified deck_id
    :parameter deck_id Destination deck id.
    :parameter move_from_dynamic_deck Specifies if we should perform move if card is in dynamic deck
     or should we just change it's "odid" old/original deck id.
     The function is not doing flush, so you need to call flush yourself in order to persist changes into DB
    """
    if move_from_dynamic_deck:
        self.col.sched.remFromDyn([self.id])
        self.load()

    if self.odid:
        self.odid = deck_id
    else:
        self.did = deck_id


Card.move_to_deck = move_to_deck
