from flask import Flask, render_template, url_for, request, redirect, flash
from flask_bootstrap import Bootstrap
from flask_login import UserMixin, LoginManager, login_user, current_user, logout_user
from flask_migrate import Migrate, migrate
from flask_sqlalchemy import SQLAlchemy
import json
from input_forms import RegisterForm, LoginForm, ToDoItemForm, EditItemForm
from sqlalchemy.orm import relationship
from urllib.request import urlopen
from werkzeug.security import generate_password_hash, check_password_hash

print(__name__)

app = Flask(__name__)
Bootstrap(app)

app.config['SECRET_KEY'] = 'dev'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///to_do.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


#User table in db
class User(UserMixin, db.Model):
    __tablename__ = "users_table"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    items = db.relationship("Todo", back_populates="author")

#List of todos table in db
class Todo(db.Model):
    __tablename__ = "thelist"
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(100), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey("users_table.id"), nullable=False)
    author = db.relationship("User", back_populates="items")

with app.app_context():
    db.create_all()

migrate = Migrate(app, db)

@app.route('/', methods=["GET", "POST"])
def home():
    todo_form = ToDoItemForm()
    edit_form = EditItemForm()
    if request.method == "GET":
        #if no one is logged in
        if current_user.get_id() is None:
            return render_template('index.html')
        else:
            lat=41.85
            lon=-87.65
            with urlopen(f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true&hourly=temperature_2m,precipitation_probability,precipitation,rain,showers,visibility&daily=temperature_2m_max,temperature_2m_min,sunrise,sunset,precipitation_hours,precipitation_probability_max&timezone=America%2FChicago") as weather_data:
                weather_data_json = weather_data.read()
                weather_data_json_clean = json.loads(weather_data_json)
                sunrise = weather_data_json_clean['daily']['sunrise'][0][-5:]
                sunset = weather_data_json_clean['daily']['sunset'][0][-5:]
                temp = str(weather_data_json_clean['current_weather']['temperature']) + weather_data_json_clean['hourly_units']['temperature_2m']
                windspeed = str(weather_data_json_clean['current_weather']['windspeed']) + " km/h"

                winddirection = int(weather_data_json_clean['current_weather']['winddirection'])
                wind_direction = ""
                if (winddirection >= 0 & winddirection <= 90):
                    wind_direction = "northeast"
                elif (winddirection > 90 & winddirection <= 180):
                    wind_direction = "southeast"
                elif (winddirection > 180 & winddirection <= 270):
                    wind_direction = "southwest"
                else:
                    wind_direction = "northwest"

                precip_prop = str(weather_data_json_clean['daily']['precipitation_probability_max'][0]) + weather_data_json_clean['daily_units']['precipitation_probability_max']


            requested_user = User.query.get(current_user.get_id())
            return render_template('index.html', current_user=current_user, todo_form=todo_form, user=requested_user, edit_form=edit_form, sunrise=sunrise, sunset=sunset, temp=temp, windspeed=windspeed, wind_direction=wind_direction, precip_prop=precip_prop)

    elif request.method == "POST":
        #adding a new item to the list
        if todo_form.submit_add.data and todo_form.validate() and todo_form.validate_on_submit():
            print("up here")
            new_item = Todo(
                category=todo_form.category.data,
                description=todo_form.description.data,
                author=User.query.get(current_user.get_id())
            )
            db.session.add(new_item)
            db.session.commit()
            return redirect(url_for('home'))
        #editing an existing item
        else:
            # had to build edit form in todo_table.html file from scratch (not using wtf.quick_form) because needed to pass in todoItem's id num
            # without having it passed in through the url
            if request.form["edit_or_delete_data_form"] == "edit_data_form":
                #print(request.form["edit_or_delete_data_form"])
                category = request.form["category"]
                description = request.form["description"]
                item_id = request.form["item_id"]
                todo_item = Todo.query.get(item_id)
                todo_item.category = category
                todo_item.description = description
                db.session.commit()
                return redirect(url_for('home'))
            else: # request coming from delete modal
                #print(request.form["edit_or_delete_data_form"])
                item_to_delete = Todo.query.get(request.form["item_id"])
                db.session.delete(item_to_delete)
                db.session.commit()
                return redirect(url_for('home'))


@app.route('/register', methods=["GET", "POST"])
def register():
    register_form = RegisterForm()
    if request.method == "GET":
        return render_template('register.html', form=register_form)
    elif request.method == "POST":
        if register_form.validate_on_submit():

            if User.query.filter_by(username=register_form.username.data).first():
                flash("Username already exists. Sign in below instead.")
                return redirect(url_for('login'))

            encrypted_pw = generate_password_hash(register_form.password.data, method='pbkdf2:sha256', salt_length=10)
            new_user = User(
                username=register_form.username.data,
                password=encrypted_pw
            )

            db.session.add(new_user)
            db.session.commit()
        return redirect(url_for('home'))


@app.route('/login', methods=["GET", "POST"])
def login():
    login_form = LoginForm()
    if request.method == "GET":
        return render_template('login.html', form=login_form)
    elif request.method == "POST":
        if login_form.validate_on_submit():
            username = login_form.username.data
            password = login_form.password.data

            user = User.query.filter_by(username=username).first()
            if not user:
                flash("Username does not exist.")
                return redirect(url_for('login'))
            elif not check_password_hash(user.password, password):
                flash("Password incorrect. Please try again.")
                return redirect(url_for('login'))
            else:
                login_user(user)
                return redirect(url_for('home'))


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/about')
def about():
    return render_template('about.html')



if __name__ == "__main__":
    #app.run(debug=False)
    app.run(host="0.0.0.0", port=5000)