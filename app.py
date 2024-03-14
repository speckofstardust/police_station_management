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

@app.route('/', methods=['GET', 'POST'])
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

        cred = runQuery("SELECT Emp_id, password FROM Employee WHERE rank_id!='Constable' AND rank_id!='Head Constable'")
        #print(cred)
        for user in cred:
            if UN==user[0] and PS==user[1]:
                return redirect('/dashboard')

        return render_template('admin.html',errors=["Wrong Username/Password"])

    return render_template('admin.html')    


@app.route('/dashboard',methods=['GET'])
def renderDashboard():
    return render_template('dashboard.html')


@app.route('/dashboard/complaint',methods=['GET','POST'])
def displayComplaints():
    complaints = runQuery('SELECT * FROM COMPLAINT')
    complaint_ids = runQuery("SELECT comp_id FROM Complaint WHERE Status='Pending'")
    print(complaint_ids)

    if request.method == 'GET':
        return render_template("complaint_display.html", complaints = complaints, complaint_ids = complaint_ids)
    if request.method == 'POST':
        comp_id = request.form['comp_id']
        complaints = runQuery("UPDATE Complaint SET Status='Completed' WHERE comp_id = '{}' ".format(comp_id))
        return render_template("comp_update_successful.html")

    
@app.route('/dashboard/employee', methods=['GET','POST'])
def displayEmployee():
    employee = runQuery('SELECT emp_id, name, rank_id, station_id, date_of_join FROM EMPLOYEE')
    #print(employee)
    station = runQuery("SELECT station_name FROM station")
    rank_info = runQuery("SELECT rank_id FROM rank_info")

    if request.method == "POST":
        try:
            emp_id = request.form["emp_id"]
            name = request.form["Name"]
            rank_id = request.form["RankType"]
            station_name = request.form["Station"]
            date_of_join = request.form["startdate"]
            password = name+"123*"

            station_id_list = runQuery("SELECT station_id FROM station WHERE station_name='{}'".format(station_name))
            station_id = station_id_list[0][0]
            runQuery("INSERT INTO Employee(emp_id, name, rank_id, station_id,date_of_join, password)VALUES('{}', '{}', '{}', '{}', '{}', '{}')".format(emp_id, name, rank_id, station_id,date_of_join, password))

        except:
            Emp_id = request.form['Emp_Id']
            runQuery("DELETE FROM Employee WHERE emp_id='{}'".format(Emp_id))

    return render_template('employee.html', employee = employee, station = station, ranks = rank_info) 

@app.route('/dashboard/fine', methods=['GET', 'POST', 'DELETE'])
def renderFine():
    fines = runQuery("SELECT * FROM fine")
    fine_ids = runQuery("SELECT fine_id FROM fine")
    matters = runQuery("SELECT matter FROM fine_info")
    police_ids = runQuery("SELECT emp_id FROM employee")

    if request.method == 'POST':
        try:
            fine_id = runQuery("SELECT MAX(fine_id) FROM fine")[0][0]+1
            police_id = request.form['police_id']
            aadhar_id = request.form['aadhar_id']
            matter = request.form['matter']
            print(matter)
            fined_date = request.form['fined_date']

            runQuery("INSERT INTO fine(fine_id, police_id, aadhar_id, matter, fined_date) VALUES('{}', '{}', '{}', '{}', '{}')".format(fine_id, police_id, aadhar_id, matter, fined_date))
            fine_ids = police_id = aadhar_id = matter = fined_date = ""
            return render_template('fine_db.html', fine_ids = fine_ids, fines = fines, matter = matters, p_id = police_ids)
        except:
            fine_id = request.form['fine_id']
            runQuery("DELETE FROM fine WHERE fine_id={}".format(fine_id))
            return render_template('fine_db.html', fine_ids = fine_ids, fines = fines,matter = matters, p_id = police_ids)
    
    if request.method == 'GET':
        return render_template('fine_db.html', fine_ids = fine_ids, fines = fines,matter = matters, p_id = police_ids)
    
    return render_template('fine_db.html', fine_ids = fine_ids, fines = fines, matter=matters, p_id = police_ids)

@app.route('/extract_finee', methods=['GET', 'POST'])
def getAadhar():
    if request.method == 'GET':
        return render_template('extract_fine.html')
    if request.method == 'POST':
        aadhar_id = request.form['aaadhar']
        #print(aadhar_id)
        present_aid = runQuery("SELECT distinct aadhar_id FROM fine")
        print(present_aid)
        aid_lst = []
        for i in range(0, len(present_aid)):
            adr = str(present_aid[i][0])
            if adr not in aid_lst:
                aid_lst.append(adr)
        if aadhar_id in aid_lst:
            fine_info = runQuery("SELECT f.fine_id, f.aadhar_id, f.matter, f.fined_date, fi.payment FROM fine f, fine_info fi WHERE f.matter=fi.matter AND f.aadhar_id = '{}'".format(aadhar_id))
            print(fine_info)
        else:
            fine_info = [(None, aadhar_id, None,None, 0)]
        aadhar_id = ""
        return render_template('your_fines.html', finess = fine_info)
    return render_template('extract_fine.html')


@app.route('/dashboard/fine_info', methods=['GET'])
def renderFineInfo():
    fine_info = runQuery("SELECT * FROM fine_info")
    return render_template('fine_info.html', fine_info = fine_info)

@app.route('/dashboard/rank_info', methods=['GET'])
def renderRankInfo():
    rank_info = runQuery("SELECT * FROM rank_info")
    return render_template('rank_info.html', rank_info = rank_info)

@app.route('/dashboard/visitors', methods=['GET'])
def renderVisitorLogs():
    visitors = runQuery("SELECT * FROM visitor")
    return render_template('visitors.html', visitors = visitors)

@app.route('/dashboard/detained', methods=['GET'])
def renderDetainedDb():
    detained = runQuery("SELECT * FROM detained")
    return render_template('detained.html', detained = detained)
        




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
