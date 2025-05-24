from functional import seq

ascii_control_chars = ''.join([chr(x) for x in range(0,32)])
invalid_filename_chars = set(":*?\"<>|/\\ \n" + ascii_control_chars)

# https://learn.microsoft.com/en-us/windows/win32/fileio/naming-a-file
windows_reserved_names = ["CON", "PRN", "AUX", "NUL", "COM1", "COM2", "COM3", "COM4", "COM5", "COM6", "COM7", "COM8", "COM9", "COM¹", "COM²", "COM³", "LPT1", "LPT2", "LPT3", "LPT4", "LPT5", "LPT6", "LPT7", "LPT8", "LPT9", "LPT¹", "LPT²", "LPT³"]

def is_reserved_name(name: str) -> bool:
    stem = name.split(".")[0]
    if stem.upper() in windows_reserved_names:
        return True

    return False


def sanitize_anki_deck_name(name: str, replace_char='_'):
    """
    Get name that conforms to fs standards from deck name
    """
    if is_reserved_name(str(name)):
        name = replace_char + name

    return seq(list(name)) \
        .map(lambda c: replace_char if c in invalid_filename_chars else c) \
        .make_string('')
