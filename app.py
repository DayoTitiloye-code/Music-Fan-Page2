from flask import Flask, request, jsonify
from flask_cors import CORS
from flask import render_template
from werkzeug import exceptions
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
CORS(app)

db = SQLAlchemy(app)

class Users(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column("name", db.String(100))
    email = db.Column("email", db.String(100))

    def __init__(self, name, email):
        self.name = name
        self.email = email

@app.route('/user', methods=['POST', 'GET'])
def login():
    email = None
    name = None
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        form_data = request.form

        existing_user = Users.query.filter_by(name=name).first()
        if existing_user:
            print(f"User {name} exists!") 
            existing_user.email = email
            db.session.commit()
        else:
            usr = Users(name, email)
            db.session.add(usr)
            db.session.commit()

        print(f'{name} was saved!')
        return render_template('completed.html', form_data=form_data)
    return render_template('index.html', email=email), 200

@app.errorhandler(exceptions.NotFound)
def handle_404(err):
    return jsonify({"message": f"Sorry... {err}"}), 404

@app.errorhandler(exceptions.InternalServerError)
def handle_500(err):
    return jsonify({"message": f"It's not you, it's us"}), 500

@app.route('/view')
def view():
    return render_template('view.html', values=Users.query.all())

@app.route('/completed', methods = ['POST', 'GET'])
def data():
    if request.method == 'GET':
        return f"The URL /completed is accessed directly. Try going to '/users to submit form"
    if request.method == 'POST':
        form_data = request.form
        return render_template('completed.html', form_data = form_data)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run()


