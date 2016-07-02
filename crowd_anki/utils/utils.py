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


def add_column(db, table_name, column_name, default_value="\"\""):
    try:
        db.execute('ALTER TABLE {} ADD COLUMN {} TEXT DEFAULT {};'.format(table_name, column_name, default_value))
    except OperationalError as e:
        # The point is to ignore error if there is already the column
        pprint(e)


def add_absent_field(pobject, field_name, default_value=None):
    """
    Add field to the object if it does not exist yet.
    :param pobject:
    :param field_name:
    :param default_value:
    :return:
    """
    setattr(pobject, field_name, getattr(pobject, field_name, default_value))