from flask import Flask
from sqlalchemy import create_engine

app = Flask(__name__)

dialect = "mysql+pymysql"
username = "root"
psw = "dummyp@ssword45"
host = "db"
dbname = "Cycling"

engine = create_engine(f"{dialect}://{username}:{psw}@{host}/{dbname}")


@app.route('/')
def index():
    return 'Test'


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
