"""
Run manually only once - to create the columns for table
"""


from database import get_connection

get_connection.create_tables_on_startup()

