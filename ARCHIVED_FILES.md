# Archived Files

This document lists files that were part of the original Dejavu design but are not used in our current implementation.

## Database Handlers

1. **postgres_database.py_ARCHIVED**

   - Original file: `dejavu_web/dejavu/database_handler/postgres_database.py`
   - Reason: Our implementation exclusively uses the Django ORM for database operations. The PostgreSQL database handler was part of the original Dejavu design but isn't used in our codebase.

2. **mysql_database.py_ARCHIVED**
   - Original file: `dejavu_web/dejavu/database_handler/mysql_database.py`
   - Reason: Our implementation exclusively uses the Django ORM for database operations. The MySQL database handler was part of the original Dejavu design but isn't used in our codebase.

## Recognizers

1. **microphone_recognizer.py_ARCHIVED**
   - Original file: `dejavu_web/dejavu/logic/recognizer/microphone_recognizer.py`
   - Reason: This file was imported in views.py but never actually used in our implementation. It's referenced in the example script but not in our web application.

## Impact

Archiving these files helps clean up the codebase without removing potentially useful code. If we need to restore any of this functionality in the future, we can easily rename the files back to their original names.

## Modifications Made

- Removed import references to MicrophoneRecognizer from views.py
- Files were renamed by adding "\_ARCHIVED" to their names rather than deleting them
