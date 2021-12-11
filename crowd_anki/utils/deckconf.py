# Note that this only works for Anki ≤ 2.1.45, or when using the old
# deck options popup with Anki 2.1.46+.  Anki 2.1.46+ has a new
# JavaScript-based options popup (with no hooks), by default.

from .constants import UUID_FIELD_NAME

def disambiguate_crowdanki_uuid(deck_conf, deck,
                                config, new_name,
                                new_conf_id):
    new_deck_conf = deck_conf.mw.col.decks.get_config(new_conf_id)
    if (new_deck_conf and (UUID_FIELD_NAME in new_deck_conf)):
        # Delete rather than generating anew, (with uuid1()) to avoid code duplication.
        del new_deck_conf[UUID_FIELD_NAME]
        deck_conf.mw.col.decks.update_config(new_deck_conf)
