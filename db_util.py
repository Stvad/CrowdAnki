from pprint import pprint
from sqlite3 import OperationalError


def add_column(db, table_name, column_name):
    try:
        db.execute('ALTER TABLE {} ADD COLUMN {};'.format(table_name, column_name))
    except OperationalError as e:
        # The point is to ignore error if there is already this column
        pprint(e)