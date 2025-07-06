from expects import be_false, be_true, expect
from mamba import before, context, description, it

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
