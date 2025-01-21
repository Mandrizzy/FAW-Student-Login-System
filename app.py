from flask import Flask, render_template, request, url_for

import sys
import sqlite3
import os

current_directory = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)

Questiondict = {
    "Q1": "What's your favourite family member name?",
    "Q2": "What's the name of your childhood crush?",
    "Q3": "What's the name of your childhood role model?",
    "Q4": "What's your favourite pet's name?"
}

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
    if request.method == "GET":
        Firstname= request.args['fname']
        Lastname= request.args['lname']
        connection = sqlite3.connect(current_directory + "/sss.db")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Students WHERE Firstname=? AND Lastname=?", (Firstname,Lastname))
        result = cursor.fetchone()
        if (result is None):
            return render_template('error.html')
        else:
   # res = list(result)
            connection.commit()
            connection.close()
            return render_template('student.html', result=result)


@app.route('/securityquestion')
def question():
    #can use try and except to catch the url error when not using the form properly
    if request.method == "GET":
        Firstname= request.args['fname']
        Lastname= request.args['lname']
        connection = sqlite3.connect(current_directory + "/sss.db")
        cursor = connection.cursor()
        cursor.execute("SELECT ID FROM Students WHERE Firstname=? AND Lastname=?", (Firstname,Lastname))
        result = cursor.fetchone()
        id=result[0]
        cursor.execute("SELECT QuestionNumber from SecurityQuestion WHERE StudentID=?",(str(id)))
        result2 = cursor.fetchone()
        if (result2 is None):
            return render_template('question.html')
        else:
            return render_template('questionAnswer.html',q=Questiondict[result2[0]])
        
    

if __name__ == "__main__":
    app.debug=True
    app.run(port=3000)