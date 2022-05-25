from flask import Flask, render_template
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError

app = Flask(__name__)

dialect = "mysql+pymysql"
username = "root"
psw = "dummypassword45"
host = "db"
dbname = "Cycling"

engine = create_engine(f"{dialect}://{username}:{psw}@{host}/{dbname}")


@app.route('/')
def index():
    return render_template('homepage.html')


@app.route('/cyclist')
def cyclist():
    query = "SELECT CID, Name, Surname FROM Cyclist;"
    try:
        con = engine.connect()
        res = con.execute(query).fetchall()
        con.close()
    except SQLAlchemyError as e:
        print(f"Error! {e}")
        raise e

    return render_template('cyclist.html', cyclists=res)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
