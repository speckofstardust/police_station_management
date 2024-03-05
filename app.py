import mysql.connector,sys
import datetime
from mysql.connector import Error
from flask import Flask, request, jsonify, render_template, redirect, url_for
from random import randint
from werkzeug.exceptions import BadRequestKeyError


app = Flask(__name__)

@app.route('/complaint',methods=['GET', 'POST'])
#@app.route('/complaint', methods=['POST'])
def submitComplaint():
    station = runQuery("SELECT station_name FROM station")
    complaint = runQuery("SELECT MAX(comp_id) FROM complaint")

    if request.method == 'POST':
        station_name = request.form['Station']
        filed_by = request.form['Name']
        phone_no = request.form['MobileNumber']
        descpt = request.form['Descpt']
        date_filed = request.form['Date']
    
        # Assuming status is initially 'Pending'
        status = 'Pending'

        # Check if phone number is valid
        if len(phone_no) != 10:
            return render_template('complaint.html', station = station, errors=["Invalid Phone Number!"])

        # Insert the complaint into the database
        id = int(complaint[0][0])+1
        station_id_list = runQuery("SELECT station_id FROM station WHERE station_name='{}'".format(station_name))
        station_id = station_id_list[0][0]
        runQuery("INSERT INTO Complaint (comp_id, station_id, date_filed, filed_by, phone_no, descpt, status) VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(id, station_id, date_filed, filed_by, phone_no, descpt, status))

        # try:
        #     bad_key = request.form['bad_key']
        # except BadRequestKeyError as ex: 
        #     return 'Unknown key: "{}"'.format(ex.args[0]), 500 

        return render_template('comp_success.html')
    
    return render_template('complaint.html', station = station)

@app.route('/home', methods=['GET', 'POST'])
def renderHome():
    return render_template('home.html')


@app.route('/loginfail',methods=['GET'])
def renderLoginFail():
    return render_template('loginfail.html')


@app.route('/admin', methods=['GET', 'POST'])
def renderAdmin():
    if request.method == 'POST':
        UN = request.form['username']
        PS = request.form['password']

        cred = runQuery("SELECT Emp_id, password FROM Employee")
        #print(cred)
        for user in cred:
            if UN==user[0] and PS==user[1]:
                return redirect('/dashboard')

        return render_template('admin.html',errors=["Wrong Username/Password"])

    return render_template('admin.html')    



@app.route('/dashboard',methods=['GET','POST'])
def getEvents():
    complaints = runQuery('SELECT * FROM COMPLAINT')
    print(complaints)
    

    if request.method == "POST":
        try:

            Name = request.form["newEvent"]
            fee=request.form["Fee"]
            participants = request.form["maxP"]
            Type=request.form["EventType"]
            Location = request.form["EventLocation"]
            Date = request.form['Date']
            runQuery("INSERT INTO events(event_title,event_price,participants,type_id,location_id,date) VALUES(\"{}\",{},{},{},{},\'{}\');".format(Name,fee,participants,Type, Location,Date))

        except:
            EventId=request.form["EventId"]
            runQuery("DELETE FROM events WHERE event_id={}".format(EventId))

    return render_template('events.html',events = events,eventTypes = eventTypes,types = types,locations = location) 


@app.route('/eventinfo')
def rendereventinfo():
    events=runQuery("SELECT *,(SELECT COUNT(*) FROM participants AS P WHERE P.event_id = E.event_id ) AS count FROM events AS E LEFT JOIN event_type USING(type_id) LEFT JOIN location USING(location_id);")

    return render_template('events_info.html',events = events)

@app.route('/participants',methods=['GET','POST'])
def renderParticipants():
    
    events = runQuery("SELECT * FROM events;")

    if request.method == "POST":
        Event = request.form['Event']

        participants = runQuery("SELECT p_id,fullname,mobile,email FROM participants WHERE event_id={}".format(Event))
        return render_template('participants.html',events = events,participants=participants)

    return render_template('participants.html',events = events)

def runQuery(query):

    try:
        db = mysql.connector.connect( host='localhost',database='police_station_db',user='RecordKeeper',password='Vertin')

        if db.is_connected():
            print("Connected to MySQL, running query: ", query)
            cursor = db.cursor(buffered = True)
            cursor.execute(query)
            db.commit()
            res = None

            try:
                res = cursor.fetchall()
            except Exception as e:
                print("Query returned nothing, ", e)
                return []
            
            return res

    except Exception as e:
        print(e)
        return []

    db.close()

    print("Couldn't connect to MySQL")
    return None


if __name__ == "__main__":
    app.run() 
