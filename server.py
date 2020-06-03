from flask import Flask
from sql import read_sql


app = Flask(__name__)


@app.route('/')
def users():
    data = read_sql('SELECT Name FROM TestDb1.TestTable1')
    return data.to_json(orient='records')


if __name__ == '__main__':
    app.run(debug=True)


