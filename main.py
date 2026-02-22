from flask import Flask, render_template,request,flash,redirect,url_for,session
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
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    passwd = db.Column(db.String(50), nullable=False)

class Athletic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    eventName = db.Column(db.String(50), nullable=False)
    date = db.Column(db.String(50), nullable=False)
    time = db.Column(db.String(50), nullable=False)
    judges = db.Column(db.String(500), nullable=False)

#client side page 
@app.route("/")
def index():
    data = Notice.query.all()
    return render_template('index.html', notices=data)

@app.route("/athletic")
def athletic():
    eventdata = Athletic.query.all()

    for event in eventdata:
        event.formatted_date = datetime.strptime(
            event.date, "%Y-%m-%d"
        ).strftime("%d-%m-%Y")

        event.formatted_time = datetime.strptime(
            event.time, "%H:%M"
        ).strftime("%I:%M %p")
    return render_template('athletic.html' , events=eventdata)


# admin page backend
@app.route("/admin-login", methods=['GET', 'POST'])
def admin_login():
    if "admin" in session:
        return redirect("/admin")
     
    if request.method == 'POST':
        email = request.form.get('email') 
        passwd = request.form.get('password')

        user = Admin.query.filter_by(email=email, passwd=passwd).first()

        if user:
            session['admin'] = user.name
            return redirect("/admin")
        else:
            return "Invalid Email or Password"

    return render_template("admin-login.html")

@app.route("/admin")
def admin():
    if 'admin' not in session:
        return redirect("/admin-login")
    return render_template("admin.html")

@app.route("/register-admin", methods=['GET', 'POST'])
def adminregister():
    if 'admin' not in session:
        return redirect("/admin-login")
    if request.method == 'POST':
        name = request.form.get('admin_name') 
        email  = request.form.get('email')
        passwd  = request.form.get('password')
        admin_data=Admin(name=name,email=email,passwd=passwd)
        db.session.add(admin_data)
        db.session.commit()
    return render_template("rigester-admin.html")

@app.route("/logout")
def logout():
    if 'admin' not in session:
        return redirect("/admin-login")
    session.pop('admin', None)
    return redirect("/admin-login")

@app.route("/manage-athletic", methods=['GET', 'POST'])
def add_event():
    if 'admin' not in session:
        return redirect("/admin-login")
    
    if request.method == "POST":
        name = request.form.get('event_name')
        date = request.form.get('event_date')
        time = request.form.get('event_time')
        judges = request.form.get('judges')
        event_data=Athletic(eventName=name,date=date,time=time,judges=judges)
        db.session.add(event_data)
        db.session.commit()
        return redirect("/manage-athletic")
    return render_template("athletic-manage.html")

@app.route("/delete-event")
def manage_event():
    if 'admin' not in session:
        return redirect("/admin-login")
    eventdata = Athletic.query.all()

    for event in eventdata:
        event.formatted_date = datetime.strptime(
            event.date, "%Y-%m-%d"
        ).strftime("%d-%m-%Y")

        event.formatted_time = datetime.strptime(
            event.time, "%H:%M"
        ).strftime("%I:%M %p")
    return render_template("delete-event.html", events=eventdata)

@app.route("/delete-event/<int:id>", methods=['GET','POST'])
def delete_event(id):
    if 'admin' not in session:
        return redirect("/admin-login")
    eventdata = Athletic.query.get(id)
    if eventdata:
        db.session.delete(eventdata)
        db.session.commit()
    return redirect("/delete-event")

@app.route("/notice", methods=['GET', 'POST'])
def notice():
    if 'admin' not in session:
        return redirect("/admin-login")
    if request.method == 'POST':
        title = request.form.get('title') 
        desc  = request.form.get('desc')
        notice=Notice(title=title,desc=desc)
        db.session.add(notice)
        db.session.commit()
        flash("Student updated.", "success")
        return redirect(url_for('notice'))
    return render_template("notice.html")

@app.route("/delete-notice")
def manage_notice():
    if 'admin' not in session:
        return redirect("/admin-login")
    notices = Notice.query.all()   
    return render_template("deletenotice.html", notices=notices)

@app.route("/delete-notice/<int:id>", methods=['GET','POST'])
def delete_notice(id):
    if 'admin' not in session:
        return redirect("/admin-login")
    notice = Notice.query.get(id)
    if notice:
        db.session.delete(notice)
        db.session.commit()
    return redirect("/delete-notice")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=5000, debug=True)