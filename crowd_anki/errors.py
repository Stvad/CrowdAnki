"""Module for CrowdAnki's exceptions."""

class CrowdAnkiException(Exception):
    """Base class for CrowdAnki's exceptions."""

class UnexportableDeckException(CrowdAnkiException):
    """Exception for decks that are not CrowdAnki-exportable.

    This is currently the set of all decks and filtered decks.

    """
