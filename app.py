from flask import Flask, render_template, request, session, redirect
import random
import sqlite3
import string

app = Flask(__name__)

app.secret_key = "my-secret-key"


# ==========================================
# CREATE DATABASE
# ==========================================

def create_database():

    connection = sqlite3.connect("messages.db")

    connection.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            message TEXT
        )
    """)

    connection.commit()
    connection.close()


# ==========================================
# HOME
# ==========================================

@app.route("/")
def home():
    return render_template("index.html")


# ==========================================
# ABOUT
# ==========================================

@app.route("/about")
def about():
    return render_template("about.html")


# ==========================================
# PROJECTS
# ==========================================

@app.route("/projects")
def projects():
    return render_template("projects.html")


# ==========================================
# PYTHON PROJECTS
# ==========================================

@app.route("/python-projects")
def python_projects():
    return render_template("python-projects.html")

# ==========================================
# NUMBER GUESSING GAME
# ==========================================

@app.route("/guessing-game", methods=["GET", "POST"])
def guessing_game():

    if "number" not in session:
        session["number"] = random.randint(1, 100)
        session["attempts"] = 0

    message = None
    won = False

    if request.method == "POST":

        guess = int(request.form["guess"])

        session["attempts"] += 1

        number = session["number"]

        if guess < number:

            message = "⬆️ Too low! Try again."

        elif guess > number:

            message = "⬇️ Too high! Try again."

        else:

            message = "🎉 Correct! You won!"

            won = True

    return render_template(
        "guessing-game.html",
        message=message,
        attempts=session["attempts"],
        won=won
    )

# ==========================================
# PYTHON QUIZ
# ==========================================

questions = [

    {
        "text": "What is Python?",
        "options": [
            "A programming language",
            "A web browser",
            "A video game",
            "An operating system"
        ],
        "answer": "A programming language"
    },

    {
        "text": "Which symbol is used to create a comment in Python?",
        "options": [
            "//",
            "#",
            "<!-- -->",
            "/* */"
        ],
        "answer": "#"
    },

    {
        "text": "Which function displays text on the screen?",
        "options": [
            "show()",
            "display()",
            "print()",
            "write()"
        ],
        "answer": "print()"
    },

    {
        "text": "Which data type stores True or False?",
        "options": [
            "String",
            "Boolean",
            "List",
            "Integer"
        ],
        "answer": "Boolean"
    },

    {
        "text": "Which symbol is used for multiplication in Python?",
        "options": [
            "x",
            "×",
            "*",
            "#"
        ],
        "answer": "*"
    }

]


@app.route("/quiz", methods=["GET", "POST"])
def quiz():

    # Start the quiz

    if request.method == "GET":

        session["quiz_index"] = 0
        session["quiz_score"] = 0

    else:

        answer = request.form["answer"]

        current_index = session["quiz_index"]

        if answer == questions[current_index]["answer"]:

            session["quiz_score"] += 1

        session["quiz_index"] += 1


    current_index = session["quiz_index"]

    # Quiz finished

    if current_index >= len(questions):

        score = session["quiz_score"]

        return render_template(
            "quiz.html",
            question=None,
            question_number=len(questions),
            total_questions=len(questions),
            score=score
        )


    # Show next question

    question = questions[current_index]

    return render_template(
        "quiz.html",
        question=question,
        question_number=current_index + 1,
        total_questions=len(questions),
        score=session["quiz_score"]
    )

# ==========================================
# PASSWORD GENERATOR
# ==========================================

@app.route("/password-generator", methods=["GET", "POST"])
def password_generator():

    password = None

    if request.method == "POST":

        length = int(request.form["length"])

        characters = (
            string.ascii_letters
            + string.digits
            + string.punctuation
        )

        password = ""

        for i in range(length):
            password += random.choice(characters)

    return render_template(
        "password-generator.html",
        password=password
    )
# ==========================================
# NEW CALCULATOR
# ==========================================

@app.route("/calculator")
def calculator():
    return render_template("calculator.html")


# ==========================================
# PYTHON CALCULATOR
# ==========================================

@app.route("/python-calculator", methods=["GET", "POST"])
def python_calculator():

    result = None

    if request.method == "POST":

        number1 = float(request.form["number1"])
        number2 = float(request.form["number2"])
        operation = request.form["operation"]

        if operation == "add":
            result = number1 + number2

        elif operation == "subtract":
            result = number1 - number2

        elif operation == "multiply":
            result = number1 * number2

        elif operation == "divide":

            if number2 == 0:
                result = "Cannot divide by zero! ❌"
            else:
                result = number1 / number2

        elif operation == "power":
            result = number1 ** number2

        elif operation == "remainder":

            if number2 == 0:
                result = "Cannot divide by zero! ❌"
            else:
                result = number1 % number2

    return render_template(
        "python-calculator.html",
        result=result
    )


# ==========================================
# CONTACT
# ==========================================

@app.route("/contact", methods=["GET", "POST"])
def contact():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        message = request.form["message"]

        connection = sqlite3.connect("messages.db")

        connection.execute(
            """
            INSERT INTO messages (name, email, message)
            VALUES (?, ?, ?)
            """,
            (name, email, message)
        )

        connection.commit()
        connection.close()

        return render_template("message_saved.html")

    return render_template("contact.html")


# ==========================================
# LOGIN
# ==========================================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        if username == "Aarav" and password == "Chand@420":

            session["logged_in"] = True

            return redirect("/messages")

        else:

            return "Wrong username or password! ❌"

    return render_template("login.html")


# ==========================================
# MESSAGES
# ==========================================

@app.route("/messages")
def messages():

    if not session.get("logged_in"):
        return redirect("/login")

    connection = sqlite3.connect("messages.db")

    connection.row_factory = sqlite3.Row

    saved_messages = connection.execute(
        "SELECT * FROM messages ORDER BY id DESC"
    ).fetchall()

    connection.close()

    return render_template(
        "messages.html",
        messages=saved_messages
    )


# ==========================================
# DELETE MESSAGE
# ==========================================

@app.route("/delete-message/<int:message_id>", methods=["POST"])
def delete_message(message_id):

    # Only logged-in admin can delete messages

    if not session.get("logged_in"):
        return redirect("/login")

    connection = sqlite3.connect("messages.db")

    connection.execute(
        "DELETE FROM messages WHERE id = ?",
        (message_id,)
    )

    connection.commit()

    connection.close()

    return redirect("/messages")


# ==========================================
# LOGOUT
# ==========================================

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/login")


# ==========================================
# START DATABASE
# ==========================================

create_database()


# ==========================================
# START WEBSITE
# ==========================================

if __name__ == "__main__":
    app.run(debug=True)