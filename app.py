from flask import Flask, request, render_template, redirect, flash, session
#from random import randint, choice, sample
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)

app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = "oneonetwotwo"
debug = DebugToolbarExtension(app)

session_key = "SSKEY"


@app.route('/')
def home():
    title = satisfaction_survey.title
    instructions = satisfaction_survey.instructions

    return render_template("survey_home.html", title=title, instructions=instructions)


@app.route('/survey-start', methods=["POST"])
def survey_start():
    session[session_key] = []
    return redirect('/questions/0')


@app.route('/answer', methods=["POST"])
def answer():
    responses = session[session_key]
    """make the user to answer all the questions"""
    if (not request.form.get('answer')):
        return redirect(f'/questions/{len(responses)}')

    """store the response in the session"""

    responses.append(request.form.get('answer'))
    session[session_key] = responses

    if len(responses) < len(satisfaction_survey.questions):
        return redirect(f'/questions/{len(responses)}')
    else:
        return redirect('/complete')


@app.route('/questions/<int:id>')
def questions(id):
    responses = session.get(session_key)
    """if trying to access questions out of order"""
    if len(responses) != id:
        flash("Please do not try to answer the questions out of order.")
        return redirect(f'/questions/{len(responses)}')

    """All the survey questions have been answered"""
    if (id >= len(satisfaction_survey.questions)) and (len(responses) == len(satisfaction_survey.questions)):
        flash("All the questions have been answered.")
        return redirect('/complete')

    question = satisfaction_survey.questions[id]
    return render_template("question.html", question=question, id=id)


@app.route('/complete')
def complete():
    return render_template("complete.html")
