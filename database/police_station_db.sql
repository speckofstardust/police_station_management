USE police_station_db;

CREATE TABLE Station (
	'station_id' VARCHAR(5),
	'station_name' VARCHAR(15),
	'phone_no' NUMERIC(10, 0),
	'address' VARCHAR(30),
	CONSTRAINT 'pk_stn' PRIMARY KEY('station_id'));

CREATE TABLE 'Rank_Info' (
	'rank' VARCHAR(20),
	'salary' INTEGER,
	'no_officers' INTEGER,
	'min_exp' INTEGER,
	'contrib_pts' INTEGER,
	CONSTRAINT 'pk_rank' PRIMARY KEY('rank'));

CREATE TABLE 'Employee' (
	'emp_id' VARCHAR(6),
	'name' VARCHAR(15),
	'rank' VARCHAR(20),
	'station_id' VARCHAR(5),
	'date_of_join' DATE,
	'password' VARCHAR(20),
	CONSTRAINT 'pk_emp' PRIMARY KEY('emp_id'),
	CONSTRAINT 'fk_emp' FOREIGN KEY('station_id') REFERENCES Station('station_id'),
	CONSTRAINT 'fk_emprank' FOREIGN KEY('rank') REFERENCES Rank_Info('rank'));

CREATE TABLE 'Detained' (
	'd_id' VARCHAR(5),
	'emp_id' VARCHAR(6),
	'name' VARCHAR(20),
	'station_id' VARCHAR(5),
	'descpt' VARCHAR(50),
	'date_in' DATE,
	CONSTRAINT 'pk_det' PRIMARY KEY('d_id'),
	CONSTRAINT 'fk_det' FOREIGN KEY('station_id') REFERENCES Station('station_id')
	CONSTRAINT 'fk_detemp' FOREIGN KEY('emp_id') REFERENCES Employee('emp_id')
);

CREATE TABLE 'Visitor' (
	'vis_id' VARCHAR(5),
	'name' VARCHAR(20),
	'station_id' VARCHAR(5),
	'purpose' VARCHAR(40),
	'entry_date' DATE,
	'time_in' TIME,
	'time_out' TIME,
	CONSTRAINT 'pk_vis' PRIMARY KEY('vis_id'),
	CONSTRAINT 'fk_vis' FOREIGN KEY('station_id') REFERENCES Station('station_id'));

CREATE TABLE Complaint (
	comp_id INTEGER,
	station_id VARCHAR(5),
	date_filed DATE,
	filed_by VARCHAR(20),
	phone_no NUMERIC(10,0),
	descpt VARCHAR(50),
	status VARCHAR(9),
	CONSTRAINT pk_comp PRIMARY KEY(comp_id),
	CONSTRAINT fk_comp FOREIGN KEY(station_id) REFERENCES Station(station_id));

CREATE TABLE Fine_Info (
	matter VARCHAR(20),
	payment INTEGER,
	CONSTRAINT fk_inf PRIMARY KEY(matter));

CREATE TABLE Fine (
	fine_id VARCHAR(5),
	police_id VARCHAR(6),
	aadhar_id NUMERIC(12, 0),
	matter VARCHAR(20),
	fined_date DATE,
	CONSTRAINT pk_fine PRIMARY KEY(fine_id),
	CONSTRAINT fk_fine FOREIGN KEY(police_id) REFERENCES Employee(emp_id),
	CONSTRAINT fk_pay FOREIGN KEY(matter) REFERENCES Fine_Info(matter));

INSERT INTO Station VALUES('A1415', 'Vijayanagar', 9428302313, 'Vijayanager, Bangalore');
INSERT INTO Station VALUES('A1416', 'Kengeri', 9428302314, 'Kengeri, Bangalore');
INSERT INTO Station VALUES('A1417', 'Rajajinagar', 9428302315, 'Rajajinagar, Bangalore');

INSERT INTO Rank_Info VALUES('Circle Inspector', 50000, 5, 10, 10);
INSERT INTO Rank_Info VALUES('Inspector', 40000, 10, 8, 8);
INSERT INTO Rank_Info VALUES('Sub-Inspector', 30000, 15, 6, 6);
INSERT INTO Rank_Info VALUES('Constable', 20000, 20, 4, 4);
INSERT INTO Rank_Info VALUES('Head Constable', 25000, 15, 5, 5);


INSERT INTO Employee VALUES('U143', 'Ajit', 'Circle Inspector', 'A1415', '20-Feb-2010', 'arkh123*');
INSERT INTO Employee VALUES('U144', 'John', 'Inspector', 'A1416', '15-Mar-2012', 'john123*');
INSERT INTO Employee VALUES('U145', 'Lisa', 'Sub-Inspector', 'A1415', '10-Jul-2015', 'lisa456*');
INSERT INTO Employee VALUES('U146', 'David', 'Constable', 'A1417', '05-Nov-2018', 'david789*'); 
INSERT INTO Employee VALUES('U147', 'Emma', 'Constable', 'A1416', '12-Jan-2020', 'emma123*'); 
INSERT INTO Employee VALUES('U148', 'Michael', 'Head Constable', 'A1415', '25-Sep-2016', 'michael456*'); 
INSERT INTO Employee VALUES('U149', 'Sophia', 'Sub-Inspector', 'A1415', '18-Apr-2014', 'sophia789*');

