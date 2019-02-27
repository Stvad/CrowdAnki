from dataclasses import dataclass


@dataclass
class AnkiDeck:
    data: dict

    deck_name_separator = '::'

    @property
    def is_dynamic(self):
        return bool(self.data['dyn'])

    @property
    def name(self):
        return self.data['name']
