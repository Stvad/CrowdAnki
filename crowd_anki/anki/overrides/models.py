import anki.hooks
from anki.models import ModelManager

from ...utils.constants import UUID_FIELD_NAME

def model_copy(*args, **kwargs):
    """Override the built-in models.copy.

    Extracting `_old` from `kwargs` is ugly, but allows passing
    arbitrary arguments to the built-in copy function (`_old()`).  For
    instance, in Anki 2.1.45, an optional `add` argument is added to
    `copy`.

    Note that this wrapper won't have any effect if `add=True` is
    passed to `copy`!  Fortunately, this will only happen if another
    add-on tries to clone a note model using `models.copy()`.  In Anki
    itself, only add=False is passed, by design — the idea is that
    normally the new model is only actually added (once!) to the
    database in `Models.onAdd` in `qt/aqt/models.py`.

    We could try to special-case `add=True` and call something like
    `models.add(cloned)` if `add=True`, but it'd make this wrapper
    more fragile to changes in `copy`, for relatively little gain.

    A more serious problem than another add-on cloning note models is
    AnkiDroid and AnkiMobile doing so, which we're currently not
    mitigating.

    """
    _old = kwargs['_old']
    del kwargs['_old']
    cloned = _old(*args, **kwargs)
    if UUID_FIELD_NAME in cloned:
        del cloned[UUID_FIELD_NAME]
    return cloned

ModelManager.copy = anki.hooks.wrap(old=ModelManager.copy, new=model_copy, pos='around')
