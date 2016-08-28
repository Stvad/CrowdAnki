# Feature list:

## Export: 
 - Introduces UUID for entities, that don't have it;
 - Exports media if any is used;
 - All significant data is exported; 
 - Export UI is integrated with Anki export UI.

## Import:
 - Creates deck/notes if not present;
 - On model type update, the dialogue for correspondence is shown;
 - When model type for note is changed -> correspondence dialogue is shown;
 - Media files are copied to main media directory (is it good enough?) test import on empty collection;
 - Dialogue is modal;
 - New id is generated for entities that don't have one;
 - If the entity with given id already exists - entity is updated (metadata is preserved);
 - Cards of the note move to the specified deck (if they are not in dynamic decks);
 - Backup is created prior to the export;
 - Correct reaction on an empty directory (without JSON).