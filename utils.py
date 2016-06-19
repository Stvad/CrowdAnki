from pprint import pprint
from sqlite3 import OperationalError


def merge_dicts(*dict_args):
    """
    Given any number of dicts, shallow copy and merge into a new dict,
    precedence goes to key value pairs in latter dicts.
    """
    result = {}
    for dictionary in dict_args:
        result.update(dictionary)
    return result


def add_column(db, table_name, column_name):
    try:
        db.execute('ALTER TABLE {} ADD COLUMN {};'.format(table_name, column_name))
    except OperationalError as e:
        # The point is to ignore error if there is already the column
        pprint(e)