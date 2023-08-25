from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey


app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)




@app.get('/')
def root_route():
    """renders start page"""

    session["responses"] = "stop"
    #remove ^ and use .get()

    title = survey.title
    instructions = survey.instructions

    return render_template('survey_start.html',
                        title = title,
                        instructions = instructions)

@app.post('/begin')
def begin():
    """redirects to first question in survey"""

    session["responses"] = []
    return redirect('/questions/0')


@app.post('/answer')
def answer():
    """redirects to either the next question in list, or completion page"""

    answer = request.form['answer']

    responses = session['responses']
    responses.append(answer)
    session['responses'] = responses

    if len(responses) < len(survey.questions):
        return redirect(f'/questions/{len(responses)}')
    else:
        return redirect('/completion')
    #could flip to if == to account for if length ever is greater than


@app.get('/questions/<int:question>')
def next_question(question):
    """displays next question in the list"""


    question_num = question
    questions = survey.questions

    if session["responses"] == "stop":
        flash("JUST HIT START. I SEE YOU.")
        return redirect('/')
    # use .get() on line 62

    elif len(session["responses"]) == len(questions):
        flash("STOP TRYING TO JUMP BACK. I SEE YOU.")
        return redirect('/completion')

    elif question == len(session['responses']):
        return render_template('question.html',
                            question = questions[question_num])

    else:
        flash("STOP TRYING TO JUMP QUESTIONS. I SEE YOU.")
        return redirect(f'/questions/{len(session["responses"])}')

    #ideally have the else be the final end goal


@app.get('/completion')
def completion():
    """renders completion page with user's question/answers"""


    questions = survey.questions
    responses = session['responses']

    if session["responses"] == "stop":
        flash("STOP TRYING TO JUMP TO COMPLETION. I SEE YOU.")
        return redirect('/')

    elif len(responses) == len(questions):
        return render_template('completion.html',
                            questions = questions,
                            responses = responses)
    else:
        flash("STOP TRYING TO JUMP TO COMPLETION. I SEE YOU.")
        return redirect(f'/questions/{len(session["responses"])}')

    #line 90 also should use .get(), have else be final goal