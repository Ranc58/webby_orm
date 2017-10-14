#Webby ORM
ORM for SQLite. Written for training.

Support:
- Create\delete tables. 
- Select from table(with join, with order, limit).
- Create with ForeignKey.
- Insert to table.
- Update table.


#How to install
ORM used python stdlib. Nothing to install.

# Base classes
- `WebbyOrm()` - Argument: path to db.\
- `NewTable()` - Arguments: path to db, new table name.
# Methods
- `.columns()` Used for create columns in new table. \
Argument - list of tuples `(column name, columntype with options)`.\
Must be used with `.create`() 
- `.create()` Used for create new table. No arguments.
- `.table()` Used for specify table for work. \
Argument - str with table name.
- `.select()` Used for select from table. \
Argument - Not required, default - all columns. But you can use str with one column name or list of str with columns names.
- `.join()` Used for join. \
Argument - str with table name.
- `.order_by()` Used for order results in select. \
Argument - str with name of column.
- `.limit()` Used for query limit in select. \
Argument - int with number.
- `.all()` - Used for fetch all. No arguments. 
- `.one()` - Used for fetch one. No arguments.
- `.insert()` - Used for insert new content to table. \
Arguments - 2 tuples: columns and values. More info in examples below.
- `.update()` Used for update table. \
Arguments - 2 tuples: column with new value and column with value for search. More info in examples below.
- `.delete()` - Used for delete table. No arguments.
- `.close_connection()` - Used for close connection with database. No arguments.
#Usage examples

Import webby ORM
```
from webby_orm import WebbyOrm, NewTable
```

Create new Table.
Columns is tuples, first value - name of column. Second - type and options like primary key, None.
```
new_table = NewTable('test.db', 'test_table2')
columns = [('id', 'integer PRIMARY KEY'),
           ('name', 'text NOT NULL'),
           ('age', 'integer')
           ]
new_table.columns(columns).create()
new_table.close_connection()
```
Create tables with foreign_key:
```
group_table = NewTable('test.db', 'StudyGroup')
columns_for_create = [('group_id', 'INTEGER PRIMARY KEY'),
                      ('group_title', 'TEXT NOT NULL'),
                      ]
group_table.columns(columns_for_create).create()
columns = ('group_title',)
values = ('Developers',), ('Testers',), ('Designers',)
group_table.insert(columns, values)
group_table.close_connection()

students_table = NewTable('test.db', 'Students')
columns_for_create = [('id', 'INTEGER PRIMARY KEY'),
                      ('name', 'TEXT NOT NULL'),
                      ('age', 'INTEGER'),
                      ('group_id', 'INTEGER')
                      ]
foreign_keys = ('group_id', 'StudyGroup(group_id)')
students_table.columns(columns_for_create, foreign_keys).create()
columns = ('name', 'age', 'group_id')
values = (('Student_developer_1', 20, 0), ('Student_developer_2', 25, 0),
          ('Student_tester_1', 27, 1), ('Student_tester_2', 23, 1),
          ('Student_designer_1', 21, 2)
          )
students_table.insert(columns, values)
students_table.close_connection()
```

Select with join (tables from example above)
```
students_table = WebbyOrm('test.db')
columns = ['name', 'age', 'group_title']
students = students_table.table('Students').select(columns).join('StudyGroup').all()
students_table.close_connection()
```

Select column `Name` from table `Artist` by database `test.db`. Limit - 3 rows, ordered by column `Name`.

```
music = WebbyOrm('test.db')
artist_table = music.table('Artist').select('Name').order_by('Name').limit(3).all()
music.close_connection()
```


Insert values to table. Columns and values is tuples. if len tuples < 2, second tuple element must be as in example.
```
new_table = NewTable('test.db', 'TestTable2')
columns = ('workers', )
values = ('worker_1', ), ('worker_2', ), ('worker_2', )
new_table.insert(columns, values)
new_table.close_connection()
```
Delete table
```
table_to_delete = WebbyOrm('test.db')
table_to_delete.table('TestTable').delete_table()
table_to_delete.close_connection()
```
Update table
```
update_table = WebbyOrm('test.db')
update_table.table('TestTable2')
column_for_update = ('age', 40)
column_for_search = ('Name', 'Worker_1')
update_table.update(column_for_update, column_for_search)
update_table.close_connection()
```

