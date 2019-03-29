from expects import expect, equal, be
from mamba import description, it, before
from unittest.mock import MagicMock

from crowd_anki.anki.adapters.anki_deck import NamedLazyDeck

test_name = 'test_name'

with description(NamedLazyDeck) as self:
    with before.each:
        self.initializer = MagicMock()
        self.deck = NamedLazyDeck(test_name, self.initializer)

    with it('should return name without calling initializer'):
        expect(self.deck.name).to(equal(test_name))
        self.initializer.assert_not_called()

    with it('should call initializer when we check whether deck is dynamic'):
        self.initializer.return_value = {'dyn': True}

        expect(self.deck.is_dynamic).to(be(True))
        self.initializer.assert_called_once_with(test_name)
