from dataclasses import dataclass
from unittest.mock import MagicMock
from copy import deepcopy

from expects import expect, equal
from mamba import description, it

from crowd_anki.utils.disambiguate_uuids import disambiguate_note_model_uuids

MODELS_WITH_DUPLICATES = [
    {
        "id": 1,
        "name": "Basic",
        "crowdanki_uuid": "79141f05-73b8-4836-a97f-438ec28bd8a5",
    },
    {
        "id": 2,
        "name": "Basic copy",
        "crowdanki_uuid": "79141f05-73b8-4836-a97f-438ec28bd8a5",
    }
]

MODELS_WITHOUT_DUPLICATES = [
    {
        "id": 1,
        "name": "Basic",
        "crowdanki_uuid": "79141f05-73b8-4836-a97f-438ec28bd8a5",
    },
    {
        "id": 2,
        "name": "Basic copy",
        "crowdanki_uuid": "6a69bc9d-de6d-42b3-9ba3-9f6e9cc09179",
    }
]

@dataclass
class Models:
    """Mock Anki's models, without initialising Anki's backend."""
    models: dict

Models.all = lambda self: self.models
Models.save = MagicMock()

with description("disambiguate_note_model_uuids"):
    with it("should disambiguate duplicated note model uuids"):
        collection = MagicMock()
        notifier = MagicMock()
        collection.models = Models(deepcopy(MODELS_WITH_DUPLICATES))
        disambiguate_note_model_uuids(collection, notifier)

        expect(collection.models.all()).not_to(equal(MODELS_WITH_DUPLICATES))
        expect(collection.models.all()[0]).to(equal(MODELS_WITH_DUPLICATES[0]))

    with it("should keep note models without duplicates unchanged uuids"):
        collection = MagicMock()
        notifier = MagicMock()
        collection.models = Models(deepcopy(MODELS_WITHOUT_DUPLICATES))
        disambiguate_note_model_uuids(collection, notifier)

        expect(collection.models.all()).to(equal(MODELS_WITHOUT_DUPLICATES))
