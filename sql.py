import mysql.connector
from config import db_name, db_host, db_pwd, db_user
import pandas as pd

cnx = mysql.connector.connect(user=db_user, password=db_pwd, host=db_host, database=db_name)
cur = cnx.cursor(dictionary=True)


def read_sql(query_string):
    cur.execute(query_string)
    # Getting dictionary back from sql server and turning it into a Dataframe
    sql_data = pd.DataFrame(cur.fetchall())
    if not sql_data.empty:
        sql_data.columns = cur.column_names
    return sql_data
