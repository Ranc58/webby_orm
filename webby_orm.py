import sqlite3


def scrub(query):
    # Against SQL injection,
    # because SELECT and FROM not formated in 'execute'
    # Link: https://stackoverflow.com/questions/3247183/#3247553
    if type(query) == list:
        return [''.join(char for char in query if char.isalnum())]
    if query:
        return ''.join(char for char in query if char.isalnum())


class WebbyOrm:
    def __init__(self, path_to_db):
        self.conn = sqlite3.connect(path_to_db)
        self.cursor = self.conn.cursor()
        self.table_name = None
        self.query_methods = {}
        self.select_query = None
        self.insert_query = None

    def table(self, table):
        self.table_name = scrub(table)
        return self

    def delete_table(self):
        self.conn.execute('DROP TABLE IF EXISTS {}'.format(self.table_name))
        self.conn.commit()

    def insert(self, columns, values):
        columns_count = '?, ' * len(columns)
        insert_query = 'INSERT INTO {table}{columns} VALUES ({columns_count})'
        if len(columns) == 1:
            columns = '({column})'.format(column=columns[0])
        self.insert_query = insert_query.format(
            table=self.table_name,
            columns=columns,
            columns_count=columns_count[:-2]
        )
        self.conn.executemany(self.insert_query, values)
        self.conn.commit()

    def update(self, column, value, ):
        update_query = 'UPDATE {table} SET {column} = ? WHERE {value} = ?'
        self.conn.execute(update_query.format(
            table=self.table_name,
            column=column[0],
            value=value[0]
        ), (column[1], value[1]))
        self.conn.commit()

    def select(self, columns_for_select='*'):
        if type(columns_for_select) == list:
            columns_for_select = ', '.join(columns_for_select)
        self.select_query = 'SELECT {columns} FROM {table_name}'.format(
            columns=columns_for_select, table_name=self.table_name
        )
        return self

    def join(self, table):
        self.select_query += ' NATURAL JOIN {table}'.format(table=table)
        return self

    def order_by(self, order_var):
        self.select_query += ' ORDER BY :order_by'
        self.query_methods.update({'order_by': order_var})
        return self

    def limit(self, query_limit):
        if type(query_limit) == int:
            self.select_query += ' LIMIT :limit'
            self.query_methods.update({'limit': query_limit})
            return self
        else:
            raise TypeError('limit must be int')


    def all(self):
        self.cursor.execute(self.select_query, self.query_methods)
        return self.cursor.fetchall()

    def one(self):
        self.cursor.execute(self.select_query, self.query_methods)
        return self.cursor.fetchone()

    def close_connection(self):
        self.conn.close()


class NewTable(WebbyOrm):
    def __init__(self, path_to_db, table):
        super().__init__(path_to_db)
        self.table_name = scrub(table)
        self.create_query = "CREATE TABLE {}".format(self.table_name)

    def columns(self, columns, foreign_keys=None):
        columns_for_create = ''
        for column in columns:
            columns_for_create += '{title} {type}, '.format(title=column[0],
                                                            type=column[1])
        if foreign_keys:
            foreign_key_query = 'FOREIGN KEY ({column}) REFERENCES {source}  '
            columns_for_create += foreign_key_query.format(
                column=foreign_keys[0],
                source=foreign_keys[1]
            )
        self.create_query += '({})'.format(columns_for_create[:-2])
        return self

    def create(self, ):
        self.cursor.execute(self.create_query)
        self.conn.commit()
