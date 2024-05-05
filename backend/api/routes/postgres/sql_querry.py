sql_example_select = '''
    SELECT example1.id, example1.test
    FROM example1
'''

sql_example_select_one = '''
    SELECT example1.id, example1.test
    FROM example1
    WHERE id = $1::INTEGER
'''
