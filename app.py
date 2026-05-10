from flask import Flask, request, redirect, session

import bcrypt
import json
import os

app = Flask(__name__)
app.secret_key = "secretkey"

USER_FILE = "users.json"

# Load users
def load_users():
    if not os.path.exists(USER_FILE):
        return {}
    
    with open(USER_FILE, "r") as file:
        return json.load(file)

# Save users
def save_users(users):
    with open(USER_FILE, "w") as file:
        json.dump(users, file)

@app.route("/")
def home():
    if "user" in session:
        return f"""
        <h2>Welcome {session['user']}</h2>
        <a href='/logout'>Logout</a>
        """
    
    return """
    <h2>Secure Login System</h2>
    <a href='/register'>Register</a><br><br>
    <a href='/login'>Login</a>
    """

# Register
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        users = load_users()

        if username in users:
            return "User already exists!"

        hashed_password = bcrypt.hashpw(
            password.encode("utf-8"),
            bcrypt.gensalt()
        ).decode("utf-8")

        users[username] = hashed_password
        save_users(users)

        return redirect("/login")

    return """
    <h2>Register</h2>
    <form method='POST'>
        Username:<br>
        <input type='text' name='username'><br><br>

        Password:<br>
        <input type='password' name='password'><br><br>

        <input type='submit' value='Register'>
    </form>
    """

# Login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        users = load_users()

        if username in users:
            stored_password = users[username]

            if bcrypt.checkpw(
                password.encode("utf-8"),
                stored_password.encode("utf-8")
            ):
                session["user"] = username
                return redirect("/")

        return "Invalid username or password"

    return """
    <h2>Login</h2>
    <form method='POST'>
        Username:<br>
        <input type='text' name='username'><br><br>

        Password:<br>
        <input type='password' name='password'><br><br>

        <input type='submit' value='Login'>
    </form>
    """

# Logout
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)