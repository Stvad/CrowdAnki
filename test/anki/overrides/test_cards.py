from unittest.mock import MagicMock, patch

from expects import be_true, be_false, expect
from mamba import before, context, description, it

from crowd_anki.anki.overrides import cards
from test_utils.anki.card_creator import create_card

with description("Card Overrides") as self:
    with before.each:
        self.card = create_card()

    with context("move_to_deck"):
        with it("should return true if the deck is changed"):
            self.card.did = 1
            result = self.card.move_to_deck(2)
            expect(result).to(be_true)

        with it("should return false if the deck is not changed"):
            self.card.did = 1
            result = self.card.move_to_deck(1)
            expect(result).to(be_false)

        with it("should return true if the odid is changed"):
            self.card.odid = 1
            result = self.card.move_to_deck(2)
            expect(result).to(be_true)

        with it("should return false if the odid is not changed"):
            self.card.odid = 1
            result = self.card.move_to_deck(1)
            expect(result).to(be_false)

        with it("should return true if moving from a dynamic deck"):
            self.card.col = MagicMock()
            self.card.col.sched.remFromDyn = MagicMock()
            self.card.load = MagicMock()

            result = self.card.move_to_deck(1, move_from_dynamic_deck=True)

            expect(result).to(be_true)
            self.card.col.sched.remFromDyn.assert_called_once_with([self.card.id])
            self.card.load.assert_called_once()
