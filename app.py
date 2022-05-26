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
    query_cyclists = "SELECT CID, Name, Surname FROM Cyclist;"
    try:
        con = engine.connect()
        cyclists = con.execute(query_cyclists).fetchall()

        if request.method == 'POST':
            CID = int(request.form['CID'])
            SID = int(request.form['SID'])

            query_position = f"""
            SELECT C1.Name,
                C1.Surname,
                T1.NameT,
                S1.SID,
                S1.Edition,
                I1.Location
            FROM Cyclist C1,
                Team T1,
                Individual_ranking I1,
                Stage S1
            WHERE T1.TID = C1.TID
                AND C1.CID = I1.CID
                AND S1.SID = I1.SID
                AND S1.Edition = I1.Edition
                AND C1.CID = {CID}
                AND S1.SID = {SID}
            ORDER BY S1.Edition ASC;
            """
            results_position = con.execute(query_position).fetchall()
        else:
            results_position = CID = SID = None
    except SQLAlchemyError as e:
        print(f"Error! {e}")
        return render_template('error.html')
    finally:
        con.close()

    return render_template('cyclist.html', cyclists=cyclists, selected_CID=CID, selected_SID=SID, results=results_position)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