INSERT INTO Detained VALUES('D001', 'U143', 'Kamal', 'A1415', 'Theft', '20-Feb-2010');
INSERT INTO Detained VALUES('D002', 'U144', 'Rahul', 'A1416', 'Murder', '13-Jan 2013');
INSERT INTO Detained VALUES('D003', 'U145', 'Ravi', 'A1415', 'Robbery', '05-Jul-2019'); 
INSERT INTO Detained VALUES('D004', 'U146', 'Sara', 'A1417', 'Assault', '10-Oct-2020'); 
INSERT INTO Detained VALUES('D005', 'U147', 'Alex', 'A1416', 'Drug Possession', '15-Feb-2021'); 
INSERT INTO Detained VALUES('D006', 'U148', 'Olivia', 'A1415', 'Fraud', '20-May-2017'); 
INSERT INTO Detained VALUES('D007', 'U149', 'Daniel', 'A1415', 'Burglary', '25-Sep-2018');

INSERT INTO Visitor VALUES('V001', 'John Doe', 'A1415', 'Meeting', '2022-01-01', '09:00:00', '10:00:00'); 
INSERT INTO Visitor VALUES('V002', 'Jane Smith', 'A1416', 'Delivery', '2022-01-02', '14:30:00', '15:30:00'); 
INSERT INTO Visitor VALUES('V003', 'Mike Johnson', 'A1417', 'Inquiry', '2022-01-03', '11:00:00', '12:00:00'); 
INSERT INTO Visitor VALUES('V004', 'Emily Brown', 'A1415', 'Appointment', '2022-01-04', '16:00:00', '17:00:00'); 
INSERT INTO Visitor VALUES('V005', 'Alex Wilson', 'A1416', 'Complaint', '2022-01-05', '10:30:00', '11:30:00');

INSERT INTO Complaint VALUES(001, 'A1415', '2022-01-01', 'John Doe', 9428302313, 'Robbery', 'Pending'); 
INSERT INTO Complaint VALUES(002, 'A1416', '2022-01-02', 'Jane Smith', 9428302314, 'Fraud', 'Pending');
INSERT INTO Complaint VALUES(003, 'A1417', '2022-01-03', 'Mike Johnson', 9428302315, 'Assault', 'Pending');
INSERT INTO Complaint VALUES(004, 'A1415', '2022-01-04', 'Emily Brown', 9428302313, 'Theft', 'Pending');

INSERT INTO Fine_Info VALUES('Speeding', 500);
INSERT INTO Fine_Info VALUES('Trespassing', 1500);
INSERT INTO Fine_Info VALUES('Parking Violation', 1000);
INSERT INTO Fine_Info VALUES('DUI', 1000);
INSERT INTO Fine_Info VALUES('No Seatbelt', 500);
INSERT INTO Fine_Info VALUES('Running a Red Light', 500);
INSERT INTO Fine_Info VALUES('Possession of Drugs', 1000)
INSERT INTO Fine_Info VALUES('Lying under Oath', 1250);

INSERT INTO Fine VALUES(1, 'U143', 123456789012, 'Speeding', '2022-01-01');
INSERT INTO Fine VALUES(2, 'U144', 123456789013, 'Trespassing', '2022-01-02');
INSERT INTO Fine VALUES(3, 'U145', 123456789014, 'Parking Violation', '2022-01-03');
INSERT INTO Fine VALUES(4, 'U146', 123456789015, 'DUI', '2022-01-04');
INSERT INTO Fine VALUES(5, 'U147', 123456789016, 'No Seatbelt', '2022-01-05');
INSERT INTO Fine VALUES(6, 'U148', 123456789017, 'Running a Red Light', '2022-01-06');
INSERT INTO Fine VALUES(7, 'U149', 123456789018, 'Possession of Drugs', '2022-01-07');
INSERT INTO Fine VALUES(8, 'U143', 123456789019, 'Lying under Oath', '2022-01-08');
INSERT INTO Fine VALUES(9, 'U144', 123456789020, 'Speeding', '2022-01-09');
INSERT INTO Fine VALUES(10, 'U150', 123456789021, 'Trespassing', '2022-01-10');
-- --------------------------------------------------------------------------------------------------------
ALTER TABLE child_table
DROP FOREIGN KEY fk_constraint_name,
ADD CONSTRAINT fk_constraint_name
FOREIGN KEY (child_column)
REFERENCES parent_table(parent_column)
ON DELETE SET NULL;

-- -----------------------------------------------------------------------------
DELIMITER //
CREATE TRIGGER increment_no_of_officers
AFTER INSERT ON employee
FOR EACH ROW
BEGIN
    UPDATE rank_info
    SET no_officers = no_officers + 1
    WHERE rank_id = NEW.rank_id;
END;
//
DELIMITER ;

SELECT rank_id, COUNT(*) AS count_of_rank
FROM employee
GROUP BY rank_id;





----------------------------------------------------------------------------------