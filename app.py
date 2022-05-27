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
    try:
        con = engine.connect()

        query_cyclists = "SELECT CID, Name, Surname FROM Cyclist;"
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
        return render_template('error.html', error_message="Database error. Contact administrators")
    finally:
        con.close()

    return render_template('cyclist.html', cyclists=cyclists, selected_CID=CID, selected_SID=SID, results=results_position)


@app.route('/newcyclist', methods=['GET', 'POST'])
def newcyclist():
    try:
        con = engine.connect()

        query_teams = "SELECT TID, NameT FROM Team;"
        results_teams = con.execute(query_teams).fetchall()

        if request.method == 'POST':
            CID = int(request.form['CID'])
            Name = request.form['Name']
            Surname = request.form['Surname']
            Nationality = request.form['Nationality']
            TID = int(request.form['TID'])
            BirthYear = int(request.form['BirthYear'])

            with con.begin() as trans:
                query_cid = f"""
                SELECT COUNT(*)
                FROM Cyclist
                WHERE CID = {CID};
                """
                result_cid = con.execute(query_cid)
                if result_cid.first()[0] != 0:
                    trans.rollback()
                    return render_template('error.html', error_message="Cyclist with this ID already exists.")

                query_team = f"""
                SELECT COUNT(*)
                FROM Team
                WHERE TID = {TID};
                """
                result_team = con.execute(query_team)
                if result_team.first()[0] == 0:
                    trans.rollback()
                    return render_template('error.html', error_message="Team doesn't exist.")

                insert_query = f"""
                INSERT INTO Cyclist (CID, Name, Surname, Nationality, TID, BirthYear)
                VALUES ({CID}, '{Name}', '{Surname}', '{Nationality}', {TID}, {BirthYear});
                """
                con.execute(insert_query)

            return render_template('success.html', success_message="Insertion successful!")

    except SQLAlchemyError as e:
        print(f"Error! {e}")
        return render_template('error.html', error_message="Database error. Contact administrators")
    finally:
        con.close()

    return render_template('newcyclist.html', teams=results_teams)


@app.route('/newposition', methods=['GET', 'POST'])
def position():
    try:
        con = engine.connect()

        query_cyclists = "SELECT CID, Name, Surname FROM Cyclist;"
        cyclists = con.execute(query_cyclists).fetchall()

        query_stages = "SELECT SID, Edition FROM Stage;"
        stages = con.execute(query_stages).fetchall()

        if request.method == 'POST':
            CID = int(request.form['CID'])
            SID, Edition = request.form["SID-Edition"].split('-')
            Location = int(request.form['Location'])

            with con.begin() as trans:
                query_cid = f"""
                SELECT COUNT(*)
                FROM Cyclist
                WHERE CID = {CID};
                """
                result_cid = con.execute(query_cid)
                if result_cid.first()[0] == 0:
                    trans.rollback()
                    return render_template('error.html', error_message="Cyclist not found.")

                query_stage = f"""
                SELECT COUNT(*)
                FROM Stage
                WHERE Edition = {Edition} AND SID = {SID};
                """
                result_stage = con.execute(query_stage)
                if result_stage.first()[0] == 0:
                    trans.rollback()
                    return render_template('error.html', error_message="Stage not found.")

                query_position = f"""
                SELECT COUNT(*)
                FROM Individual_ranking
                WHERE Edition = {Edition}
                    AND SID = {SID}
                    AND Location = {Location};
                """
                result_position = con.execute(query_position)
                if result_position.first()[0] != 0:
                    trans.rollback()
                    return render_template('error.html', error_message="Position already occupied.")

                query_cyclist = f"""
                SELECT COUNT(*)
                FROM Individual_ranking
                WHERE Edition = {Edition}
                    AND SID = {SID}
                    AND CID = {CID};
                """
                result_cyclist = con.execute(query_cyclist)
                if result_cyclist.first()[0] != 0:
                    trans.rollback()
                    return render_template('error.html', error_message="Cyclist is already in that stage.")

                insert_query = f"""
                INSERT INTO Individual_ranking (Edition, SID, CID, Location)
                VALUES ({Edition}, {SID}, {CID}, {Location});
                """
                con.execute(insert_query)

            return render_template('success.html', success_message="Position added!")

    except SQLAlchemyError as e:
        print(f"Error! {e}")
        return render_template('error.html', error_message="Database error. Contact administrators")
    finally:
        con.close()

    return render_template('newposition.html', cyclists=cyclists, stages=stages)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
