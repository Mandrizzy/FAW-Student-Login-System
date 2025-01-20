from flask import Flask, render_template, request, g

import sys
import sqlite3
import os

current_directory = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)

@app.route('/')
def index():
    # connection = sqlite3.connect(current_directory + "/sss.db")
    # cursor = connection.cursor()
    # cursor.execute("INSERT INTO Students (Firstname, Lastname,Email,Grade) VALUES ('Vlad', 'Volley','watford@gmail.com', 9)");
    # connection.commit()
    # connection.close()
    return render_template('index.html')

@app.route('/student')
def student():
    connection = sqlite3.connect(current_directory + "/sss.db")
    cursor = connection.cursor()
    Lastname='Coley'
    Firstname='Theodore'
    cursor.execute("SELECT * FROM Students WHERE Firstname=? AND Lastname=?", (Firstname,Lastname))
    result = cursor.fetchone()
   # res = list(result)
    connection.commit()
    connection.close()
    return render_template('student.html', result=result)

if __name__ == "__main__":
    app.debug=True
    app.run(port=3000)