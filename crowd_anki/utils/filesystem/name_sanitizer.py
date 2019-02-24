from functional import seq

invalid_filename_chars = set(":*?\"<>|/\\ ")


def sanitize_anki_deck_name(name: str, replace_char='_'):
    """
    Get name that conforms to fs standards from deck name
    """
    return seq(list(name)) \
        .map(lambda c: replace_char if c in invalid_filename_chars else c) \
        .make_string('')
