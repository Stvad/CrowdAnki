from pprint import pprint


def add_column(self, table_name, column_name):
    try:
        self.db.execute('ALTER TABLE {} ADD COLUMN {};'.format(table_name, column_name))
    except Exception as e:
        # The point is to ignore error if there is already this column
        pprint(e)