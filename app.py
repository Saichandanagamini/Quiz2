from flask import Flask, render_template, request
import pyodbc
import math
#import mysql.connector

app = Flask(__name__)

# Define the database connection details
server = "tcp:my-server01.database.windows.net"
database = "My-db"
username = "sxg6912"
password = "PoiuytrewQ@239"
driver = "{ODBC Driver 17 for SQL Server}"

@app.route('/')
def home():
    return render_template("Home.html")



@app.route('/', methods=['POST'])
def my_form():
    #query = request.form['5mag']
    minlat = request.form['magmin']
    maxlat = request.form['magmax']
    minlon = request.form['mintime']
    maxlon = request.form['maxtime']
    city = request.form['city']
    state = request.form['state']
    popu = request.form['pop']
    lati = request.form['lati']
    long = request.form['long']

    cities = request.form['cities']
    states = request.form['states']

    if(cities != '' and states != ''):
        cnxn = pyodbc.connect(
            'DRIVER=' + driver + ';SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
        cursor = cnxn.cursor()
        query = "DELETE FROM [dbo].[data5] WHERE City = " + "'" + cities + "'" + " AND State = " + "'" + states + "'"
        cursor.execute(query)
        cnxn.commit()
        print(query)
        return render_template("deleted.html")
    if(city != '' and state != '' and popu != '' and lati != '' and long != ''):
        cnxn = pyodbc.connect(
            'DRIVER=' + driver + ';SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
        cursor = cnxn.cursor()
        query = "INSERT INTO [dbo].[data5] VALUES(" + "'" + city + "'" + "," + "'" + state + "'" + "," + popu + "," + lati + "," + long + ")"
        print(query)
        cursor.execute(query)
        cnxn.commit()
        return render_template("upload.html")
    if(minlat!= '' and maxlat != '' and minlon != '' and maxlon != ''):
        cnxn = pyodbc.connect(
            'DRIVER=' + driver + ';SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
        cursor = cnxn.cursor()
        query = "SELECT * FROM [dbo].[data5] WHERE (lat >= " + minlat + " AND lat <= " + maxlat + ")" + " AND (lon >= " + "'" + minlon + "'" + " AND lon <= " + "'" + maxlon + "'" + ")"
        print(query)
        cursor.execute(query)
        row = cursor.fetchall()
        data = []
        for i in range(len(row)):
            l = list(row[i])
            print(l)
            data.append(l)

        return render_template("earthquakesmag.html", data=data)

    lp = request.form['lat']
    hp = request.form['lon']
    n = request.form['dis']
    if(lp != '' and hp != '' and n != ''):
        cnxn = pyodbc.connect(
            'DRIVER=' + driver + ';SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)

        cursor = cnxn.cursor()
        query =  "SELECT * FROM (SELECT TOP " + n + " City, State, Population FROM [dbo].[data5] WHERE Population > " + lp + " AND Population < " + hp + " ORDER BY Population DESC) AS d UNION SELECT * FROM (SELECT TOP " + n + " City, State, Population FROM [dbo].[data5] WHERE Population > " + lp + " AND Population < " + hp + " ORDER BY Population ASC) AS a"
        print(query)
        cursor.execute(query)
        row = cursor.fetchall()
        data = []
        for i in range(len(row)):
            l = list(row[i])
            print(l)
            data.append(l)

        return render_template("earthquakesmag.html", data=data)






#@app.route('/mag5')
#def get_data(data):
#    return render_template("earthquakesmag.html", data=data)



app.run()

# Define a route to handle the home page
#@app.route('/')
#def home():
#    return render_template('home.html')

# Define a route to handle queries for earthquakes with a magnitude greater than 5.0
#@app.route('/mag_gt_5')
#def mag_gt_5():
#    cnxn = pyodbc.connect(
#        'DRIVER=' + driver + ';SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
#    cursor = cnxn.cursor()
#    cursor.execute(f"SELECT * FROM [dbo].[earthquake_month] WHERE mag > 5")
#    row = cursor.fetchall()
#    print(row)
 #   for i in range(len(row)):

#    return get_earthquakemag()

#def get_earthquakemag():
#    return render_template('earthquakesmag.html')