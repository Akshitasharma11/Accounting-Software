from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
import mysql.connector
from werkzeug.security import check_password_hash
from models import User  # Import User class from models

auth = Blueprint("auth", __name__)

# Database Connection
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="roxanne",
        database="accounting"
    )

# Login Route
@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # Connect to database and fetch user
        conn = connect_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        conn.close()

        # Check if user exists and password is correct
        if user and check_password_hash(user["password"], password):
            # If valid, log the user in
            login_user(User(user["id"], user["username"], user["role"]))
            return redirect(url_for("home"))  # Redirect to home page
        else:
            flash("Invalid credentials!", "danger")  # Show error message

    return render_template("login.html")  # Show login form if GET request

# Logout Route
@auth.route("/logout")
@login_required  # This ensures the user must be logged in to access this route
def logout():
    logout_user()  # Logs out the current user
    return redirect(url_for("auth.login"))  # Redirect to login page
