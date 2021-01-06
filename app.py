import sqlite3

from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import login_required, find_term, find_definition

app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

app.secret_key = b'_5k2L"FdQ8z\3n4\xec]/'

@app.route("/")
@login_required
def index():

    # Generate SQL objects (the connection and the cursor) and query table "flashcard_titles"
    # for all of the current user's sets
    with sqlite3.connect("FlashStudy.db") as conn:
        c = conn.cursor()

        c.execute("SELECT * FROM flashcard_titles WHERE user_id = (?)",
                  (session["user_id"],))

        titles = c.fetchall()

    # Render "index.html" and pass in variable "titles"
    return render_template("index.html", titles=titles)

@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Generate SQL objects (the connection and the cursor) and query table "flashcard_titles"
        # for all of the current user's sets.
        # Do this so that the select menu still has access to the sets if add.html needs to be rendered in post.
        with sqlite3.connect("FlashStudy.db") as conn:
            c = conn.cursor()

            c.execute("SELECT * FROM flashcard_titles WHERE user_id = (?)",
                      (session["user_id"],))

            titles = c.fetchall()

        # Prepare variables to be used throughout add()
        set = request.form.get("set")
        term = request.form.get("term")
        definition = request.form.get("definition")

        # Ensure set was selected
        if set == None:
            flag = True
            return render_template("add.html", error="Choose a set to add to", flag=flag, titles=titles)

        # Ensure term was submitted
        if not term:
            flag = True
            return render_template("add.html", error="Missing term", flag=flag, titles=titles)

        # Ensure definition was submitted
        if not definition:
            flag = True
            return render_template("add.html", error="Missing definition", flag=flag, titles=titles)

        # Generate SQL objects (the connection and the cursor) and query table "flashcards" for the terms/definitions
        # for all of the flashcards from the set that the current user selected
        with sqlite3.connect("FlashStudy.db") as conn:
            c = conn.cursor()

            c.execute("SELECT term, definition FROM flashcards WHERE user_id = (?) AND title = (?)",
                      (session["user_id"], set))

            flashcards = c.fetchall()

        # Ensure the terms/definitions being inputted are not already used as a term/definition in the set
        for i in range(len(flashcards)):

            # Return an error if the term/definition being inputted is already used as a term in the set's ith flashcard
            if term in flashcards[i][0] or definition in flashcards[i][0]:
                flag = True
                return render_template("add.html", error="You can not use the same term/definition twice in a set!",
                                       flag=flag, titles=titles)

            # Return an error if the term/definition being inputted is already used as a definition in the set's ith flashcard
            if term in flashcards[i][1] or definition in flashcards[i][1]:
                flag = True
                return render_template("add.html", error="You can not use the same term/definition twice in a set!",
                                       flag=flag, titles=titles)

        # Ensure term and definition being inputted are different
        if term == definition:
            flag = True
            return render_template("add.html", error="You can not use the same term/definition twice in a set!",
                                   flag=flag, titles=titles)

        # Generate SQL objects (the connection and the cursor) and insert current user's id,
        # their new flashcard set title, term, and definition into table "flashcards"
        with sqlite3.connect("FlashStudy.db") as conn:
            c = conn.cursor()

            c.execute("INSERT INTO flashcards (user_id, title, term, definition) VALUES (?, ?, ?, ?)",
                      (session["user_id"], set, term, definition))

            conn.commit()

        # Let user know
        flash('Successfully added flashcard to set "' + set + '"')

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via direct)
    else:

        # Generate SQL objects (the connection and the cursor) and query table "flashcard_titles"
        # for all of the current user's sets
        with sqlite3.connect("FlashStudy.db") as conn:
            c = conn.cursor()

            c.execute("SELECT * FROM flashcard_titles WHERE user_id = (?)",
                      (session["user_id"],))

            titles = c.fetchall()

        # Render "add.html" and pass in variable "titles"
        return render_template("add.html", titles=titles)

@app.route("/study", methods=["GET", "POST"])
@login_required
def study():
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Prepare variable "set_title" to be used throughout study()
        set_title = request.form.get("index_input_name")

        # Generate SQL objects (the connection and the cursor) and query table "flashcards"
        # for all of the flashcards from the set that the current user selected in index.html
        with sqlite3.connect("FlashStudy.db") as conn:
            c = conn.cursor()

            c.execute("SELECT * FROM flashcards WHERE user_id = (?) AND title = (?)",
                      (session["user_id"], set_title))

            inputs = c.fetchall()

            return render_template("study.html", inputs=inputs, set_title=set_title)

    # User reached route via GET (as by clicking a link or via direct)
    else:

        # Redirect user to home page
        return redirect("/")

