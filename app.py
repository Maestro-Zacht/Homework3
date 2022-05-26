from flask import Flask, render_template, request
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


@app.route('/cyclist', methods=['GET', 'POST'])
def cyclist():
    query = "SELECT CID, Name, Surname FROM Cyclist;"
    try:
        con = engine.connect()
        cyclists = con.execute(query).fetchall()
        con.close()
    except SQLAlchemyError as e:
        print(f"Error! {e}")
        return render_template('error.html')

    return render_template('cyclist.html', cyclists=cyclists)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
