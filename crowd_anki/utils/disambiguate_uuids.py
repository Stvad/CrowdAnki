from uuid import uuid1

from .notifier import AnkiModalNotifier

def disambiguate_note_model_uuids(collection, notifier=None) -> None:
    """Disambiguate duplicate note model UUIDs.

    In CrowdAnki ≤ 0.9, cloning a note model with an already assigned
    crowdanki_uuid resulted in the clone inheriting the "original's"
    crowdanki_uuid.

    This has been fixed (#136), but:

    1. Users will still have duplicate UUIDs from before the upgrade.

    2. Users who create note models on platforms other than Anki with
    CrowdAnki installed — for instance on mobile — will still have the
    old issue, since cloning note models on those platforms will again
    clone UUIDs.

    """
    if notifier is None:
        notifier = AnkiModalNotifier()
    uuids = []
    full_message = ""
    for model in filter(lambda model: "crowdanki_uuid" in model,
                        sorted(collection.models.all(), key=lambda m: m["id"])):
        # We're sorting by note model id, because it almost always
        # (see the discussion in the PR for this addition) corresponds
        # to the time of creation of the note model, in milliseconds
        # since the epoch, so the copies will almost always have
        # larger ids than the originals, so we'll hopefully be
        # changing the UUIDs of the copies, not the originals.
        crowdanki_uuid = model["crowdanki_uuid"]
        if crowdanki_uuid in uuids:
            new_crowdanki_uuid = str(uuid1())
            model["crowdanki_uuid"] = new_crowdanki_uuid
            collection.models.save(model)
            message = (f"Replacing duplicate UUID ({crowdanki_uuid}) for note model "
                       f"“{model['name']}” with new UUID ({new_crowdanki_uuid})!\n")
            # Printing in the unlikely case there's a crash later in
            # the loop.
            print(message)
            full_message += message
        else:
            uuids.append(crowdanki_uuid)

    if full_message:
        full_message += (
            "\nFor details, please see "
            "https://github.com/Stvad/CrowdAnki/wiki/Workarounds-—-Duplicate-note-model-uuids .\n\n"
            "The replacement should be a one-off occurrence.  "
            "If this message appears frequently, please open an issue!"
        )
        notifier.info("UUIDs disambiguated", full_message)