@app.route("/delete", methods=["GET", "POST"])
def delete():
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Prepare variable "deleted_set" to be used throughout delete()
        deleted_set = request.form.get("delete_set")

        # Generate SQL objects (the connection and the cursor) and delete data (from table "flashcard_titles")
        # that matches with the set the current user wanted to delete in study.html
        with sqlite3.connect("FlashStudy.db") as conn:
            c = conn.cursor()

            c.execute("DELETE FROM flashcard_titles WHERE user_id = (?) AND title = (?)",
                      (session["user_id"], deleted_set))

            conn.commit()

        # Generate SQL objects (the connection and the cursor) and delete data (from table "flashcards")
        # that matches with the set the current user wanted to delete in study.html
        with sqlite3.connect("FlashStudy.db") as conn:
            c = conn.cursor()

            c.execute("DELETE FROM flashcards WHERE user_id = (?) AND title = (?)",
                      (session["user_id"], deleted_set))

            conn.commit()

        # Let user know
        flash('Successfully deleted set "' + deleted_set + '"')

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via direct)
    else:

        # Redirect user to home page
        return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Prepare variables to be used in register()
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Ensure username was submitted
        if not username:
            flag = True
            return render_template("register.html", error="Missing username", flag=flag)

        # Generate SQL objects (the connection and the cursor) and query table "users" for the inputted username
        with sqlite3.connect("FlashStudy.db") as conn:
            c = conn.cursor()

            c.execute("SELECT * FROM users WHERE username = (?)",
                      (username,))

        # If inputted username is already in database, flash error message
        if c.fetchone():
            flag = True
            return render_template("register.html", error="Username already taken", flag=flag)

        # Ensure password was submitted
        if not password:
            flag = True
            return render_template("register.html", error="Missing password", flag=flag)

        # Ensure confirmation was submitted
        if not confirmation:
            flag = True
            return render_template("register.html", error="Missing confirmation", flag=flag)

        # Ensure password and confirmation match
        if password != confirmation:
            flag = True
            return render_template("register.html", error="Password and password confirmation must match", flag=flag)

        # Hash inputted password
        hashed_value = generate_password_hash(password)

        # Generate SQL objects (the connection and the cursor) and insert new username and hash into table "users"
        with sqlite3.connect("FlashStudy.db") as conn:
            c = conn.cursor()

            c.execute("INSERT INTO users (username, hash) VALUES (?, ?)",
                      (username, hashed_value))

            conn.commit()

        # Query table "users" for the inputted username
        c.execute("SELECT * FROM users WHERE username = (?)",
                  (username,))

        # Insert new user's data into variable "user"
        user = c.fetchone()

        # Remember which user has registered, so they don't have to login again
        session["user_id"] = user[0]

        # Let user know
        flash("Successfully registered!")

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via direct)
    else:

        # Render "register.html"
        return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Prepare variables to be used in login()
        username = request.form.get("username")
        password = request.form.get("password")

        # Ensure username was submitted
        if not username:
            flag = True
            return render_template("login.html", error="Missing username", flag=flag)

        # Ensure password was submitted
        if not password:
            flag = True
            return render_template("login.html", error="Missing password", flag=flag)

        # Generate SQL objects (the connection and the cursor) and query table "users" for inputted username
        with sqlite3.connect("FlashStudy.db") as conn:
            c = conn.cursor()

            c.execute("SELECT * FROM users WHERE username = (?)",
                      (username,))

        # Insert user's data into variable "user"
        user = c.fetchall()

        # Ensure inputted username exists
        if len(user) != 1:
            flag = True
            return render_template("login.html", error="Invalid username", flag=flag)

        # Ensure inputted password matches with stored hashed password when compared by check_password_hash
        if not check_password_hash(user[0][2], password):
            flag = True
            return render_template("login.html", error="Invalid password", flag=flag)

        # Remember which user has logged in
        session["user_id"] = user[0][0]

        # Let user know
        flash("Successfully signed in!")

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via direct)
    else:

        # Render "login.html"
        return render_template("login.html")

@app.route("/logout")
def logout():

    # Forget any user_id
    session.clear()

    # Redirect user to home page
    return redirect("/")

