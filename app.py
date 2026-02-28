from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Habit, HabitLog


app = Flask(__name__)
app.config["SECRET_KEY"] = "supersecretkey"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///habit.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

with app.app_context():
    db.create_all()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# ---------------- REGISTER ----------------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        hashed_pw = generate_password_hash(request.form["password"])
        user = User(username=request.form["username"], password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("login"))
    return render_template("register.html")


# ---------------- LOGIN ----------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = User.query.filter_by(username=request.form["username"]).first()

        if user and check_password_hash(user.password, request.form["password"]):
            login_user(user)
            return redirect(url_for("dashboard"))
        flash("Invalid credentials")

    return render_template("login.html")


# ---------------- DASHBOARD ----------------
@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html", habits=current_user.habits)


# ---------------- ADD HABIT ----------------
@app.route("/add", methods=["GET", "POST"])
@login_required
def add_habit():
    if request.method == "POST":
        habit = Habit(name=request.form["name"], user=current_user)
        db.session.add(habit)
        db.session.commit()
        return redirect(url_for("dashboard"))

    return render_template("add_habit.html")

# ---------------- COMPLETE HABIT ----------------
@app.route("/complete/<int:habit_id>")
@login_required
def complete_habit(habit_id):
    habit = Habit.query.get(habit_id)
    log = HabitLog(habit=habit)
    db.session.add(log)
    db.session.commit()
    return redirect(url_for("dashboard"))



