from tempfile import TemporaryDirectory

from expects import expect
from hypothesis import given, assume, example
from hypothesis.strategies import text, characters
from mamba import description, it
from pathlib import Path

from crowd_anki.utils.filesystem.name_sanitizer import sanitize_anki_deck_name, \
    invalid_filename_chars
from test_utils.matchers import contain_any

size_limit = 255


def byte_length_size(sample):
    return len(bytes(sample, "utf-8")) <= size_limit


with description("AnkiDeckNameSanitizer"):
    with it("should remove all bad characters from the string"):
        expect(sanitize_anki_deck_name(invalid_filename_chars)) \
            .not_to(contain_any(*invalid_filename_chars))

    with it("should be possible to create a file name from a random sanitized string"):
        @given(text(characters(min_codepoint=1, max_codepoint=800), max_size=size_limit, min_size=1)
               .filter(byte_length_size))
        @example("line\n another one")
        def can_create(potential_name):
            assume(potential_name not in ('.', '..'))
            with TemporaryDirectory() as dir_name:
                Path(dir_name).joinpath(sanitize_anki_deck_name(potential_name)).mkdir()


        can_create()