@app.route("/make", methods=["GET", "POST"])
@login_required
def make():
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Prepare variable "title" to be used throughout make()
        title = request.form.get("title")

        # Repeat for all 10 flashcards in make.html
        for i in range(0, 10):

            # Return error if the current flashcard's term input field is blank
            if request.form.get(find_term(i)) == "":
               flag = True
               return render_template("make.html", error="Do not leave any inputs blank!", flag=flag)

            # Return error if the current flashcard's definition input field is blank
            if request.form.get(find_definition(i)) == "":
               flag = True
               return render_template("make.html", error="Do not leave any inputs blank!", flag=flag)

        # Ensure title was submitted
        if not title:
            flag = True
            return render_template("make.html", error="Missing title", flag=flag)

        # Generate SQL objects (the connection and the cursor) and query table "flashcard_titles"
        # to see if the current user already has a flashcard set with the same title
        with sqlite3.connect("FlashStudy.db") as conn:
            c = conn.cursor()

            c.execute("SELECT * FROM flashcard_titles WHERE title = (?) AND user_id = (?)",
                      (title, session["user_id"]))

            same_title = c.fetchall()

        # Return an error message if user already has a flashcard set with the same title
        if same_title:
            flag = True
            return render_template("make.html", error="You can not have flashcard sets with the same title!", flag=flag)

        # Make empty list used in loop below
        inputs = []

        # Repeat for all 10 flashcards to ensure all the inputs are different
        for i in range(0, 10):

            # Prep variables to be used throughout loop
            term = request.form.get(find_term(i))
            definition = request.form.get(find_definition(i))

            # Continue to the next flashcard if the current flashcard's term input is None
            # (which also means the current flashcard's definition input is None since inputs/definitions come in pairs)
            if term == None:
                continue

            # Ensure the term being inputted hasn't already been used as a either a term or definition
            # in the creation of this set
            if term in inputs:
                flag = True
                return render_template("make.html", error="You can not use the same term/definition twice in a set!",
                                       flag=flag)

            # Append the term to list "inputs"
            inputs.append(term)

            # Ensure the definition being inputted hasn't already been used as a either a term or definition
            # in the creation of this set
            if definition in inputs:
                flag = True
                return render_template("make.html", error="You can not use the same term/definition twice in a set!",
                                       flag=flag)

            # Append the definition to list "inputs"
            inputs.append(definition)

        # Clear the inputs list
        inputs.clear()

        # Generate SQL objects (the connection and the cursor) and insert current user's id
        # and their new flashcard title into table "flashcard_titles"
        with sqlite3.connect("FlashStudy.db") as conn:
            c = conn.cursor()

            c.execute("INSERT INTO flashcard_titles (user_id, title) VALUES (?, ?)",
                      (session["user_id"], title))

            conn.commit()

        # Repeat for all 10 flashcards and insert into database
        for i in range(0, 10):

            # Prep variables to be used throughout loop
            term = request.form.get(find_term(i))
            definition = request.form.get(find_definition(i))

            # Continue to the next flashcard if the current flashcard's term input is None
            # (which also means the current flashcard's definition input is None since inputs/definitions come in pairs)
            if term == None:
                continue

            # Generate SQL objects (the connection and the cursor) and insert current user's id,
            # their new flashcard set title, current term, and current definition into table "flashcards"
            with sqlite3.connect("FlashStudy.db") as conn:
                c = conn.cursor()

                c.execute("INSERT INTO flashcards (user_id, title, term, definition) VALUES (?, ?, ?, ?)",
                          (session["user_id"], title, term, definition))

                conn.commit()

        # Let user know
        flash('Successfully made set "' + title + '"')

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via direct)
    else:

        # Render "make.html"
        return render_template("make.html")


@app.route("/edit", methods=["GET", "POST"])
@login_required
def edit():
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Prepare variable "edit_set" to be used throughout edit()
        edit_set = request.form.get("edit_set")

        # Generate SQL objects (the connection and the cursor) and query table "flashcards" for
        # all of the flashcards from the set the current user wants to edit
        with sqlite3.connect("FlashStudy.db") as conn:
            c = conn.cursor()

            c.execute("SELECT * FROM flashcards WHERE user_id = (?) AND title = (?)",
                      (session["user_id"], edit_set))

            flashcards = c.fetchall()

        # Render edit.html and pass in the set's flashcards and title
        return render_template("edit.html", flashcards=flashcards, set_title=edit_set)

    # User reached route via GET (as by clicking a link or via direct)
    else:

        # Redirect user to home page
        return redirect("/")

