from flask import Flask,request,render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey


app = Flask(__name__)
app.config['SECRET_KEY'] ="IamMouhamedDoumbia86"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
toolbar = DebugToolbarExtension(app)
responses =[]

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/')
def index():
    responses.clear()
    return render_template('index.html',survey=satisfaction_survey)

@app.route("/start", methods=["POST"])
def start():
    return redirect("/questions/0")


@app.route('/questions/<id>')
def get_questions(id):

    questions_size=len(satisfaction_survey.questions)
    responses_size=len(responses)

    if (responses_size == questions_size):
        return redirect("/complete")
    
    try:
      id=int(id)
    except ValueError:
        flash(f"Invalid type: {id}")
        return redirect(f"/questions/{responses_size}")

    if (id > questions_size or id < 0):
        flash(f"Out of index: {id}")
        return redirect(f"/questions/{responses_size}")
    
    question = satisfaction_survey.questions[id].question
    choices = satisfaction_survey.questions[id].choices

    if (responses is None):
        return redirect("/")
    
    if (responses_size != id):
        flash(f"Invalid question: {id}")
        return redirect(f"/questions/{responses_size}")
    
    return render_template('questions.html',question = question,choices = choices,id=id)


@app.route("/answer", methods=["POST"])
def get_answer():
  
    answer = request.form.get('answer')
    responses.append(answer)

    questions_size=len(satisfaction_survey.questions)
    responses_size=len(responses)

    if (responses_size == questions_size):
        return redirect("/complete")
    else:
        return redirect(f"/questions/{responses_size}")
    
@app.route('/complete')
def end():
    questions_size=len(satisfaction_survey.questions)
    return render_template('complete.html',questions=satisfaction_survey.questions,responses=responses,size=questions_size)

