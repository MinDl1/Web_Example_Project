sql_example_select = '''
    SELECT example1.id, example1.test
    FROM example1
'''

sql_example_select_one = '''
    SELECT example1.id, example1.test
    FROM example1
    WHERE id = $1::INTEGER
'''

sql_example_create = '''
    INSERT INTO example1(test)
    VALUES ($1::VARCHAR)
    RETURNING example1.id, example1.test
'''

sql_example_update = '''
    UPDATE example1
    SET test = $1::VARCHAR
    WHERE id = $2::INTEGER
    RETURNING example1.id, example1.test
'''

sql_example_delete = '''
    DELETE FROM example1
    where id = $1::INTEGER
    RETURNING example1.id, example1.test
'''