@app.route("/editing", methods=["GET", "POST"])
@login_required
def editing():
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Prepare variable "edited_set" to be used throughout editing()
        edited_set = request.form.get("edit_set")

        # Generate SQL objects (the connection and the cursor) and query table "flashcards" for
        # all of the flashcards from the set the current user is editing
        with sqlite3.connect("FlashStudy.db") as conn:
            c = conn.cursor()

            c.execute("SELECT * FROM flashcards WHERE user_id = (?) AND title = (?)",
                      (session["user_id"], edited_set))

            flashcards = c.fetchall()

        # Make empty list used in loop below
        inputs = []

        # Loop over all the flashcards in the set that the current user is editing.
        # Ensure no input is used twice in the newly inputted set
        for i in range(len(flashcards)):

            # Prepare variables "current_term" and "current_definition" to be used within loop,
            # and set them to values being inputted in the edit form (take a look at how names are set up in edit.html).
            current_term = request.form.get(flashcards[i][2])
            current_definition = request.form.get(flashcards[i][3])

            # Ensure the term being inputted hasn't already been used as either a term or definition
            # in the new version of this set
            if current_term in inputs:
                flag = True
                return render_template("edit.html", error="You can not use the same term/definition twice in a set!", flashcards=flashcards, set_title=edited_set, flag=flag)

            # Append the term to list "inputs"
            inputs.append(current_term)

            # Ensure the definition being inputted hasn't already been used as either a term or definition
            # in the new version of this set
            if current_definition in inputs:
                flag = True
                return render_template("edit.html", error="You can not use the same term/definition twice in a set!", flashcards=flashcards, set_title=edited_set, flag=flag)

            # Append the definition to list "inputs"
            inputs.append(current_definition)

        # Clear the inputs list.
        inputs.clear()

        # Loop over all the flashcards in the set that the current user is editing.
        # Update each flashcard in the set being edited.
        for i in range(len(flashcards)):

            # Prepare variables "past_term" and "past_definition" to be used within loop,
            # and set them to the set's old flashcard terms/definitions.
            past_term = flashcards[i][2]
            past_definition = flashcards[i][3]

            # Prepare variables "current_term" and "current_definition" to be used within loop,
            # and set them to values being inputted in the edit form (take a look at how names are set up in edit.html).
            current_term = request.form.get(flashcards[i][2])
            current_definition = request.form.get(flashcards[i][3])

            # Generate SQL objects (the connection and the cursor) and update the current set's
            # old terms/definitions to the new terms/definitions being inputted
            with sqlite3.connect("FlashStudy.db") as conn:
                c = conn.cursor()

                c.execute("UPDATE flashcards SET term = (?), definition = (?) WHERE term = (?) AND definition = (?) AND user_id = (?) AND title = (?)",
                          (current_term, current_definition, past_term, past_definition, session["user_id"], edited_set))

                conn.commit()

        # Let user know
        flash('Successfully edited set "' + edited_set + '"')

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via direct)
    else:

        # Redirect user to home page
        return redirect("/")

@app.route("/change_password", methods=["GET", "POST"])
@login_required
def change_password():
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Prepare variables to be used in change_password()
        new_password = request.form.get("new_password")
        confirmation = request.form.get("confirmation")

        # Ensure user submitted new_password
        if not new_password:
            flag = True
            return render_template("change_password.html", error="Missing new password", flag=flag)

        # Ensure user submitted confirmation
        if not confirmation:
            flag = True
            return render_template("change_password.html", error="Missing confirmation", flag=flag)

        # Ensure new_password and confirmation match
        if new_password != confirmation:
            flag = True
            return render_template("change_password.html", error="Passwords do not match", flag=flag)

        # Generate SQL objects (the connection and the cursor) and query table "users" for the current user's hash value
        with sqlite3.connect("FlashStudy.db") as conn:
            c = conn.cursor()

            c.execute("SELECT hash FROM users WHERE id = (?)",
                      (session["user_id"],))

            old_hash = c.fetchone()

        # Ensure user is not changing to their current password
        if check_password_hash(old_hash[0], new_password):
            flag = True
            return render_template("change_password.html", error="Can not change to your current password", flag=flag)

        # Hash the new password
        hashed_value = generate_password_hash(new_password)

        # Generate SQL objects (the connection and the cursor) and update the current user's hash
        # to the new hash value of their new password
        with sqlite3.connect("FlashStudy.db") as conn:
            c = conn.cursor()

            c.execute("UPDATE users SET hash = (?) WHERE id = (?)",
                      (hashed_value, session["user_id"]))

            conn.commit()

        # Let user know
        flash("Password successfully changed!")

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via direct)
    else:

        # Render "change_password.html"
        return render_template("change_password.html")

if __name__ == '__main__':

    app.run()