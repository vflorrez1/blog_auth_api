import mysql.connector
from config import db_name, db_host, db_pwd, db_user
import pandas as pd

cnx = mysql.connector.connect(user=db_user, password=db_pwd, host=db_host, database=db_name)
cur = cnx.cursor(dictionary=True)


def read_sql(query_string):
    cur.execute(query_string)
    sql_data = pd.DataFrame(cur.fetchall())
    sql_data.columns = cur.column_names
    return sql_data
