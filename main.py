from flask import Flask, render_template,request,flash,redirect,url_for
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder="templates", static_folder="static")

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "king-754345"

db = SQLAlchemy(app)

class Notice(db.Model):
    sno = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(5000), nullable=False)

class Admin(db.Model):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), nullable=False)
    passwd = db.Column(db.String(50), nullable=False)

@app.route("/")
def index():
    data = Notice.query.all()
    return render_template('index.html', notices=data)

@app.route("/admin-login", methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        email = request.form.get('email') 
        passwd = request.form.get('password')

        user = Admin.query.filter_by(email=email, passwd=passwd).first()

        if user:
            return redirect("/admin")
        else:
            return "Invalid Email or Password"

    return render_template("admin-login.html")

@app.route("/admin")
def admin():
    return render_template("admin.html")

@app.route("/notice", methods=['GET', 'POST'])
def notice():
    if request.method == 'POST':
        title = request.form.get('title') 
        desc  = request.form.get('desc')
        print(title)
        print(desc) 
        notice=Notice(title=title,desc=desc)
        db.session.add(notice)
        db.session.commit()
        flash("Student updated.", "success")
        return redirect(url_for('notice'))
    return render_template("notice.html")



if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=5000, debug=True)