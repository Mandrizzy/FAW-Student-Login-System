from flask import Flask, render_template, request, url_for, abort, redirect

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

def clean_string(input_string):
    # Convert to lowercase and remove white spaces
    return input_string.replace(" ", "").lower()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/student')
def student():
    if request.method == "GET":
        Firstname = clean_string(request.args['fname'])
        Lastname = clean_string(request.args['lname'])
        connection = sqlite3.connect(current_directory + "/sss.db")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Student WHERE firstname=? AND lastname=?", (Firstname,Lastname))
        result = cursor.fetchone()
        if (result is None):
            error = ":( Sorry I wasn't able to find your name in my database please try again"
            return render_template('error.html',error=error)
        else:
            connection.commit()
            connection.close()
            return render_template('student.html', result=result)


@app.route('/securityquestion')
def question():
    #can use try and except to catch the url error when not using the form properly
    if request.method == "GET":
        Firstname = clean_string(request.args['fname'])
        Lastname = clean_string(request.args['lname'])
        connection = sqlite3.connect(current_directory + "/sss.db")
        cursor = connection.cursor()
        cursor.execute("SELECT ID FROM Student WHERE firstname=? AND lastname=?", (Firstname,Lastname))
        result = cursor.fetchone()
        id=result[0]
        str_id = str(id)
        cursor.execute("SELECT question from SecurityQuestion WHERE studentID=?",(str_id,))
        result2 = cursor.fetchone()
        if (result2 is None):
            return render_template('question.html',id=str(id))
        else:
            return render_template('questionAnswer.html',q=Questiondict[result2[0]],id=str(id))
        


@app.route('/studentinfo', methods=['GET','POST'])
def student_info():
    if request.method =="POST":
        securityQuestion = request.form['questions']
        securityAnswer = clean_string(request.form['answer'])
        studentID = int(request.form['student_id'])
        str_ID = str(studentID)
        connection = sqlite3.connect(current_directory + "/sss.db")
        cursor = connection.cursor()
        cursor.execute("INSERT INTO SecurityQuestion (studentID,question,answer) VALUES (?,?,?)",(studentID,securityQuestion,securityAnswer))
        cursor.execute("SELECT * from Student WHERE ID=?",(str_ID,))
        student = cursor.fetchone()
        connection.commit()
        connection.close()
        #more logic needed to grap student detail
        return render_template('studentInfo.html',student=student)
    

@app.route('/checkanswer', methods=['GET','POST'])
def check_answer():
    if request.method =="POST":
        answer = clean_string(request.form['answer'])
        student_id = request.form['student_id']
        connection = sqlite3.connect(current_directory + "/sss.db")
        cursor = connection.cursor()
        cursor.execute("SELECT answer from SecurityQuestion WHERE studentID=?",(student_id,))
        inquiry = cursor.fetchone()
        if (answer == inquiry[0]):
            cursor.execute("SELECT * from Student WHERE ID=?",(student_id,))
            student = cursor.fetchone()
            connection.commit()
            connection.close()
            return render_template('studentInfo.html',student=student)
        else:
            error = " :( Sorry that was not the correct answer you must start over again"
            return render_template('error.html',error=error)

if __name__ == "__main__":
    app.debug=True
    app.run(port=3000)