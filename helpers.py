from flask import redirect, session
from functools import wraps

# Function that returns the term name in the same syntax as displayed in make.html
def find_term(i):
    return "term" + str(i)

# Function that returns the definition name in the same syntax as displayed in make.html
def find_definition(i):
    return "definition" + str(i)

# Login_required decorator which ensures the user is logged in
def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function